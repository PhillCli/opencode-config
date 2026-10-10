#!/usr/bin/env python3
"""Skill usage analytics and dead-skill audit from OpenCode session history.

Skill loads are `skill` tool calls recorded as parts, either in the local
OpenCode server database or (fallback) as JSON part files. Neither store is a
public contract; both are read read-only and may need adjusting after
OpenCode upgrades.

The currently registered skill set comes from the running server's
`GET /api/skill` (authoritative: resolves sources, precedence, and nested
SKILL.md), falling back to a filesystem scan of the standard skill sources.

Buckets:
  dead          registered from a global source, advertised, zero loads in window, file older than the window
  manual        autoinvoke false / disable-model-invocation (never advertised)
  unadvertised  no description (the model cannot see or pick it)
  ghost         loaded historically, not registered or found in any project source
"""

import argparse
import collections
import datetime
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys

DB = os.path.expanduser("~/.local/share/opencode/opencode.db")
STORAGE_PART = os.path.expanduser("~/.local/share/opencode/storage/part")
GLOBAL_SOURCES = ["~/.config/opencode/skills", "~/.claude/skills", "~/.agents/skills"]
PROJECT_SOURCES = [".opencode/skills", ".claude/skills", ".agents/skills"]
MS_DAY = 86_400_000


def iso(t):
    return datetime.datetime.fromtimestamp(t / 1000, datetime.UTC).isoformat()


def parse_part(d, fallback_time=None):
    """Return (tool, time_ms, skill_id, status, error) for tool parts."""
    if d.get("type") != "tool":
        return None
    state = d.get("state") or {}
    inp = state.get("input") or {}
    t = (state.get("time") or {}).get("start") or fallback_time
    return (
        d.get("tool"),
        t,
        inp.get("name") or inp.get("id"),
        state.get("status"),
        state.get("error"),
    )


