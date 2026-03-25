"""Scenario matrix generator determinism."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_generate_scenarios_json_stable_order() -> None:
    p1 = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    p2 = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert p1.stdout == p2.stdout
    data = json.loads(p1.stdout)
    assert data["version"] == 1
    assert len(data["rows"]) >= 5 * 3
