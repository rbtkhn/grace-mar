#!/usr/bin/env python3
"""
Context efficiency analytics (tokens, retrieval misses) from workflow events.

Labels inferred metrics explicitly. Does not claim precision where sources lack token counts.
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
    load_events_from_jsonl_lines,
    median_or_none,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--events-file", type=Path, default=None)
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
    tokens = [float(e["contextTokensLoaded"]) for e in events if isinstance(e.get("contextTokensLoaded"), (int, float))]
    misses = sum(1 for e in events if (e.get("retrievalMisses") or 0) > 0)
    doc = {
        "schemaVersion": "1.0.0-context-efficiency",
        "inferredPartial": True,
        "eventCount": len(events),
        "medianContextTokensLoaded": median_or_none(tokens),
        "retrievalMissEventShare": misses / max(len(events), 1),
        "notes": "Token counts only where sources populated contextTokensLoaded; see docs/context-efficiency.md",
    }

    out_dir = root / "artifacts" / "workflow-observability"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "context-efficiency-report.json"
    p.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    md = out_dir / "context-efficiency-report.md"
    md.write_text(
        "\n".join(
            [
                "# Context efficiency (inferred)",
                "",
                f"- Events analyzed: {len(events)}",
                f"- Median context tokens (where present): {doc['medianContextTokensLoaded']}",
                f"- Share of events with retrieval miss > 0: {doc['retrievalMissEventShare']:.3f}",
                "",
                "See [context-efficiency.md](../../docs/context-efficiency.md) for doctrine.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
