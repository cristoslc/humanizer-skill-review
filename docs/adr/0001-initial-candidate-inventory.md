# ADR-0001: Initial candidate inventory

- Status: adopted
- Date: 2026-07-07

## Context

This workspace compares open-source humanizer/de-slop agent skills to inform the construction of a personal humanizer skill at `~/code/output-humanizer-skill/`. We need an initial set of candidates to begin evaluation.

## Options

Five public GitHub repos were identified as candidates:

1. `stephenturner/skill-deslop` — lean, prose-only, opinionated trope list.
2. `blader/humanizer` — WikiProject AI Cleanup basis, voice calibration, draft→audit→final loop.
3. `brandonwise/humanizer` — full app with 28 detectors, 560+ vocab terms, statistical analysis.
4. `conorbronsdon/avoid-ai-writing` — three modes (rewrite/detect/edit), ethics-framed, most mature.
5. `lguz/humanize-writing-skill` — voice selection (specified→mirror→default), explicit opt-out cases.

All five target the same domain (remove AI writing patterns) but differ in approach, size, maturity, and ethics framing.

## Decision

Adopt all five as the initial candidate inventory. Fetch each into `skills/<short-name>/` using the short-name convention (`<owner>-<repo>` lowercased, hyphenated). Profile, score, and decide on each.

The list may grow over time; additional candidates are added via new ADRs amending the inventory.

## Rationale

The five span the design space: prose-only vs code-backed, single-mode vs multi-mode, no-voice vs voice-calibration, no-ethics vs strong-ethics. This breadth gives the comparison matrix enough variance to surface what matters for the personal skill.