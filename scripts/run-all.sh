#!/usr/bin/env bash
# run-all.sh — full automated test + scoring pipeline.
#
# Steps:
#   1. Fetch candidate repos (scripts/fetch-candidates.sh)
#   2. Exercise each skill against the fixed corpus (tests/harness/exercise-skill.sh)
#   3. Score each candidate's outputs with an LLM judge (tests/harness/score-outputs.py)
#   4. Regenerate the comparison matrix (tests/harness/build-matrix.py)
#
# Usage: run-all.sh [--skip-fetch] [--only <short-name>]
set -euo pipefail

cd "$(dirname "$0")/.."

SKIP_FETCH=0
ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --skip-fetch) SKIP_FETCH=1; shift ;;
    --only) ONLY="${2:?--only requires a value}"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

CANDIDATES=(
  stephenturner-skill-deslop
  blader-humanizer
  brandonwise-humanizer
  conorbronsdon-avoid-ai-writing
  lguz-humanize-writing-skill
)

if [ -n "${ONLY}" ]; then
  CANDIDATES=("${ONLY}")
fi

echo "=== 1. Fetch candidates ==="
if [ "${SKIP_FETCH}" -eq 1 ]; then
  echo "skipped (--skip-fetch)"
else
  ./scripts/fetch-candidates.sh
fi

echo
echo "=== 2. Exercise skills ==="
for c in "${CANDIDATES[@]}"; do
  ./tests/harness/exercise-skill.sh "${c}" || echo "warn: ${c} exercise had failures"
done

echo
echo "=== 3. Score outputs ==="
for c in "${CANDIDATES[@]}"; do
  python3 ./tests/harness/score-outputs.py "${c}" || echo "warn: ${c} scoring failed"
done

echo
echo "=== 4. Regenerate matrix ==="
python3 ./tests/harness/build-matrix.py

echo
echo "=== Done. See docs/plans/comparison-matrix.md ==="