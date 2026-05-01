"""Offline tests for scripts/backfill_x_profile_raw_input.py."""

from __future__ import annotations

import shutil
from datetime import date, datetime
from pathlib import Path

from scripts.backfill_x_profile_raw_input import (
    _build_doc,
    _extract_status_text,
    _extract_status_urls,
    _profile_handle,
    _extract_status_datetime,
    run,
)


def test_profile_handle_infers_last_path_segment() -> None:
    assert _profile_handle("https://x.com/RealScottRitter") == "RealScottRitter"
    assert _profile_handle("https://x.com/@RealScottRitter") == "RealScottRitter"


def test_extract_status_urls_from_profile_html() -> None:
    html = """
    <a href="/RealScottRitter/status/2044552836260999446">one</a>
    <a href="https://x.com/RealScottRitter/status/2044502233849475530">two</a>
    <a href="/RealScottRitter/status/2044552836260999446">dup</a>
    """
    urls = _extract_status_urls(html, "RealScottRitter")
    assert urls == [
        "https://x.com/RealScottRitter/status/2044552836260999446",
        "https://x.com/RealScottRitter/status/2044502233849475530",
    ]


def test_extract_status_text_prefers_tweet_text_block() -> None:
    html = """
    <div data-testid="tweetText"><span>Hello</span><br/>world</div>
    <meta property="og:description" content="Scott Ritter on X: fallback">
    """
    assert _extract_status_text(html) == "Hello\nworld"


def test_extract_status_text_falls_back_to_meta() -> None:
    html = """
    <meta property="og:description" content="Scott Ritter on X: War porn is nonsense">
    """
    assert _extract_status_text(html) == "War porn is nonsense"


def test_extract_status_datetime_from_meta() -> None:
    html = '<meta property="article:published_time" content="2026-04-16T19:45:00Z">'
    dt = _extract_status_datetime(html)
    assert dt is not None
    assert dt.date() == date(2026, 4, 16)


def test_build_doc_includes_x_frontmatter() -> None:
    doc = _build_doc(
        handle="RealScottRitter",
        profile_url="https://x.com/RealScottRitter",
        status_url="https://x.com/RealScottRitter/status/2044552836260999446",
        ingest_date=date(2026, 4, 25),
        pub_date=date(2026, 4, 16),
        status_id="2044552836260999446",
        text="Hello world",
        thread="ritter",
    )
    assert "kind: x-post-text" in doc
    assert "account_author: @RealScottRitter" in doc
    assert "source_url_profile: https://x.com/RealScottRitter" in doc
    assert "status_id: 2044552836260999446" in doc
    assert "thread: ritter" in doc
    assert "# @RealScottRitter Post" in doc
    assert "Hello world" in doc


def test_run_writes_status_files_from_explicit_urls(monkeypatch) -> None:
    profile = "https://x.com/RealScottRitter"
    status_url = "https://x.com/RealScottRitter/status/2044552836260999446"
    profile_html = '<a href="/RealScottRitter/status/2044552836260999446">post</a>'
    status_html = """
    <meta property="article:published_time" content="2026-04-16T19:45:00Z">
    <div data-testid="tweetText"><span>Hello</span><br/>world</div>
    """
    monkeypatch.setattr(
        "scripts.backfill_x_profile_raw_input._fetch_html",
        lambda url, timeout=45: profile_html if url == profile else status_html,
    )
    tmpdir = Path.cwd() / ".codex-tmp" / "backfill-x-profile-test"
    try:
        tmpdir.mkdir(parents=True, exist_ok=True)
        raw_root = tmpdir / "raw-input"
        run(
            profile_url=profile,
            raw_root=raw_root,
            ingest_date=date(2026, 4, 25),
            thread="ritter",
            apply=True,
            limit=10,
            status_urls=[status_url],
        )
        files = list(raw_root.rglob("*.md"))
        assert len(files) == 1
        text = files[0].read_text(encoding="utf-8")
        assert "kind: x-post-text" in text
        assert "Hello\nworld" in text or "Hello world" in text
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
