#!/usr/bin/env python3
"""Merge work-dev machine artifacts into a summary JSON."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "artifacts/work-dev/work-dev-status-summary.json"


def main() -> int:
    summary: dict = {
        "schemaVersion": "1.0.0-work-dev",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "artifacts": {},
    }
    for name in ("known-gaps.json", "capability-status.json", "proof_ledger.json"):
        p = REPO_ROOT / "artifacts/work-dev" / name
        if p.is_file():
            summary["artifacts"][name] = json.loads(p.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
