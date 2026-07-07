#!/usr/bin/env python3
"""Score a single candidate's outputs with an LLM judge.

For each (fixture, output) pair, build a judge prompt from the template,
call `opencode run`, parse the JSON verdict, and collect into an aggregate
scores document.

Usage: score-outputs.py <short-name>
Writes: tests/results/<short-name>/scores.json
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HARNESS = REPO / "tests" / "harness"

CRITERIA = [
    "pattern_coverage",
    "detection_rigor",
    "voice_calibration",
    "modes",
    "convergence",
    "ethics_framing",
    "skill_structure",
    "maturity",
    "portability",
    "conciseness",
]

FIXTURE_STEMS = ["blog-post", "email", "report", "marketing", "essay"]


def load_template() -> str:
    return (HARNESS / "judge-prompt.md").read_text()


def fill(template: str, rubric: str, skill_md: str, input_text: str, output_text: str) -> str:
    return (
        template
        .replace("{{RUBRIC}}", rubric)
        .replace("{{SKILL_MD}}", skill_md)
        .replace("{{INPUT}}", input_text)
        .replace("{{OUTPUT}}", output_text)
    )


def run_judge(prompt: str) -> dict:
    """Call opencode run with the judge prompt and parse JSON from the output."""
    tmp = Path(subprocess.check_output(["mktemp", "-d"], text=True).strip())
    try:
        prompt_file = tmp / "prompt.md"
        prompt_file.write_text(prompt)
        raw_file = tmp / "raw.json"
        with prompt_file.open() as fh, raw_file.open("w") as raw_fh:
            proc = subprocess.run(
                ["opencode", "run", "--format", "json", "--dangerously-skip-permissions"],
                stdin=fh,
                stdout=raw_fh,
                stderr=subprocess.PIPE,
                text=True,
            )
        if proc.returncode != 0:
            return {"error": f"opencode run failed: {proc.stderr[:500]}", "scores": {}}
        # Extract the final text via the same extractor
        extracted = tmp / "extracted.md"
        subprocess.run(
            ["python3", str(HARNESS / "extract-output.py"), str(raw_file), str(extracted)],
            check=True,
        )
        text = extracted.read_text().strip()
        # The judge should output JSON only; strip fences if present
        if text.startswith("```"):
            text = text.split("```", 2)[1] if text.count("```") >= 2 else text
            if text.startswith("json"):
                text = text[4:]
            if text.endswith("```"):
                text = text[:-3]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": f"non-JSON judge output: {text[:300]}", "scores": {}}
    finally:
        subprocess.run(["rm", "-rf", str(tmp)], check=False)


def aggregate(verdicts: list[dict]) -> dict:
    """Aggregate per-fixture verdicts into a single scores document.

    For each criterion, pick the modal rating across fixtures and join rationales.
    """
    agg = {}
    for crit in CRITERIA:
        ratings = []
        rationales = []
        for v in verdicts:
            s = v.get("scores", {}).get(crit, {})
            r = s.get("rating")
            if r:
                ratings.append(r)
            rat = s.get("rationale")
            if rat:
                rationales.append(rat)
        if not ratings:
            agg[crit] = {"rating": "n/a", "rationale": "no verdicts collected"}
            continue
        # Modal rating, with high > med > low precedence on ties
        order = {"high": 3, "med": 2, "low": 1, "n/a": 0}
        counts = {}
        for r in ratings:
            counts[r] = counts.get(r, 0) + 1
        top = sorted(counts.items(), key=lambda kv: (kv[1], order.get(kv[0], 0)), reverse=True)
        agg[crit] = {
            "rating": top[0][0],
            "rationale": " | ".join(rationales[:3]) if rationales else "",
            "per_fixture": ratings,
        }
    return agg


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: score-outputs.py <short-name>", file=sys.stderr)
        return 1
    short = sys.argv[1]
    skill_dir = REPO / "skills" / short
    results_dir = REPO / "tests" / "results" / short
    corpus_dir = REPO / "tests" / "fixtures" / "corpus"

    if not skill_dir.is_dir():
        print(f"error: {skill_dir} not found. Run scripts/fetch-candidates.sh first.", file=sys.stderr)
        return 1
    if not results_dir.is_dir():
        print(f"error: {results_dir} not found. Run exercise-skill.sh first.", file=sys.stderr)
        return 1

    # Locate SKILL.md
    candidates = list(skill_dir.rglob("SKILL.md"))
    if not candidates:
        print(f"error: no SKILL.md under {skill_dir}", file=sys.stderr)
        return 1
    skill_md = candidates[0].read_text()

    rubric = (REPO / "docs" / "plans" / "rubric.md").read_text()
    template = load_template()

    verdicts = []
    for stem in FIXTURE_STEMS:
        input_path = corpus_dir / f"{stem}.md"
        output_path = results_dir / f"{stem}.md"
        if not input_path.is_file():
            print(f"warn: missing fixture {input_path}", file=sys.stderr)
            continue
        if not output_path.is_file():
            print(f"warn: missing output {output_path}; skipping", file=sys.stderr)
            continue
        input_text = input_path.read_text()
        output_text = output_path.read_text()
        prompt = fill(template, rubric, skill_md, input_text, output_text)
        print(f"  judging {short} on {stem}...", file=sys.stderr)
        verdict = run_judge(prompt)
        verdict["_fixture"] = stem
        verdicts.append(verdict)

    scores = {
        "short_name": short,
        "skill_md_path": str(candidates[0]),
        "verdicts": verdicts,
        "aggregate": aggregate(verdicts),
    }
    out_path = results_dir / "scores.json"
    out_path.write_text(json.dumps(scores, indent=2))
    print(f"wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())