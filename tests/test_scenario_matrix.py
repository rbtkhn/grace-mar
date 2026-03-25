"""Scenario matrix runner — pytest hints and CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from work_dev.run_scenario_matrix import build_run_hints  # noqa: E402


def test_build_run_hints_maps_required_checks_to_tests() -> None:
    rows = [
        {
            "scenario_id": "continuity_failure",
            "runtime": "openclaw",
            "variation": "receipt_state=missing",
            "severity": "high",
            "required_checks": ["continuity_required", "lane_scope"],
        }
    ]

    hints = build_run_hints(rows)
    assert len(hints) == 1
    hint = hints[0]
    assert hint["risk_bucket"] == "tail-risk"
    assert "tests/test_continuity_receipts.py" in hint["pytest_targets"]
    assert "tests/test_handback_requires_continuity.py" in hint["pytest_targets"]
    assert "tests/test_lane_scope.py" in hint["pytest_targets"]
    assert hint["suggested_pytest"].startswith("pytest ")


def test_build_run_hints_falls_back_to_scenario_tests() -> None:
    rows = [
        {
            "scenario_id": "misc_case",
            "runtime": "cursor",
            "variation": "default",
            "severity": "low",
            "required_checks": [],
        }
    ]

    hints = build_run_hints(rows)
    assert len(hints) == 1
    assert hints[0]["risk_bucket"] == "low-risk"
    assert hints[0]["pytest_targets"] == [
        "tests/test_scenario_generation.py",
        "tests/test_scenario_matrix.py",
    ]


def test_run_scenario_matrix_stdout_jsonl() -> None:
    rc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "run_scenario_matrix.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert rc.returncode == 0, rc.stderr
    lines = [ln for ln in rc.stdout.splitlines() if ln.strip()]
    assert lines
    obj = json.loads(lines[0])
    assert "suggested_pytest" in obj
    assert "pytest_targets" in obj
    assert "risk_bucket" in obj
    assert "variation" in obj
