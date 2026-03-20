"""
Shared fields for pipeline-events.jsonl and harness-events.jsonl (replay envelope v1).

See docs/harness-replay-spec.md. Append-only; fields are additive for older readers.
"""

from __future__ import annotations

import secrets
from datetime import datetime, timezone

ENVELOPE_VERSION = 1


def new_pipeline_event_id(fork_id: str) -> str:
    """
    Globally unique id for one append-only audit line. fork_id is reserved for future
    namespacing; currently uniqueness is time + random hex.
    """
    _ = fork_id  # reserved
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    return f"evt_{stamp}_{secrets.token_hex(4)}"
