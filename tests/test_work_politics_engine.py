"""Tests for scripts/work_politics_engine.py (isolated repo_root)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from work_politics_engine import (  # noqa: E402
    PolicyViolation,
    WorkPoliticsEngine,
    validate_channel_key,
)


@pytest.fixture
def engine(tmp_path: Path) -> WorkPoliticsEngine:
    repo = tmp_path / "repo"
    repo.mkdir()
    e = WorkPoliticsEngine(user_id="test-user", repo_root=repo)
    e.init_db()
    return e


def test_validate_channel_key_massie():
    assert validate_channel_key("operator:wap:us-ky4-massie")


def test_validate_channel_key_artifact_slug():
    assert validate_channel_key("operator:wap:iran-brief")


def test_validate_channel_key_rejects_garbage():
    assert not validate_channel_key("telegram:123")


def test_funnel_metrics_empty(engine: WorkPoliticsEngine):
    m = engine.funnel_metrics(days=30)
    assert m["total_revenue_usd"] == 0.0
    assert m["stages"] == {}


def test_client_engagement_review_and_funnel(engine: WorkPoliticsEngine):
    cid = engine.create_or_update_client(
        client_slug="massie-ky4",
        display_name="Test",
        channel_key="operator:wap:us-ky4-massie",
        principal_type="candidate",
        compliance_status="cleared",
        reviewed_by="test",
        notes={},
    )
    eid, decision = engine.submit_engagement(
        client_id=cid,
        title="Brief",
        work_type="brief",
        created_by="test",
        record_touch=True,
    )
    assert decision.requires_review
    pending = engine.list_review_queue(status="pending")
    assert len(pending) == 1

    engine.log_funnel_event(
        stage="test_stage",
        outcome="ok",
        client_id=cid,
        engagement_id=eid,
        amount_usd=10.0,
    )
    m = engine.funnel_metrics(days=30)
    assert m["total_revenue_usd"] == 10.0
    assert "test_stage" in m["stages"]


def test_engagement_blocked_without_compliance(engine: WorkPoliticsEngine):
    cid = engine.create_or_update_client(
        client_slug="x",
        display_name="X",
        channel_key="operator:wap:us-ky4-massie",
        principal_type="candidate",
        compliance_status="pending",
        notes={},
    )
    with pytest.raises(PolicyViolation):
        engine.submit_engagement(
            client_id=cid,
            title="T",
            work_type="w",
            created_by="test",
        )
