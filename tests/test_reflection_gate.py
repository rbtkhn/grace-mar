"""Reflection Gates v1: impact_tier-derived labels and validator advisory paths."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = str(REPO_ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)


def test_reflection_gate_label_mapping() -> None:
    from recursion_gate_review import _reflection_gate_label

    assert _reflection_gate_label("") == "none"
    assert _reflection_gate_label("low") == "none"
    assert _reflection_gate_label("medium") == "light"
    assert _reflection_gate_label("high") == "heavy"
    assert _reflection_gate_label("boundary") == "heavy"


def test_validate_gate_heavy_advisory_envelope_class(tmp_path: Path) -> None:
    from validate_gate_comprehension_envelope import validate_gate

    gate = tmp_path / "recursion-gate.md"
    gate.write_text(
        """
## Candidates

### CANDIDATE-1001
```yaml
status: pending
impact_tier: high
envelope_class: none
summary: s
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
suggested_entry: x
```

## Processed
""",
        encoding="utf-8",
    )
    strict, advisory = validate_gate(gate)
    assert not strict
    assert any("Heavy Gate" in line and "envelope_class" in line for line in advisory)


def test_validate_gate_strict_required_missing_envelope(tmp_path: Path) -> None:
    from validate_gate_comprehension_envelope import validate_gate

    gate = tmp_path / "recursion-gate.md"
    gate.write_text(
        """
## Candidates

### CANDIDATE-1002
```yaml
status: pending
envelope_class: required
summary: s
mind_category: knowledge
profile_target: IX-A. KNOWLEDGE
suggested_entry: x
```

## Processed
""",
        encoding="utf-8",
    )
    strict, _adv = validate_gate(gate)
    assert len(strict) == 1
    assert "envelope_class is required" in strict[0]
