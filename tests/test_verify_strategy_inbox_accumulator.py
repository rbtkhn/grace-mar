"""Tests for scripts/verify_strategy_inbox_accumulator.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "verify_strategy_inbox_accumulator.py"
PY = sys.executable


def test_verify_script_ok_when_dates_match(tmp_path):
    inbox = tmp_path / "daily-strategy-inbox.md"
    inbox.write_text(
        "**Accumulator for:** 2030-06-15 _(note)_\n\n_(Append below)_\n",
        encoding="utf-8",
    )
    r = subprocess.run(
        [PY, str(SCRIPT), "--inbox", str(inbox), "--date", "2030-06-15"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr


def test_verify_script_fails_on_mismatch(tmp_path):
    inbox = tmp_path / "daily-strategy-inbox.md"
    inbox.write_text("**Accumulator for:** 2030-01-01\n", encoding="utf-8")
    r = subprocess.run(
        [PY, str(SCRIPT), "--inbox", str(inbox), "--date", "2030-01-02"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1


def test_verify_script_fails_without_accumulator_line(tmp_path):
    inbox = tmp_path / "x.md"
    inbox.write_text("# no accumulator\n", encoding="utf-8")
    r = subprocess.run(
        [PY, str(SCRIPT), "--inbox", str(inbox), "--date", "2030-01-01"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
