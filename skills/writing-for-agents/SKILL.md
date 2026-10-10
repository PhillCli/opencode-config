---
name: writing-for-agents
description: Writing discipline for documents agents consume - skills, commands, AGENTS.md, and anything reached by a pointer. Use when creating or editing any of those, including through the skill-creator skill.
license: MIT
---

# Writing for agents

The same levers make every agent-consumed document predictable: the agent takes the same process every run rather than producing the same output.

## Context pointers

A **context pointer** names out-of-context material and encodes when to reach it (a skill description, an AGENTS.md line). The wording, not the target, decides when it fires. A must-have target behind a weakly worded pointer is a variance bug: sharpen the wording first, inline only if sharpening fails.

- Front-load the leading trigger word.
- One trigger per branch: synonyms renaming one case are one branch written twice.
- Cut identity the body already carries.

## Two loads

- **Context load**: always-loaded material spends tokens and attention every turn, fired or not. Prune it hard.
- **Cognitive load**: the human's cost of knowing what exists and when to reach for it. Spend it where human judgement matters; remove it where it does not.

## Information hierarchy

Rank each piece by how immediately the agent needs it:

1. **In-file step**: what the agent does, in order.
2. **In-file reference**: rules consulted on demand. A flat peer-set (every rule of a review on one rung) is a fine arrangement.
3. **Disclosed reference**: pushed behind a pointer into a sibling file, loaded only when the pointer fires.

Push too little down and the top bloats; push too much and you hide material the agent needs. Inline what every branch needs; disclose what only some branches reach.

## Completion criteria

Every step ends on a criterion the agent can check: done vs not-done. A vague bound ("understanding reached") invites premature completion. The strongest criteria are both checkable and exhaustive ("every modified module accounted for").

## Leading words

A compact pretrained concept (_frontier_, _red_, _sediment_) anchors a region of behaviour in one token by recruiting priors the model already holds. Prefer an existing word over coining one: a made-up word pays in definition tokens what a pretrained word gives free. Collapse passages that restate one idea into a single token.

**Prompt the positive.** Prohibition drags the forbidden behaviour into context (don't think of an elephant). State the target behaviour; reserve a ban for what cannot be phrased positively.

## Pruning

- One meaning, one source of truth. Duplication inflates prominence and costs maintenance.
- The environment is a source of truth (mise tasks, config, `--help`). A doc restating it is a cache: keep only what cannot be looked up - the unwritten convention, the reason behind a choice, the gotcha no config confesses.
- Hunt no-ops sentence by sentence: an instruction the model obeys by default says nothing. Delete the whole sentence, don't trim words from it.
- The default fate is **sediment**: stale layers settling because adding feels safe and removing feels risky. Shorter documents stay relevant.

Adapted from mattpocock/skills `writing-for-agents` (MIT), condensed.
