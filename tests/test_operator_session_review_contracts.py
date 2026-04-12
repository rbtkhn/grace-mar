"""
Contract tests: operator session-review mitigations stay documented in-repo.

Maps to docs/skill-work/work-coffee/operator-session-review-checklist.md and
session-review verification design (coffee / harness / lanes / memory audit).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def _read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def test_coffee_skill_step1_and_compass_and_exit_rule():
    md = _read(".cursor/skills/coffee/SKILL.md")
    assert "Step 1" in md
    assert "operator_coffee.py" in md
    assert "C. Strategy (daily brief)" in md or "**C. Strategy (daily brief)**" in md
    assert "stay in coffee" in md.lower()
    assert "exit to normal workflow" in md.lower()


def test_menu_reference_bare_compass_vs_full_coffee():
    md = _read("docs/skill-work/work-coffee/menu-reference.md")
    assert "### Bare **`compass`** vs **`coffee`** then **`C`**" in md
    assert "Bare `compass`" in md
    assert "operator_coffee.py --mode reentry" in md


def test_operator_agent_lanes_plan_default_and_execute():
    md = _read("docs/operator-agent-lanes.md")
    assert "### `PLAN`" in md
    assert "### `EXECUTE`" in md
    assert "### `DOCSYNC`" in md
    assert "default" in md.lower() and "PLAN" in md
    assert "implement" in md.lower()
    assert "push" in md.lower()


def test_harness_warmup_rule_coffee_overlap_and_skip_when_warmup_pasted():
    md = _read(".cursor/rules/harness-warmup.mdc")
    assert "harness_warmup.py" in md
    assert "coffee" in md.lower()
    assert "Warmup was already pasted" in md or "already pasted in this thread" in md


def test_operator_coffee_invokes_harness_warmup():
    src = _read("scripts/operator_coffee.py")
    assert "harness_warmup.py" in src


def test_memory_self_audit_telemetry_note():
    md = _read("docs/memory-self-audit.md")
    assert "### Telemetry note (dream / normalize)" in md
    assert "blank_lines_collapsed" in md
    assert "changed" in md


def test_date_time_conventions_iso_utc():
    md = _read("docs/date-time-conventions.md")
    assert "YYYY-MM-DD" in md
    assert "UTC" in md
    assert "operator_clock.py" in md


def test_grace_mar_recursion_gate_parseable():
    gate = REPO / "users/grace-mar/recursion-gate.md"
    if not gate.is_file():
        pytest.skip("grace-mar recursion-gate absent")
    text = gate.read_text(encoding="utf-8")
    assert "## Candidates" in text or "# " in text
    assert len(text) > 50
