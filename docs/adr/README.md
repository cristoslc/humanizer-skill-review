# Architecture Decision Records

Numbered decision records for the humanizer-skill-review workspace. Each ADR captures a decision and its rationale.

## Numbering

ADRs are numbered zero-padded: `0001-decision-title.md`, `0002-...`. Numbers are never reused.

## Lifecycle

`proposed → adopted → superseded`

- **Proposed** — drafted but not yet accepted.
- **Adopted** — accepted and in force. Immutable once adopted.
- **Superseded** — replaced by a later ADR. The old ADR is NOT edited; a new ADR references it via `Supersedes ADR-NNNN`.

## Format

```markdown
# ADR-NNNN: Title

- Status: proposed | adopted | superseded
- Date: YYYY-MM-DD
- Supersedes: ADR-NNNN (optional)

## Context

Why this decision is being made.

## Options

What was considered.

## Decision

What was chosen.

## Rationale

Why it was chosen.
```

## Index

- [ADR-0001: Initial candidate inventory](0001-initial-candidate-inventory.md) — adopted