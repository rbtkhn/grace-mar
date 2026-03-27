"""Tests for backfill_session_log_from_pipeline_events.py."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def script_module():
    import importlib.util

    path = REPO_ROOT / "scripts" / "backfill_session_log_from_pipeline_events.py"
    spec = importlib.util.spec_from_file_location("backfill_session_log", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_dedupe_applied_keeps_earliest_per_candidate(script_module):
    events = [
        {"event": "applied", "ts": "2026-03-20T08:07:12.551688", "candidate_id": "CANDIDATE-0088"},
        {"event": "applied", "ts": "2026-03-20T08:06:49.142480", "candidate_id": "CANDIDATE-0088"},
    ]
    by = script_module._dedupe_applied_by_candidate(events)
    assert len(by) == 1
    assert by["CANDIDATE-0088"]["ts"] == "2026-03-20T08:06:49.142480"


def test_existing_merge_candidate_ids(script_module):
    text = """
## Pipeline merge (automated)

- 2026-03-16 21:53:08 | pipeline merge | CANDIDATE-0086 | approved by operator

## Something else
"""
    assert script_module._existing_merge_candidate_ids(text) == {"CANDIDATE-0086"}


def test_run_apply_inserts_section_before_footer(tmp_path, script_module):
    user = "test-fork"
    root = tmp_path / "users" / user
    root.mkdir(parents=True)
    session = root / "session-log.md"
    session.write_text(
        "# Log\n\n### SESSION 001\n\nok\n\n---\n\nEND OF FILE — test\n",
        encoding="utf-8",
    )
    pipe = root / "pipeline-events.jsonl"
    pipe.write_text(
        json.dumps(
            {
                "event": "applied",
                "ts": "2026-01-02T12:00:00",
                "candidate_id": "CANDIDATE-0001",
                "actor": "operator",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    # Patch profile_dir for this test
    orig_pd = script_module.profile_dir

    def _pd(uid: str):
        if uid == user:
            return root
        return orig_pd(uid)

    script_module.profile_dir = _pd

    try:
        rc = script_module.run(user, apply=True, events_path=pipe)
        assert rc == 0
    finally:
        script_module.profile_dir = orig_pd

    out = session.read_text(encoding="utf-8")
    assert "## Pipeline merge (automated)" in out
    assert "CANDIDATE-0001" in out
    assert out.index("Pipeline merge") < out.index("END OF FILE")
    assert "- 2026-01-02 12:00:00 | pipeline merge | CANDIDATE-0001 | approved by operator" in out


def test_run_skips_when_already_logged(tmp_path, script_module):
    user = "test-fork2"
    root = tmp_path / "users" / user
    root.mkdir(parents=True)
    session = root / "session-log.md"
    session.write_text(
        "## Pipeline merge (automated)\n\n"
        "- 2026-01-02 12:00:00 | pipeline merge | CANDIDATE-0001 | approved by operator\n",
        encoding="utf-8",
    )
    pipe = root / "pipeline-events.jsonl"
    pipe.write_text(
        json.dumps(
            {
                "event": "applied",
                "ts": "2026-01-02T12:00:00",
                "candidate_id": "CANDIDATE-0001",
                "actor": "operator",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    orig_pd = script_module.profile_dir

    def _pd(uid: str):
        if uid == user:
            return root
        return orig_pd(uid)

    script_module.profile_dir = _pd
    try:
        rc = script_module.run(user, apply=True, events_path=pipe)
        assert rc == 0
    finally:
        script_module.profile_dir = orig_pd

    assert session.read_text(encoding="utf-8").count("CANDIDATE-0001") == 1
