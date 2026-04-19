"""Tests for scripts/strategy_thread.py (operator `thread` → expert corpus rebuild)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_bin_thread_help_matches_python_entrypoint() -> None:
    """bin/thread forwards argv to scripts/strategy_thread.py."""
    wrapper = REPO / "bin" / "thread"
    proc = subprocess.run(
        [str(wrapper), "--help"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "--dry-run" in proc.stdout


def test_strategy_thread_help_delegates_to_corpus_script() -> None:
    script = REPO / "scripts" / "strategy_thread.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "strategy_expert_corpus.py" in proc.stdout
    assert "--dry-run" in proc.stdout


def test_strategy_thread_dry_run_exits_zero() -> None:
    """Wrapper forwards argv; dry-run lists targets without writing."""
    script = REPO / "scripts" / "strategy_thread.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--dry-run"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "experts/" in proc.stdout
    assert "Done (dry-run):" in proc.stdout
