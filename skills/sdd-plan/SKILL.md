---
name: sdd-plan
description: Write the plan (implementation plan) document for an SDD feature. The plan defines HOW to build it — technical approach, file changes, implementation steps, and testing strategy. Reads the spec.md and produces plan.md. Called with the feature folder path.
---

# SDD Plan Writer

Write a `plan.md` for the feature at `$ARGUMENTS`.

`$ARGUMENTS`: feature folder path (e.g. `doc/features/003-user-authentication`)

If `$ARGUMENTS` is missing, ask the user for the feature folder path.

## Workflow

### 1. Read the Spec

Read `$ARGUMENTS/spec.md`. If it does not exist, stop and tell the user to run `/sdd-spec` first.

Extract from the spec:
- Feature name and goals
- Functional and non-functional requirements
- Acceptance criteria

### 2. Analyze the Codebase

Explore the codebase to produce a grounded, concrete plan:
- Identify the tech stack, frameworks, and architectural patterns in use
- Find files that will need to be created or modified
- Look for existing patterns to reuse (auth middleware, DB models, API route conventions, etc.)
- Identify dependencies (libraries, services, APIs) required
- Check for existing tests to understand the testing conventions

### 3. Write plan.md

Create `$ARGUMENTS/plan.md` with the following structure:

```markdown
# Implementation Plan — <Feature Name>

> Spec: [spec.md](./spec.md)

## Technical Approach

High-level description of the implementation strategy. Explain the key design decisions and why this approach was chosen over alternatives.

## Architecture

Describe how this feature fits into the existing architecture:
- Which layers are affected (API, service, data, UI)?
- New components or modules introduced
- Data flow diagram (if complex)

## Implementation Steps

Ordered list of concrete tasks. Each step should be independently implementable.

### Step 1 — <Step Title>

- [ ] Task description
- [ ] Task description

**Files:**
- `path/to/file.ts` — create: description of what goes in it
- `path/to/other.ts` — modify: what changes

---

### Step 2 — <Step Title>

- [ ] Task description

**Files:**
- `path/to/file.ts` — create/modify: description

---

_(repeat for each step)_

## New Files

| File | Type | Description |
|------|------|-------------|
| `path/to/file` | create | What it contains |

## Modified Files

| File | Change | Reason |
|------|--------|--------|
| `path/to/file` | What changes | Why |

## Dependencies

List any new packages or external services required:

- `package-name@version` — reason

## Testing Strategy

How each acceptance criterion will be verified:

| AC | Test Type | Description |
|----|-----------|-------------|
| AC-01 | unit | Test file: `path/to/test` |
| AC-02 | integration | ... |
| AC-03 | e2e | ... |

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk description | High/Med/Low | High/Med/Low | Mitigation strategy |

## Rollout

Steps to safely deploy this feature:

1. ...
2. ...

## Open Questions

Any unresolved technical questions that block or affect the plan:

1. Question?
```

### 4. Review

After writing, verify:
- [ ] Every acceptance criterion in the spec has a corresponding test entry
- [ ] All file paths are real paths that exist or are logically placed
- [ ] Implementation steps are in a valid dependency order
- [ ] No step is vague (e.g. "implement the feature") — each must be concrete

## Wrap Up

Inform the user:
- Path to the created `plan.md`
- Any blocking open questions
- Next step: start implementation by working through the steps in `plan.md`
