#!/usr/bin/env python3
"""
Analyze rejected candidates in recursion-gate.md to strengthen routing (WORK only).

Parses real gate YAML (### CANDIDATE-* blocks). See docs/governance-unbundling.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from gate_block_parser import iter_candidate_yaml_blocks  # noqa: E402
from rejection_feedback import REJECTION_CATEGORIES, infer_rejection_category  # noqa: E402


def _is_rejected(yaml_body: str) -> bool:
    return bool(re.search(r"^status:\s*rejected\s*$", yaml_body, re.MULTILINE))


def collect_rejections(gate_text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for cid, _title, yaml_body in iter_candidate_yaml_blocks(gate_text):
        if not _is_rejected(yaml_body):
            continue
        cat = infer_rejection_category(yaml_body)
        note = ""
        if m := re.search(r"^rejection_reason:\s*(.+)$", yaml_body, re.MULTILINE):
            note = m.group(1).strip()
        out.append({"candidate_id": cid, "category": cat, "rejection_reason_line": note[:500]})
    return out


def run_analysis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"total_rejections": 0, "by_category": {}, "category_percent": {}}
    c = Counter(r["category"] for r in rows)
    total = len(rows)
    return {
        "total_rejections": total,
        "by_category": dict(c.most_common()),
        "category_percent": {k: round(100.0 * v / total, 1) for k, v in c.items()},
    }


def recommendations(stats: dict[str, Any]) -> list[str]:
    if not stats.get("total_rejections"):
        return ["No rejected candidates found in gate file."]
    top = next(iter(stats["by_category"]), None)
    if not top:
        return []
    pct = stats["category_percent"].get(top, 0)
    lines = [f"Top category: **{top}** ({pct}%) — see REJECTION_CATEGORIES in scripts/rejection_feedback.py"]
    if top == "routing_error":
        lines.append("Consider tightening analyst dedup / classification before staging.")
    elif top == "sensemaking_mismatch":
        lines.append("Consider richer IX cross-references in candidate summaries when staging.")
    elif top == "accountability_violation":
        lines.append("Reinforce stage-only discipline (AGENTS.md); avoid assuming merge intent.")
    elif top == "ethics_boundary":
        lines.append("Review condition-derived ethics prompts and constitutional flags.")
    elif top == "evidence_weak":
        lines.append("Raise evidence tier or require stronger source_exchange before staging.")
    lines.append("Re-run monthly; optional YAML rejection_category: for cleaner stats.")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze rejected gate candidates for routing feedback.")
    ap.add_argument("-u", "--user", default="grace-mar", help="User id under users/ (default grace-mar)")
    ap.add_argument("--gate", type=Path, default=None, help="Explicit path to recursion-gate.md")
    ap.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Write report JSON (default: artifacts/rejection_analysis.json)",
    )
    ap.add_argument("--quiet", action="store_true", help="Suppress stdout summary")
    args = ap.parse_args()

    gate = args.gate
    if gate is None:
        gate = REPO_ROOT / "users" / args.user.strip() / "recursion-gate.md"
    if not gate.is_file():
        print(f"gate file not found: {gate}", file=sys.stderr)
        return 2

    text = gate.read_text(encoding="utf-8")
    rows = collect_rejections(text)
    stats = run_analysis(rows)
    report = {
        "gate_path": str(gate),
        "stats": stats,
        "rejections": rows,
        "recommendations": recommendations(stats),
        "categories_legend": REJECTION_CATEGORIES,
    }

    out_path = args.output_json
    if out_path is None:
        art = REPO_ROOT / "artifacts"
        art.mkdir(parents=True, exist_ok=True)
        out_path = art / "rejection_analysis.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if not args.quiet:
        print(json.dumps(stats, indent=2))
        print("\nRecommendations:")
        for line in report["recommendations"]:
            print(line)
        print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
