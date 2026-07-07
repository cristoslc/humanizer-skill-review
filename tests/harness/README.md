# Harness

Scripts that exercise candidate skills, score their outputs, and regenerate the comparison matrix.

## Scripts

- `exercise-skill.sh <short-name>` — load a candidate's SKILL.md, feed each corpus fixture to `opencode run`, capture rewritten output
- `extract-output.py` — parse the final assistant text from an `opencode run --format json` event stream
- `score-outputs.py <short-name>` — LLM judge scores all 10 rubric criteria per fixture, aggregates into `scores.json`
- `build-matrix.py` — regenerate `comparison/matrix.md` from all `scores.json` files
- `judge-prompt.md` — template for the LLM judge prompt

## Orchestration

`scripts/run-all.sh` chains: fetch → exercise → score → matrix.