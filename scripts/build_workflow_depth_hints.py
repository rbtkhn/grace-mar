#!/usr/bin/env python3
"""
Operator-facing hints from workflow-depth audit JSON (human review only — no automation).

Reads the report emitted by build_workflow_depth_report.py or recomputes from JSONL with --from-jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def _hints_from_report(report: dict[str, Any]) -> str:
    lines = [
        "# Workflow depth hints (operator)",
        "",
        "These lines are **heuristic hints** from batch receipts — not routing rules and not merge signals.",
        "",
    ]
    n = int(report.get("receiptCount") or 0)
    if n < 5:
        lines.append(f"_Low sample ({n} receipts) — interpret cautiously._")
        lines.append("")

    totals = report.get("totalsByLaneAndWorkflowDepth") or {}
    # Find lane with most "normal" vs "shallow"
    lane_stats: dict[str, dict[str, int]] = {}
    for key, c in totals.items():
        if "|" not in key:
            continue
        lane, wd = key.split("|", 1)
        lane_stats.setdefault(lane, {})[wd] = int(c)

    for lane, m in sorted(lane_stats.items(), key=lambda x: -sum(x[1].values()))[:8]:
        total = sum(m.values())
        n_norm = m.get("normal", 0)
        n_deep = m.get("deep", 0)
        n_shallow = m.get("shallow", 0)
        if total >= 3 and n_norm >= n_deep and n_norm >= n_shallow:
            lines.append(f"- **{lane}**: often fine with **normal** depth in this window ({n_norm}/{total} normal).")
        elif total >= 3 and n_deep > n_norm + 1:
            lines.append(f"- **{lane}**: **deep** appears frequently ({n_deep}/{total}) — check for contradiction-heavy work.")
        elif total >= 4 and n_shallow >= total - 1:
            lines.append(f"- **{lane}**: mostly **shallow** runs — if churn is high, consider whether **normal** would reduce repeat passes.")

    auto = report.get("auto") or {}
    rate = auto.get("escalationRate")
    if rate is not None and auto.get("total", 0) >= 3:
        if rate >= 0.45:
            lines.append(
                f"- **auto** escalates often in this window (~{rate:.0%}) — review task anchors and query fit before blaming budgets."
            )
        elif rate <= 0.15:
            lines.append(
                f"- **auto** rarely escalates here (~{rate:.0%}) — compact paths are usually sufficient."
            )

    rare = report.get("lanesRarelyUsingDeep") or []
    if rare:
        lines.append(
            f"- Lanes with **no deep** in sample but multiple runs: {', '.join(f'`{x}`' for x in rare[:6])} — deep may be unused or unnecessary there."
        )

    lines.extend(["", "---", "", "_Inspection only. See `docs/runtime/workflow-depth-contract.md`._", ""])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit operator hints Markdown from workflow-depth audit JSON.")
    ap.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Path to workflow-depth-report.json (from build_workflow_depth_report.py)",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write hints (default: stdout)",
    )
    args = ap.parse_args()
    report_path = args.report
    if report_path is None:
        report_path = REPO_ROOT / "artifacts" / "workflow-depth" / "workflow-depth-report.json"
    if not report_path.is_file():
        print(f"error: report not found: {report_path}", file=sys.stderr)
        return 2
    report: dict[str, Any] = json.loads(report_path.read_text(encoding="utf-8"))
    text = _hints_from_report(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
