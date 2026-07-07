#!/usr/bin/env python3
"""Gather repo-level context for a candidate skill from the trove.

Reads docs/troves/humanizer-skills/sources/<short-name>/ and produces a
structured summary the LLM judge can use alongside the SKILL.md.

Usage: repo-context.py <short-name>
Prints the context block to stdout.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TROVE = REPO / "docs" / "troves" / "humanizer-skills" / "sources"


def gather(short: str) -> str:
    src = TROVE / short
    if not src.is_dir():
        print(f"error: {src} not found. Run tests/harness/build-trove.py first.", file=sys.stderr)
        sys.exit(1)

    snapshot = src / f"{short}-snapshot.md"
    summary = src / f"{short}-summary.md"

    parts = [f"# Repo context: {short}\n"]

    if snapshot.is_file():
        parts.append(snapshot.read_text())
    else:
        # Fallback: list mirrored files
        parts.append("## Mirrored files\n")
        for p in sorted(src.rglob("*")):
            if p.is_file() and p.name not in (f"{short}-snapshot.md", f"{short}-summary.md"):
                parts.append(f"- `{p.relative_to(src)}`\n")

    parts.append("\n## Key file contents\n")
    for p in sorted(src.rglob("*")):
        if ".git" in p.parts or not p.is_file():
            continue
        if p.name in (f"{short}-snapshot.md", f"{short}-summary.md"):
            continue
        rel = p.relative_to(src)
        content = p.read_text(errors="replace")
        if len(content) > 4000:
            content = content[:4000] + "\n... (truncated)\n"
        parts.append(f"\n### `{rel}`\n```\n{content}\n```\n")

    if summary.is_file():
        parts.append("\n## Structured summary\n")
        parts.append(summary.read_text())

    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: repo-context.py <short-name>", file=sys.stderr)
        return 1
    sys.stdout.write(gather(sys.argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())