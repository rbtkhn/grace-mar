"""Tests for grace_mar.runtime.workflow_depth."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grace_mar.runtime.workflow_depth import (  # noqa: E402
    append_workflow_depth_receipt,
    auto_escalation_detected,
    build_workflow_depth_receipt_record,
    decision_from_fixed,
    fixed_depth_to_budget_and_max_obs,
)

if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
import build_workflow_depth_report as _bwd  # noqa: E402

build_report = _bwd.build_report


def test_fixed_depth_mapping() -> None:
    assert fixed_depth_to_budget_and_max_obs("shallow") == ("compact", 30)
    assert fixed_depth_to_budget_and_max_obs("exhaustive") == ("deep", 48)


def test_auto_escalation_detected() -> None:
    assert auto_escalation_detected("low_utilization_escalate", "medium") is True
    assert auto_escalation_detected("sufficient_signal", "compact") is False


def test_build_report_empty() -> None:
    r = build_report([])
    assert r["receiptCount"] == 0
    assert r["partialMetrics"] is True


def test_build_report_one_row() -> None:
    rows = [
        {
            "lane": "lane-a",
            "workflow_depth": "auto",
            "escalated": True,
            "timestamp": "2026-01-01T00:00:00Z",
            "initialDepth": "auto",
            "finalDepth": "medium",
        }
    ]
    r = build_report(rows)
    assert r["receiptCount"] == 1
    assert r["auto"]["total"] == 1
    assert r["auto"]["escalatedApprox"] == 1


def test_append_receipt_minimal(tmp_path: Path) -> None:
    d = decision_from_fixed(
        preset="shallow",
        lane="x",
        task_anchor="t",
        constraint=None,
        source_workflow="test",
    )
    rec = build_workflow_depth_receipt_record(
        schema_version="1.0-workflow-depth-receipt",
        status="ok",
        timestamp="2026-01-01T00:00:00Z",
        boundary_notes=["non_canonical"],
        output_markdown="out.md",
        scores={},
        run_id="r1",
        workflow_depth_label="shallow",
        effective_mode="compact",
        max_observations=30,
        phases=[],
        stop_reason="fixed_shallow",
        task_anchor="t",
        constraint_anchor=None,
        lane="x",
        decision=d,
    )
    p = append_workflow_depth_receipt(tmp_path, rec)
    assert p.is_file()
    line = p.read_text(encoding="utf-8").strip()
    row = json.loads(line)
    assert row["initialDepth"] == "shallow"
    assert row["sourceWorkflow"] == "test"
