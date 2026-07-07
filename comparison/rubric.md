# Scoring Rubric

Each candidate is scored against the criteria below. Scores are integers 1–3 (3 is strongest, 1 is weakest), or 0 if the criterion does not apply. The LLM judge assigns a score per criterion per fixture; the aggregator takes the mean and modal rating across the 5 fixtures. Record in `comparison/matrix.md`.

## Criteria

### 1. Pattern coverage

Does the skill cover the full range of AI writing patterns — filler phrases, formulaic structures, trope vocabulary, false vulnerability, invented concept labels, false ranges?

### 2. Detection rigor

Is detection grounded in cited sources (Wikipedia Signs of AI writing, WikiProject AI Cleanup, stylometric research, academic work)? Or is it an opinionated list with no backing?

### 3. Voice calibration

Can the skill adapt output to a user-provided writing sample? Are named voice profiles offered? Is the voice selection order sensible (user-specified → mirror → default)?

### 4. Modes

Does the skill offer the modes that matter — rewrite, detect (flag only), edit (in-place file edits)? Is the default mode sensible?

### 5. Convergence

Does the skill iterate to convergence (rewrite until no patterns remain), or does it do a single pass?

### 6. Ethics framing

Does the skill acknowledge that AI-pattern detection is probabilistic and biased against non-native English writers? Does it cite academic work (Stanford Liang et al., BFI 2025-116)? Does it frame output as "signals, not proof"?

### 7. Skill structure

Is the SKILL.md well-organized? Is frontmatter correct (name, description, compatibility, allowed-tools)? Are references well-separated from instructions? Is the skill portable across agents?

### 8. Maturity

Version history, changelog, CONTRIBUTING, tests, CI. Is this a one-shot or a maintained project?

### 9. Portability

Does the skill assume a specific agent (Claude, Cursor) or is it agent-agnostic? Does it use `compatibility: any-agent`? Does it avoid agent-specific tool calls?

### 10. Conciseness

Is the skill lean enough to load cheaply, or is it bloated? Lines of SKILL.md is a rough proxy.

## Scoring guide

- `3` — strongly meets the criterion; best-in-class.
- `2` — meets the criterion adequately; room for improvement.
- `1` — weakly meets or misses the criterion.
- `0` — criterion does not apply to this candidate.