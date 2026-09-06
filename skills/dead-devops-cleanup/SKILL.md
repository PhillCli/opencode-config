---
name: dead-devops-cleanup
description: Find and remove dead DevOps surface area (CI/CD, Docker, Compose, Make, entrypoints, deploy helpers, test harness scripts, ops-only docs). Use when the user asks to clean dead infra/CI/scripts, remove unused Docker/Compose/Make/CI paths, delete orphan deploy or prestart/wait_for_db helpers, or prune devops dead code without touching app business logic.
---

# Dead DevOps / infra / CI / test-harness cleanup

## Role

Clean **dead DevOps surface area**: CI/CD, containers, Compose/local runners, Make/task targets, entrypoints, deploy helpers, test-harness utilities, and docs that only describe those paths.

**Do not touch application business logic** except pure harness/utilities that exist only for local/CI startup—and only after proving zero live callers.

Prefer **delete** over rewrite. Prefer **separate crisp commits** over one blob.

## Scope (in)

| Area | Examples |
|------|----------|
| CI/CD | Pipeline configs, included job files, unused jobs/rules/variables |
| Containers | Dockerfiles, ignore files, image entrypoints/scripts |
| Local run | Compose files, root run/stop/build shells |
| Task runners | Make/task targets nobody invokes |
| Ops packaging leftovers | Orphan lock/requirements files after a packaging migration |
| Test **infra** | DB-wait scripts, coverage wrappers, bootstrap shells not used by the test runner or CI |
| Deploy leftovers | Remote deploy/render/SSH helpers no longer wired into any pipeline |
| Docs | Sections that only document removed commands |

## Scope (out)

- Domain/application code (APIs, services, models, business rules)
- Product test cases and fixtures that exercise behavior
- Schema/migration **revision** history (unless a revision file is proven unused *and* user approves)
- Dependency bumps or “align with sister service” refactors
- Live entrypoint rewrites unless required to drop a dead path

When unsure app vs devops: **stop and ask** with evidence.

## Hard rules

1. **Prove dead before delete.** Dead means:
   - no references outside the file (mutual refs inside a dead cluster = one cluster), and
   - not invoked by image `CMD`/`ENTRYPOINT`, Compose `command`/`entrypoint`, task runner, CI job, deploy manifests in-repo, or a documented operator path still in the README.
2. **Trace the live path first.** Inventory before deleting:
   - image start → entrypoint → migrate? → process
   - local test → task/CI → dependencies (e.g. DB) → test runner
   - deploy → what still runs after merge
3. **Do not break the live contract.** Match how the service actually starts today (including any bootstrap that only runs under `__main__` or a specific entry module).
4. **Fail-fast + orchestrator restart is fine.** Do not reintroduce readiness-wait helpers unless a real single-shot path has no restart policy and needs them.
5. **Separate commits**, one concern each.
6. **No drive-by** formatting, renames, or live-pipeline “improvements.”
7. **Secrets / examples:** never put real secrets in example env files; don’t delete env fixtures CI still injects.
8. **Ask before** deleting anything that might only live in external runbooks, other repos, or shared pipeline libraries. Flag residual risk instead of guessing.

## Workflow

### 1. Map live surfaces

```text
Runtime:   [image CMD/ENTRYPOINT] → [script] → [process]
Local app: [task/compose target] → …
Local test:[task / CI job] → [deps setup] → [test runner]
CI build:  [jobs] → [image target]
CI test:   [jobs] → [env/fixtures] → …
Deploy:    [still in-repo? external?]
```

Cite paths. Mark each node LIVE or UNKNOWN.

### 2. Candidate harvest

Likely dead clusters:

- Script trees not referenced by Docker/Compose/Make/CI
- `prestart` / `wait_for_*` / coverage-wrapper / legacy start shells
- CI include trees not pulled in by the root pipeline file
- Compose files never passed as `-f`
- Task targets never referenced in docs/CI/other targets
- Image stages/targets with no consumer
- Auth/secret mounts for unused private package sources
- Duplicate old + new Dockerfiles after a migration
- Docs for removed commands

### 3. Reference proof (per candidate)

```bash
# exclude VCS, lockfiles, virtualenvs
rg -n "basename_or_symbol" --glob '!.git/**' --glob '!**/.venv/**' --glob '!**/node_modules/**'
```

Also check:

- image `CMD`/`ENTRYPOINT` and Compose overrides
- CI includes and job scripts
- task-runner graphs
- whether the test runner would collect the file (helper name vs `test_*` pattern)

| Class | Action |
|-------|--------|
| Dead cluster | Delete in one commit |
| Live | Leave |
| Only mutual refs | Delete whole cluster together |
| External-only suspicion | Report, don’t delete |
| Ambiguous | Ask |

### 4. Execute

- Delete only proven-dead paths
- Update README/task files only where they **reference** deleted paths
- No replacement features
- Commit body: what was unused + what the live path is

### 5. Verify

- Search again for deleted basenames → zero hits (except history)
- Image entrypoint path still exists and matches config
- Lint/validate CI config if the project has a standard check
- Run the **minimal** task/job that proves a changed harness path; don’t boil the ocean

### 6. Report

```markdown
## Dead DevOps cleanup

### Live path (unchanged)
- …

### Removed (per commit)
- `commit`: files — why dead — replaced by …

### Left alone (with reason)
- …

### Residual risks
- external runbooks / other repos / prod overrides
```

## Heuristics

- **Image CMD/ENTRYPOINT + Compose command/entrypoint** beat unreferenced script trees.
- Scripts that only call each other are **one dead cluster**.
- Path under `tests/` ≠ used by tests; prove import or collection.
- Orchestrator restart/healthchecks often replace in-process wait loops; prefer infra-level ordering for local UX if needed (separate change).
- Sister-service entrypoint style is **not** a drop-in without verifying startup side effects.
- Drop unused registry credential mounts when no package source needs them.
- Tooling migrations often orphan entire old CI/deploy trees—delete only after the root pipeline no longer includes them.

## Commit style

- Conventional commits: `chore:` / `ci:` / `build:`
- One concern per commit
- Body: unused path + live replacement
- No mixed app + infra commits

## Reject

- Base-image/runtime bumps unless asked
- Rewriting entrypoints to match another service
- Deleting migration history or domain tests
- “Cleaning” product fixtures
- Layout/package renames

## Inputs (fill before run)

```text
Repo root:
Branch:
Compare base:
Known live CI entry:
Known live process start:
App roots to avoid:
Allowed harness paths under app/tests (if any):
Read-only reference repos (optional):
```

## Success

- Only devops/harness dead code removed
- Live start/test/CI paths match the inventory
- Separate, reversible commits
- Residual risks written down for anything not provable in-repo
