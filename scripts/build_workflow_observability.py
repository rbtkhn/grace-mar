#!/usr/bin/env python3
"""
Aggregate workflow-observability-report.json from normalized events JSONL.

Reads: runtime/observability/workflow-events/events_<batch>.jsonl or --events-file
Output: artifacts/workflow-observability/workflow-observability-report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.observability.workflow_aggregate import (  # noqa: E402
    aggregate_events,
    load_events_from_jsonl_lines,
)

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

SCHEMA_PATH = REPO_ROOT / "schema-registry" / "workflow-observability-report.v1.json"


def load_events(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return load_events_from_jsonl_lines(lines)


def find_latest_events_file(root: Path) -> Path | None:
    d = root / "runtime" / "observability" / "workflow-events"
    if not d.is_dir():
        return None
    files = sorted(d.glob("events_*.jsonl"))
    return files[-1] if files else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--events-file", type=Path, default=None)
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Default: artifacts/workflow-observability/workflow-observability-report.json",
    )
    ap.add_argument("--batch-id", default="", help="Override batch id (default: from events filename)")
    ap.add_argument("--no-schema-validate", action="store_true")
    args = ap.parse_args()
    root = args.repo_root.resolve()

    ev_path = args.events_file
    if ev_path is None:
        ev_path = find_latest_events_file(root)
    if ev_path is None or not ev_path.is_file():
        print("ERROR: no events JSONL found; run scripts/emit_workflow_event.py first", file=sys.stderr)
        return 1

    batch_id = args.batch_id.strip()
    if not batch_id:
        batch_id = ev_path.stem.replace("events_", "", 1) if ev_path.name.startswith("events_") else "unknown"

    events = load_events(ev_path)
    report = aggregate_events(events, batch_id=batch_id, sources_used=[str(ev_path.relative_to(root))])

    out = args.output or (root / "artifacts" / "workflow-observability" / "workflow-observability-report.json")
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")

    if not args.no_schema_validate and jsonschema is not None and SCHEMA_PATH.is_file():
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(instance=json.loads(text), schema=schema)

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
