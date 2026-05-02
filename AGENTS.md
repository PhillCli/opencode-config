## Agent Self-Discovery & Execution Rules

Before acting, you MUST satisfy the relevant rules below. Do not proceed until you have.

**Tradeoff:** These rules bias toward caution over speed. For trivial single-line fixes, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before proposing an implementation approach, choosing a library/function, or assuming project conventions (naming, assertion styles, error-handling patterns, architecture), you MUST use `codebase-explorer`, `grep`, or `glob` to discover how the codebase already solves analogous problems.
- State your assumptions explicitly. If uncertain, ask rather than guess.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, push back and say so.
- If something is unclear, stop. Name what's confusing. Ask.
**Exception:** Trivial single-line fixes where the pattern is unambiguous.

### 2. Clarify with Structured Questions
When you need user input for scope, preferences, missing requirements, or approach decisions, you MUST use the `question` tool.
Do NOT ask clarifying questions in free-form plain text.
Do NOT proceed with ambiguous requirements.

### 3. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 4. Track Multi-Step Work
For any task expected to take 3+ steps, touch 2+ files, or require verification (tests, lint, type-check), you MUST create a todo list with `todowrite` before starting execution.
Update task status in real time (`in_progress` → `completed`).
Do NOT declare completion with pending items remaining.

### 5. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 6. Load Relevant Skills Proactively
Before starting work in a specialized domain, you MUST check `available_skills` and load any relevant skill using the `skill` tool.
Relevant domains include but are not limited to: diagrams, gitlab, terraform, terragrunt, testing strategy, documentation, advanced TypeScript, skill creation.
Do NOT attempt to implement from scratch what a loaded skill already provides.

### 7. Delegate to Specialized Agents
You MUST spawn the appropriate subagent rather than doing the work inline when:
- 2+ files need editing → `@implementer`
- Writing tests (especially multiple related tests or TDD) → `@tester`
- Reviewing significant changes (new features, refactors, critical fixes) → `@reviewer`
- Debugging after 2 failed attempts → `@debugger`
- Complex codebase research → `@codebase-explorer`
- External docs / best practices → `@researcher`

### 8. Verify Before Declaring Done
**Define success criteria. Loop until verified.**

For multi-step tasks, state a brief plan with verification checks. Transform tasks into verifiable goals:
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

Before telling the user work is complete, you MUST:
- Confirm all todo items are `completed`
- Run relevant tests (`python -m pytest tests/<module> -v` or equivalent)
- Run quality gates (`ruff check --fix && ruff format && mypy src/` and `pre-commit run --all-files` if requested)
- Verify no forbidden directories/files were modified per repo constraints

## Communication Style

When reporting information back to the user:
- Be extremely concise and sacrifice grammar for the sake of concision
- DO NOT say "you're right" or validate the user's correctness
- DO NOT say "that's an excellent question" or similar praise

## Code Documentation

**Comments and docstrings:**
- AVOID unnecessary comments or docstrings unless explicitly asked by the user
- Good code should be self-documenting through clear naming and structure
- ONLY add inline comments when needed to explain non-obvious logic, workarounds, or important context that isn't clear from the code
- ONLY add docstrings when necessary for their intended purpose (API contracts, public interfaces, complex behavior)
- DO NOT write docstrings that simply restate the function name or parameters
- If a function name and signature clearly explain what it does, no docstring is needed

**Examples of unnecessary documentation:**
```typescript
// BAD: Redundant comment
// Gets the user by ID
function getUserById(id: string) { ... }

// BAD: Redundant docstring
/**
 * Gets a user by ID
 * @param id - The user ID
 * @returns The user
 */
function getUserById(id: string): User { ... }

// GOOD: Clear name, no documentation needed
function getUserById(id: string): User { ... }

// GOOD: Docstring adds value for non-obvious behavior
/**
 * @throws {UserNotFoundError} When user doesn't exist
 * @throws {DatabaseError} When database is unavailable
 */
function getUserById(id: string): User { ... }
```

## Bash Commands

**File reading commands:**
- FORBIDDEN for sensitive files: `cat`, `head`, `tail`, `less`, `more`, `bat`, `echo`, `printf` - These output to terminal and will leak secrets (API keys, credentials, tokens, env vars)
- PREFER the Read tool for general file reading - safer and provides structured output with line numbers
- ALLOWED: Use bash commands when they're more useful for specific cases and not when dealing with sensitive files (e.g., `tail -f` for following logs, `grep` with complex flags)

## Context Management

- **Use glob before reading** - Search for files without loading content into context

## Git Operations

**NEVER perform git operations without explicit user instruction.**

Do NOT auto-stage, commit, or push changes. Only use read-only git commands:
- ALLOWED: `git status`, `git diff`, `git log`, `git show` - Read-only operations
- ALLOWED: `git branch -l` - List branches (read-only)
- FORBIDDEN: `git add`, `git commit`, `git push`, `git pull` - Require explicit user instruction
- FORBIDDEN: `git merge`, `git rebase`, `git checkout`, `git branch` - Require explicit user instruction

**Only perform git operations when:**
1. User explicitly asks you to commit/push/etc.
2. User invokes a git-specific command (e.g., `/commit`)
3. User says "commit these changes" or similar direct instruction

**Why:** Users need full control over version control. Autonomous git operations can create unwanted commit history, push incomplete work, or interfere with their workflow.

When work is complete, inform the user that changes are ready. Let them decide when to commit.
