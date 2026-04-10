"""Tests for xavier_journal_ob1_digest (GitHub fetch mocked)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from unittest.mock import patch
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import xavier_journal_ob1_digest as xj  # noqa: E402


def test_next_journal_day_number(tmp_path: Path) -> None:
    (tmp_path / "2026-04-06-day-01.md").write_text("x", encoding="utf-8")
    (tmp_path / "noise.md").write_text("x", encoding="utf-8")
    assert xj.next_journal_day_number(tmp_path) == 2


def test_build_markdown_includes_commits() -> None:
    commits = [
        xj.CommitLine(sha="abc1234", short_message="Add journal", html_url="https://example/c"),
    ]
    md = xj.build_markdown(
        day_label=date(2026, 4, 10),
        journal_day=3,
        tz_name="UTC",
        owner="Xavier-x01",
        repo="Cici",
        branch="main",
        commits=commits,
    )
    assert "abc1234" in md
    assert "Add journal" in md
    assert "Day 3" in md
    assert "OB1 repo activity" in md
    assert "Cici" in md


def test_fetch_commits_for_day_mocked() -> None:
    payload = [
        {
            "sha": "deadbeef" * 5,
            "html_url": "https://github.com/Xavier-x01/Cici/commit/x",
            "commit": {"message": "Test commit\n\nbody"},
        }
    ]

    def fake_json(url: str, token: str | None) -> list | dict:
        assert "api.github.com" in url
        assert "since=" in url
        assert "until=" in url
        return payload

    with patch.object(xj, "_http_json", side_effect=fake_json):
        out = xj.fetch_commits_for_day(
            "Xavier-x01",
            "Cici",
            "main",
            date(2026, 4, 10),
            "UTC",
            None,
        )
    assert len(out) == 1
    assert out[0].sha == "deadbee"  # first 7 of sha
    assert out[0].short_message == "Test commit"
