# humanizer-skill-review — Agent Instructions

This repo is a **review and comparison workspace** for open-source humanizer/de-slop agent skills. It does not ship a skill, an app, or a deployable artifact. Agents working here are evaluating, scoring, and decision-recording — not building a product.

## Purpose

See `PURPOSE.md`: compare humanizer skills to inform selection or construction of a personal humanizer skill at `~/code/output-humanizer-skill/`.

## What agents do here

- **Fetch** candidate skill repos into `skills/<short-name>/` (gitignored). Use `scripts/fetch-candidates.sh`.
- **Profile** each candidate using `docs/plans/candidate-profile-template.md`. Write the profile to `docs/plans/profiles/<short-name>.md`.
- **Score** each candidate against the rubric in `docs/plans/rubric.md`. Record scores in the comparison matrix at `docs/plans/comparison-matrix.md`.
- **Decide** via ADRs in `docs/adr/`. Each keep/reject/merge decision gets a numbered ADR citing the profile and matrix.
- **Synthesize** the final recommendation into `docs/plans/recommendation.md` once enough candidates are scored.

## Test command

This is a documentation-only repo with no code to test. There is no automated test suite.

## Test command exemption

This project produces no executable code, no library, and no deployable artifact. It is a review workspace containing markdown documents and shell scripts that fetch read-only git repos. Automated tests are not applicable. Verification is by human review of profiles, the comparison matrix, and ADRs.

## Project navigation

Full spoke: `docs/agents-detail/project-navigation.md`.

## Candidate inventory

Five initial candidates (see ADR-0001); list may grow:

- `stephenturner/skill-deslop` → `skills/deslop/`
- `blader/humanizer` → `skills/blader-humanizer/`
- `brandonwise/humanizer` → `skills/brandonwise-humanizer/`
- `conorbronsdon/avoid-ai-writing` → `skills/conorbronsdon-avoid-ai-writing/`
- `lguz/humanize-writing-skill` → `skills/lguz-humanize-writing-skill/`

## Conventions

- **Short names**: `<owner>-<repo>` lowercased, hyphenated (e.g. `blader-humanizer`). Used for `skills/` dir, profile filename, and matrix row id.
- **No redistribution**: do not commit candidate skill source into this repo. `skills/` is gitignored. Reference by SHA in profiles.
- **ADRs are immutable once adopted**: supersede, don't edit.
- **Profiles are mutable**: update as candidates release new versions; note the SHA reviewed.
- **The matrix is a living doc**: reorder columns freely; keep row order stable once scored.

## Staging

No staging target exists — see `scripts/staging/README.md`. This repo has nothing to deploy.