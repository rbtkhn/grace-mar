#!/usr/bin/env python3
"""
Append a pipeline event (approved, rejected, applied) to PIPELINE-EVENTS.jsonl.

Used when processing the review queue. The bot emits "staged" automatically;
approved/rejected/applied are emitted by the operator or assistant.

Usage:
    python scripts/emit_pipeline_event.py applied CANDIDATE-0040 evidence_id=ACT-0014
    python scripts/emit_pipeline_event.py approved CANDIDATE-0039
    python scripts/emit_pipeline_event.py rejected CANDIDATE-0002
    python scripts/emit_pipeline_event.py rejected CANDIDATE-0045 rejection_reason="too trivial"
"""

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = REPO_ROOT / "users" / "pilot-001" / "PIPELINE-EVENTS.jsonl"


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    event_type = sys.argv[1].lower()
    candidate_id = sys.argv[2]
    if event_type not in ("approved", "rejected", "applied"):
        print("event_type must be approved, rejected, or applied", file=sys.stderr)
        sys.exit(1)
    extras = {}
    for arg in sys.argv[3:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            extras[k] = v
    event = {
        "ts": datetime.now().isoformat(),
        "event": event_type,
        "candidate_id": candidate_id,
        **extras,
    }
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"Emitted {event_type} {candidate_id}")


if __name__ == "__main__":
    main()
