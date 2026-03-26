"""CI guard: session continuity proof-of-read script runs and canonical files exist."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "continuity_read_log.py"
REQUIRED_FILES = ("session-log.md", "recursion-gate.md", "self-archive.md")


def test_continuity_read_log_dry_run_grace_mar() -> None:
    """Every push: script exits 0 and reports all continuity files present for grace-mar."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "-u", "grace-mar", "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    payload = json.loads(proc.stdout.strip())
    assert payload.get("user_id") == "grace-mar"
    assert payload.get("purpose") == "openclaw_startup"
    read = set(payload.get("files_read") or [])
    assert set(REQUIRED_FILES) <= read, payload
    assert "missing" not in payload, f"expected all continuity files in repo: {payload}"


@pytest.mark.parametrize("name", REQUIRED_FILES)
def test_grace_mar_continuity_files_committed(name: str) -> None:
    """Guardrail if someone deletes or renames a continuity path."""
    p = REPO_ROOT / "users" / "grace-mar" / name
    assert p.is_file(), f"missing continuity file: {p}"
