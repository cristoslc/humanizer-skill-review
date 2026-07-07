# Synthesis: humanizer-skills trove

Five open-source humanizer/de-slop agent skills, cloned and mirrored for evaluation against a fixed AI-slop corpus. All MIT-licensed. All target the same domain — removing AI writing patterns from prose — but differ in structure, modes, voice handling, detection rigor, ethics framing, and maturity.

## Key findings across sources

- **Pattern coverage is uniformly strong** — all five candidates score well on covering filler phrases, formulaic structures, trope vocabulary, and false vulnerability. This is a saturated space.
- **Modes vary widely** — conorbronsdon offers all three (rewrite/detect/edit); most offer only rewrite. blader and stephenturner are single-mode.
- **Voice calibration splits the field** — conorbronsdon (5 named profiles + sample-mirroring), blader (sample-mirroring), and lguz (3 voices + selection order) have it; stephenturner and brandonwise do not.
- **Ethics framing is rare** — only conorbronsdon cites academic false-positive research (Stanford Liang et al., BFI 2025-116, arXiv:2506.07001) and frames output as 'signals, not proof.' The others are silent.
- **Maturity signals cluster** — conorbronsdon (CHANGELOG, CONTRIBUTING, CI, tests, v3.13.0) and brandonwise (package.json, eslint, vitest, tests, CI) are the most engineered. stephenturner and lguz are lean single-file skills.
- **Conciseness inversely correlates with breadth** — stephenturner (130 lines) and lguz (234) are lean; conorbronsdon (~660) and blader (~620) are comprehensive but expensive to load.

## Points of agreement

- All five treat filler phrases, trope vocabulary, and formulaic structures as the core problem.
- All five default to a rewrite mode that returns humanized prose inline.
- All five are MIT-licensed and agent-portable (SKILL.md format).

## Points of disagreement

- **Detection rigor:** conorbronsdon and brandonwise cite external sources; stephenturner and lguz are opinionated lists with no backing.
- **Convergence:** conorbronsdon iterates to convergence (capped at 2); blader has a draft→audit→final loop; the rest do a single pass.
- **Opt-out:** only lguz has an explicit 'When NOT to Use' section.

## Gaps

- None of the five provide quantitative false-positive rates for their own detection rules; the ethics framing is qualitative.
- None integrate with stylometric tooling (burstiness, type-token ratio) — brandonwise describes the approach but it lives in the app layer, not the skill.
- The corpus used here is English-only; non-native-English bias is cited by conorbronsdon but not tested by any candidate.

## Reference

This trove feeds `tests/harness/repo-context.py` for repo-level scoring. Per-source verdicts live in `tests/results/<short-name>/scores.json`.
