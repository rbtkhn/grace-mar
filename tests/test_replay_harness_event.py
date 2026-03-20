"""Smoke tests for harness replay (audit-lane correlation)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from replay_harness_event import (  # noqa: E402
    _find_candidate_yaml,
    _harness_rows_for_event_id,
    build_report,
)


def test_find_candidate_yaml_sample_gate():
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
    assert _find_candidate_yaml(md, "CANDIDATE-0001") == "status: pending\nfoo: bar"
    assert _find_candidate_yaml(md, "candIdate-0002") == "status: approved\nx: 1"


def test_harness_rows_for_event_id_lists():
    hv = [
        {"ts": "a", "event_id": "evt_self"},
        {"ts": "b", "applied_pipeline_event_ids": ["evt_x", "evt_y"]},
        {"ts": "c", "staged_parent_event_ids": ["evt_z"]},
    ]
    assert len(_harness_rows_for_event_id(hv, "evt_x")) == 1
    assert len(_harness_rows_for_event_id(hv, "evt_self")) == 1
    assert len(_harness_rows_for_event_id(hv, "evt_z")) == 1
    assert _harness_rows_for_event_id(hv, "missing") == []


def test_build_report_unknown_event_id():
    text = build_report("grace-mar", event_id="evt_does_not_exist_00000000_deadbeef")
    assert "No pipeline row" in text or "no pipeline row" in text.lower()


@pytest.mark.skipif(not (ROOT / "users/grace-mar/recursion-gate.md").is_file(), reason="no grace-mar profile")
def test_build_report_grace_mar_known_candidate():
    text = build_report("grace-mar", candidate_id="CANDIDATE-0089")
    assert "CANDIDATE-0089" in text
    assert "pipeline-events.jsonl" in text
    assert "harness-events.jsonl" in text or "merge-receipts" in text
