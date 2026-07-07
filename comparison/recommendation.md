# Recommendation

- **Status:** adopted (round 2)
- **Date:** 2026-07-07
- **Scoring round:** 2 (5 fixtures × 5 candidates, LLM judge with full repo context, numeric 1–3 scale)
- **Matrix:** [`comparison/matrix.md`](./matrix.md)

## Summary

Five open-source humanizer skills were exercised against a fixed 5-passage AI-slop corpus and scored by an LLM judge across 10 rubric criteria. The judge saw each candidate's SKILL.md **and** its full repo context (file tree, README, LICENSE, CHANGELOG, CI workflows, test files, package manifest, git history) mirrored into the trove at `docs/troves/humanizer-skills/`.

| Rank | Candidate | Sum /30 | Avg | Verdict |
|---|---|---|---|---|
| 1 | conorbronsdon-avoid-ai-writing | **29** | 2.85 | Adopt as the base |
| 2 | blader-humanizer | 23 | 2.35 | Steal voice calibration + convergence |
| 2 | brandonwise-humanizer | 23 | 2.26 | Steal the detector taxonomy + vocab tiers |
| 4 | lguz-humanize-writing-skill | 20 | 2.02 | Steal the "when NOT to use" opt-out section |
| 5 | stephenturner-skill-deslop | 17 | 1.76 | Steal the lean prose-only philosophy |

blader and brandonwise tie at 23/30; blader edges ahead on average (2.35 vs 2.26). They complement each other — blader leads on voice/convergence/portability, brandonwise leads on detection rigor/maturity/conciseness.

## Which candidate to adopt

**`conorbronsdon/avoid-ai-writing`** is the clear winner at 29/30. With repo context visible, the judge upgraded maturity from 2 to 3 (CHANGELOG, CONTRIBUTING, CI workflows, detector tests, v3.13.0, 97 commits all surfaced from the repo). It now scores 3 on 9 of 10 criteria; the only 2 is conciseness — the inherent cost of its ~660-line comprehensiveness.

Strengths that drove the win:
- **Three modes** (rewrite default, detect flag-only, edit in-place) — no other candidate offers all three.
- **Iterate-to-convergence** with an explicit `--iterate` flag capped at 2, plus a built-in second-pass audit.
- **Ethics framing** citing Stanford Liang et al. (false-positive >60% on non-native English), BFI 2025-116 (>70% misclassification), and arXiv:2506.07001 (adversarial paraphrase ~88% reduction). Framed explicitly as "signals, not proof." No other candidate does this.
- **Five named voice profiles** with concrete targets and a sensible selection order: user-specified → mirror from sample → default.
- **Detection rigor** grounded in cited academic sources and attributed adaptations from other skills.
- **Maturity** — 97 commits, CHANGELOG, CONTRIBUTING, CI workflows (detector-test.yml, plugin-skill-sync.yml), detector test suite, v3.13.0.

Its only weak spot:
- **Conciseness (2, mean 1.5):** ~660–1000 lines. Comprehensive but expensive to load. This is the natural cost of its breadth — and the gap the stephenturner graft addresses.

## Which candidates to merge (if constructing a personal skill)

Adopt **conorbronsdon-avoid-ai-writing as the base** for the personal skill at `~/code/output-humanizer-skill/`, then graft on the best ideas the others contribute:

| From | Take | Why |
|---|---|---|
| **stephenturner/skill-deslop** | The lean, opinionated philosophy; the dedicated `references/` split (`phrases.md`, `structures.md`, `tropes.md`, `examples.md`) | conorbronsdon is comprehensive but bloated. stephenturner proves the same job can be done in 130 lines. Use this as a forcing function to keep the personal skill lean — push detail into `references/` rather than the SKILL.md body. |
| **blader/humanizer** | Voice calibration from a user writing sample; the draft→audit→final loop; the "PERSONALITY AND SOUL" framing | conorbronsdon already has voice profiles, but blader's sample-mirroring is more concrete. The draft→audit→final loop is a lighter-weight version of conorbronsdon's iterate-to-convergence that may suit a personal skill better. |
| **brandonwise/humanizer** | The 28-detector taxonomy and 560+ vocabulary terms across 3 tiers; the statistical analysis approach (burstiness, type-token ratio, sentence uniformity) | conorbronsdon's word lists are good; brandonwise's are more systematic and machine-checkable. Its repo has a full test suite (`src/`, vitest, eslint) and MCP/API servers — the engineering maturity is real. Consider lifting the tier structure for the personal skill's `references/` dir. The statistical analysis is over-engineered for a personal skill — note it, probably skip it. |
| **lguz/humanize-writing-skill** | The explicit "When NOT to Use" section (technical writing, formal/academic, commit messages); the voice-selection order (user-specified → mirror → default) | No other candidate is this honest about when humanizing is the wrong move. The personal skill should carry an equivalent opt-out section. lguz's voice-selection order is also cleaner than conorbronsdon's — adopt it verbatim. |

## What the personal skill at `~/code/output-humanizer-skill/` should look like

1. **Base:** conorbronsdon-avoid-ai-writing v3.13.0, trimmed.
2. **Modes:** keep all three (rewrite / detect / edit). They're the decisive feature.
3. **Convergence:** keep `--iterate` capped at 2, but also offer blader's single draft→audit→final as the default lightweight path.
4. **Voice:** five named profiles from conorbronsdon + blader's sample-mirroring + lguz's selection order (user-specified → mirror → default).
5. **Ethics:** keep conorbronsdon's "signals, not proof" section and citations verbatim. This is non-negotiable — it's the single biggest differentiator and the right thing to do.
6. **Opt-out:** add lguz's "When NOT to Use" section.
7. **Structure:** push word lists and pattern tables into `references/` (stephenturner's model). Target SKILL.md body under ~250 lines; references hold the bulk.
8. **Detection rigor:** keep conorbronsdon's citations. Optionally cross-reference brandonwise's tier structure in `references/`.

## Caveats

- Scores are LLM-judge-generated, not human-verified. The judge saw each candidate's SKILL.md, full repo context (mirrored in the trove), and its own output on the 5 fixtures.
- The corpus is short (5 passages, 3–6 paragraphs each). A larger corpus might shift scores on pattern coverage and convergence.
- Re-run the harness (`./scripts/run-all.sh`) to regenerate scores against new candidate versions. The trove rebuilds automatically.