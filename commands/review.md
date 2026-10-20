---
description: Bugs-first review of local changes or a GitLab MR
---

Review $ARGUMENTS.

If an MR IID was given, or this branch has an open GitLab MR, load the `mr-review` skill and follow it. Show findings and ask before posting.

Otherwise review the local diff against the default branch. Bugs, security, and broken behavior first. No style nits. No pre-existing issues unless the change depends on them. Do not edit unless asked.

For both review paths, give each finding a priority, file:line, and three concise parts:

- **Issue:** The specific trigger, broken behavior, and impact. Make the reason for the priority clear. P1 means a validated defect breaking core behavior under expected conditions; P2 means a validated defect with narrower impact, not an optional suggestion. State uncertainty separately from priority.
- **Suggested fix:** Recommend the simplest sound change within the existing design, with any important tradeoff. Prefer one approach over a menu of options. If the implementation depends on an unresolved design choice, describe the required outcome and preferred approach rather than inventing certainty.
- **Verify:** Give the shortest useful repro or acceptance check. Distinguish checks already run from checks merely proposed.

Recommendations are advisory: do not implement fixes, add test files, or change infrastructure unless asked.
