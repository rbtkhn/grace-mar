"""Smoke test: performance tier 1 completes without error."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SUITE = REPO_ROOT / "scripts" / "run_perf_suite.py"


@pytest.mark.skipif(not (REPO_ROOT / "users" / "grace-mar" / "recursion-gate.md").exists(), reason="grace-mar fork not present")
def test_perf_tier1_smoke():
    env = {**os.environ, "GRACE_MAR_USER_ID": "grace-mar"}
    r = subprocess.run(
        [
            sys.executable,
            str(SUITE),
            "--tier",
            "1",
            "--warmup",
            "1",
            "--iterations",
            "2",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "1.1_parse_gate" in r.stdout
    assert "1.3_retrieve" in r.stdout
