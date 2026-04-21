#!/usr/bin/env python3
"""
Batch-emit normalized workflow observability events (JSONL) from existing repo surfaces.

Does not mutate sources. Writes under runtime/observability/workflow-events/ by default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.observability.workflow_events import (  # noqa: E402
    event_from_change_proposal,
    event_from_lane_observability,
    event_from_observability_report_aggregate,
    event_from_retrieval_miss_line,
    event_from_runtime_trace_line,
    event_from_workflow_depth_line,
    load_jsonl,
)


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Default: <repo>/runtime/observability/workflow-events",
    )
    ap.add_argument("--batch-id", default="", help="Default: auto UUID")
    ap.add_argument("--dry-run", action="store_true", help="Print counts only")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    batch_id = args.batch_id.strip() or f"batch_{uuid.uuid4().hex[:12]}"
    out_dir = args.output_dir or (root / "runtime" / "observability" / "workflow-events")
    out_dir = out_dir.resolve()
    out_file = out_dir / f"events_{batch_id}.jsonl"
    manifest = out_dir / "latest-batch.json"

    events: list[dict] = []
    sources_used: list[str] = []

    # Runtime worker traces
    trace = root / "runtime" / "runtime-worker" / "traces" / "index.jsonl"
    env_home = os.environ.get("GRACE_MAR_RUNTIME_WORKER_HOME", "").strip()
    if not trace.is_file() and env_home:
        trace = Path(env_home) / "traces" / "index.jsonl"
    if trace.is_file():
        for obj in load_jsonl(trace):
            events.append(
                event_from_runtime_trace_line(
                    obj, source_path=str(trace.relative_to(root)), batch_id=batch_id
                )
            )
        sources_used.append(str(trace.relative_to(root)))

    # Workflow depth
    wd = root / "runtime" / "workflow-depth" / "index.jsonl"
    if wd.is_file():
        for obj in load_jsonl(wd):
            events.append(
                event_from_workflow_depth_line(obj, source_path=str(wd.relative_to(root)), batch_id=batch_id)
            )
        sources_used.append(str(wd.relative_to(root)))

    # Retrieval misses
    rm = root / "runtime" / "retrieval-misses" / "index.jsonl"
    if rm.is_file():
        for obj in load_jsonl(rm):
            events.append(
                event_from_retrieval_miss_line(obj, source_path=str(rm.relative_to(root)), batch_id=batch_id)
            )
        sources_used.append(str(rm.relative_to(root)))

    # Lane observability JSON
    for pattern in (
        "artifacts/work-strategy/strategy-observability.json",
        "artifacts/skill-think/think-observability.json",
        "artifacts/skill-write/write-observability.json",
    ):
        p = root / pattern
        if p.is_file():
            doc = _read_json(p)
            if doc:
                lane = str(doc.get("lane") or pattern.split("/")[1])
                events.append(
                    event_from_lane_observability(
                        doc, lane=lane, source_path=str(p.relative_to(root)), batch_id=batch_id
                    )
                )
                sources_used.append(str(p.relative_to(root)))

    # Change proposals (per-file)
    for prop in sorted((root / "users").glob("*/review-queue/proposals/*.json")):
        doc = _read_json(prop)
        if doc:
            events.append(
                event_from_change_proposal(doc, source_path=str(prop.relative_to(root)), batch_id=batch_id)
            )
            sources_used.append(str(prop.relative_to(root)))

    # Observability report aggregate (when no proposals or as supplement)
    for obs in (root / "users").glob("*/observability/observability-report.json"):
        doc = _read_json(obs)
        if doc:
            events.append(
                event_from_observability_report_aggregate(
                    doc, source_path=str(obs.relative_to(root)), batch_id=batch_id
                )
            )
            sources_used.append(str(obs.relative_to(root)))

    if args.dry_run:
        print(f"batchId={batch_id} events={len(events)} sources={len(sources_used)}")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    manifest.write_text(
        json.dumps({"batchId": batch_id, "eventFile": str(out_file.relative_to(root)), "count": len(events)}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(out_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
