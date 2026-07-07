# Candidate Profile Template

Copy this file to `profiles/<short-name>.md` and fill in.

---

# Profile: <short-name>

- **Repo**: https://github.com/<owner>/<repo>
- **License**: <license>
- **SHA reviewed**: <commit-sha>
- **Date reviewed**: YYYY-MM-DD
- **Version reviewed**: <version tag, if any>

## Summary

One-paragraph characterization of the candidate.

## Skill structure

- SKILL.md path: `<path>`
- Lines: <n>
- Frontmatter: name `<name>`, compatibility `<...>`, allowed-tools `<...>`
- References dir: yes/no — list files
- Plugin/marketplace metadata: yes/no — list
- Code (beyond SKILL.md): yes/no — describe (detectors, scripts, tests)

## Modes

- Which modes does the skill offer? (rewrite, detect, edit, other)
- Default mode?

## Voice handling

- Voice calibration from sample? yes/no
- Named voice profiles? list
- Voice selection order?

## Detection approach

- Pattern list only? Statistical analysis? Both?
- Sources cited (Wikipedia, WikiProject AI Cleanup, Copyleaks, academic)?
- Iterate-to-convergence? yes/no

## Ethics stance

- Explicit ethics section? yes/no
- Citations to academic work on false positives / bias?
- "Signals, not proof" framing?

## Notable design choices

Bullet list of anything distinctive.

## What to steal

If this candidate were merged into a personal skill, what is worth taking?

## What to skip

What is not worth taking, and why?

## Scores (summary)

See `comparison/matrix.md` for full scores. Summary: <one-line verdict>.