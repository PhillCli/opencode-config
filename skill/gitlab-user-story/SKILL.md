---
name: gitlab-user-story
description: Create GitLab-ready User Story issues with clear context, scoped checklist, and testable acceptance criteria. Use when user asks to create, refine, or rewrite a backlog story/issue. Before drafting, ask missing details with the question tool, including the target language.
---

# GitLab User Story

Create concise, structured User Story content ready to paste into a GitLab issue.

## Scope

- Generic style only.
- No company-specific process, labels, repos, team names, or internal jargon.
- Keep output practical and directly actionable.

## Mandatory intake protocol (question tool)

Before writing, collect missing info with `question` tool.

### Rule 1: Ask for language first

If language is not explicit, ask it first via `question` tool.

Recommended options pattern:
- `Polish (Recommended)`
- `English`

Keep custom answer enabled so user can type another language.

### Rule 2: Ask only for missing details

If prompt is incomplete, ask for:
- scope boundaries (in scope / out of scope),
- success criteria (what must be true to call it done),
- constraints (time, compliance, tooling, environment),
- dependencies/owners,
- target level of detail (compact vs narrative).

Use concise options, recommended option first with `(Recommended)`.

## Writing workflow

1. Identify the problem and desired outcome.
2. Draft description focused on intent and business/operational impact.
3. Add implementation scope as checklist items.
4. Add measurable acceptance criteria.
5. Validate clarity, testability, and language consistency.

## Publish Safety Protocol (MANDATORY)

For any request that could mutate a GitLab issue/work item:

1. **Preview first**: always return proposed markdown draft in chat.
2. **No implicit publish**: do not treat "add/update/write/fill" as permission to mutate.
3. **Explicit confirmation required** via `question` tool before running mutating commands.
4. Allowed confirmation options:
   - `Publish as-is (Recommended)`
   - `Revise draft`
   - `Cancel`
5. Only after `Publish as-is` may the agent run `glab issue update/create/...`.
6. After publish, show executed command summary and resulting URL.

If confirmation is missing, stop at preview.

## Output format

Use headings in selected language.

### Polish template

```md
## Historia
<krótki kontekst: problem, cel, oczekiwany rezultat>

## Zakres
- [ ] <element 1>
- [ ] <element 2>

## Kryteria akceptacji
- [ ] <kryterium mierzalne 1>
- [ ] <kryterium mierzalne 2>
```

### English template

```md
## Story
<short context: problem, goal, expected outcome>

## Scope
- [ ] <item 1>
- [ ] <item 2>

## Acceptance Criteria
- [ ] <measurable criterion 1>
- [ ] <measurable criterion 2>
```

## Style guide distilled from strong GitLab US examples

- Description first, criteria second.
- Keep description outcome-oriented, not tool-command-oriented.
- Use checklist format for Scope and Acceptance Criteria.
- Acceptance Criteria must be observable and testable.
- Prefer concrete verbs: "defined", "documented", "verified", "published", "measured".
- Keep AC concise; avoid long narrative in AC.
- If references are given, include them as links in the description.
- Avoid hidden assumptions; state dependencies explicitly.

## Quality gate before returning

- Language matches user choice.
- No company-specific details added.
- Scope is clear and bounded.
- AC are testable and unambiguous.
- Output is paste-ready for GitLab.

## Optional clarification set (single question-tool batch)

Use this when multiple gaps exist:

1. Language
2. Story type (feature, bugfix, infrastructure, process)
3. Target environment (dev/stage/prod/all)
4. Done definition strictness (minimal, standard, strict)
5. Output verbosity (compact, balanced, detailed)

Ask only what is missing.
