# humanizer-skill-review — Agent Instructions

This repo is a **review and comparison workspace** for open-source humanizer/de-slop agent skills. It does not ship a skill, an app, or a deployable artifact. Agents working here are evaluating, scoring, and decision-recording — not building a product.

## Purpose

See `PURPOSE.md`: compare humanizer skills to inform selection or construction of a personal humanizer skill at `~/code/output-humanizer-skill/`.

## What agents do here

- **Fetch** candidate skill repos into `skills/<short-name>/` (gitignored raw snapshots). Use `scripts/fetch-candidates.sh`.
- **Build trove** from the raw clones into `docs/troves/humanizer-skills/sources/<short-name>/` using `tests/harness/build-trove.py`. The trove is the committed, reviewed source for evaluation.
- **Profile** each candidate using `comparison/profile-template.md`. Write the profile to `comparison/profiles/<short-name>.md`.
- **Score** each candidate against the rubric in `comparison/rubric.md`. Scores are auto-generated into `comparison/matrix.md` by `tests/harness/build-matrix.py`.
- **Decide** via ADRs in `docs/adr/`. Each keep/reject/merge decision gets a numbered ADR citing the profile and matrix.
- **Synthesize** the final recommendation into `comparison/recommendation.md` once enough candidates are scored.

## Test command

```bash
./scripts/run-all.sh
```

This runs the full automated pipeline: fetch candidates → exercise each skill against the fixed corpus → score outputs with an LLM judge → regenerate the comparison matrix. See `tests/README.md` for details.

Flags:
- `--skip-fetch` — skip the fetch step (candidates already cloned)
- `--only <short-name>` — run one candidate only

## Test command exemption

This project produces no executable code, no library, and no deployable artifact. The "test suite" is the review harness in `tests/` which exercises candidate skills (not this repo's code) and scores them with an LLM judge. There is no unit-test framework because there is no code under test here. Verification of the review conclusions is by human review of profiles, the comparison matrix, and ADRs; verification of the harness is by running it end-to-end.

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
- **No redistribution**: do not commit candidate skill source into this repo. `skills/` is gitignored (raw snapshots only). The committed, reviewed source is the trove at `docs/troves/humanizer-skills/`. Reference by SHA in profiles.
- **ADRs are immutable once adopted**: supersede, don't edit.
- **Profiles are mutable**: update as candidates release new versions; note the SHA reviewed.
- **The matrix is a living doc**: reorder columns freely; keep row order stable once scored.
- **Comparison artifacts are primary outputs**: they live in `comparison/` at the repo root, not under `docs/plans/`.

## Staging

No staging target exists — see `scripts/staging/README.md`. This repo has nothing to deploy.