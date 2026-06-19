---
name: sdd-create-spec
description: Write the spec.md for an SDD feature folder. The spec defines WHAT needs to be built — problem, goals, requirements, and acceptance criteria. Never describes HOW to build it (no code, no file paths, no framework choices). Validates the output automatically with a Python script before finishing.
---

# SDD Spec Creator

Write and validate a `spec.md` for the feature described in `$ARGUMENTS`.

`$ARGUMENTS` format: `<feature-folder-path> | <feature description and context>`

Example: `doc/features/003-payment-integration | Users need to pay for subscriptions via Stripe`

## Core Principle

A spec answers **WHAT** the feature must do. It never answers **HOW**.

| Belongs in spec (WHAT) | Never in spec (HOW) |
|------------------------|---------------------|
| "Users must be able to reset their password" | "Call POST /api/auth/reset with email field" |
| "Passwords must be at least 8 characters" | "Validate with bcrypt before saving to users table" |
| "Email must be delivered within 5 minutes" | "Use SendGrid with retry queue" |

## Workflow

### 1. Parse Arguments

Split `$ARGUMENTS` on ` | `:
- **folder**: feature folder path (e.g. `doc/features/003-payment-integration`)
- **context**: user-provided description of the feature

If arguments are missing or malformed, ask:
- What is the feature folder path?
- What does this feature need to accomplish?

### 2. Gather Context

Read the following before writing:
- `CLAUDE.md` — project conventions and domain language
- `doc/features/` — other spec files for style and terminology reference
- Any existing code related to this feature area

Do **not** read code to determine implementation details for the spec — only read to understand the problem domain and existing product context.

### 3. Write spec.md

Create `<folder>/spec.md` following this exact structure:

```
# <Feature Name>

## Overview

One paragraph describing what this feature is and why it matters to users.

## Problem Statement

What problem does this feature solve? Who is affected? What is the current friction or gap?

## Goals

- Goal expressed as an outcome, not an action
- Goal 2
- Goal 3

## Non-Goals

What is explicitly excluded from this feature (prevents scope creep):

- Non-goal 1
- Non-goal 2

## Requirements

### Functional Requirements

- **FR-01**: <Capability the system must have, described from the user's perspective>
- **FR-02**: <Another capability>
- **FR-03**: <Another capability>

### Non-Functional Requirements

- **NFR-01**: Performance — <measurable target>
- **NFR-02**: Security — <constraint>
- **NFR-03**: Reliability — <constraint>

## User Stories

- **US-01**: As a <role>, I want to <action>, so that <benefit>.
- **US-02**: As a <role>, I want to <action>, so that <benefit>.

## Acceptance Criteria

- [ ] **AC-01**: Given <precondition> When <action> Then <expected outcome>
- [ ] **AC-02**: Given <precondition> When <action> Then <expected outcome>
- [ ] **AC-03**: Given <precondition> When <action> Then <expected outcome>

## Open Questions

Questions that must be resolved before or during implementation:

1. <Question>?
```

**Rules for writing the spec:**
- Every requirement describes observable behavior, not internal mechanics
- Acceptance criteria must be independently verifiable without reading code
- Goals describe outcomes users experience, not things engineers build
- Non-goals are specific enough to prevent scope creep arguments later
- No code blocks, file paths, SQL, or HTTP routes anywhere in the document
- No placeholder text — every field must be filled with real content

### 4. Validate the Spec

After writing, run the validator:

```bash
python skills/sdd-create-spec/validate_spec.py <folder>/spec.md
```

The validator checks:
- All required sections are present
- No code blocks or implementation details
- Requirements follow FR-XX / NFR-XX numbering
- User stories follow "As a ... I want to ... so that ..." format
- Acceptance criteria are testable (Given/When/Then or checkbox format)
- No placeholder text remains

**If validation fails:**
- Read each issue in the JSON output
- Fix all `error` severity issues before proceeding
- Fix `warning` severity issues where possible
- Re-run the validator until the spec is valid

**If validation passes (exit code 0):**
- Present the spec to the user for review
- Ask: "Does this spec capture what needs to be built? Would you like to adjust anything?"
- Incorporate feedback and re-validate if changes are made

### 5. Confirm and Wrap Up

Once the spec is validated and approved, inform the user:

- Path to the created `spec.md`
- Validation score from the script output
- Any open questions that need answers before planning
- Next step: run `/sdd-plan <folder>` to generate the implementation plan
