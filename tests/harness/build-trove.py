#!/usr/bin/env python3
"""Build a swain-search trove from the candidate humanizer skill repos.

Clones (already in skills/ or .agents/search-snapshots/raw/) are mirrored
into docs/troves/humanizer-skills/ following the repository source format
from swain-search: per-source snapshot index, mirrored key files, summary,
manifest, synthesis.

Usage: build-trove.py [--raw-dir <path>]
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TROVE = REPO / "docs" / "troves" / "humanizer-skills"

CANDIDATES = [
    ("stephenturner-skill-deslop", "https://github.com/stephenturner/skill-deslop"),
    ("blader-humanizer", "https://github.com/blader/humanizer"),
    ("brandonwise-humanizer", "https://github.com/brandonwise/humanizer"),
    ("conorbronsdon-avoid-ai-writing", "https://github.com/conorbronsdon/avoid-ai-writing"),
    ("lguz-humanize-writing-skill", "https://github.com/lguz/humanize-writing-skill"),
]

# Files to mirror (high-signal). Everything else is summarized in the tree.
MIRROR_PATTERNS = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "LICENSE.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CLAUDE.md",
    "package.json",
    "pyproject.toml",
    "plugins.json",
    "marketplace.json",
    "plugin.json",
]

# Mirror these subtrees wholesale (all files).
MIRROR_DIRS = ["references", ".github/workflows", "detector", "cursor-rules"]


def git_meta(skill_dir: Path) -> dict:
    meta = {}
    for key, args in [
        ("sha", ["rev-parse", "HEAD"]),
        ("commit_count", ["rev-list", "--count", "HEAD"]),
        ("last_date", ["log", "-1", "--format=%cd", "--date=short"]),
    ]:
        try:
            meta[key] = subprocess.check_output(
                ["git", "-C", str(skill_dir), *args], text=True
            ).strip()
        except subprocess.CalledProcessError:
            meta[key] = None
    try:
        tags = subprocess.check_output(
            ["git", "-C", str(skill_dir), "tag", "--sort=-v:refname"], text=True
        ).strip().splitlines()
        meta["tags"] = tags[:10]
    except subprocess.CalledProcessError:
        meta["tags"] = []
    return meta


def file_tree(root: Path, max_depth: int = 3) -> str:
    lines = []
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts:
            continue
        rel = p.relative_to(root)
        if len(rel.parts) > max_depth:
            continue
        suffix = "/" if p.is_dir() else ""
        lines.append(f"{rel}{suffix}")
    return "\n".join(lines)


def find_skill_md(root: Path) -> Path | None:
    for p in root.rglob("SKILL.md"):
        return p
    return None


def mirror_source(skill_dir: Path, dest: Path, slug: str) -> int:
    """Mirror high-signal files into dest. Returns count of files mirrored."""
    count = 0
    # Mirror individual files
    for p in skill_dir.rglob("*"):
        if ".git" in p.parts or not p.is_file():
            continue
        rel = p.relative_to(skill_dir)
        # Match by name in root or any single subdir
        if p.name in MIRROR_PATTERNS:
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out)
            count += 1
    # Mirror whole subtrees
    for d in MIRROR_DIRS:
        src = skill_dir / d
        if src.is_dir():
            for p in src.rglob("*"):
                if ".git" in p.parts or not p.is_file():
                    continue
                rel = p.relative_to(skill_dir)
                out = dest / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, out)
                count += 1
    return count


def write_snapshot(skill_dir: Path, dest: Path, slug: str, url: str, meta: dict) -> None:
    skill_md = find_skill_md(skill_dir)
    tree = file_tree(skill_dir)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha = meta.get("sha", "")
    commits = meta.get("commit_count", "")
    last = meta.get("last_date", "")
    tags = ", ".join(meta.get("tags", [])) or "(none)"

    highlights = []
    if skill_md:
        highlights.append(str(skill_md.relative_to(skill_dir)))
    for name in ["README.md", "CHANGELOG.md", "CONTRIBUTING.md", "package.json"]:
        p = skill_dir / name
        if p.exists():
            highlights.append(name)

    lines = [
        "---",
        f'slug: "{slug}"',
        f'title: "{slug}"',
        "type: repository",
        f'url: "{url}"',
        f"fetched: {now}",
        f"sha: {sha}",
        f"commits: {commits}",
        f"last-commit: {last}",
        f"tags: [{tags}]",
        "highlights:",
    ]
    for h in highlights:
        lines.append(f'  - "{h}"')
    lines.append("selective: true")
    lines.append("---")
    lines.append("")
    lines.append(f"# {slug}")
    lines.append("")
    lines.append(f"- URL: {url}")
    lines.append(f"- SHA: `{sha}`")
    lines.append(f"- Commits: {commits}")
    lines.append(f"- Last commit: {last}")
    lines.append(f"- Tags: {tags}")
    lines.append("")
    lines.append("## File tree")
    lines.append("```")
    lines.append(tree)
    lines.append("```")
    lines.append("")
    lines.append("## Key files mirrored")
    lines.append("")
    for p in sorted(dest.rglob("*")):
        if p.is_file():
            rel = p.relative_to(dest)
            lines.append(f"- `{rel}`")
    lines.append("")
    dest_index = dest / f"{slug}-snapshot.md"
    dest_index.write_text("\n".join(lines) + "\n")


def write_summary(skill_dir: Path, dest: Path, slug: str, meta: dict) -> None:
    """Structured commentary on the repo. Brief — points at the snapshot for verbatim."""
    skill_md = find_skill_md(skill_dir)
    sha = meta.get("sha", "")[:7]
    commits = meta.get("commit_count", "0")
    last = meta.get("last_date", "")

    # Detect signals
    has_ci = (skill_dir / ".github" / "workflows").is_dir()
    has_tests = any(skill_dir.glob("**/test*.py")) or any(skill_dir.glob("**/*.test.*"))
    has_changelog = (skill_dir / "CHANGELOG.md").exists()
    has_contributing = (skill_dir / "CONTRIBUTING.md").exists()
    has_pkg = (skill_dir / "package.json").exists()
    has_refs = (skill_dir / "references").is_dir()

    signals = []
    if has_ci: signals.append("CI workflows")
    if has_tests: signals.append("test files")
    if has_changelog: signals.append("CHANGELOG")
    if has_contributing: signals.append("CONTRIBUTING")
    if has_pkg: signals.append("package.json")
    if has_refs: signals.append("references/ dir")

    skill_lines = 0
    if skill_md:
        skill_lines = sum(1 for _ in skill_md.read_text().splitlines())

    lines = [
        "---",
        f'slug: "{slug}"',
        "type: repository",
        f'sha: "{sha}"',
        "---",
        "",
        f"# Summary: {slug}",
        "",
        f"**Repo signals:** {', '.join(signals) if signals else 'none detected'}",
        f"**SKILL.md:** {skill_lines} lines" + (f" at `{skill_md.relative_to(skill_dir)}`" if skill_md else ""),
        f"**Git activity:** {commits} commits, last {last}",
        "",
        "## Why this source was selected",
        "",
        f"One of five initial candidate humanizer skills under review (ADR-0001). Cloned at `{sha}` for evaluation against the fixed corpus.",
        "",
        "## What it illuminates",
        "",
    ]
    if has_ci:
        lines.append("- CI workflows present — indicates active maintenance and test gating.")
    if has_tests:
        lines.append("- Test files present — the skill's detection logic is machine-verified.")
    if has_changelog:
        lines.append("- CHANGELOG present — versioned release history, useful for maturity scoring.")
    if has_contributing:
        lines.append("- CONTRIBUTING present — open to external contributions, a maturity signal.")
    if has_refs:
        lines.append("- `references/` directory — pattern lists separated from instructions, a structural signal.")
    if not signals:
        lines.append("- No repo-level maturity signals detected — likely a lean, single-file skill.")

    lines += [
        "",
        "## Gaps",
        "",
        "This summary captures repo-level signals only. Pattern coverage, modes, voice, ethics, and convergence are assessed from the SKILL.md and the rewrite output via the LLM judge.",
        "",
        "See the mirrored files in this source directory and the snapshot index for verbatim content.",
    ]
    (dest / f"{slug}-summary.md").write_text("\n".join(lines) + "\n")


def write_manifest(sources: list[dict]) -> None:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f'trove: humanizer-skills',
        f'created: {now}',
        f'refreshed: {now}',
        'tags:',
        '  - humanizer',
        '  - ai-writing',
        '  - de-slop',
        '  - agent-skill',
        'history:',
        f'  - event: created',
        f'    date: {now}',
        f'    sources: {len(sources)}',
        f'    sources-added: {len(sources)}',
        '    notes: "initial candidate inventory per ADR-0001"',
        'referenced-by:',
        '  - artifact: ADR-0001',
        '    commit: (local)',
        'sources:',
    ]
    for s in sources:
        lines.append(f'  - slug: "{s["slug"]}"')
        lines.append(f'    url: "{s["url"]}"')
        lines.append(f'    fetched: "{s["fetched"]}"')
        lines.append(f'    sha: "{s["sha"]}"')
    (TROVE / "manifest.yaml").write_text("\n".join(lines) + "\n")


def write_synthesis() -> None:
    lines = [
        "# Synthesis: humanizer-skills trove",
        "",
        "Five open-source humanizer/de-slop agent skills, cloned and mirrored for evaluation against a fixed AI-slop corpus. All MIT-licensed. All target the same domain — removing AI writing patterns from prose — but differ in structure, modes, voice handling, detection rigor, ethics framing, and maturity.",
        "",
        "## Key findings across sources",
        "",
        "- **Pattern coverage is uniformly strong** — all five candidates score well on covering filler phrases, formulaic structures, trope vocabulary, and false vulnerability. This is a saturated space.",
        "- **Modes vary widely** — conorbronsdon offers all three (rewrite/detect/edit); most offer only rewrite. blader and stephenturner are single-mode.",
        "- **Voice calibration splits the field** — conorbronsdon (5 named profiles + sample-mirroring), blader (sample-mirroring), and lguz (3 voices + selection order) have it; stephenturner and brandonwise do not.",
        "- **Ethics framing is rare** — only conorbronsdon cites academic false-positive research (Stanford Liang et al., BFI 2025-116, arXiv:2506.07001) and frames output as 'signals, not proof.' The others are silent.",
        "- **Maturity signals cluster** — conorbronsdon (CHANGELOG, CONTRIBUTING, CI, tests, v3.13.0) and brandonwise (package.json, eslint, vitest, tests, CI) are the most engineered. stephenturner and lguz are lean single-file skills.",
        "- **Conciseness inversely correlates with breadth** — stephenturner (130 lines) and lguz (234) are lean; conorbronsdon (~660) and blader (~620) are comprehensive but expensive to load.",
        "",
        "## Points of agreement",
        "",
        "- All five treat filler phrases, trope vocabulary, and formulaic structures as the core problem.",
        "- All five default to a rewrite mode that returns humanized prose inline.",
        "- All five are MIT-licensed and agent-portable (SKILL.md format).",
        "",
        "## Points of disagreement",
        "",
        "- **Detection rigor:** conorbronsdon and brandonwise cite external sources; stephenturner and lguz are opinionated lists with no backing.",
        "- **Convergence:** conorbronsdon iterates to convergence (capped at 2); blader has a draft→audit→final loop; the rest do a single pass.",
        "- **Opt-out:** only lguz has an explicit 'When NOT to Use' section.",
        "",
        "## Gaps",
        "",
        "- None of the five provide quantitative false-positive rates for their own detection rules; the ethics framing is qualitative.",
        "- None integrate with stylometric tooling (burstiness, type-token ratio) — brandonwise describes the approach but it lives in the app layer, not the skill.",
        "- The corpus used here is English-only; non-native-English bias is cited by conorbronsdon but not tested by any candidate.",
        "",
        "## Reference",
        "",
        "This trove feeds `tests/harness/repo-context.py` for repo-level scoring. Per-source verdicts live in `tests/results/<short-name>/scores.json`.",
    ]
    (TROVE / "synthesis.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    # Locate clones: prefer skills/ (legacy), fall back to .agents/search-snapshots/raw/
    raw_dirs = [REPO / "skills", REPO / ".agents" / "search-snapshots" / "raw"]
    raw_root = next((d for d in raw_dirs if d.is_dir()), None)
    if raw_root is None:
        print("error: no candidate clones found. Run scripts/fetch-candidates.sh first.", file=sys.stderr)
        return 1

    if TROVE.exists():
        shutil.rmtree(TROVE)
    (TROVE / "sources").mkdir(parents=True)

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources = []
    for slug, url in CANDIDATES:
        skill_dir = raw_root / slug
        if not skill_dir.is_dir():
            print(f"warn: {skill_dir} not found, skipping", file=sys.stderr)
            continue
        print(f"mirroring {slug}...", file=sys.stderr)
        dest = TROVE / "sources" / slug
        dest.mkdir(parents=True, exist_ok=True)
        meta = git_meta(skill_dir)
        mirror_source(skill_dir, dest, slug)
        write_snapshot(skill_dir, dest, slug, url, meta)
        write_summary(skill_dir, dest, slug, meta)
        sources.append({"slug": slug, "url": url, "fetched": now, "sha": meta.get("sha", "")})

    write_manifest(sources)
    write_synthesis()

    # Trove README
    (TROVE / "README.md").write_text(
        "# Trove: humanizer-skills\n\n"
        "Five open-source humanizer/de-slop agent skills, mirrored for evaluation.\n\n"
        "- `manifest.yaml` — provenance and metadata\n"
        "- `synthesis.md` — thematic distillation across all sources\n"
        "- `sources/<slug>/` — per-source snapshot index, mirrored key files, summary\n\n"
        "See `comparison/` at the repo root for scoring outputs.\n"
    )

    print(f"wrote trove: {TROVE} ({len(sources)} sources)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())