---
name: sdd
description: Orchestrate the full SDD (Software Design Document) flow for a new feature. Creates the feature folder with incremental count, then generates both spec.md (what to build) and plan.md (how to build it). Use when starting work on any new feature.
---

# SDD Orchestrator

Create a complete SDD for a new feature.

`$ARGUMENTS`: feature name in kebab-case, optionally followed by a description after ` — `

Examples:
- `/sdd user-authentication`
- `/sdd payment-integration — Users should be able to pay via Stripe checkout`

## Workflow

Make a todo list for all tasks below and work through them one by one.

### 1. Parse Feature Name

Extract from `$ARGUMENTS`:
- **feature-name**: kebab-case slug (e.g. `user-authentication`)
- **description**: optional context after ` — ` separator

If `$ARGUMENTS` is empty, ask: "What feature do you want to document? Provide a kebab-case name and optional description."

### 2. Determine Next Count

Scan `doc/features/` for existing feature folders to determine the next incremental count:

```bash
ls doc/features/ 2>/dev/null | sort
```

- If the folder doesn't exist or is empty, start at `001`
- Otherwise, find the highest existing prefix number and increment by 1
- Format: zero-padded to 3 digits (`001`, `002`, ..., `010`, `011`, etc.)

### 3. Create Feature Folder

```bash
mkdir -p doc/features/<count>-<feature-name>
```

Example: `doc/features/003-user-authentication`

Confirm creation to the user: "Creating SDD at `doc/features/<count>-<feature-name>/`"

### 4. Gather Feature Context

If the user provided a description in `$ARGUMENTS`, use it. Otherwise, ask:

> "Describe what `<feature-name>` should do. Include:
> - The problem it solves
> - Who will use it
> - Key behaviors or requirements you have in mind"

Wait for the user's response before proceeding.

### 5. Write the Spec

Invoke the spec-writing workflow for this feature:

- Folder: `doc/features/<count>-<feature-name>`
- Context: user-provided description + any codebase context you gathered

Follow the full workflow defined in the `sdd-spec` skill:
- Research the codebase for context
- Write `doc/features/<count>-<feature-name>/spec.md`
- Cover: overview, problem, goals, non-goals, requirements, user stories, acceptance criteria, open questions

Show the user the completed `spec.md` content and ask:

> "Here is the draft spec. Would you like to adjust anything before I write the implementation plan?"

Incorporate any feedback before moving on.

### 6. Write the Plan

Once the spec is approved, invoke the plan-writing workflow:

- Feature folder: `doc/features/<count>-<feature-name>`

Follow the full workflow defined in the `sdd-plan` skill:
- Re-read the approved spec
- Analyze the codebase for patterns and file locations
- Write `doc/features/<count>-<feature-name>/plan.md`
- Cover: technical approach, architecture, implementation steps, files, dependencies, testing strategy, risks, rollout

### 7. Commit the SDD

Once both files are written and reviewed:

```bash
git add doc/features/<count>-<feature-name>/
git commit -m "docs: add SDD for <feature-name>

- spec.md: defines requirements and acceptance criteria
- plan.md: defines implementation approach and steps"
```

## Wrap Up

Provide a summary with:

- **Feature folder**: `doc/features/<count>-<feature-name>/`
- **Spec**: `spec.md` — summary of key requirements
- **Plan**: `plan.md` — summary of implementation approach and number of steps
- **Next step**: "Start implementing by working through the steps in `plan.md`"
