"""Shared recursion-gate.md candidate block parsing."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def gbp():
    import sys

    s = str(REPO_ROOT / "scripts")
    if s not in sys.path:
        sys.path.insert(0, s)
    import gate_block_parser as mod

    return mod


def test_mean_pending_provenance_two_blocks(gbp) -> None:
    md = """## Candidates

### CANDIDATE-1
```yaml
status: pending
candidate_source: openclaw
artifact_path: a
artifact_sha256: x
continuity_receipt_path: r.json
constitution_check_status: ok
```

### CANDIDATE-2
```yaml
status: pending
candidate_source: x
```

## Processed
"""
    score = gbp.mean_pending_provenance_score(md)
    assert score is not None
    assert abs(score - 0.6) < 1e-6


def test_iter_candidate_yaml_in_active_section(gbp) -> None:
    md = """## Candidates
### CANDIDATE-9
```yaml
status: pending
summary: hi
```
## Processed
## More
"""
    active, tail = gbp.split_gate_sections(md)
    assert "## Processed" not in tail or tail.strip() == ""
    ids = [c for c, _, _ in gbp.iter_candidate_yaml_blocks(active)]
    assert ids == ["CANDIDATE-9"]


def test_pending_region_excludes_processed_candidates(gbp) -> None:
    """Block after ## Processed must not count as pending for provenance."""
    md = """## Candidates

## Processed
### CANDIDATE-99
```yaml
status: pending
```
"""
    assert gbp.mean_pending_provenance_score(md) is None
