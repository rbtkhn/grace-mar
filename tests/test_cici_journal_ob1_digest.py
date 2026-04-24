"""Tests for cici_journal_ob1_digest (GitHub fetch mocked)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from unittest.mock import patch
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import cici_journal_ob1_digest as xj  # noqa: E402


def test_next_journal_day_number_from_body(tmp_path: Path) -> None:
    (tmp_path / "2026-04-06.md").write_text("**Journal day:** 4\n", encoding="utf-8")
    (tmp_path / "noise.md").write_text("x", encoding="utf-8")
    assert xj.next_journal_day_number(tmp_path) == 5


def test_next_journal_day_number_legacy_filename(tmp_path: Path) -> None:
    (tmp_path / "2026-04-06-day-01.md").write_text("x", encoding="utf-8")
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
    assert "# Cici notebook — Day 3" in md
    assert "Day overview (auto from commits)" in md
    assert "OB1 repo activity" in md
    assert "Cici" in md
    assert "Focus" not in md


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


def test_load_inbox_single_file(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True)
    (inbox / "2026-04-10.md").write_text("Hello from inbox.\n", encoding="utf-8")
    body, prov, arts = xj.load_inbox_for_day(tmp_path, date(2026, 4, 10), no_inbox=False)
    assert body == "Hello from inbox."
    assert prov == ["inbox/2026-04-10.md"]
    assert arts == []


def test_load_inbox_folder_order(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox" / "2026-04-10"
    inbox.mkdir(parents=True)
    (inbox / "b.md").write_text("second\n", encoding="utf-8")
    (inbox / "a.md").write_text("first\n", encoding="utf-8")
    body, prov, arts = xj.load_inbox_for_day(tmp_path, date(2026, 4, 10), no_inbox=False)
    assert "first" in body and "second" in body
    assert prov[0].endswith("a.md") and prov[1].endswith("b.md")


def test_build_markdown_operator_and_artifacts(tmp_path: Path) -> None:
    readme = tmp_path / "docs" / "x.md"
    readme.parent.mkdir(parents=True)
    readme.write_text("x", encoding="utf-8")
    ctx = xj.DayContext(
        inbox_markdown="Note.",
        inbox_provenance=["inbox/2026-04-10.md"],
        transcript_excerpt=None,
        artifacts=["docs/x.md"],
    )
    md = xj.build_markdown(
        day_label=date(2026, 4, 10),
        journal_day=1,
        tz_name="UTC",
        owner="o",
        repo="r",
        branch="main",
        commits=[xj.CommitLine("a", "msg", "http://u")],
        day_context=ctx,
        repo_root=tmp_path,
    )
    assert "Operator context (ingested)" in md
    assert "### Inbox" in md
    assert "Note." in md
    assert "Artifacts referenced" in md
    assert "docs/x.md" in md
    assert "OB1 repo activity" in md


def test_extract_session_transcript_for_day(tmp_path: Path) -> None:
    st = tmp_path / "st.md"
    st.write_text(
        "**[2026-04-09 12:00:00]** x\n\n"
        "**[2026-04-10 08:00:00]** `USER`\n"
        "> hello\n\n"
        "**[2026-04-11 00:00:00]** y\n",
        encoding="utf-8",
    )
    out = xj.extract_session_transcript_for_day(st, date(2026, 4, 10))
    assert out is not None
    assert "hello" in out
    assert "2026-04-11" not in out


def test_artifact_sidecar(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True)
    (inbox / "2026-04-10-artifacts.txt").write_text(
        "# comment\ndocs/skill-work/work-cici/README.md\n",
        encoding="utf-8",
    )
    body, prov, arts = xj.load_inbox_for_day(tmp_path, date(2026, 4, 10), no_inbox=False)
    assert body is None
    assert "README.md" in arts[0]


def test_extract_strategy_notebook_day_block(tmp_path: Path) -> None:
    ym = "2026-04"
    days = tmp_path / "docs" / "skill-work" / "work-strategy" / "strategy-notebook" / "chapters" / ym
    days.mkdir(parents=True)
    (days / "days.md").write_text(
        "# Month\n\n## 2026-04-09\nold\n\n## 2026-04-10\n### Chronicle\ngeo line\n\n## 2026-04-11\nnext\n",
        encoding="utf-8",
    )
    block, rel = xj.extract_strategy_notebook_day_block(tmp_path, date(2026, 4, 10), max_chars=5000)
    assert block is not None
    assert "2026-04-10" in block
    assert "geo line" in block
    assert "2026-04-11" not in block
    assert "days.md" in (rel or "")


def test_build_markdown_includes_strategy_notebook_section() -> None:
    ctx = xj.DayContext(
        strategy_notebook_excerpt="## 2026-04-10\n\nx",
        strategy_notebook_source="docs/.../days.md",
    )
    md = xj.build_markdown(
        day_label=date(2026, 4, 10),
        journal_day=1,
        tz_name="UTC",
        owner="o",
        repo="r",
        branch="main",
        commits=[],
        day_context=ctx,
    )
    assert "From strategy-notebook (same day)" in md
    assert "x" in md


def test_no_inbox_returns_empty_context(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True)
    (inbox / "2026-04-10.md").write_text("x", encoding="utf-8")
    body, _, _ = xj.load_inbox_for_day(tmp_path, date(2026, 4, 10), no_inbox=True)
    assert body is None
