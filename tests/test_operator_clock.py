"""scripts/operator_clock.py — single-line UTC output."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_operator_clock_full_iso_utc():
    out = subprocess.run(
        [sys.executable, str(REPO / "scripts/operator_clock.py")],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert len(out) == 20  # YYYY-MM-DDTHH:MM:SSZ
    assert out.endswith("Z")
    parsed = datetime.strptime(out, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    assert abs((datetime.now(timezone.utc) - parsed).total_seconds()) < 120


def test_operator_clock_date_only():
    out = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts/operator_clock.py"),
            "--date-only",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert len(out) == 10
    assert out == datetime.now(timezone.utc).strftime("%Y-%m-%d")
