#!/usr/bin/env python3
"""
One-time / dev seed for work-politics SQLite engine (Massie KY-4 lane).

Creates client + engagement + funnel row under users/<id>/work-politics/work-politics.db.
compliance_status cleared is an operator assertion, not legal sign-off.

Usage:
    python scripts/bootstrap_work_politics.py
"""

from __future__ import annotations

import os
import sys

_SCRIPTS = __file__.rsplit("/", 1)[0]
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from work_politics_engine import WorkPoliticsEngine  # noqa: E402

USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
OPERATOR = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-bootstrap")


def main() -> int:
    engine = WorkPoliticsEngine(user_id=USER_ID)
    engine.init_db()

    client_id = engine.create_or_update_client(
        client_slug="massie-ky4",
        display_name="Thomas Massie (KY-4)",
        channel_key="operator:wap:us-ky4-massie",
        principal_type="candidate",
        compliance_status="cleared",
        reviewed_by=OPERATOR,
        notes={
            "phase": "phase-1-primary",
            "scope": ["briefs", "opposition", "message-discipline", "calendar", "x-copy"],
        },
    )

    engagement_id, decision = engine.submit_engagement(
        client_id=client_id,
        title="Weekly district brief",
        work_type="brief",
        created_by=OPERATOR,
        public_attribution=False,
        record_touch=True,
        metadata={"artifact": "weekly-district-brief.md"},
    )

    engine.log_funnel_event(
        client_id=client_id,
        engagement_id=engagement_id,
        stage="brief_created",
        outcome="queued_for_review",
        source="bootstrap",
        notes={"policy_reason": decision.reason},
    )

    print(
        {
            "client_id": client_id,
            "engagement_id": engagement_id,
            "requires_review": decision.requires_review,
            "db": str(engine.db_path),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
