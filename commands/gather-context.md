---
description: Summarize repository state and recent changes
---

Summarize the repo for $ARGUMENTS.

Working tree and recent commits:

!`git status -sb && echo '---' && git diff --stat && echo '---' && git log --oneline -10`

Cite file:line for anything that matters. Skip subagents unless the search is wide.
