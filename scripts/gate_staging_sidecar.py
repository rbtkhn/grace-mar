#!/usr/bin/env python3
"""
Optional JSON sidecar per staged candidate for analytics (does not replace recursion-gate.md).

Writes users/<user_id>/gate-staging/<CANDIDATE-id>.json — gitignored by default.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_gate_staging_sidecar(
    repo_root: Path,
    user_id: str,
    *,
    candidate_id: str,
    channel_key: str,
    staging_meta: dict[str, Any] | None,
) -> Path:
    """Write or overwrite sidecar for one candidate. Returns path written."""
    d = repo_root / "users" / user_id / "gate-staging"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{candidate_id}.json"
    payload = {
        "schema": "gate_staging_sidecar/v1",
        "candidate_id": candidate_id,
        "user_id": user_id,
        "channel_key": channel_key,
        "emitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "staging_meta": staging_meta or {},
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
