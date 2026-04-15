"""Tests for scripts/strategy_thread.py (operator `thread` → expert corpus rebuild)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


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
