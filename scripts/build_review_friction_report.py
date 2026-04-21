#!/usr/bin/env python3
"""
Review friction analytics from workflow events (governance drag visibility, not policy).

Reads workflow events JSONL; writes JSON + optional Markdown under artifacts/workflow-observability/.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.observability.workflow_aggregate import load_events_from_jsonl_lines  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--events-file", type=Path, default=None)
    ap.add_argument("--output-json", type=Path, default=None)
    ap.add_argument("--output-md", type=Path, default=None)
    args = ap.parse_args()
    root = args.repo_root.resolve()

    ev_path = args.events_file
    if ev_path is None:
        d = root / "runtime" / "observability" / "workflow-events"
        files = sorted(d.glob("events_*.jsonl")) if d.is_dir() else []
        ev_path = files[-1] if files else None
    if ev_path is None or not ev_path.is_file():
        print("ERROR: no events file", file=sys.stderr)
        return 1

    events = load_events_from_jsonl_lines(ev_path.read_text(encoding="utf-8").splitlines())

    by_lane = Counter(str(e.get("lane") or "unknown") for e in events)
    by_status = Counter(str(e.get("status") or "unknown") for e in events)
    revision_loops = defaultdict(int)
    for e in events:
        rc = e.get("reviewCycles")
        if isinstance(rc, (int, float)) and rc > 1:
            revision_loops[str(e.get("lane"))] += 1

    churn_surfaces: Counter[str] = Counter()
    for e in events:
        for s in e.get("touchedSurfaces") or []:
            if isinstance(s, str):
                churn_surfaces[s] += 1

    doc = {
        "schemaVersion": "1.0.0-review-friction",
        "generatedFrom": str(ev_path.relative_to(root)),
        "eventCount": len(events),
        "countsByLane": dict(by_lane),
        "countsByStatus": dict(by_status),
        "revisionLoopHints": dict(revision_loops),
        "surfaceChurn": dict(churn_surfaces.most_common(20)),
        "notes": "Inspection only; does not change gate policy.",
    }

    out_json = args.output_json or (
        root / "artifacts" / "workflow-observability" / "review-friction-report.json"
    )
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    out_md = args.output_md or (root / "artifacts" / "workflow-observability" / "review-friction-report.md")
    lines = [
        "# Review friction report",
        "",
        f"- Events: {len(events)}",
        "",
        "## By lane",
        "",
    ]
    for k, v in by_lane.most_common():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Surface churn (from touchedSurfaces)", ""])
    for k, v in churn_surfaces.most_common(10):
        lines.append(f"- {k}: {v}")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
