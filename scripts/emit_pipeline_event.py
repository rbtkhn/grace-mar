#!/usr/bin/env python3
"""
Append a pipeline event to pipeline-events.jsonl.

Each line includes **event_id**, **fork_id** (user id), **envelope_version** (see
`pipeline_event_envelope.py`) unless overridden via `--merge-json`. Used by operator
scripts and maintenance jobs.

Usage:
    python scripts/emit_pipeline_event.py applied CANDIDATE-0040 evidence_id=ACT-0014
    python scripts/emit_pipeline_event.py approved CANDIDATE-0039
    python scripts/emit_pipeline_event.py rejected CANDIDATE-0002 rejection_reason="too trivial"
    python scripts/emit_pipeline_event.py validation_failed CANDIDATE-0046 reason="missing evidence"
    python scripts/emit_pipeline_event.py maintenance none action=rotate_context rotated=true
    python scripts/emit_pipeline_event.py --user grace-mar applied CANDIDATE-0040

Closed-loop verification (optional):
    python scripts/emit_pipeline_event.py export_used none export_id=abc123 used_in_openclaw=true
    python scripts/emit_pipeline_event.py merge_feedback CANDIDATE-0040 helpful=true

Rich payloads (schema 2 fields, safe for special chars):
    python scripts/emit_pipeline_event.py -u grace-mar --merge-json '{"event_schema":2,"ix_entry_id":"LEARN-0042"}' applied CANDIDATE-0040
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

try:
    from pipeline_event_envelope import ENVELOPE_VERSION, new_pipeline_event_id
except ImportError:
    from scripts.pipeline_event_envelope import ENVELOPE_VERSION, new_pipeline_event_id


def append_pipeline_event(
    user_id: str,
    event_type: str,
    candidate_id: str | None,
    *,
    merge: dict | None = None,
    extras: dict[str, str] | None = None,
) -> dict:
    """
    Append one JSON line to users/<user_id>/pipeline-events.jsonl.
    Returns the full event dict (includes event_id). Prefer this over subprocess from
    process_approved_candidates so callers can correlate IDs.
    """
    fork = user_id.strip() or "grace-mar"
    cid = candidate_id.strip() if candidate_id else None
    if cid and cid.lower() == "none":
        cid = None
    et = event_type.lower().strip()
    event: dict = {
        "ts": datetime.now().isoformat(),
        "event": et,
        "candidate_id": cid,
        **(merge or {}),
        **(extras or {}),
    }
    event.setdefault("event_id", new_pipeline_event_id(fork))
    event.setdefault("fork_id", fork)
    event.setdefault("envelope_version", ENVELOPE_VERSION)
    events_path = REPO_ROOT / "users" / user_id / "pipeline-events.jsonl"
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


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
    parser.add_argument(
        "--merge-json",
        metavar="JSON",
        default=None,
        help="JSON object merged into the event (after base fields; extras still override)",
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

    merge: dict = {}
    if args.merge_json:
        try:
            parsed = json.loads(args.merge_json)
        except json.JSONDecodeError as e:
            print(f"Invalid --merge-json: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(parsed, dict):
            print("--merge-json must be a JSON object", file=sys.stderr)
            sys.exit(1)
        merge = parsed
    extras: dict[str, str] = {}
    for arg in args.extras:
        if "=" in arg:
            k, v = arg.split("=", 1)
            extras[k] = v
    append_pipeline_event(args.user, event_type, candidate_id, merge=merge, extras=extras)
    print(f"Emitted {event_type} {candidate_id or '(none)'} for {args.user}")


if __name__ == "__main__":
    main()
