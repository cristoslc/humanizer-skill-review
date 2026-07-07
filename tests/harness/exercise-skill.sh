#!/usr/bin/env bash
# Exercise one candidate humanizer skill against the fixed corpus.
# Loads the candidate's SKILL.md as the agent's instructions, feeds each
# corpus fixture as the user message, and captures the rewritten output.
#
# Usage: exercise-skill.sh <short-name>
# Output: tests/results/<short-name>/<fixture-stem>.md
set -euo pipefail

cd "$(cd "$(dirname "$0")/../.." && pwd)"

SHORT_NAME="${1:?usage: exercise-skill.sh <short-name>}"
TROVE_SRC="docs/troves/humanizer-skills/sources/${SHORT_NAME}"
SKILL_DIR="skills/${SHORT_NAME}"  # legacy fallback
RESULTS_DIR="tests/results/${SHORT_NAME}"
CORPUS_DIR="tests/fixtures/corpus"
HARNESS_DIR="tests/harness"

if [ ! -d "${TROVE_SRC}" ]; then
  echo "error: ${TROVE_SRC} not found. Run tests/harness/build-trove.py first." >&2
  exit 1
fi

SKILL_MD=$(find "${TROVE_SRC}" -name 'SKILL.md' -print -quit)
if [ -z "${SKILL_MD}" ]; then
  echo "error: no SKILL.md found under ${TROVE_SRC}" >&2
  exit 1
fi

mkdir -p "${RESULTS_DIR}"

exercise_one() {
  local fixture="$1"
  local stem
  stem=$(basename "${fixture}" .md)
  local out="${RESULTS_DIR}/${stem}.md"
  local tmp
  tmp=$(mktemp -d)

  {
    printf 'You are operating under the following humanizer skill. Apply it faithfully to the text below the line. Return ONLY the rewritten text — no preamble, no commentary, no meta-discussion.\n\n'
    printf '=== SKILL INSTRUCTIONS BEGIN ===\n'
    cat "${SKILL_MD}"
    printf '\n=== SKILL INSTRUCTIONS END ===\n\n'
    printf '=== TEXT TO HUMANIZE BEGIN ===\n'
    cat "${fixture}"
    printf '\n=== TEXT TO HUMANIZE END ===\n\n'
    printf 'Rewrite the text above per the skill'\''s instructions. Output only the final rewritten prose.\n'
  } > "${tmp}/prompt.md"

  echo "  exercising ${SHORT_NAME} on ${stem}..."
  if ! opencode run --format json --dangerously-skip-permissions \
        < "${tmp}/prompt.md" \
        > "${tmp}/raw.json" 2>"${tmp}/stderr.log"; then
    echo "    opencode run failed on ${stem}; see ${tmp}/stderr.log" >&2
    cp "${tmp}/stderr.log" "${out}.error"
    rm -rf "${tmp}"
    return 1
  fi

  if ! python3 "${HARNESS_DIR}/extract-output.py" "${tmp}/raw.json" "${out}"; then
    echo "    failed to parse output for ${stem}" >&2
    cp "${tmp}/raw.json" "${out}.raw"
    rm -rf "${tmp}"
    return 1
  fi

  rm -rf "${tmp}"
}

echo "Exercising ${SHORT_NAME}..."
shopt -s nullglob
failures=0
for fixture in "${CORPUS_DIR}"/*.md; do
  [ "$(basename "${fixture}")" = "README.md" ] && continue
  if ! exercise_one "${fixture}"; then
    failures=$((failures + 1))
  fi
done

echo "Done: ${SHORT_NAME} (${failures} fixture(s) failed)"
[ "${failures}" -eq 0 ]