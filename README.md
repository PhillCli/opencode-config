# opencode-config

Global OpenCode config, versioned here and symlinked into `~/.config/opencode/`:

- `skills/`, `commands/`, `agents/`, `AGENTS.md` — symlinked live
- `opencode.json` — **template only**; the live config is `~/.config/opencode/opencode.json`. No secrets here (use `{env:VAR}` substitution).

## Usage

- Update git-submodule skills: `./scripts/update-skills.sh`
- Skill usage analytics (reads `~/.local/share/opencode/opencode.db`, read-only):
  `python3 scripts/skill-usage.py`

## Pruning policy

Review skill usage quarterly (`scripts/skill-usage.py`). Skills with zero loads
after ~3 months get archived on a branch and removed from main.
