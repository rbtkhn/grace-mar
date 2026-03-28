"""Tests for work_jiang warmup_jiang_pulse."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def pulse_mod():
    path = REPO_ROOT / "scripts" / "work_jiang" / "warmup_jiang_pulse.py"
    spec = importlib.util.spec_from_file_location("warmup_jiang_pulse", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_parse_instance_work_context_yaml_v1(pulse_mod):
    md = """x
<!-- work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 -->
```yaml
status: TEST
edge: "hello"
notes: "n1"
```
<!-- /work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 -->
"""
    d = pulse_mod._parse_instance_work_context_yaml(md)
    assert d.get("status") == "TEST"
    assert "hello" in d.get("edge", "")


def test_parse_instance_work_context_yaml_legacy_container(pulse_mod):
    md = """<!-- WORK-JIANG-CONTAINER-START -->
```yaml
status: LEG
edge: "legacy"
```
<!-- WORK-JIANG-CONTAINER-END -->
"""
    d = pulse_mod._parse_instance_work_context_yaml(md)
    assert d.get("status") == "LEG"


def test_first_chapter_next_action(pulse_mod):
    q = """# Q
## ch01 — Title
- **Status:** x
**Next action:** Do the thing
## ch02 — Other
"""
    cid, act = pulse_mod._first_chapter_next_action(q)
    assert cid == "ch01"
    assert "thing" in act


def test_build_morning_contains_sections(pulse_mod):
    lines = pulse_mod.build_morning_pulse_lines("grace-mar")
    text = "\n".join(lines)
    assert "Predictive History — morning momentum" in text
    assert "Spark:" in text or "Instance context" in text
