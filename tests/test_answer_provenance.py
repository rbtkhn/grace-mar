"""Tests for replay synthesis and heuristic answer provenance."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from grace_mar.replay.synthesis import (
    build_replay_events,
    classify_pipeline_row_provenance,
    infer_answer_provenance,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HRE_SCHEMA = REPO_ROOT / "schema-registry" / "harness-replay-event.v1.json"
AP_SCHEMA = REPO_ROOT / "schema-registry" / "answer-provenance.v1.json"


@pytest.fixture
def hre_validator():
    with HRE_SCHEMA.open(encoding="utf-8") as f:
        schema = json.load(f)
    return jsonschema.Draft202012Validator(schema)


@pytest.fixture
def ap_validator():
    with AP_SCHEMA.open(encoding="utf-8") as f:
        schema = json.load(f)
    return jsonschema.Draft202012Validator(schema)


def test_classify_record_backed():
    row = {
        "event": "applied",
        "candidate_id": "CANDIDATE-0001",
        "record_refs": ["users/x/self.md"],
    }
    assert classify_pipeline_row_provenance(row) == "record_backed"


def test_classify_staged_without_refs_is_audit_lane():
    row = {"event": "staged", "candidate_id": "CANDIDATE-0001"}
    assert classify_pipeline_row_provenance(row) == "audit_only"


def test_classify_truly_unresolved():
    row = {"event": "unknown_custom", "candidate_id": "CANDIDATE-0001"}
    assert classify_pipeline_row_provenance(row) == "unresolved"


def test_build_replay_events_validates(tmp_path: Path, hre_validator):
    repo = tmp_path / "repo"
    repo.mkdir()
    uid = tmp_path / "repo" / "users" / "test-user"
    (uid).mkdir(parents=True)
    pe = uid / "pipeline-events.jsonl"
    pe.write_text(
        json.dumps(
            {
                "event": "staged",
                "ts": "2026-03-30T12:00:00",
                "event_id": "evt_test_001",
                "candidate_id": "CANDIDATE-0099",
                "record_refs": ["users/test-user/self.md"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (uid / "self.md").write_text("# Self\n", encoding="utf-8")
    events = build_replay_events(uid, repo, limit=50)
    assert len(events) == 1
    hre_validator.validate(events[0])


def test_infer_answer_provenance_validates(tmp_path: Path, ap_validator):
    repo = tmp_path / "repo"
    repo.mkdir()
    uid = tmp_path / "repo" / "users" / "u2"
    uid.mkdir(parents=True)
    lines = [
        {"event": "applied", "ts": "2026-03-30T10:00:00", "record_refs": ["users/u2/self.md"]},
        {"event": "staged", "ts": "2026-03-30T11:00:00", "candidate_id": "CANDIDATE-1"},
    ]
    (uid / "pipeline-events.jsonl").write_text(
        "\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8"
    )
    (uid / "self.md").touch()
    prov = infer_answer_provenance(uid, repo, session_window_events=10)
    ap_validator.validate(prov)
    assert prov["weights_are_heuristic"] is True
