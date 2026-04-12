"""analyze_rejection_feedback — gate YAML rejections."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from analyze_rejection_feedback import collect_rejections, run_analysis  # noqa: E402
from rejection_feedback import infer_rejection_category  # noqa: E402


def test_infer_duplicate_routing_error() -> None:
    y = """status: rejected
rejection_reason: duplicate IX-A — Mars already in self
summary: test
"""
    assert infer_rejection_category(y) == "routing_error"


def test_infer_explicit_category() -> None:
    y = """status: rejected
rejection_category: ethics_boundary
rejection_reason: x
"""
    assert infer_rejection_category(y) == "ethics_boundary"


def test_collect_rejections_from_gate_snippet() -> None:
    gate = """
## Candidates

### CANDIDATE-0099 (x)
```yaml
status: rejected
rejection_reason: duplicate lane
summary: Voice test
profile_target: IX-A. KNOWLEDGE
```

## Processed
"""
    rows = collect_rejections(gate)
    assert len(rows) == 1
    assert rows[0]["candidate_id"] == "CANDIDATE-0099"
    assert rows[0]["category"] == "routing_error"


def test_run_analysis_empty() -> None:
    stats = run_analysis([])
    assert stats["total_rejections"] == 0
