#!/usr/bin/env python3
"""
Batch workflow-depth audit: read append-only receipts JSONL, emit aggregate JSON (+ optional MD).

Inspection only — not governance. See docs/runtime/workflow-depth-audit.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def _wd_root(repo_root: Path) -> Path:
    raw = os.environ.get("GRACE_MAR_WORKFLOW_DEPTH_HOME", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return repo_root / "runtime" / "workflow-depth"


def _load_lines(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def build_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_lane_depth: dict[tuple[str, str], int] = defaultdict(int)
    auto_total = 0
    auto_escalated = 0
    by_source: dict[str, int] = defaultdict(int)
    override_n = 0
    shallow_by_lane: dict[str, int] = defaultdict(int)
    shallow_runs: list[tuple[str, str]] = []  # (lane, ts)

    for r in rows:
        lane = str(r.get("lane") or "")
        wd = str(r.get("workflow_depth") or "")
        by_lane_depth[(lane, wd)] += 1
        if wd == "auto":
            auto_total += 1
            if r.get("escalated") is True:
                auto_escalated += 1
        sw = str(r.get("sourceWorkflow") or "unknown")
        by_source[sw] += 1
        if r.get("operatorOverride") is True:
            override_n += 1
        if wd == "shallow":
            shallow_by_lane[lane] += 1
            shallow_runs.append((lane, str(r.get("timestamp") or "")))

    # Lanes rarely using deep
    deep_by_lane: dict[str, int] = defaultdict(int)
    total_by_lane: dict[str, int] = defaultdict(int)
    for r in rows:
        lane = str(r.get("lane") or "")
        wd = str(r.get("workflow_depth") or "")
        total_by_lane[lane] += 1
        if wd == "deep":
            deep_by_lane[lane] += 1

    rare_deep_lanes = sorted(
        [lane for lane in total_by_lane if total_by_lane[lane] >= 2 and deep_by_lane[lane] == 0],
        key=lambda x: total_by_lane[x],
        reverse=True,
    )[:12]

    # Shallow churn: repeated shallow same lane (heuristic: count pairs with same lane in window)
    churn_hints: list[dict[str, Any]] = []
    lane_shallow_streak: dict[str, int] = defaultdict(int)
    for lane, _ts in sorted(shallow_runs, key=lambda x: x[1]):
        lane_shallow_streak[lane] += 1
        if lane_shallow_streak[lane] >= 3:
            churn_hints.append({"lane": lane, "shallowRunsAtLeast": lane_shallow_streak[lane]})

    auto_escalation_rate = (auto_escalated / auto_total) if auto_total else None

    top_sources = sorted(by_source.items(), key=lambda x: -x[1])[:8]

    return {
        "schemaVersion": "1.0-workflow-depth-audit",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "receiptCount": len(rows),
        "totalsByLaneAndWorkflowDepth": {f"{a}|{b}": c for (a, b), c in sorted(by_lane_depth.items())},
        "auto": {
            "total": auto_total,
            "escalatedApprox": auto_escalated,
            "escalationRate": round(auto_escalation_rate, 4) if auto_escalation_rate is not None else None,
        },
        "sourceWorkflowCounts": {k: v for k, v in top_sources},
        "operatorOverrideCount": override_n,
        "lanesRarelyUsingDeep": rare_deep_lanes,
        "shallowChurnHints": churn_hints[:20],
        "partialMetrics": len(rows) < 3,
    }


def _markdown_summary(report: dict[str, Any]) -> str:
    lines = [
        "# Workflow depth audit (batch)",
        "",
        f"Generated: `{report.get('generatedAt')}`",
        f"Receipt lines read: **{report.get('receiptCount', 0)}**",
        "",
        "## Auto",
        "",
        f"- Total `auto` runs: {report.get('auto', {}).get('total')}",
        f"- Approx. escalated: {report.get('auto', {}).get('escalatedApprox')} "
        f"(rate {report.get('auto', {}).get('escalationRate')})",
        "",
        "## By lane × workflow_depth",
        "",
    ]
    t = report.get("totalsByLaneAndWorkflowDepth") or {}
    for k, v in sorted(t.items(), key=lambda x: -x[1])[:24]:
        lines.append(f"- `{k}`: {v}")
    lines.extend(["", "## Source workflow", ""])
    for k, v in (report.get("sourceWorkflowCounts") or {}).items():
        lines.append(f"- `{k}`: {v}")
    if report.get("partialMetrics"):
        lines.extend(["", "_Low sample — treat as weather, not policy._", ""])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate workflow-depth JSONL receipts (batch).")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="JSON report path (default: artifacts/workflow-depth/workflow-depth-report.json)",
    )
    ap.add_argument("--markdown", type=Path, default=None, help="Optional Markdown summary path")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    idx = _wd_root(root) / "index.jsonl"
    rows = _load_lines(idx)
    report = build_report(rows)
    out = args.output
    if out is None:
        out = root / "artifacts" / "workflow-depth" / "workflow-depth-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    if args.markdown is not None:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(_markdown_summary(report), encoding="utf-8")
        print(f"wrote {args.markdown}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
