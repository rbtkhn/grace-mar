"""Tests for scripts/seed_expert_thread_segments.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "seed_expert_thread_segments.py"


def test_main_requires_dry_run_or_apply() -> None:
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--expert-id",
            "x",
            "--segments",
            "2026-01",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2


def test_inserts_segment_above_marker(tmp_path: Path) -> None:
    t = tmp_path / "strategy-expert-test-expert-thread.md"
    t.write_text(
        "head\n\n<!-- strategy-expert-thread:start -->\nmachine-line\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--thread-path",
            str(t),
            "--expert-id",
            "ignored-when-thread-path-set",
            "--segments",
            "2026-04",
            "--apply",
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    out = t.read_text(encoding="utf-8")
    assert "## 2026-04" in out
    assert "Core stance / through-line" in out
    assert "<!-- strategy-expert-thread:start -->" in out
    assert "machine-line" in out


def test_skips_existing_segment(tmp_path: Path) -> None:
    t = tmp_path / "thread.md"
    t.write_text(
        "## 2026-04\n- existing\n\n<!-- strategy-expert-thread:start -->\nx\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--thread-path",
            str(t),
            "--expert-id",
            "x",
            "--segments",
            "2026-04",
            "--apply",
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    text = t.read_text(encoding="utf-8")
    assert text.count("## 2026-04") == 1
    assert "- existing" in text
