# opencode.db reference (ad-hoc usage analysis)

Schema notes for `~/.local/share/opencode/opencode.db`, the main store (every
session). Neither store is a public contract; re-verify shapes after OpenCode
upgrades. `skill-usage.py` encodes the same knowledge for its own path.

- No `sqlite3` CLI on this machine: use `python3` heredocs with
  `sqlite3.connect(f"file:{DB}?mode=ro", uri=True)`.
- Times are ms epochs. `opencode-tui-v2.db` is a small legacy TUI store with a
  different `session_message` shape - ignore it for usage analysis.

## Table map

| Table | What it holds |
| --- | --- |
| `session` | TUI-facing session row: `agent`, `model`, `cost`, `tokens_*`, `directory`, `time_created` |
| `session_v2` | Engine-side near-duplicate of `session`; prefer `session` (it carries agent/model) |
| `message` | Message metadata JSON `{role, agent, model, summary, tools}` - no text |
| `part` | Per-message parts: `type` = tool / text / reasoning / step-start / step-finish / patch / agent / compaction |
| `session_message` | User prompts: `data` JSON `{text, time}` |
| `project`, `todo`, `event`, `kv`, `instruction_*`, `workspace`, `worktree` | Supporting state; rarely needed |

## JSON shapes (`part.data`)

- tool part: `{type: "tool", tool, callID, state: {input, output, status, error, time}}`
- text part: `{type: "text", text}` (assistant text; user text lives in `session_message`)
- agent part: `{type: "agent", name}` (subagent boundary)

## Common queries

- Tool calls: `part` where `json_extract(data,'$.type')='tool'`, group by `$.tool`
- Skill loads: `$.tool='skill'`, id from `state.input.name` (or `.id`)
- Subagents: `$.tool='task'`, type from `state.input.subagent_type`
- Monthly trend: join `part.session_id` to `session.time_created`
- Prompt openings: `json_extract(data,'$.text')` from `session_message`

## Traps

- `session_message` is a `data` JSON column in the main DB but a `text` column
  in `opencode-tui-v2.db` - "no such column: text" means wrong DB.
- Assistant text lives in `part` (`type='text'`); `message.data` has no body.
- Fallback if the DB is unreadable: JSON part files under
  `~/.local/share/opencode/storage/part/`.
