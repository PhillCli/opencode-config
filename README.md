# opencode-config

Global OpenCode config, versioned here and symlinked into `~/.config/opencode/`:

- `skills/`, `commands/`, `agents/`, `AGENTS.md` — symlinked live
- `plugins/` — versioned source; the V2 global plugin loader fails on symlinked entrypoints (anomalyco/opencode#23553), so `~/.config/opencode/plugins/` holds generated one-line re-export shims instead — refreshed by `mise run install`
- `opencode.json` — loaded as project config in this repo, so it overrides `~/.config/opencode/opencode.json` while the workspace is here. Other projects load only the global file, synced by `mise run install`. No secrets (use `{env:VAR}`).

Primary agent is OpenCode `build`. `AGENTS.md` is a short overlay, not a replacement prompt. The only custom subagent is `reviewer`. Start a new session after agent changes; an open session keeps the agent it started with.

## Usage

- Install/refresh the preset in `~/.config/opencode/` (symlinks, `opencode.json`, plugin shims): `mise run install`
- Clone with `--recurse-submodules` (or run `git submodule update --init`) before `mise run install` — `skills/` is submodule-backed and symlinked as-is
- Update git-submodule skills: `./scripts/update-skills.sh`
- Skill usage audit — dead/ghost/error analysis over a time window. Reads the
  OpenCode session DB read-only plus the running server's skill list:
  `python3 scripts/skill-usage.py` (options: `--days 90`, `--json`, `--tools`)

## Pruning policy

Review skill usage quarterly (`mise run skill-audit`). Act on the report
buckets:

- `dead` (on disk, advertised, zero loads in the window): archive on a branch
  and remove from main
- `never advertised` (no `description`): fix the frontmatter or drop the skill
- `manual-only` (`autoinvoke` off) and ghosts (deleted/renamed skills): no
  action, listed for context
- `failed loads`: the model guessed an ID that did not resolve — rename the
  skill or sharpen its description
