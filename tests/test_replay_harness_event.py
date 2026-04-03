"""Smoke tests for harness replay (audit-lane correlation)."""

from __future__ import annotations

from pathlib import Path

import pytest

from grace_mar.replay.correlate import find_candidate_yaml, harness_rows_for_event_id
from grace_mar.replay.report import build_report

ROOT = Path(__file__).resolve().parent.parent


def test_find_candidate_yaml_sample_gate() -> None:
    md = """
## Candidates
### CANDIDATE-0001 (test)
```yaml
status: pending
foo: bar
```

## Processed

### CANDIDATE-0002 (done)
```yaml
status: approved
x: 1
```
"""
    assert find_candidate_yaml(md, "CANDIDATE-0001") == "status: pending\nfoo: bar"
    assert find_candidate_yaml(md, "candIdate-0002") == "status: approved\nx: 1"


def test_harness_rows_for_event_id_lists() -> None:
    hv = [
        {"ts": "a", "event_id": "evt_self"},
        {"ts": "b", "applied_pipeline_event_ids": ["evt_x", "evt_y"]},
        {"ts": "c", "staged_parent_event_ids": ["evt_z"]},
    ]
    assert len(harness_rows_for_event_id(hv, "evt_x")) == 1
    assert len(harness_rows_for_event_id(hv, "evt_self")) == 1
    assert len(harness_rows_for_event_id(hv, "evt_z")) == 1
    assert harness_rows_for_event_id(hv, "missing") == []


def test_build_report_unknown_event_id() -> None:
    text = build_report(
        ROOT / "users" / "grace-mar",
        event_id="evt_does_not_exist_00000000_deadbeef",
    )
    assert "No pipeline row" in text or "no pipeline row" in text.lower()


@pytest.mark.skipif(not (ROOT / "users/grace-mar/recursion-gate.md").is_file(), reason="no grace-mar profile")
def test_build_report_grace_mar_known_candidate() -> None:
    text = build_report(ROOT / "users" / "grace-mar", candidate_id="CANDIDATE-0089")
    assert "CANDIDATE-0089" in text
    assert "pipeline-events.jsonl" in text
    assert "harness-events.jsonl" in text or "merge-receipts" in text
