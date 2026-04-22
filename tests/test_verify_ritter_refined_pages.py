"""Ritter refined pages: manifest primaries must have files + transcript backlinks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_verify_ritter_refined_pages_exits_zero() -> None:
    repo = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, str(repo / "scripts" / "strategy" / "verify_ritter_refined_pages.py")],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
