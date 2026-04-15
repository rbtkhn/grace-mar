#!/usr/bin/env python3
"""Emit artifacts/skill-write/write-observability.json from write-claims.json.

Surface-aware metrics for operator WRITE capability tracking.

Usage:
  python3 scripts/build_write_observability.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAIMS_PATH = REPO_ROOT / "artifacts/skill-write/write-claims.json"
OUT_PATH = REPO_ROOT / "artifacts/skill-write/write-observability.json"


def main() -> int:
    data = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    claims = data.get("claims", [])
    today = date.today()
    cutoff = today - timedelta(days=30)

    by_type = Counter(c.get("capability_type") for c in claims)
    by_level = Counter(c.get("level") for c in claims)

    recent = 0
    for c in claims:
        lu = c.get("last_updated", "")
        try:
            parts = [int(x) for x in lu.split("-")]
            if date(parts[0], parts[1], parts[2]) >= cutoff:
                recent += 1
        except (ValueError, IndexError):
            pass

    tested = [c for c in claims if c.get("test_type")]
    untested = [c for c in claims if not c.get("test_type")]
    tests_by_type = Counter(c.get("test_type") for c in tested)
    tests_by_surface = Counter(
        c.get("target_surface") for c in claims if c.get("target_surface")
    )
    test_results = Counter(c.get("test_result") for c in tested if c.get("test_result"))
    scaffolding_dist = Counter(
        c.get("scaffolding_level") for c in tested if c.get("scaffolding_level")
    )

    claims_with_samples = sum(1 for c in claims if c.get("sample_ref"))

    surfaces = ["locals", "x", "youtube_comment", "general"]
    surface_coverage: dict[str, float] = {}
    for s in surfaces:
        surface_claims = [c for c in claims if c.get("target_surface") == s]
        tested_surface = [c for c in surface_claims if c.get("test_type")]
        if surface_claims:
            surface_coverage[s] = round(len(tested_surface) / len(surface_claims) * 100, 1)
        else:
            surface_coverage[s] = 0.0

    stale_tested: list[str] = []
    stale_days = 90
    for c in tested:
        td = c.get("test_date", "")
        try:
            parts = [int(x) for x in td.split("-")]
            if (today - date(parts[0], parts[1], parts[2])).days > stale_days:
                stale_tested.append(c.get("id", ""))
        except (ValueError, IndexError):
            pass

    doc = {
        "schemaVersion": "1.0.0-skill-write",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "claim_count": len(claims),
            "claims_by_capability_type": dict(by_type),
            "claims_by_level": dict(by_level),
            "claims_updated_last_30d": recent,
            "claims_with_tests": len(tested),
            "claims_without_tests": len(untested),
            "tests_by_type": dict(tests_by_type),
            "tests_by_surface": dict(tests_by_surface),
            "test_results": dict(test_results),
            "scaffolding_distribution": dict(scaffolding_dist),
            "surface_coverage_pct": surface_coverage,
            "claims_with_samples": claims_with_samples,
            "stale_tested_claim_ids": stale_tested,
        },
        "notes": [
            "Operator WRITE observability — public-copy capability, not companion Record.",
            "Sibling to skill-think observability.",
        ],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
