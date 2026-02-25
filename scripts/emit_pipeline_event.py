#!/usr/bin/env python3
"""
Append a pipeline event to PIPELINE-EVENTS.jsonl.

Used by operator scripts and maintenance jobs.

Usage:
    python scripts/emit_pipeline_event.py applied CANDIDATE-0040 evidence_id=ACT-0014
    python scripts/emit_pipeline_event.py approved CANDIDATE-0039
    python scripts/emit_pipeline_event.py rejected CANDIDATE-0002 rejection_reason="too trivial"
    python scripts/emit_pipeline_event.py validation_failed CANDIDATE-0046 reason="missing evidence"
    python scripts/emit_pipeline_event.py maintenance none action=rotate_context rotated=true
    python scripts/emit_pipeline_event.py --user grace-mar applied CANDIDATE-0040
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Append event to pipeline ledger.")
    parser.add_argument(
        "--user",
        "-u",
        default=(os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"),
        help="User id (default: GRACE_MAR_USER_ID or grace-mar)",
    )
    parser.add_argument("event_type", help="Event name (approved/rejected/applied/validation_failed/maintenance/...)")
    parser.add_argument(
        "candidate_id",
        help="Candidate id, or 'none' when event is not candidate-specific",
    )
    parser.add_argument("extras", nargs="*", help="Extra key=value fields")
    args = parser.parse_args()

    event_type = args.event_type.lower().strip()
    if not event_type:
        print("event_type must be non-empty", file=sys.stderr)
        sys.exit(1)
    candidate_id = args.candidate_id.strip() or None
    if candidate_id and candidate_id.lower() == "none":
        candidate_id = None

    events_path = REPO_ROOT / "users" / args.user / "PIPELINE-EVENTS.jsonl"
    extras = {}
    for arg in args.extras:
        if "=" in arg:
            k, v = arg.split("=", 1)
            extras[k] = v
    event = {
        "ts": datetime.now().isoformat(),
        "event": event_type,
        "candidate_id": candidate_id,
        **extras,
    }
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    print(f"Emitted {event_type} {candidate_id or '(none)'} for {args.user}")


if __name__ == "__main__":
    main()
