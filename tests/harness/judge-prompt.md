You are a strict judge evaluating a humanizer skill. You will be given:

1. The skill's SKILL.md (its instructions to the agent).
2. The original AI-slop input text (one fixture from a fixed corpus).
3. The rewritten output produced by an agent operating under that skill.
4. The scoring rubric with 10 criteria.

Score the skill on ALL 10 rubric criteria. For each criterion, assign one of: `high`, `med`, `low`, or `n/a`. Also give a one-sentence rationale for each score, grounded in evidence from the SKILL.md and the output.

Output STRICT JSON only — no prose, no markdown fences, no commentary. The output must parse with `json.loads`. Use exactly this schema:

```json
{
  "scores": {
    "pattern_coverage": { "rating": "high|med|low|n/a", "rationale": "..." },
    "detection_rigor": { "rating": "...", "rationale": "..." },
    "voice_calibration": { "rating": "...", "rationale": "..." },
    "modes": { "rating": "...", "rationale": "..." },
    "convergence": { "rating": "...", "rationale": "..." },
    "ethics_framing": { "rating": "...", "rationale": "..." },
    "skill_structure": { "rating": "...", "rationale": "..." },
    "maturity": { "rating": "...", "rationale": "..." },
    "portability": { "rating": "...", "rationale": "..." },
    "conciseness": { "rating": "...", "rationale": "..." }
  },
  "overall_verdict": "one-line summary"
}
```

Scoring guide:
- `high` — strongly meets the criterion; best-in-class evidence.
- `med` — meets the criterion adequately; some room for improvement.
- `low` — weakly meets or misses the criterion.
- `n/a` — criterion does not apply to this candidate.

Be critical. Do not default to `med` when evidence supports `high` or `low`. Ground every rationale in something concrete you can point to in the SKILL.md or the output.

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