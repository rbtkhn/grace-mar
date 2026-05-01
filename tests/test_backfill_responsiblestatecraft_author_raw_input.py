"""Offline tests for scripts/backfill_responsiblestatecraft_author_raw_input.py."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

from scripts.backfill_responsiblestatecraft_author_raw_input import (
    _author_handle,
    _build_doc,
    _extract_article_body,
    _extract_article_urls,
    _extract_datetime,
    _extract_title,
    run,
)


def test_author_handle_infers_last_path_segment() -> None:
    assert _author_handle("https://responsiblestatecraft.org/author/tparsi/") == "tparsi"


def test_extract_article_urls_from_author_html() -> None:
    html = """
    <a href="/ceasefire-iran-us-israel/">one</a>
    <a href="https://responsiblestatecraft.org/israel-new-attacks-iran/">two</a>
    <a href="/analysis/">ignore</a>
    <a href="/ceasefire-iran-us-israel/">dup</a>
    """
    urls = _extract_article_urls(html, "https://responsiblestatecraft.org/author/tparsi/")
    assert urls == [
        "https://responsiblestatecraft.org/ceasefire-iran-us-israel/",
        "https://responsiblestatecraft.org/israel-new-attacks-iran/",
    ]


def test_extract_title_and_body_from_article_html() -> None:
    html = """
    <meta property="og:title" content="A ceasefire on Iran's terms underscores war's strategic blunder">
    <meta property="article:published_time" content="2026-04-08T12:00:00Z">
    <article>
      <h1>A ceasefire on Iran's terms underscores war's strategic blunder</h1>
      <p>Trump's failed use of force has blunted the credibility of American military threats.</p>
      <p>It matters because the diplomatic track now depends on compromise.</p>
    </article>
    """
    title = _extract_title(html)
    assert title == "A ceasefire on Iran's terms underscores war's strategic blunder"
    body = _extract_article_body(html, title)
    assert "Trump's failed use of force" in body
    assert "It matters because the diplomatic track now depends on compromise." in body


def test_extract_datetime_from_meta() -> None:
    html = '<meta property="article:published_time" content="2026-04-08T12:00:00Z">'
    dt = _extract_datetime(html)
    assert dt is not None
    assert dt.date() == date(2026, 4, 8)


def test_build_doc_includes_expected_frontmatter() -> None:
    doc = _build_doc(
        author="@tparsi",
        author_url="https://responsiblestatecraft.org/author/tparsi/",
        article_url="https://responsiblestatecraft.org/ceasefire-iran-us-israel/",
        slug="ceasefire-iran-us-israel",
        ingest_date=date(2026, 4, 25),
        pub_date=date(2026, 4, 8),
        title="A ceasefire on Iran's terms underscores war's strategic blunder",
        body_text="Trump's failed use of force has blunted the credibility of American military threats.",
        thread="parsi",
    )
    assert "kind: rss-item" in doc
    assert "account_author: @tparsi" in doc
    assert "source_url_profile: https://responsiblestatecraft.org/author/tparsi/" in doc
    assert "source_url: https://responsiblestatecraft.org/ceasefire-iran-us-israel/" in doc
    assert "thread: parsi" in doc
    assert "Article text" in doc


def test_run_writes_article_files_from_explicit_urls(monkeypatch) -> None:
    author = "https://responsiblestatecraft.org/author/tparsi/"
    article_url = "https://responsiblestatecraft.org/ceasefire-iran-us-israel/"
    author_html = '<a href="/ceasefire-iran-us-israel/">one</a>'
    article_html = """
    <meta property="og:title" content="A ceasefire on Iran's terms underscores war's strategic blunder">
    <meta property="article:published_time" content="2026-04-08T12:00:00Z">
    <article>
      <h1>A ceasefire on Iran's terms underscores war's strategic blunder</h1>
      <p>Trump's failed use of force has blunted the credibility of American military threats.</p>
    </article>
    """
    monkeypatch.setattr(
        "scripts.backfill_responsiblestatecraft_author_raw_input._fetch_html",
        lambda url, timeout=45: author_html if url == author else article_html,
    )
    tmpdir = Path.cwd() / ".codex-tmp" / "backfill-rs-author-test"
    try:
        tmpdir.mkdir(parents=True, exist_ok=True)
        raw_root = tmpdir / "raw-input"
        run(
            author_url=author,
            raw_root=raw_root,
            ingest_date=date(2026, 4, 25),
            thread="parsi",
            apply=True,
            limit=10,
            article_urls=[article_url],
        )
        files = list(raw_root.rglob("*.md"))
        assert len(files) == 1
        text = files[0].read_text(encoding="utf-8")
        assert "kind: rss-item" in text
        assert "Trump's failed use of force" in text
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
