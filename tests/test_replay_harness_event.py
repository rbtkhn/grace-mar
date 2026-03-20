"""Smoke tests for harness replay (audit-lane correlation)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from replay_harness_event import _find_candidate_yaml, build_report  # noqa: E402


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


@pytest.mark.skipif(not (ROOT / "users/grace-mar/recursion-gate.md").is_file(), reason="no grace-mar profile")
def test_build_report_grace_mar_known_candidate():
    text = build_report("grace-mar", candidate_id="CANDIDATE-0089")
    assert "CANDIDATE-0089" in text
    assert "pipeline-events.jsonl" in text
    assert "harness-events.jsonl" in text or "merge-receipts" in text
