"""Smoke tests for work-layer hardening scripts (validators + builders)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / name), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_validate_strategy_decision_points_ok() -> None:
    cp = _run_script("validate_strategy_decision_points.py")
    assert cp.returncode == 0, cp.stderr


def test_validate_work_strategy_sources() -> None:
    pytest.importorskip("yaml")
    cp = _run_script("validate_work_strategy_sources.py")
    assert cp.returncode == 0, cp.stderr


def test_validate_work_dev_gaps() -> None:
    pytest.importorskip("jsonschema")
    cp = _run_script("validate_work_dev_gaps.py")
    assert cp.returncode == 0, cp.stderr


def test_validate_work_lane_contracts() -> None:
    cp = _run_script("validate_work_lane_contracts.py")
    assert cp.returncode == 0, cp.stderr


def test_work_lanes_dashboard_shape() -> None:
    cp = _run_script("build_work_lanes_dashboard.py")
    assert cp.returncode == 0, cp.stderr
    path = REPO_ROOT / "artifacts/work-lanes-dashboard.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get("schemaVersion")
    assert "recordMergeAuthority" in data
    assert "lanes" in data
