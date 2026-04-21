"""Workflow observability aggregate and event helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grace_mar.observability.workflow_aggregate import aggregate_events, median_or_none  # noqa: E402
from grace_mar.observability.workflow_events import (  # noqa: E402
    event_from_change_proposal,
    event_from_observability_report_aggregate,
)


def test_median_or_none_empty() -> None:
    assert median_or_none([]) is None


def test_median_or_none_values() -> None:
    assert median_or_none([1.0, 2.0, 3.0]) == 2.0


def test_aggregate_events_counts_by_workflow_type() -> None:
    ev = [
        event_from_change_proposal(
            {
                "proposalId": "p1",
                "status": "proposed",
                "createdAt": "2026-01-01T00:00:00Z",
                "changeType": "x",
                "targetSurface": "SELF",
                "supportingEvidence": [],
            },
            source_path="users/demo/review-queue/proposals/p1.json",
            batch_id="t1",
        ),
        event_from_observability_report_aggregate(
            {
                "generatedAt": "2026-01-02T00:00:00Z",
                "reviewRoot": "users/demo/review-queue",
                "staleReviewCount": 0,
            },
            source_path="users/demo/observability/observability-report.json",
            batch_id="t1",
        ),
    ]
    r = aggregate_events(ev, batch_id="t1", sources_used=["test"])
    assert r["eventCount"] == 2
    assert r["totalsByWorkflowType"]["change_proposal"] == 1
    assert r["totalsByWorkflowType"]["change_proposal_aggregate"] == 1
    assert r["batchId"] == "t1"


def test_aggregate_validates_report_schema_when_jsonschema() -> None:
    pytest.importorskip("jsonschema")
    import jsonschema  # type: ignore

    schema_path = REPO_ROOT / "schema-registry" / "workflow-observability-report.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    ev = [
        event_from_change_proposal(
            {
                "proposalId": "p2",
                "status": "approved",
                "createdAt": "2026-01-01T00:00:00Z",
                "changeType": "x",
                "targetSurface": "SELF",
                "supportingEvidence": [],
            },
            source_path="x.json",
            batch_id="b",
        )
    ]
    r = aggregate_events(ev, batch_id="b", sources_used=["x"])
    jsonschema.validate(instance=r, schema=schema)
