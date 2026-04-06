#!/usr/bin/env python3
"""
Render a unified Record Diff Queue from identity-diff JSON files.

Template-portable: works in companion-self and any instance repo.

Each diff card shows: Scope, Prior State, Proposed State, Evidence,
Why It Matters, Confidence Delta, Conflict Note, Recommended Action.

Usage:
  python3 scripts/render_record_diff_queue.py users/demo/review-queue/diffs/
  python3 scripts/render_record_diff_queue.py diff-a.json diff-b.json
  python3 scripts/render_record_diff_queue.py --output queue.md users/demo/review-queue/diffs/
  python3 scripts/render_record_diff_queue.py --json users/demo/review-queue/diffs/
  python3 scripts/render_record_diff_queue.py --from-gate -u grace-mar
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FIELDS = {"schemaVersion", "diffId", "userSlug", "category", "before", "after", "changeSummary", "evidenceRefs"}


def load_diff(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        if not REQUIRED_FIELDS.issubset(data.keys()):
            return None
        data["_source_path"] = str(path)
        return data
    except (json.JSONDecodeError, OSError):
        return None


def collect_diffs(paths: list[str]) -> list[dict[str, Any]]:
    """Collect identity-diff JSON files from paths (files or directories)."""
    diffs: list[dict[str, Any]] = []
    for p in paths:
        target = Path(p) if Path(p).is_absolute() else ROOT / p
        if target.is_dir():
            for f in sorted(target.glob("*.json")):
                d = load_diff(f)
                if d:
                    diffs.append(d)
        elif target.is_file():
            d = load_diff(target)
            if d:
                diffs.append(d)
    return diffs


def _sort_key(diff: dict[str, Any]) -> tuple[float, str]:
    """Sort by confidence delta magnitude (descending), then diffId."""
    cd = diff.get("confidenceDelta")
    if cd and isinstance(cd, dict):
        delta = abs(cd.get("after", 0) - cd.get("before", 0))
    else:
        delta = 0.0
    return (-delta, diff.get("diffId", ""))


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
        return "\n".join(
            f"{prefix}- {item}" if not isinstance(item, (dict, list))
            else f"{prefix}-\n{render_value(item, indent + 1)}"
            for item in value
        )
    return f"{prefix}{value}"


def render_card(diff: dict[str, Any]) -> str:
    """Render one diff as a Markdown card."""
    lines: list[str] = []
    diff_id = diff["diffId"]
    category = diff["category"]
    user = diff["userSlug"]

    lines.append(f"### {diff_id}")
    lines.append("")
    lines.append(f"**Scope:** `{category}` | **User:** `{user}`")
    lines.append("")

    lines.append("#### Prior State")
    lines.append("")
    lines.append(render_value(diff["before"]))
    lines.append("")

    lines.append("#### Proposed State")
    lines.append("")
    lines.append(render_value(diff["after"]))
    lines.append("")

    lines.append("#### Change Summary")
    lines.append("")
    lines.append(diff["changeSummary"])
    lines.append("")

    why = diff.get("whyItMatters")
    if why:
        lines.append("#### Why It Matters")
        lines.append("")
        lines.append(why)
        lines.append("")

    evidence = diff.get("evidenceRefs", [])
    lines.append("#### Evidence")
    lines.append("")
    if evidence:
        for ref in evidence:
            lines.append(f"- `{ref}`")
    else:
        lines.append("- None provided")
    lines.append("")

    cd = diff.get("confidenceDelta")
    if cd and isinstance(cd, dict):
        lines.append("#### Confidence Delta")
        lines.append("")
        lines.append(f"- Before: `{cd.get('before', '?')}`")
        lines.append(f"- After: `{cd.get('after', '?')}`")
        lines.append("")

    conflict = diff.get("conflictNote")
    if conflict:
        lines.append("#### Conflict Note")
        lines.append("")
        lines.append(conflict)
        lines.append("")

    action = diff.get("recommendedAction")
    if action:
        labels = {"accept": "Accept", "reject": "Reject", "defer": "Defer", "merge_partially": "Merge partially"}
        lines.append(f"#### Recommended Action: **{labels.get(action, action)}**")
        lines.append("")

    return "\n".join(lines)


def render_queue(diffs: list[dict[str, Any]]) -> str:
    """Render the full queue as Markdown."""
    sorted_diffs = sorted(diffs, key=_sort_key)
    lines: list[str] = []
    lines.append("# Record Diff Queue")
    lines.append("")
    lines.append(f"{len(sorted_diffs)} pending change(s)")
    lines.append("")
    lines.append("---")
    lines.append("")
    for diff in sorted_diffs:
        lines.append(render_card(diff))
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def _load_from_gate(user_slug: str) -> list[dict[str, Any]]:
    """Load diffs by converting recursion-gate pending candidates via the adapter."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from gate_to_diff_adapter import convert_gate
    return convert_gate(user_slug)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a unified Record Diff Queue from identity-diff JSON files."
    )
    parser.add_argument("paths", nargs="*", help="Identity-diff JSON files or directories containing them")
    parser.add_argument("--output", "-o", help="Write Markdown output to file")
    parser.add_argument("--json", action="store_true", help="Output collected diffs as JSON array instead of Markdown")
    parser.add_argument("--from-gate", action="store_true", help="Convert recursion-gate pending candidates to diffs")
    parser.add_argument("-u", "--user", default="grace-mar", help="User slug for --from-gate (default: grace-mar)")
    args = parser.parse_args()

    diffs: list[dict[str, Any]] = []
    if args.from_gate:
        diffs.extend(_load_from_gate(args.user))
    if args.paths:
        diffs.extend(collect_diffs(args.paths))

    if not args.from_gate and not args.paths:
        parser.error("Provide paths to identity-diff JSON files/directories, or use --from-gate")

    if not diffs:
        print("No valid identity-diff JSON files found.", file=sys.stderr)
        return 1

    if args.json:
        clean = [{k: v for k, v in d.items() if k != "_source_path"} for d in diffs]
        output = json.dumps(clean, indent=2)
    else:
        output = render_queue(diffs)

    if args.output:
        out_path = Path(args.output) if Path(args.output).is_absolute() else ROOT / args.output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
        print(f"Wrote queue to: {out_path}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
