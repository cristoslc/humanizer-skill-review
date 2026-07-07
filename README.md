# humanizer-skill-review

Comparison of open-source "humanizer" / "de-slop" agent skills that remove AI writing patterns from prose. This repo evaluates candidates and informs the construction of a personal humanizer skill at `~/code/output-humanizer-skill/`.

## What this repo is

- A **review workspace**: each candidate skill is fetched, summarized, and scored against a common rubric.
- A **decision record**: ADRs capture why a skill was kept, rejected, or merged into the personal skill.
- A **comparison matrix**: a living table tracking features, modes, voice calibration, detection approach, ethics stance, and maturity across all candidates.

## What this repo is not

- Not a skill itself — it produces no `SKILL.md`.
- Not a fork or redistribution of any candidate.
- Not a deployment target — no staging or production environment.

## Candidates under review

| Repo | License | Lines | Approach |
|---|---|---|---|
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) | MIT | ~130 | Prose-only, lean, opinionated trope list |
| [blader/humanizer](https://github.com/blader/humanizer) | MIT | ~622 | WikiProject AI Cleanup basis, voice calibration, draft→audit→final |
| [brandonwise/humanizer](https://github.com/brandonwise/humanizer) | MIT | ~155 (skill) | Full app: 28 detectors, 560+ vocab terms, statistical analysis |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | MIT | ~662 | Three modes (rewrite/detect/edit), ethics-framed, most mature |
| [lguz/humanize-writing-skill](https://github.com/lguz/humanize-writing-skill) | MIT | ~234 | Voice selection (specified→mirror→default), explicit opt-out cases |

The list may grow over time. See `docs/domain-architecture/CONTEXT-MAP.md` for the candidate inventory and `docs/adr/` for decisions.

## Repo layout

- `PURPOSE.md` — one-paragraph intent
- `AGENTS.md` — agent guidance for this project
- `docs/` — technical + domain architecture, cross-cutting hubs
- `skills/` — local clones of candidate skills (gitignored, fetched on demand)
- `scripts/staging/` — explains why no staging target exists

## Quickstart

```bash
# Fetch all candidate skills locally
./scripts/fetch-candidates.sh

# Regenerate the comparison matrix
./scripts/build-matrix.sh
```

## License

This review repo itself is MIT. Each candidate skill retains its own license — see `skills/<name>/LICENSE` after fetch.