---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions - build a red feedback loop, minimise, ranked hypotheses, instrument, fix, regression-test. Use when the user reports something broken, throwing, failing, or slow, or says diagnose/debug this.
license: MIT
---

# Diagnosing bugs

Skip a phase only when you explicitly justify it. Redact every secret before showing commands, outputs, and captured artifacts.

## Phase 1: build a feedback loop

This is the skill; everything else is mechanical. A **red** signal - one command that goes red on this bug and green once fixed - finds the cause. No red signal, no theory-building: reading code to build a hypothesis before this command exists is the exact failure this skill prevents.

Loop forms, roughly in order: failing test at the nearest seam; curl/CLI script with a fixture input diffed against known-good; `terraform validate`/`plan` diff or `kubectl diff --dry-run`; replay of a captured trace/payload; throwaway harness (one service, mocked deps); property/fuzz loop for "sometimes wrong" bugs; bisect harness between two known states; differential run (same input through old vs new version/config). Last resort: a bash script walking the human through steps only they can perform.

Phase 1 is done when you can name **one command, already run at least once**, that is:

- [ ] **Red-capable**: drives the real bug path and asserts the user's exact symptom, not "runs without erroring"
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate - 50% is debuggable, 1% is not)
- [ ] **Fast**: seconds, not minutes
- [ ] **Agent-runnable**: unattended

Tighten the loop like a product: faster, sharper signal (assert the symptom, not "didn't crash"), more deterministic (pin time, seed RNG, isolate filesystem/network).

If you cannot build a loop, stop and say so. List what you tried. Ask for a reproducing environment, a redacted captured artifact, or permission for temporary instrumentation. Do not hypothesise without a loop.

## Phase 2: reproduce + minimise

Run the loop red. Confirm the failure is the one the user described, not a different failure nearby. Then shrink to the smallest scenario that still goes red: cut inputs, callers, config, data one at a time, re-running after each cut. Done when every remaining element is load-bearing - removing any one turns it green.

## Phase 3: hypothesise

Generate 3-5 ranked hypotheses before testing any of them (single-hypothesis generation anchors on the first plausible idea). Each must be falsifiable: "if X is the cause, changing Y makes the bug disappear / changing Z makes it worse." Show the ranked list to the user - domain knowledge re-ranks instantly - but do not block on it.

## Phase 4: instrument

Each probe maps to one hypothesis's prediction; change one variable at a time. Prefer debugger/REPL over logs; targeted logs at the boundaries that distinguish hypotheses; never log everything and grep. Tag every debug log with a unique prefix (e.g. `[DEBUG-a4f2]`) so cleanup is one grep. Perf regressions: logs are usually wrong - establish a baseline measurement, then bisect. Measure first, fix second.

## Phase 5: fix + regression test

Write the regression test before the fix, only if a **correct seam** exists: one where the test exercises the real bug pattern as it occurs at the call site. If no correct seam exists, that itself is the finding - the architecture prevents locking the bug down; flag it. Otherwise: red test, fix, green test, re-run the Phase 1 loop against the original un-minimised scenario.

## Phase 6: cleanup

- [ ] Original repro no longer reproduces (re-run the loop)
- [ ] Regression test passes (or the missing seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (grep the prefix)
- [ ] Throwaway prototypes deleted
- [ ] The hypothesis that turned out correct stated in the commit/MR message

Adapted from mattpocock/skills `diagnosing-bugs` (MIT), condensed.
