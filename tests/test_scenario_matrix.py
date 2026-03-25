"""Scenario matrix runner emits JSONL."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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
    json.loads(lines[0])
