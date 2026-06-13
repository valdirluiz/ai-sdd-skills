# ai-sdd-skills

Skills for managing Software Design Documents (SDD) with Claude Code.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `sdd` | `/sdd <feature-name>` | Orchestrates the full SDD flow — creates folder, writes spec and plan |
| `sdd-spec` | `/sdd-spec <folder> \| <description>` | Writes `spec.md` (WHAT to build) for an existing feature folder |
| `sdd-plan` | `/sdd-plan <folder>` | Writes `plan.md` (HOW to build it) from an existing `spec.md` |

## SDD Structure

```
doc/
  features/
    001-feature-name/
      spec.md   ← what to build (requirements, acceptance criteria)
      plan.md   ← how to build it (steps, files, tests)
    002-another-feature/
      spec.md
      plan.md
```

## Installing Skills

Copy the `skills/` folder contents into your project's `.claude/skills/` directory, or register the path in your Claude Code settings.

## Typical Workflow

```
/sdd payment-integration — Users pay via Stripe checkout
```

Claude will:
1. Determine the next count and create `doc/features/00N-payment-integration/`
2. Ask for context if needed
3. Write `spec.md` and ask for your approval
4. Write `plan.md` based on the approved spec
5. Commit the SDD to git
