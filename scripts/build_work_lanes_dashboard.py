#!/usr/bin/env python3
"""Aggregate work-layer JSON artifacts into artifacts/work-lanes-dashboard.json.

WORK-only dashboard. Does not read or modify Record files.

**Authority:** This JSON is operator telemetry. RECURSION-GATE merge authority is unchanged;
see schema field recordMergeAuthority.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "artifacts/work-lanes-dashboard.json"


def _read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    doc = {
        "schemaVersion": "1.0.0-work-lanes-dashboard",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "recordMergeAuthority": "RECURSION-GATE and companion approval only — never implied by lane metrics.",
        "lanes": {
            "work_strategy": _read_json(
                REPO_ROOT / "artifacts/work-strategy/strategy-observability.json"
            ),
            "work_dev": _read_json(
                REPO_ROOT / "artifacts/work-dev/work-dev-status-summary.json"
            ),
            "cadence": _read_json(
                REPO_ROOT / "artifacts/work-cadence/cadence-pressure-report.json"
            ),
            "work_dev_dashboard_legacy": _read_json(
                REPO_ROOT / "artifacts/work_dev_dashboard.json"
            ),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
