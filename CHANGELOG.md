# Unreleased

- Initial scaffolding: docs/ tree, AGENTS.md, README.md, CHANGELOG.md
- Added 5 candidate skills to comparison inventory (ADR-0001)
- Created comparison matrix and candidate profile template
- Built automated test harness: exercise skills → LLM judge → regenerate matrix
- Switched scoring to numeric 1-3 scale with row sums and color-coded badges
- Moved comparison artifacts to `comparison/` at repo root (primary outputs)
- Scored all 5 candidates (round 1); adopted conorbronsdon-avoid-ai-writing as base (ADR-0002)
- Wrote recommendation with graft list from the other four candidates
- Built swain-search trove at `docs/troves/humanizer-skills/` — candidates mirrored from raw clones into committed, reviewed source
- Round 2: judge now sees full repo context (tree, README, LICENSE, CHANGELOG, CI, tests, git history), not just SKILL.md
- conorbronsdon maturity 2→3 (29/30); brandonwise maturity 2→3, detection 2→3 (tied at 23 with blader)
- Updated recommendation and exec summary with round 2 results