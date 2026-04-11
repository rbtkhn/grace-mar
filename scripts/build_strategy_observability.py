#!/usr/bin/env python3
"""Emit strategy lane observability JSON (WORK-only metrics).

Reads: decision-points/*.md, authorized-sources.yaml, promotion-policy.json
Output: artifacts/work-strategy/strategy-observability.json

Usage:
  python3 scripts/build_strategy_observability.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "artifacts/work-strategy/strategy-observability.json"


def main() -> int:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required", file=sys.stderr)
        return 1

    dp_dir = REPO_ROOT / "docs/skill-work/work-strategy/decision-points"
    decision_files = [p for p in dp_dir.glob("*.md") if p.name != "README.md"]
    open_count = 0
    status_re = re.compile(r"^\*\*Status:\*\*\s*(\S+)", re.MULTILINE)
    for p in decision_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        m = status_re.search(text)
        st = (m.group(1) if m else "").lower().rstrip(".")
        if st == "open":
            open_count += 1

    yaml_path = REPO_ROOT / "docs/skill-work/work-strategy/authorized-sources.yaml"
    src_count = 0
    if yaml_path.is_file():
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        src_count = len(data.get("sources", []))

    policy_path = REPO_ROOT / "docs/skill-work/work-strategy/promotion-policy.json"
    policy_ok = policy_path.is_file()

    doc = {
        "schemaVersion": "1.0.0-work-strategy",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "lane": "work-strategy",
        "metrics": {
            "decision_point_files": len(decision_files),
            "decision_points_open": open_count,
            "authorized_sources_yaml_entries": src_count,
            "promotion_policy_present": policy_ok,
        },
        "notes": [
            "Recommendation acceptance/rejection rates are phase-2 (need operator workflow).",
            "Cross-lane references: manual until automated extract.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
