"""
Dream / self-memory normalization telemetry (docs/memory-self-audit.md § Telemetry note).

`blank_lines_collapsed` can be > 0 while normalized text is byte-identical to input
(`changed` False in maintain_self_memory). Operators must not read that as a failed write.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import auto_dream  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/self_memory_normalize_telemetry_note.md"


def _fixture_date() -> date:
    """Extract the date from the fixture's 'Last rotated:' line."""
    text = FIXTURE.read_text(encoding="utf-8")
    m = re.search(r"^Last rotated:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    assert m, "fixture must contain a 'Last rotated: YYYY-MM-DD' line"
    return date.fromisoformat(m.group(1))


def test_normalize_fixture_round_trip_collapsed_count_telemetry_note():
    """Fixed fixture reproduces Telemetry note pairing (see memory-self-audit.md)."""
    before = FIXTURE.read_text(encoding="utf-8")
    with patch("auto_dream.date") as mock_date:
        mock_date.today.return_value = _fixture_date()
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        after, added, deduped, collapsed = auto_dream.normalize_self_memory_content(before)
    assert after == before, "round-trip must be byte-identical for this fixture"
    assert collapsed == 3
    assert deduped == 0
    assert added == []


def test_maintain_self_memory_exposes_telemetry_fields(tmp_path):
    user_dir = tmp_path / "users" / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self-memory.md").write_text(
        FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    with patch("auto_dream.date") as mock_date:
        mock_date.today.return_value = _fixture_date()
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        r = auto_dream.maintain_self_memory(user_id="demo", users_dir=tmp_path / "users", apply=False)
    assert r.blank_lines_collapsed == 3
    assert r.changed is False
    assert r.deduped_lines == 0


def test_run_auto_dream_summary_self_memory_json_keys(tmp_path):
    user_dir = tmp_path / "users" / "demo"
    user_dir.mkdir(parents=True)
    (user_dir / "self-memory.md").write_text(
        FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (user_dir / "self.md").write_text("# SELF\n\nminimal\n", encoding="utf-8")
    (user_dir / "recursion-gate.md").write_text(
        "# Gate\n\n## Candidates\n\n## Processed\n",
        encoding="utf-8",
    )
    with patch("auto_dream.date") as mock_date:
        mock_date.today.return_value = _fixture_date()
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        summary = auto_dream.run_auto_dream(
            user_id="demo",
            users_dir=tmp_path / "users",
            apply=False,
            emit_event=False,
            write_artifacts=False,
            strict_mode=False,
        )
    mem = summary.get("self_memory") or {}
    assert "changed" in mem
    assert "blank_lines_collapsed" in mem
    assert "would_change" in mem
    assert mem["blank_lines_collapsed"] == 3
    assert mem["changed"] is False
