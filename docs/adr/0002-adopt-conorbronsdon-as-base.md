# ADR-0002: Adopt conorbronsdon-avoid-ai-writing as the personal skill base

- Status: adopted
- Date: 2026-07-07
- Supersedes: (none)

## Context

Five candidates were scored by an LLM judge across 10 rubric criteria (see `comparison/matrix.md`). The personal skill at `~/code/output-humanizer-skill/` needs a starting point. This ADR records the selection decision and the graft list from the other candidates.

## Options

1. Adopt the top scorer as-is.
2. Adopt the top scorer as a base and graft on features from the others.
3. Build from scratch.

## Decision

Option 2: adopt `conorbronsdon/avoid-ai-writing` v3.13.0 as the base and graft on the best ideas from the other four candidates.

The graft list (full reasoning in `comparison/recommendation.md`):

| From | Take |
|---|---|
| stephenturner/skill-deslop | Lean philosophy; `references/` split for detail |
| blader/humanizer | Sample-mirroring voice calibration; draft→audit→final loop |
| brandonwise/humanizer | 3-tier vocab structure for `references/` |
| lguz/humanize-writing-skill | "When NOT to Use" opt-out section; voice-selection order |

## Rationale

conorbronsdon scored 28/30 — 5 points clear of the next candidate. It is the only candidate with all three modes (rewrite/detect/edit), iterate-to-convergence, and an explicit ethics stance citing academic false-positive research. The two criteria where it scored 2 (maturity, conciseness) are the exact gaps the grafts address: stephenturner's lean model fixes conciseness, and the repo-level maturity signals exist in conorbronsdon's repo even though they didn't surface in the SKILL.md the judge saw.