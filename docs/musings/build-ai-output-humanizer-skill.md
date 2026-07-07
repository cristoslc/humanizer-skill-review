# Musing: Build `skills/ai-output-humanizer/` — Superset Humanizer Skill

**Date:** 2026-07-07
**Status:** draft
**Based on:** `comparison/recommendation.md` (scoring round 1)

## What

Build a superset humanizer skill at `skills/ai-output-humanizer/` that synthesizes the best ideas from all five reviewed candidates, then evaluate it with a non-deterministic test harness (LLM judge, pass^k metrics, session-enriched JSONL logs).

## Why here, not at `~/code/output-humanizer-skill/`

The recommendation targets the personal skill at `~/code/output-humanizer-skill/`. Building it here first lets us:
1. Run it through the same harness as the candidates (apples-to-apples comparison)
2. Iterate on design before committing to the personal repo
3. Keep the review workspace self-contained — the skill becomes a sixth row in the comparison matrix

Once validated, the skill can be copied to the personal location.

## Design

### Base: conorbronsdon-avoid-ai-writing v3.13.0

Adopt as the structural skeleton. Keep:
- Three modes (rewrite / detect / edit) — the decisive feature
- The pattern catalog (all ~46 detection categories)
- The 3-tier vocabulary system (Tier 1 always-flag, Tier 2 cluster-flag, Tier 3 density-flag)
- The context profiles (linkedin, blog, technical-blog, investor-email, docs, casual) with tolerance matrix
- The severity tiers (P0/P1/P2)
- The ethics section with citations (Liang et al., BFI 2025-116, arXiv:2506.07001)
- The output format (issues → rewrite → diff → second-pass audit)

### Grafts from other candidates

| From | What to take | How |
|------|-------------|-----|
| stephenturner/skill-deslop | Lean philosophy; `references/` split | Push word tables, pattern catalogs, and examples into `references/`. Target SKILL.md body ~250 lines. |
| blader/humanizer | Voice calibration from sample; draft→audit→final loop; PERSONALITY AND SOUL | Add sample-mirroring as the primary voice-calibration path. Offer draft→audit→final as the default lightweight convergence (conorbronsdon's `--iterate` stays as the heavy option). |
| brandonwise/humanizer | 28-detector taxonomy; 560+ vocab terms across 3 tiers | Cross-reference brandonwise's tier structure in `references/vocabulary-tiers.md`. The statistical analysis (burstiness, TTR) is over-engineered for a personal skill — note it, skip it. |
| lguz/humanize-writing-skill | "When NOT to Use" section; voice-selection order (user-specified → mirror → default) | Add opt-out section verbatim. Adopt lguz's cleaner voice-selection order. |

### Structural changes from conorbronsdon

1. **Split into SKILL.md + references/**: SKILL.md contains only the core instructions, modes, process, and ethics. Word tables, pattern catalogs, and examples go into `references/`.
2. **Add opt-out section**: "When NOT to Use" — technical writing, formal/academic, commit messages, quoted material.
3. **Voice selection order**: User-specified → mirror from sample → named profile → default (lguz's model, cleaner than conorbronsdon's).
4. **Default convergence**: Single draft→audit→final pass (blader's model). `--iterate` remains available for heavy cases.

## Non-deterministic test harness

The existing harness (`tests/harness/`) already uses an LLM judge. The superset-skill needs its own evaluation suite that follows the non-deterministic testing principles from `~/.agents/agents-md-detail/test-driven-design.md`:

### Metrics

- **pass^1**: per-trial success rate (proportion of individual trials that pass)
- **pass^k**: probability that all k independent trials succeed — primary metric
- **pass@k**: reported for reference only
- **k = 5** recommended standard, **k = 3** minimum floor

### Session-enriched JSONL format

Each test run produces a JSONL log with:
- `session-start` record (UUID, commit, model, judge_model, k, threshold)
- `case-run` records (k per case, with raw agent + judge responses)
- `case-summary` records (one per case, with pass@k)
- `session-end` record (total cases, total pass, suite_pass, duration)

### Structured output contract

LLM judge assertions MUST return JSON with:
- `result`: "pass" | "fail" | "skip"
- `reason`: human-readable explanation
- `confidence`: 0.0–1.0 (optional)

### Test cases

The evaluation should cover:

1. **Happy path**: Standard rewrite of AI-slop text → output reads as human-written
2. **Detect mode**: Flag-only mode identifies patterns without rewriting
3. **Edit mode**: In-place file editing with minimal changes
4. **Voice calibration**: Output matches a provided writing sample
5. **Opt-out**: Technical/academic text is left mostly untouched
6. **Convergence**: `--iterate` reduces pattern count across passes
7. **Ethics framing**: Skill acknowledges probabilistic nature and bias
8. **Adversarial**: Non-native English text is not over-flagged

### Test runner

`tests/harness/evaluate-superset.sh` — runs k trials per test case, collects JSONL logs, computes pass^k, and produces a summary report.

## Open questions

1. **SKILL.md target line count**: conorbronsdon is ~662 lines. Can we get to ~250 with references/ split? The core instructions (modes, process, ethics) are probably ~200 lines; the rest is word tables and pattern detail that can move to references/.
2. **How to handle the tolerance matrix**: It's ~30 lines in conorbronsdon. Keep it in SKILL.md or push to references/? I think keep it — it's core to how the skill behaves differently per context.
3. **Should the superset-skill be a sixth candidate in the comparison matrix?** Yes — run it through `tests/harness/exercise-skill.sh` and `score-outputs.py` to get an apples-to-apples score. This validates that the synthesis actually improves on the base.
4. **What model to use for the LLM judge?** The existing harness uses whatever `opencode run` defaults to. For pass^k rigor, we should pin a specific judge model.
5. **Threshold for pass^k**: What pass^k threshold counts as "passing"? 0.8 at k=5? 0.9? Need to calibrate.

## Next steps

1. Create `skills/ai-output-humanizer/SKILL.md` with the core instructions (~250 lines)
2. Create `skills/ai-output-humanizer/references/` with word tables, pattern catalogs, examples
3. Create `tests/harness/evaluate-superset.sh` for non-deterministic evaluation
4. Create test cases in `tests/superset/` (YAML or markdown)
5. Run evaluation, compute pass^k, iterate
6. Once validated, copy to `~/code/output-humanizer-skill/`
