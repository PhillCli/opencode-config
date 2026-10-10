---
name: grilling
description: Interview the user relentlessly about a plan, decision, or change until every branch of the design tree is resolved. Use when the user says "grill me", asks to stress-test or align on a plan before implementation, or before a risky change (terraform apply, k8s rollout, migration, wide refactor).
license: MIT
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Model the plan as a **design tree**: every decision branches into the decisions that hang off it.

## Rounds

Work the tree in rounds. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask now without guessing at answers you have not heard yet.

Each round:

1. Ask the whole frontier at once: every unblocked question, numbered, each with your recommended answer underneath. Word each question so "yes" accepts the recommendation.
2. Wait for the answers. Settled decisions push the frontier outward; recompute it and ask the next round.

A question whose answer depends on another question still open in this round belongs to a later round, not this one.

Present a round with the question tool when the questions fit its option format (recommended option first); otherwise as numbered markdown.

## Facts vs decisions

- **Facts are your job.** When a frontier question needs a fact from the environment (repo, cluster, docs), dispatch a subagent to find it; never ask the user what you can look up. Do not block the round on it: only questions downstream of the running exploration wait for it.
- **Decisions are the user's.** Put each to the user and wait.

## Done

The frontier is empty: every branch visited, nothing left silently assumed. Do not act on the plan until the user confirms shared understanding.

Adapted from mattpocock/skills `grilling` (MIT), condensed.
