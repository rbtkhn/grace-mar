"""Tests for scripts/log_operator_choice.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import log_operator_choice as loc  # noqa: E402


def test_append_work_choice_creates_block(tmp_path):
    user_dir = tmp_path / "users" / "test-user"
    user_dir.mkdir(parents=True)
    p = loc.append_work_choice(
        user_dir,
        context="WORK",
        picked="A",
        tags="~15m",
        note="gate pass",
    )
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "[WORK-choice]" in text
    assert "context: WORK" in text
    assert "picked: A" in text
    assert "tags: ~15m" in text
    assert "gate pass" in text


def test_append_second_choice_preserves_first(tmp_path):
    user_dir = tmp_path / "users" / "u2"
    user_dir.mkdir(parents=True)
    loc.append_work_choice(user_dir, context="DAILY", picked="1", tags="", note="")
    loc.append_work_choice(user_dir, context="WORK", picked="B", tags="", note="")
    text = (user_dir / "session-transcript.md").read_text(encoding="utf-8")
    assert text.count("### [WORK-choice]") == 2
