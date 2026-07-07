# Troves

Swain-search troves: cached, normalized source collections for evaluation and research.

## Contents

- `humanizer-skills/` — five candidate humanizer skill repos, mirrored for evaluation against the fixed corpus. Referenced by ADR-0001 and the test harness.

Each trove has:
- `manifest.yaml` — provenance and metadata
- `synthesis.md` — thematic distillation across sources
- `sources/<slug>/` — per-source snapshot index, mirrored key files, summary

See `~/.agents/skills/swain-search/SKILL.md` for the trove protocol.