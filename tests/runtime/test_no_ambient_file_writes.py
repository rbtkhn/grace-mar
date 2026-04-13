"""Regression: runtime logger must not write outside the observations tree."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "runtime" / "log_observation.py"


def test_log_observation_never_writes_claude_md(tmp_path: Path) -> None:
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--lane",
            "x",
            "--source-kind",
            "manual_note",
            "--title",
            "T",
            "--summary",
            "S",
        ],
        cwd=str(tmp_path),
        check=True,
        env=env,
    )
    claude = tmp_path / "CLAUDE.md"
    assert not claude.exists()
    nested = tmp_path / "src" / "foo"
    nested.mkdir(parents=True)
    assert not (nested / "CLAUDE.md").exists()
