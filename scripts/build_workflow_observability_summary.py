#!/usr/bin/env python3
"""
Compact operator-facing Markdown summary from workflow observability JSON outputs.

Reads aggregate report + friction + context-efficiency JSON if present.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    art = root / "artifacts" / "workflow-observability"

    agg = _load(art / "workflow-observability-report.json")
    fr = _load(art / "review-friction-report.json")
    ctx = _load(art / "context-efficiency-report.json")

    lines = [
        "# Workflow observability summary",
        "",
        "Inspection-only rollup. Regenerate via `scripts/build_*` after `emit_workflow_event.py`.",
        "",
    ]
    if agg:
        lines.extend(
            [
                "## Headline",
                "",
                f"- Events: {agg.get('eventCount', 0)}",
                f"- Partial metrics: {agg.get('partialMetrics')}",
                "",
                "## High friction (from aggregate hotspots)",
                "",
            ]
        )
        for h in (agg.get("reviewFrictionHotspots") or [])[:5]:
            lines.append(f"- {h.get('label')} (lane={h.get('lane')} score={h.get('score')})")
        lines.extend(["", "## Leverage candidates", ""])
        for h in (agg.get("leverageCandidates") or [])[:5]:
            lines.append(f"- {h.get('label')} ({h.get('workflowType')})")
    else:
        lines.append("_No aggregate report found; run build_workflow_observability.py._\n")

    if fr:
        lines.extend(["", "## Friction report (lanes)", ""])
        for k, v in (fr.get("countsByLane") or {}).items():
            lines.append(f"- {k}: {v}")

    if ctx:
        lines.extend(
            [
                "",
                "## Context efficiency",
                "",
                f"- Median tokens (where known): {ctx.get('medianContextTokensLoaded')}",
                f"- Miss share: {ctx.get('retrievalMissEventShare')}",
            ]
        )

    out = art / "workflow-observability-summary.md"
    art.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
