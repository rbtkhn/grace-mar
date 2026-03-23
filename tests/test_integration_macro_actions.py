"""Smoke tests for scripts/integration_macro_actions.py (stateless branch helpers)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "integration_macro_actions.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_branches_smoke():
    r = _run("branches", "--session", "smoke-test", "--slots", "2")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "macro/smoke-test-agent-1" in out
    assert "macro/smoke-test-agent-2" in out
    assert "Merge order" in out


def test_branches_custom_prefix():
    r = _run("branches", "--session", "x", "--slots", "1", "--prefix", "agents")
    assert r.returncode == 0, r.stderr
    assert "agents/x-agent-1" in r.stdout


def test_checklist_smoke():
    r = _run("checklist", "--session", "smoke-test", "--slots", "2")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "## Macro-session:" in out
    assert "macro/smoke-test-agent-1" in out
    assert "process_approved_candidates.py" in out


def test_cli_requires_subcommand():
    r = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode != 0
