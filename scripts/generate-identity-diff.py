#!/usr/bin/env python3
"""
Generate a human-readable Markdown diff from a structured identity-diff JSON artifact.

Usage:
  python3 scripts/generate-identity-diff.py users/demo/review-queue/diffs/diff-001.json
  python3 scripts/generate-identity-diff.py users/demo/review-queue/diffs/diff-001.json --output users/demo/review-queue/identity_diff.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_value(value: Any, indent: int = 0) -> str:
    prefix = "  " * indent
    if isinstance(value, dict):
        lines = []
        for key, subvalue in value.items():
            if isinstance(subvalue, (dict, list)):
                lines.append(f"{prefix}- **{key}**:")
                lines.append(render_value(subvalue, indent + 1))
            else:
                lines.append(f"{prefix}- **{key}**: {subvalue}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(render_value(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
        return "\n".join(lines)
    return f"{prefix}- {value}"


def make_markdown(diff: dict[str, Any]) -> str:
    category = diff["category"]
    summary = diff["changeSummary"]
    evidence_refs = diff.get("evidenceRefs", [])
    conflict_note = diff.get("conflictNote", "")
    confidence = diff.get("confidenceDelta")

    lines = []
    lines.append("# Proposed Identity / Policy Diff")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"Primary scope: `{category}`")
    lines.append("")
    lines.append("## Prior State")
    lines.append("")
    lines.append(render_value(diff["before"]))
    lines.append("")
    lines.append("## Proposed State")
    lines.append("")
    lines.append(render_value(diff["after"]))
    lines.append("")
    lines.append("## Change Summary")
    lines.append("")
    lines.append(summary)
    lines.append("")

    if conflict_note:
        lines.append("## Conflict Note")
        lines.append("")
        lines.append(conflict_note)
        lines.append("")

    if confidence:
        lines.append("## Confidence Delta")
        lines.append("")
        lines.append(f"- Before: `{confidence['before']}`")
        lines.append(f"- After: `{confidence['after']}`")
        lines.append("")

    lines.append("## Supporting Evidence")
    lines.append("")
    if evidence_refs:
        for ref in evidence_refs:
            lines.append(f"- `{ref}`")
    else:
        lines.append("- None provided")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Markdown from an identity diff JSON file.")
    parser.add_argument("diff_json", help="Path to diff JSON file")
    parser.add_argument("--output", help="Optional output Markdown path")
    args = parser.parse_args()

    diff_path = (ROOT / args.diff_json).resolve() if not Path(args.diff_json).is_absolute() else Path(args.diff_json)
    diff = load_json(diff_path)
    md = make_markdown(diff)

    if args.output:
        output_path = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md + "\n", encoding="utf-8")
        print(f"Wrote Markdown diff to: {output_path}")
    else:
        print(md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
