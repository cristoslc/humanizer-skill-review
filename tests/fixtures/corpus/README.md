# Test corpus

A fixed corpus of AI-slop prose, one passage per file, used as the input to every humanizer skill under review. Each skill receives the same input — apples-to-apples comparison.

## Files

- `blog-post.md` — a typical AI-generated blog post intro
- `email.md` — an AI-drafted professional email
- `report.md` — an AI-generated executive summary
- `marketing.md` — an AI-drafted product marketing blurb
- `essay.md` — an AI-drafted essay paragraph

Each file is short (3-6 paragraphs) and deliberately saturated with common AI writing patterns: filler phrases, formulaic structures (binary contrasts, tricolons, anaphora), trope vocabulary ("delve", "quietly", "serves as"), false vulnerability, invented concept labels, and false ranges.

## Purpose

The corpus is the constant input across all candidates. Outputs land in `tests/results/<short-name>/<fixture-stem>.md`. The LLM judge compares output against input and scores per `docs/plans/rubric.md`.