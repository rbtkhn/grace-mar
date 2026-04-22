"""Tri-mind mind SSOT symlinks / files must exist (regression: missing strategy-expert-*-mind.md)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_verify_strategy_tri_mind_ssot_exits_zero() -> None:
    repo = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, str(repo / "scripts" / "verify_strategy_tri_mind_ssot.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
