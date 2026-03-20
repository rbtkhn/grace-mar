#!/usr/bin/env python3
"""
Append-only harness audit stream: users/<id>/harness-events.jsonl

Not part of the Record. Used for operator replay (merge, OpenClaw export) without
merging chat context. Complements pipeline-events.jsonl (pipeline-focused).
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

try:
    from pipeline_event_envelope import ENVELOPE_VERSION, new_pipeline_event_id
except ImportError:
    from scripts.pipeline_event_envelope import ENVELOPE_VERSION, new_pipeline_event_id

_lock = threading.Lock()
REPO_ROOT = Path(__file__).resolve().parent.parent


def harness_events_path(user_id: str) -> Path:
    return REPO_ROOT / "users" / user_id / "harness-events.jsonl"


def append_harness_event(
    user_id: str,
    harness_id: str,
    action: str,
    *,
    path: str | None = None,
    candidate_id: str | None = None,
    **kwargs: object,
) -> None:
    """Append one JSON line. Non-fatal on failure."""
    try:
        rec: dict[str, object] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_id": new_pipeline_event_id(user_id),
            "fork_id": user_id,
            "envelope_version": ENVELOPE_VERSION,
            "harness_id": harness_id,
            "action": action,
        }
        if path is not None:
            rec["path"] = path
        if candidate_id is not None:
            rec["candidate_id"] = candidate_id
        for k, v in kwargs.items():
            if v is not None:
                rec[k] = v
        p = harness_events_path(user_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(rec, ensure_ascii=True) + "\n"
        with _lock:
            with open(p, "a", encoding="utf-8") as f:
                f.write(line)
    except Exception:
        pass  # audit only; never block merge/export


def main() -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser(description="Append one harness-events.jsonl line (manual / CI).")
    ap.add_argument("-u", "--user", required=True)
    ap.add_argument("--harness-id", default="manual", help="e.g. cursor, openclaw, operator")
    ap.add_argument("--action", required=True)
    ap.add_argument("--path", default=None)
    ap.add_argument("--candidate-id", default=None)
    args, rest = ap.parse_known_args()
    extras = {}
    for i in range(0, len(rest) - 1, 2):
        if rest[i].startswith("--") and not rest[i + 1].startswith("--"):
            extras[rest[i][2:].replace("-", "_")] = rest[i + 1]
    append_harness_event(
        args.user,
        args.harness_id,
        args.action,
        path=args.path,
        candidate_id=args.candidate_id,
        **extras,
    )
    print(harness_events_path(args.user))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
