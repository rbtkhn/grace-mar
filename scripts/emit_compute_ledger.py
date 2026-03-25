#!/usr/bin/env python3
"""
Append one integration/export row to users/<id>/compute-ledger.jsonl.

Extends the Voice ledger shape with optional integration fields (operation, runtime, wall_ms, …).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def append_integration_ledger(
    user_id: str,
    *,
    operation: str,
    runtime: str,
    success: bool,
    wall_ms: int | None = None,
    bytes_processed: int = 0,
    source_artifact_count: int = 0,
    repo_root: Path | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    root = repo_root or REPO_ROOT
    path = root / "users" / user_id / "compute-ledger.jsonl"
    channel_key = os.getenv("GRACE_MAR_LEDGER_CHANNEL_KEY", f"{runtime}:integration")
    rec: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "channel_key": channel_key,
        "bucket": "integration",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "model": "",
        "operation": operation,
        "runtime": runtime,
        "success": success,
        "wall_ms": wall_ms,
        "bytes_processed": bytes_processed,
        "source_artifact_count": source_artifact_count,
    }
    if extra:
        rec.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(description="Emit one integration compute-ledger line (manual test).")
    p.add_argument("-u", "--user", default="grace-mar")
    p.add_argument("--operation", default="test")
    p.add_argument("--runtime", default="cli")
    p.add_argument("--success", action="store_true", default=True)
    args = p.parse_args()
    append_integration_ledger(
        args.user,
        operation=args.operation,
        runtime=args.runtime,
        success=args.success,
        wall_ms=0,
    )
    print("emit_compute_ledger: appended")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
