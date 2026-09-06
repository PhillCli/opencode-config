#!/usr/bin/env python3
"""Skill usage analytics from OpenCode's session DB (read-only)."""

import collections
import datetime
import json
import os
import sqlite3
import sys

DB = os.path.expanduser("~/.local/share/opencode/opencode.db")


def iso(tc):
    if isinstance(tc, (int, float)):
        return datetime.datetime.fromtimestamp(tc / 1000, datetime.UTC).isoformat()
    return str(tc or "")


def main():
    show_tools = "--tools" in sys.argv
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()

    skills = collections.Counter()
    last = {}
    months = collections.defaultdict(collections.Counter)
    tools = collections.Counter()

    query = "SELECT time_created, data FROM part"
    if not show_tools:
        query += ' WHERE data LIKE \'%"tool":"skill"%\''
    for tc, data in cur.execute(query):
        try:
            d = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            continue
        if d.get("type") != "tool":
            continue
        s = iso(tc)
        tool = d.get("tool")
        tools[tool] += 1
        if tool == "skill":
            sid = ((d.get("state") or {}).get("input") or {}).get("name") or "?"
            skills[sid] += 1
            if s > last.get(sid, ""):
                last[sid] = s
            if s:
                months[s[:7]][sid] += 1

    if show_tools:
        print("== tool calls ==")
        for t, c in tools.most_common():
            print(f"{c:>6}  {t}")
    print("== skill loads ==")
    for sid, c in skills.most_common():
        print(f"{c:>5}  last={last[sid][:10]}  {sid}")
    print("== by month ==")
    for m in sorted(months):
        print(f"{m}  {dict(months[m].most_common())}")


if __name__ == "__main__":
    main()
