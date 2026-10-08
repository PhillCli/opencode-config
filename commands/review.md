---
description: Bugs-first review of local changes or a GitLab MR
---

Review $ARGUMENTS.

If an MR IID was given, or this branch has an open GitLab MR, load the `mr-review` skill and follow it. Show findings and ask before posting.

Otherwise review the local diff against the default branch. Bugs, security, and broken behavior first. No style nits. No pre-existing issues unless the change depends on them. Do not edit unless asked.
