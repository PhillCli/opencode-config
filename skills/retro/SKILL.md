---
name: retro
description: Propose improvements to the agent environment at the end of a session - skills, commands, agents, AGENTS.md, permissions, formatters, tooling - most severe first. Use when the user wraps up the session ("that's all", "wrap up", "done for today") or asks for a retro, and the session had friction: rework loops, permission prompts, repeated corrections. Skip clean sessions.
license: MIT
---

# Retro

Propose changes to the agent's environment, not the project's code. Default to the current session; read session history if the user names another one.

## Scan for friction

- **Steering gaps**: steps the agent redid because a rule, pointer, or check was missing. An AGENTS.md line, skill, or command that would have prevented the friction.
- **Broken checks**: a check that exists but sat unwired or silently broken (formatter, lint, CI, mise task). A repo with no guardrail is itself a finding.
- **Permission friction**: prompts that broke flow; a permission rule to loosen or tighten.
- **Tool economy**: expensive tool calls a narrower command or a skill would have saved.
- **No-ops**: steering-file lines that do not change the agent's behavior.
- **Information access**: a crucial piece of information the agent could not reach.

## Propose

List candidates most severe first. One line each: what to change, in which file of the opencode-config repo (skills/, commands/, agents/, AGENTS.md, opencode.json), and which friction it removes.

Before proposing a new skill, check an existing one covers it (`mise run skill-audit` in the config repo); prefer sharpening an existing description over adding a file. Judgement-call standards go to the review stage (reviewer agent rules), not the implementation context, which stays lean.

Propose only. Ask before editing anything.

Adapted from mattpocock/skills `retro` (MIT), condensed.
