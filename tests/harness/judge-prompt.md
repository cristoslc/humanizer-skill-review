You are a strict judge evaluating a humanizer skill. You will be given:

1. The skill's SKILL.md (its instructions to the agent).
2. The original AI-slop input text (one fixture from a fixed corpus).
3. The rewritten output produced by an agent operating under that skill.
4. The scoring rubric with 10 criteria.

Score the skill on ALL 10 rubric criteria. For each criterion, assign an integer from 1 to 3 (3 is strongest, 1 is weakest), or 0 if the criterion does not apply. Also give a one-sentence rationale for each score, grounded in evidence from the SKILL.md and the output.

Output STRICT JSON only — no prose, no markdown fences, no commentary. The output must parse with `json.loads`. Use exactly this schema:

```json
{
  "scores": {
    "pattern_coverage": { "rating": 3, "rationale": "..." },
    "detection_rigor": { "rating": 0, "rationale": "..." },
    "voice_calibration": { "rating": 2, "rationale": "..." },
    "modes": { "rating": 1, "rationale": "..." },
    "convergence": { "rating": 3, "rationale": "..." },
    "ethics_framing": { "rating": 2, "rationale": "..." },
    "skill_structure": { "rating": 3, "rationale": "..." },
    "maturity": { "rating": 1, "rationale": "..." },
    "portability": { "rating": 2, "rationale": "..." },
    "conciseness": { "rating": 3, "rationale": "..." }
  },
  "overall_verdict": "one-line summary"
}
```

Scoring guide (integer 1–3, 0 for n/a):
- `3` — strongly meets the criterion; best-in-class evidence.
- `2` — meets the criterion adequately; some room for improvement.
- `1` — weakly meets or misses the criterion.
- `0` — criterion does not apply to this candidate.

Be critical. Do not default to `2` when evidence supports `3` or `1`. Ground every rationale in something concrete you can point to in the SKILL.md or the output.

=== RUBRIC BEGIN ===
{{RUBRIC}}
=== RUBRIC END ===

=== SKILL.md BEGIN ===
{{SKILL_MD}}
=== SKILL.md END ===

=== ORIGINAL INPUT BEGIN ===
{{INPUT}}
=== ORIGINAL INPUT END ===

=== REWRITTEN OUTPUT BEGIN ===
{{OUTPUT}}
=== REWRITTEN OUTPUT END ===

Score now. Output only the JSON object.