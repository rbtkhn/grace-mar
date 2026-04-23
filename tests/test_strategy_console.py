"""Smoke tests for scripts/strategy_console.py (WORK only; read-only on notebook)."""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def minimal_notebook(tmp_path: Path) -> Path:
    nb = tmp_path / "strategy-notebook"
    nb.mkdir()
    today = date.today()
    month = f"{today.year:04d}-{today.month:02d}"
    day = today.isoformat()
    (nb / "daily-strategy-inbox.md").write_text(
        f"Accumulator for: {day}\n", encoding="utf-8"
    )
    (nb / "strategy-commentator-threads.md").write_text(
        "| expert_id | Name |\n|---|---|\n| `ztest` | Test expert |\n",
        encoding="utf-8",
    )
    exp = nb / "experts" / "ztest"
    exp.mkdir(parents=True)
    (exp / "thread.md").write_text(
        f"<!-- strategy-page:start id=\"x\" -->\n{day}\n", encoding="utf-8"
    )
    ch = nb / "chapters" / month
    ch.mkdir(parents=True)
    (ch / "days.md").write_text(f"## {day}\n", encoding="utf-8")
    (nb / "forecast-watch-log.md").write_text("log\n", encoding="utf-8")
    (nb / "STATUS.md").write_text("ok\n", encoding="utf-8")
    (nb / "strategy-console").mkdir()
    return nb


def test_strategy_console_writes_console_view(minimal_notebook: Path) -> None:
    script = REPO_ROOT / "scripts" / "strategy_console.py"
    r = subprocess.run(
        [
            sys.executable,
            str(script),
            "--notebook-dir",
            str(minimal_notebook),
            "--no-receipt",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    out = minimal_notebook / "strategy-console" / "console-view.md"
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "# Strategy Console" in text
    assert "## Snapshot" in text
    assert "## What changed" in text
    assert "### Input gaps" in text
    assert "## Expert thread movement" in text
    assert "## Tonight review queue" in text
    assert "`ztest`" in text


def test_strategy_console_missing_roster_lists_gap(tmp_path: Path) -> None:
    nb = tmp_path / "nb"
    nb.mkdir()
    (nb / "daily-strategy-inbox.md").write_text("x\n", encoding="utf-8")
    (nb / "strategy-console").mkdir()
    script = REPO_ROOT / "scripts" / "strategy_console.py"
    r = subprocess.run(
        [
            sys.executable,
            str(script),
            "--notebook-dir",
            str(nb),
            "--no-receipt",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    text = (nb / "strategy-console" / "console-view.md").read_text(encoding="utf-8")
    assert "strategy-commentator-threads" in text
    assert "### Input gaps" in text
