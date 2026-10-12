---
name: stacked-split
description: Split a feature branch into stacked review branches (series of MRs) by replaying commits onto a new base - recipe persistence, carving big commits into file groups, dependency-ordered cherry-picks, hook-gated tips, byte-identity proof. Use when the user says split, carve, or stack a branch into MRs or review chunks, or replay commits onto another base.
license: MIT
---

# Stacked split

Replay a feature branch as a stack of smaller branches for review, keeping the final tip byte-identical to the original.

## Before the first pick

- Write the recipe - series names, branch names, commit list per series, dependency notes - to a scratch file (e.g. `/tmp/opencode/<split>.md`) and tick commits off as they land. Resume from the file, not from memory.
- Confirm the recipe with the user before the first pick; reassigning a commit between series mid-run changes what reviewers see, so ask first.
- Branch the first series off the trunk the user names (`origin/main` unless stated) and stack each later series on the previous tip. Pushing and MR creation stay with the user.

## Building a series

- Carve a big commit into file-group commits with `git checkout <commit> -- <path>`, one theme per commit; close the group by accounting for every hunk in `git diff <big-commit> HEAD --stat`.
- Order picks dependency-first - a pick needs its imports and diff context on disk. Find which commits touch a file with `git log --format='%h %s' <branch> -- <file>`.
- Cherry-pick with original subjects and `--keep-redundant-commits` so replayed empty picks stay as records (`--empty=keep` needs git >= 2.45; check `git --version` first).
- Gate each tip (repo hooks + fast tests), not each intermediate: intermediates replay historical hook states.
- An intermediate failing today's hooks (a linter tightened after the original commit): fold the curing commit earlier in the series when it applies clean; otherwise `--no-verify` that one commit and disclose it in the summary; ask when neither works.
- An empty first pick usually means the base already carries the content via a redo commit - verify with `git diff <base> <pick>^ -- <paths>` and skip with a note.

## Finishing

- Prove the replay with `git diff <original-tip> <final-tip>`: empty, or only base-side drift (lockfile/dev-dep bumps the trunk carries) with every hunk named.
- Report each branch - name, commits, gate result - for the user to push.
