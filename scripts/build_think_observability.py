#!/usr/bin/env python3
"""Emit artifacts/skill-think/think-observability.json from think-claims.json.

Does NOT merge into schema-registry observability-report.v1 (change-proposal shape).

Usage:
  python3 scripts/build_think_observability.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.observability.metric_contract import WORKFLOW_METRIC_KEY, fill_contract  # noqa: E402
CLAIMS_PATH = REPO_ROOT / "artifacts/skill-think/think-claims.json"
OUT_PATH = REPO_ROOT / "artifacts/skill-think/think-observability.json"


def main() -> int:
    data = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    claims = data.get("claims", [])
    today = date.today()
    cutoff = today - timedelta(days=30)

    by_type = Counter(c.get("capability_type") for c in claims)
    by_level = Counter(c.get("level") for c in claims)
    multi_evidence = sum(1 for c in claims if len(c.get("evidence_refs", [])) > 1)
    promo = sum(1 for c in claims if c.get("promotion_candidate"))

    recent = 0
    for c in claims:
        lu = c.get("last_updated", "")
        try:
            parts = [int(x) for x in lu.split("-")]
            if date(parts[0], parts[1], parts[2]) >= cutoff:
                recent += 1
        except (ValueError, IndexError):
            pass

    topics = Counter(c.get("topic") for c in claims)
    top_topics = [t for t, _ in topics.most_common(5)]

    tested = [c for c in claims if c.get("test_type")]
    untested = [c for c in claims if not c.get("test_type")]
    tests_by_type = Counter(c.get("test_type") for c in tested)
    test_results = Counter(c.get("test_result") for c in tested if c.get("test_result"))
    scaffolding_dist = Counter(
        c.get("scaffolding_level") for c in tested if c.get("scaffolding_level")
    )

    transferable_claims = [c for c in claims if c.get("level") == "transferable"]
    transferable_with_test = sum(
        1 for c in transferable_claims if c.get("test_type") == "transfer"
    )
    transfer_pct = (
        round(transferable_with_test / len(transferable_claims) * 100, 1)
        if transferable_claims
        else 0.0
    )

    consistent_plus = [
        c for c in claims if c.get("level") in ("consistent", "transferable", "independent")
    ]
    fm_covered = sum(1 for c in consistent_plus if c.get("failure_mode_notes"))
    fm_pct = (
        round(fm_covered / len(consistent_plus) * 100, 1)
        if consistent_plus
        else 0.0
    )

    doc = {
        "schemaVersion": "1.1.0-skill-think",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "claim_count": len(claims),
            "claims_by_capability_type": dict(by_type),
            "claims_by_level": dict(by_level),
            "claims_updated_last_30d": recent,
            "claims_with_multiple_evidence_refs": multi_evidence,
            "open_promotion_candidates": promo,
            "top_topics": top_topics,
            "claims_with_tests": len(tested),
            "claims_without_tests": len(untested),
            "tests_by_type": dict(tests_by_type),
            "test_results": dict(test_results),
            "scaffolding_distribution": dict(scaffolding_dist),
            "transfer_test_coverage_pct": transfer_pct,
            "failure_mode_coverage_pct": fm_pct,
        },
        "notes": [
            "Test-coverage metrics added in v1.1.0 (exercise layer).",
            "Sibling to work-strategy observability — not merged into observability-report.v1.",
        ],
        "lane": "skill-think",
    }
    doc[WORKFLOW_METRIC_KEY] = fill_contract(
        "skill-think",
        workflow_count=len(claims),
        revision_count=promo,
        partial=True,
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
