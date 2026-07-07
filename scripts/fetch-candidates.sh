#!/usr/bin/env bash
# Fetch candidate humanizer skill repos into skills/<short-name>/.
# Clones are gitignored and not redistributed.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p skills

# short_name|url
candidates=(
  "stephenturner-skill-deslop|https://github.com/stephenturner/skill-deslop"
  "blader-humanizer|https://github.com/blader/humanizer"
  "brandonwise-humanizer|https://github.com/brandonwise/humanizer"
  "conorbronsdon-avoid-ai-writing|https://github.com/conorbronsdon/avoid-ai-writing"
  "lguz-humanize-writing-skill|https://github.com/lguz/humanize-writing-skill"
)

for entry in "${candidates[@]}"; do
  short="${entry%%|*}"
  url="${entry##*|}"
  dest="skills/${short}"
  if [ -d "${dest}/.git" ]; then
    echo "Updating ${short}..."
    git -C "${dest}" fetch --quiet --prune
    git -C "${dest}" pull --quiet --ff-only
  else
    echo "Cloning ${short}..."
    git clone --quiet "${url}" "${dest}"
  fi
  sha=$(git -C "${dest}" rev-parse HEAD)
  echo "  ${short} @ ${sha}"
done

echo "Done. Candidate skills are in skills/ (gitignored)."