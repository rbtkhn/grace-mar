"""Tests for operator_handoff_check gate section."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def handoff_mod():
    path = REPO_ROOT / "scripts" / "operator_handoff_check.py"
    spec = importlib.util.spec_from_file_location("operator_handoff_check", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_gate_detail_lines_empty_queue(handoff_mod):
    text = "## Candidates\n\n## Processed\n"
    lines = handoff_mod._gate_detail_lines(text, "grace-mar")
    joined = "\n".join(lines)
    assert "**Total pending:** 0" in joined
    assert "process_approved_candidates.py" in joined
    assert "operator_gate_review_pass.py" in joined


def test_gate_detail_lists_pending_wap_and_companion(handoff_mod):
    gate = """## Candidates

### CANDIDATE-0998 (wap)

```yaml
status: pending
summary: WAP item one
territory: work-politics
```

### CANDIDATE-0999 (companion)

```yaml
status: pending
summary: Companion item two
channel_key: telegram:1
```

## Processed
"""
    lines = handoff_mod._gate_detail_lines(gate, "test-user")
    joined = "\n".join(lines)
    assert "**Total pending:** 2 (work-politics: 1 · companion: 1)" in joined
    assert "CANDIDATE-0998" in joined and "Work-politics" in joined
    assert "CANDIDATE-0999" in joined and "Companion" in joined
    assert "complete processing" in joined
    assert "users/test-user/recursion-gate.md" in joined