def load_parts():
    """Yield (part_dict, fallback_time_ms, session_directory|None)."""
    try:
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        cur = con.cursor()
        cur.execute(
            "select p.time_created, p.data, s.directory"
            " from part p left join session s on s.id = p.session_id"
        )
        for tc, data, directory in cur:
            try:
                yield json.loads(data), tc, directory
            except (json.JSONDecodeError, TypeError):
                continue
        con.close()
        return
    except sqlite3.Error:
        pass  # schema changed or DB missing; use the JSON part files
    for path in glob.glob(os.path.join(STORAGE_PART, "*", "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                yield json.load(fh), None, None
        except (OSError, json.JSONDecodeError):
            continue


def current_skills():
    """Registered skills from the running server: id -> {path, description, autoinvoke}.

    Returns None when the server is unreachable, so the caller can fall back
    to a filesystem scan.
    """
    try:
        out = subprocess.run(
            ["opencode", "api", "get", "/api/skill"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        data = json.loads(out.stdout)["data"]
        return {
            s["id"]: {
                "path": s.get("path") or "",
                "description": s.get("description") or "",
                "autoinvoke": s.get("autoinvoke", True),
            }
            for s in data
        }
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError):
        return None


def scan_skills_dir(base):
    """Map skill ID -> entry file: root-level *.md and SKILL.md at any depth."""
    found = {}
    if not os.path.isdir(base):
        return found
    try:
        entries = list(os.scandir(base))
    except OSError:
        return found
    for entry in entries:
        try:
            if entry.is_file() and entry.name.endswith(".md"):
                found[entry.name[:-3]] = entry.path
        except OSError:
            continue
    for path in glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True):
        found.setdefault(os.path.basename(os.path.dirname(path)), path)
    return found


def frontmatter_flags(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.read(4000)
    except OSError:
        return False, False
    m = re.match(r"^---\s*\n(.*?)\n---", head, re.DOTALL)
    fm = m.group(1) if m else ""
    manual = bool(
        re.search(r"disable-model-invocation:\s*true", fm)
        or re.search(r"opencode/autoinvoke:\s*false", fm)
    )
    described = bool(re.search(r"^description:\s*\S", fm, re.MULTILINE))
    return manual, described


def file_age_days(path):
    """Days since the skill file's mtime, or None when the path is unusable."""
    try:
        now = datetime.datetime.now().timestamp()
        return max(0.0, (now - os.path.getmtime(path)) / 86_400)
    except (OSError, TypeError):
        return None


def find_project_skills(session_dirs):
    """Scan session directories and their ancestors for project skill sources."""
    found = {}
    for start in session_dirs:
        if not start or not os.path.isdir(start):
            continue
        cur = os.path.abspath(start)
        while True:
            for rel in PROJECT_SOURCES:
                found.update(scan_skills_dir(os.path.join(cur, rel)))
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--days",
        type=int,
        default=90,
        help="window for dead-skill detection (default: 90)",
    )
    ap.add_argument("--tools", action="store_true", help="also count every tool")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    now = datetime.datetime.now(datetime.UTC).timestamp() * 1000
    cutoff = now - args.days * MS_DAY

    tools = collections.Counter()
    months = collections.defaultdict(collections.Counter)
    skills = {}  # id -> {all, win, last, errors[]}
    session_dirs = set()
    for d, tc, directory in load_parts():
        if directory:
            session_dirs.add(directory)
        parsed = parse_part(d, tc)
        if not parsed:
            continue
        tool, t, sid, status, error = parsed
        if args.tools:
            tools[tool] += 1
        if tool != "skill" or not sid:
            continue
        rec = skills.setdefault(sid, {"all": 0, "win": 0, "last": 0, "errors": []})
        rec["all"] += 1
        if t:
            if t >= cutoff:
                rec["win"] += 1
            rec["last"] = max(rec["last"], t)
            months[iso(t)[:7]][sid] += 1
        if status == "error":
            msg = error if isinstance(error, str) else json.dumps(error)
            rec["errors"].append(msg)

    # id -> {global, manual_only, described, age}; `global` marks the user's
    # own prunable sources (builtins and other projects' skills are excluded).
    registry = {}
    api = current_skills()
    if api is not None:
        for sid, s in api.items():
            path = s["path"]
            registry[sid] = {
                "global": any(
                    path.startswith(os.path.expanduser(src)) for src in GLOBAL_SOURCES
                ),
                "manual_only": not s["autoinvoke"],
                "described": bool(s["description"]),
                "age": file_age_days(path),
            }
    else:
        for src in GLOBAL_SOURCES:
            for sid, path in scan_skills_dir(os.path.expanduser(src)).items():
                manual, described = frontmatter_flags(path)
                registry[sid] = {
                    "global": True,
                    "manual_only": manual,
                    "described": described,
                    "age": file_age_days(path),
                }

    project = find_project_skills(session_dirs)

    rows = []
    for sid, rec in skills.items():
        reg = registry.get(sid)
        rows.append(
            {
                "id": sid,
                **rec,
                "last": iso(rec["last"])[:10] if rec["last"] else "",
                "registered": reg is not None or sid in project,
                "global": reg["global"] if reg else False,
                "manual_only": reg["manual_only"] if reg else False,
                "described": reg["described"] if reg else True,
            }
        )
    rows.sort(key=lambda r: -r["all"])

    dead, unadvertised, manual = [], [], []
    for sid, reg in registry.items():
        if not reg["global"]:
            continue
        rec = skills.get(sid)
        if reg["manual_only"]:
            manual.append(sid)
        elif not reg["described"]:
            unadvertised.append(sid)
        elif (not rec or rec["win"] == 0) and (
            reg["age"] is None or reg["age"] >= args.days
        ):
            dead.append(
                (
                    sid,
                    rec["all"] if rec else 0,
                    iso(rec["last"])[:10] if rec and rec["last"] else "never",
                )
            )
    ghosts = [r for r in rows if not r["registered"]]

    if args.json:
        print(
            json.dumps(
                {
                    "days": args.days,
                    "source": "api" if api is not None else "filesystem",
                    "skills": rows,
                    "dead": [{"id": s, "all": a, "last": l} for s, a, l in dead],
                    "unadvertised": unadvertised,
                    "manual": manual,
                    "ghosts": ghosts,
                },
                indent=2,
            )
        )
        return 0

    if args.tools:
        print("== tool calls ==")
        for t, c in tools.most_common():
            print(f"{c:>6}  {t}")
    print(f"== skill loads (win = last {args.days}d) ==")
    for r in rows:
        marks = []
        if not r["registered"]:
            marks.append("NOT-REGISTERED")
        elif not r["global"]:
            marks.append("project-source")
        if r["manual_only"]:
            marks.append("manual-only")
        if not r["described"]:
            marks.append("no-description")
        print(
            f"{r['all']:>5}  win={r['win']:<4} last={r['last'] or 'never':<10} {r['id']}"
            + (f"  [{', '.join(marks)}]" if marks else "")
        )
    print("== by month ==")
    for m in sorted(months):
        print(f"{m}  {dict(months[m].most_common())}")

    print(
        f"== dead: global source, advertised, 0 loads in {args.days}d, "
        f"file at least {args.days}d old (prune or fix) =="
    )
    for sid, count, last in dead:
        print(f"  {sid}  (all={count}, last={last})")
    if not dead:
        print("  none")
    print("== never advertised: no description (model cannot see them) ==")
    for sid in unadvertised:
        print(f"  {sid}")
    if not unadvertised:
        print("  none")
    print("== manual-only: autoinvoke off (intentional, not dead) ==")
    for sid in manual:
        print(f"  {sid}")
    if not manual:
        print("  none")
    print(
        "== ghosts: loaded before, not registered or project-local (deleted/renamed) =="
    )
    for r in ghosts:
        print(f"  {r['id']}  (all={r['all']}, last={r['last'] or 'never'})")
    if not ghosts:
        print("  none")
    print("== failed loads (error text includes the available-skills list) ==")
    seen = set()
    for r in rows:
        for msg in r["errors"]:
            key = (r["id"], msg)
            if key not in seen:
                seen.add(key)
                print(f"  {r['id']}: {msg[:140]}")
    if not seen:
        print("  none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
