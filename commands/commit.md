---
description: Create atomic git commits with conventional messages
model: opencode-go/glm-5.3-flash
---

Commit $ARGUMENTS

Create git commits for my changes. Running `/commit` is explicit authorization: do not ask whether to proceed, stage and commit directly.

## Process

1. **Analyze and plan** - Review conversation history, run `git status -s` and `git diff`, determine if changes should be one or multiple logical commits, group related files, draft conventional commit messages (`type: description`) in imperative mood. Subject line only.
   - Attribute each dirty file to this session or another origin: commit session-made files; ask before including unattributed ones; when the session made none, commit the unattributed changes as-is.
2. **Execute directly** - Use `git add` with specific files (never `-A` or `.`), create commits with the planned messages, list each commit's files and message, show result with `git log --oneline -n [N]`

## Commit Message Format

Use conventional commit format: `type: description` or `type(scope): description`.

Subject line only. Do not add a body that restates the diff, the file list, or the merge request. Body only when git cannot show it: BREAKING CHANGE, required operator action, revert reason.

**Types:**
- `feat:` - New feature (user-facing)
- `fix:` - Bug fix (user-facing)
- `docs:` - Documentation only
- `chore:` - Maintenance, tooling, dependencies
- `refactor:` - Code restructuring without behavior change
- `test:` - Adding or updating tests
- `perf:` - Performance improvement
- `ci:` - CI/CD changes

**Note:** During release generation, `chore:`, `docs:`, and `ci:` commits are filtered from changelog. Only user-facing changes (`fix:`, `feat:`, etc.) are included.

