---
description: Explain what this preset provides and how to use it
---

Explain this OpenCode preset. Be practical and short.

## How it works

- The primary agent is OpenCode `build`. It acts. It is not an orchestrator.
- Plan mode is opt-in. Use the `plan` agent, or ask for a plan, on architectural or risky work.
- `AGENTS.md` adds short global rules on top of the model prompt. It does not replace that prompt.
- Built-in `explore` and `general` are for wide or isolated digs. `reviewer` is a read-only second pass. Do not delegate ordinary edits.
- Skills load when the task is in that domain (GitLab, Terraform, Terragrunt, and others in `skills/`).
- You own git. The agent does not commit or push unless you ask, run `/commit`, or grant it for the session.

## Commands

- `/commit` — stage and commit with a conventional subject, no confirmation step
- `/review` — bugs-first review; GitLab MR posting goes through the mr-review skill
- `/test` — write or run tests the way this repo already does
- `/debug` — reproduce, fix, add a regression test
- `/refactor` — small steps, tests after each step, no commit unless asked
- `/research` — repo plus web, with links and file:line references
- `/document` — update docs to match the code
- `/init` — write a short project `AGENTS.md` (commands and conventions only)
- `/gather-context` — working tree and recent commits
- `/rmslop` — strip AI slop from the branch diff
- `/rm-ci-slop` — strip noise from CI YAML without changing behavior

Start a new session after harness changes. An existing session keeps the agent it started with.
