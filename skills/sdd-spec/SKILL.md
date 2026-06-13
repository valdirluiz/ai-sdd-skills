---
name: sdd-spec
description: Write the spec (specification) document for an SDD feature. The spec defines WHAT needs to be built — problem, goals, requirements, and acceptance criteria. Called with the feature folder path and a description of what needs to be built.
---

# SDD Spec Writer

Write a `spec.md` for the feature described in `$ARGUMENTS`.

`$ARGUMENTS` format: `<feature-folder-path> | <feature description and context>`

Example: `doc/features/003-user-authentication | Users need to log in with email and password`

## Workflow

### 1. Parse Arguments

Split `$ARGUMENTS` on ` | `:
- First part: feature folder path (e.g. `doc/features/003-user-authentication`)
- Second part: feature description/context provided by the user

If `$ARGUMENTS` is missing or malformed, ask the user:
- What is the feature folder path?
- What does this feature need to accomplish?

### 2. Research Context

Before writing, gather context:
- Read `CLAUDE.md` if it exists for project conventions
- Scan the existing codebase to understand the current architecture, tech stack, and patterns
- Look at other `spec.md` files in `doc/features/` for style reference
- Identify any related existing features or code

### 3. Write spec.md

Create `<feature-folder-path>/spec.md` with the following structure:

```markdown
# <Feature Name>

## Overview

One paragraph describing what this feature is and why it matters.

## Problem Statement

What problem does this feature solve? Who is affected? What is the current pain point?

## Goals

- Goal 1
- Goal 2
- Goal 3

## Non-Goals

What is explicitly out of scope for this feature:

- Non-goal 1
- Non-goal 2

## Requirements

### Functional Requirements

- **FR-01**: ...
- **FR-02**: ...
- **FR-03**: ...

### Non-Functional Requirements

- **NFR-01**: Performance — ...
- **NFR-02**: Security — ...
- **NFR-03**: Reliability — ...

## User Stories

**As a** [type of user], **I want to** [action], **so that** [benefit].

- US-01: As a ..., I want to ..., so that ...
- US-02: As a ..., I want to ..., so that ...

## Acceptance Criteria

- [ ] AC-01: Given ... When ... Then ...
- [ ] AC-02: Given ... When ... Then ...
- [ ] AC-03: Given ... When ... Then ...

## Open Questions

Questions that need to be answered before or during implementation:

1. Question 1?
2. Question 2?
```

### 4. Review

After writing, verify:
- [ ] All sections are filled with relevant content (not placeholder text)
- [ ] Acceptance criteria are testable and specific
- [ ] Non-goals are clearly stated to prevent scope creep
- [ ] The spec is grounded in the actual codebase context

## Wrap Up

Inform the user:
- Path to the created `spec.md`
- Any open questions that need answers before planning can begin
- Next step: run `/sdd-plan` to generate the implementation plan
