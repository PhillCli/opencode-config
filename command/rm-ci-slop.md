---
description: Remove Slop from CI/CD pipelines
---

Scan common CI/CD for all ci-cd piplines YAML definitions. Remove all slop, do not change any functional behavior otherwise.
We define slop as anything that contributes to low signal-to-noise ratio about what pipelines does, suggest if for removal as well.

This includes, but it not limited to:
- asci-arts,
- empty echo " " and unecessary line breaks,
- colorful printouts,
- overbose echos,
- section collapses,

We want to see crisp pipeline logic in section related to running the script (i.e. 'scripts:' in Gitlab CI/CD).

Report at the end with only a 1-3 sentence summary of what you changed
