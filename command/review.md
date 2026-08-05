---
description: Code review with reviewer-researcher consensus loop and GitLab MR integration
---

Review $ARGUMENTS

Review code changes using a reviewer-researcher consensus loop that grounds findings in SOTA best practices before delivering a verdict.

## Workflow

1. **Gather context** — Determine the review target:
   - If $ARGUMENTS has an MR IID (number), load the `mr-review` skill and run its `get-mr-context.sh --mr <IID>` for MR metadata + diffs
   - If no IID, check for an open MR on the current branch: `glab mr list --source-branch $(git branch --show-current) 2>/dev/null`
   - If no MR, fall back to local diff: determine base branch (`origin/main` if it exists, else `origin/master`, else `main`), then `git diff --merge-base <base> -- .`
   - Run automated checks in parallel (tests, type-check, lint)
   - Ask me the purpose if unclear from MR description or commits

2. **Initial review pass** — Spawn @reviewer with diffs, MR metadata, check results, and stated purpose. @reviewer produces initial findings (location, category, severity P0–P3, what's wrong, suggested fix).

3. **Consensus loop** — Iterate up to 3 times. Exit early when findings converge (no additions, removals, or modifications since last iteration).
   - a) **@researcher turn**: Given @reviewer's current findings + relevant diff snippets, research SOTA best practices for each flagged pattern. Verify whether the issue is genuine against current standards. Find authoritative references (official docs, RFCs, established patterns, library docs). Flag false positives. Surface missed issues that SOTA patterns would catch. Output: annotated findings with research backing + new candidate findings.
   - b) **@reviewer turn**: Given @researcher's annotations + previous findings. Drop false positives confirmed by research. Strengthen confirmed findings with authoritative references. Evaluate new candidates from @researcher. Refine suggested fixes based on SOTA solutions. Output: updated findings list.
   - c) **Convergence check**: No findings added/removed/modified → converged, exit loop. Changed and iterations < 3 → continue. Iterations = 3 → force exit, note unresolved disagreements between reviewer and researcher.

4. **Verdict** — Combine converged findings:
   - **P0** Critical — must fix before merge (bugs, security, breaking changes)
   - **P1** Important — should fix before merge
   - **P2** Suggestion — worth considering
   - **P3** Nit — minor preference
   - Recommendation: Approve / Approve with notes / Request changes

5. **Format comments** — Follow the `mr-review` skill rubric. Each finding becomes a GitLab MR comment.
   - **Sound human**: matter-of-fact tone, like a colleague leaving a remark or nitpick. NO AI indicators — no `:robot:`, no "AI-generated" labels, no machine phrasing. No AI vocabulary ("delve", "navigate", "tapestry", "realm", "leverage", "embark"). No em dash overuse, no rule-of-three patterns, no promotional language. At most 1 paragraph per finding. Backticks for all code elements (annotations, method names, variables) to prevent accidental mentions. Use "MR" not "PR". State why the issue is a problem, matter-of-fact, not accusatory.
   - **Code suggestions**: Where a concrete fix exists, include a GitLab suggestion block (triple-backtick `suggestion` fence containing the replacement code) in the positioned diff comment. This creates an "Apply suggestion" button in GitLab. Only include suggestions when the fix is clear and unambiguous — for conceptual issues, describe the problem without a suggestion block.

6. **Present and post** — Show me the verdict and all findings with severity, location, description, and code suggestions. Ask for confirmation before posting anything. After confirmation, post via the `mr-review` skill's `post-comment.sh` (positioned diff comments with `--file`/`--line` or `--old-line`, general comment for overall verdict). If no MR (local review only), skip posting and present findings inline.
