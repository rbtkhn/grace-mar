"""Smoke test: integration readiness script exits 0 on a healthy repo checkout."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_integration_readiness.py"


def test_check_integration_readiness_exits_zero():
    rc = subprocess.run(
        [sys.executable, str(SCRIPT), "-u", "grace-mar"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert rc.returncode == 0, rc.stderr + rc.stdout
