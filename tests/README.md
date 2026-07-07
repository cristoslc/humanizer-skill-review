# Tests

Automated test harness for the humanizer-skill-review workspace. Exercises each candidate skill against a fixed corpus, scores the outputs with an LLM judge, and regenerates the comparison matrix.

## Layout

- `fixtures/corpus/` — fixed AI-slop corpus (5 passages, committed)
- `harness/` — exercise, scoring, and matrix-building scripts (committed)
- `results/` — per-candidate rewritten outputs and scores (gitignored, regenerated)

## Pipeline

```
fetch-candidates.sh → exercise-skill.sh → score-outputs.py → build-matrix.py
```

1. **Fetch** — `scripts/fetch-candidates.sh` clones candidate repos into `skills/<short-name>/` (gitignored).
2. **Exercise** — `tests/harness/exercise-skill.sh <short-name>` loads the candidate's SKILL.md, feeds each corpus fixture to `opencode run`, and captures the rewritten output in `tests/results/<short-name>/<fixture>.md`.
3. **Score** — `tests/harness/score-outputs.py <short-name>` sends each (input, output, SKILL.md, rubric) tuple to an LLM judge via `opencode run`, parses the JSON verdict, and aggregates into `tests/results/<short-name>/scores.json`.
4. **Matrix** — `tests/harness/build-matrix.py` reads all `scores.json` files and regenerates `docs/plans/comparison-matrix.md`.

## Run it

```bash
# Full pipeline: fetch + exercise + score + matrix
./scripts/run-all.sh

# Skip fetch (candidates already cloned)
./scripts/run-all.sh --skip-fetch

# One candidate only
./scripts/run-all.sh --only conorbronsdon-avoid-ai-writing

# Just regenerate the matrix from existing scores
./scripts/build-matrix.sh
```

## Corpus

Five short AI-slop passages in `fixtures/corpus/`, each saturated with common AI writing patterns:

- `blog-post.md` — blog intro
- `email.md` — professional email
- `report.md` — executive summary
- `marketing.md` — product marketing
- `essay.md` — essay paragraph

Every skill receives the same input — apples-to-apples comparison.

## LLM judge

The judge is prompted with the rubric (`docs/plans/rubric.md`), the candidate's SKILL.md, the original input, and the rewritten output. It returns strict JSON scoring all 10 criteria. Per-fixture verdicts are aggregated by modal rating into `scores.json`. The aggregation code is in `tests/harness/score-outputs.py`.

## Why `opencode run`

Each candidate is a SKILL.md that instructs an LLM — they don't run as standalone code. Using `opencode run` exercises the skill as it's meant to be used: an agent operating under those instructions. This tests agent-tool integration, not just prompt→text behavior.

## Costs

Each full run exercises 5 skills × 5 fixtures = 25 rewrite calls, then 25 judge calls. 50 LLM calls total per full run. Use `--only` to scope down.