"""Tests for coffee_lane_next_hints (work-xavier + work-dev one-liners)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.coffee_lane_next_hints import (
    format_lane_next_hints,
    next_work_dev_line,
    next_work_xavier_line,
)


def test_next_work_dev_finds_first_open_item(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text(
        """# workspace

## Next actions

1. ~~done item~~
2. Ship the widget
3. Another thing
""",
        encoding="utf-8",
    )
    line = next_work_dev_line(tmp_path)
    assert "Ship the widget" in line
    assert "#2" in line or "(#2)" in line


def test_next_work_dev_all_struck(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text(
        """## Next actions

1. ~~only struck~~
""",
        encoding="utf-8",
    )
    line = next_work_dev_line(tmp_path)
    assert "no open item" in line


def test_next_work_xavier_prefers_sync_daily_top_task(tmp_path: Path) -> None:
    xdir = tmp_path / "docs/skill-work/work-xavier"
    xdir.mkdir(parents=True)
    (xdir / "SYNC-DAILY.md").write_text(
        """### 3) Combined next action
- top sync task: Run mirror scan today
- owner:
""",
        encoding="utf-8",
    )
    (xdir / "WORK-LEDGER.md").write_text("## II-A. ACTIVE WATCHES\n\n- **Watch:** fallback\n", encoding="utf-8")
    line = next_work_xavier_line(tmp_path)
    assert "mirror scan" in line.lower()


def test_format_lane_next_hints_two_lines(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text("## Next actions\n\n1. Alpha\n", encoding="utf-8")
    xdir = tmp_path / "docs/skill-work/work-xavier"
    xdir.mkdir(parents=True)
    (xdir / "SYNC-DAILY.md").write_text(
        "### 3) Combined next action\n- top sync task: Beta\n", encoding="utf-8"
    )
    out = format_lane_next_hints(tmp_path)
    lines = out.strip().splitlines()
    assert len(lines) == 2
    assert "Beta" in lines[0]
    assert "Alpha" in lines[1]


def test_assess_session_load_includes_menu_weights() -> None:
    from scripts.assess_session_load import assess_load

    r = assess_load("grace-mar")
    ow = r.get("option_weights") or {}
    assert set(ow.keys()) == {"A", "B", "C", "D1", "D2", "E"}
    assert r.get("recommended") in ("A", "B", "C")
