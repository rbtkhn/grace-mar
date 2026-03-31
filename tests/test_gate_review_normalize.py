"""Tests for scripts/gate_review_normalize.normalize_review_item."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from gate_review_normalize import normalize_review_item  # noqa: E402


def _base_row(**kwargs):
    r = {
        "id": "CANDIDATE-0999",
        "status": "pending",
        "summary": "Test summary",
        "proposal_class": "SELF_KNOWLEDGE_ADD",
        "risk_tier": "review_batch",
        "territory_label": "Companion",
        "channel_key": "telegram:1",
        "timestamp": "2026-03-30T12:00:00Z",
        "ready_for_quick_merge": False,
        "signal_type": "",
        "territory": "companion",
        "raw_block": "",
        "duplicate_hints": [],
    }
    r.update(kwargs)
    return r


def test_work_politics_boundary_maps_work_layer():
    row = _base_row(
        territory="work-politics",
        boundary_review={
            "target_surface": "WORK-LAYER",
            "suggested_surface": "WORK-LAYER",
            "misfiled_warning": None,
        },
    )
    n = normalize_review_item(row)
    assert n["target_surface"] == "work_layer"
    assert n["suggested_surface"] == "work_layer"
    assert n["requires_reclassification"] is False
    assert n["review_type"] == "routine"


def test_civ_mem_proposal_boundary():
    row = _base_row(
        proposal_class="CIV_MEM_ADD",
        boundary_review={
            "target_surface": "CIV-MEM",
            "suggested_surface": "CIV-MEM",
            "misfiled_warning": None,
        },
    )
    n = normalize_review_item(row)
    assert n["target_surface"] == "civ_mem"
    assert n["proposal_class"] == "CIV_MEM_ADD"


def test_misfiled_triggers_boundary_review_type():
    row = _base_row(
        boundary_review={
            "target_surface": "SELF-KNOWLEDGE",
            "suggested_surface": "SELF-LIBRARY",
            "misfiled_warning": "Target surface is SELF-KNOWLEDGE but content suggests SELF-LIBRARY.",
        },
    )
    n = normalize_review_item(row)
    assert n["requires_reclassification"] is True
    assert n["review_type"] == "boundary"
    assert n["target_surface"] == "self"
    assert n["suggested_surface"] == "self_library"


def test_quick_merge_risk_maps_low():
    row = _base_row(risk_tier="quick_merge_eligible")
    n = normalize_review_item(row)
    assert n["risk_level"] == "low"
    assert n["materiality"] == "low"


def test_manual_escalate_maps_high():
    row = _base_row(risk_tier="manual_escalate")
    n = normalize_review_item(row)
    assert n["risk_level"] == "high"
    assert n["materiality"] == "high"


def test_evidence_count_from_raw_block():
    row = _base_row(
        raw_block="evidence_id: ACT-0001\nevidence_id: ACT-0002\n",
    )
    n = normalize_review_item(row)
    assert n["evidence_count"] == 2


def test_validate_change_review_demo_subprocess():
    script = REPO_ROOT / "scripts" / "validate-change-review.py"
    demo = REPO_ROOT / "users" / "demo" / "review-queue"
    r = subprocess.run(
        [sys.executable, str(script), str(demo)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def _write_pre_decision_review_queue_fixture(review_dir: Path) -> None:
    """Minimal valid tree: proposals + diffs, empty decisions/."""
    (review_dir / "proposals").mkdir(parents=True, exist_ok=True)
    (review_dir / "decisions").mkdir(exist_ok=True)
    (review_dir / "diffs").mkdir(exist_ok=True)
    (review_dir / "derived").mkdir(exist_ok=True)
    (review_dir / "derived" / "prior.json").write_text("{}", encoding="utf-8")
    (review_dir / "derived" / "proposed.json").write_text("{}", encoding="utf-8")

    proposal = {
        "schemaVersion": "1.0.0",
        "proposalId": "proposal-gap3-test",
        "userSlug": "gap3",
        "createdAt": "2026-03-29T12:00:00Z",
        "primaryScope": "pedagogy",
        "changeType": "refinement",
        "priorStateRef": "derived/prior.json",
        "proposedStateRef": "derived/proposed.json",
        "supportingEvidence": [
            {
                "type": "interaction",
                "ref": "session-gap3-fixture",
                "summary": "Fixture evidence.",
            }
        ],
        "riskLevel": "low",
        "status": "proposed",
        "targetSurface": "self",
        "materiality": "low",
        "reviewType": "routine",
        "queueSummary": "Gap3 fixture queue summary.",
    }
    (review_dir / "proposals" / "proposal-gap3-test.json").write_text(
        json.dumps(proposal, indent=2), encoding="utf-8"
    )

    diff = {
        "schemaVersion": "1.0.0",
        "diffId": "diff-gap3-test",
        "userSlug": "gap3",
        "category": "pedagogy",
        "before": {"snippet": "before"},
        "after": {"snippet": "after"},
        "changeSummary": "Gap3 diff summary.",
        "evidenceRefs": ["session-gap3-fixture"],
    }
    (review_dir / "diffs" / "diff-gap3-test.json").write_text(
        json.dumps(diff, indent=2), encoding="utf-8"
    )

    queue = {
        "schemaVersion": "1.0.0",
        "userSlug": "gap3",
        "queueGeneratedAt": "2026-03-29T12:00:00Z",
        "items": [
            {
                "proposalId": "proposal-gap3-test",
                "status": "proposed",
                "priority": "low",
                "summary": "Gap3 fixture item.",
                "proposalClass": "identity",
                "targetSurface": "self",
                "materiality": "low",
                "reviewType": "routine",
                "riskLevel": "low",
                "requiresReclassification": False,
            }
        ],
    }
    (review_dir / "change_review_queue.json").write_text(
        json.dumps(queue, indent=2), encoding="utf-8"
    )

    event_log = {
        "schemaVersion": "1.0.0",
        "userSlug": "gap3",
        "events": [],
    }
    (review_dir / "change_event_log.json").write_text(
        json.dumps(event_log, indent=2), encoding="utf-8"
    )


def test_validate_change_review_allow_missing_decisions_subprocess(tmp_path):
    script = REPO_ROOT / "scripts" / "validate-change-review.py"
    rq = tmp_path / "review-queue"
    _write_pre_decision_review_queue_fixture(rq)

    strict = subprocess.run(
        [sys.executable, str(script), str(rq)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert strict.returncode == 1, strict.stderr + strict.stdout
    assert "decisions" in strict.stdout

    relaxed = subprocess.run(
        [
            sys.executable,
            str(script),
            str(rq),
            "--allow-missing-decisions",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert relaxed.returncode == 0, relaxed.stderr + relaxed.stdout
