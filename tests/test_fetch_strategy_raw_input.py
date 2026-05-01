"""Offline tests for scripts/fetch_strategy_raw_input.py (RSS/Atom parsing)."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

from scripts.fetch_strategy_raw_input import (
    _build_rss_item_document,
    _iter_rss_items,
    _parse_pub_date,
    _rss_no_thread_filename,
    _strip_html,
    _threaded_raw_input_filename,
    load_config,
    run,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
FETCH_SOURCES = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/raw-input/fetch-sources.json"
)

_SUBSTACK_RSS_ONE_ITEM = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item>
    <title>Stub Title</title>
    <link>https://example.com/p/stub</link>
    <pubDate>Mon, 21 Apr 2026 00:00:00 GMT</pubDate>
    <guid>https://example.com/p/stub</guid>
    <description>&lt;p&gt;Stub summary&lt;/p&gt;</description>
  </item>
</channel></rss>"""


def test_parse_pub_date_rfc822() -> None:
    d = _parse_pub_date("Mon, 21 Apr 2026 12:00:00 GMT")
    assert d == date(2026, 4, 21)


def test_parse_pub_date_iso_z() -> None:
    d = _parse_pub_date("2026-04-21T18:30:00Z")
    assert d == date(2026, 4, 21)


def test_strip_html() -> None:
    assert "hello" in _strip_html("<p>hello <b>world</b></p>").lower()


def test_rss20_items() -> None:
    xml = b"""<?xml version="1.0"?>
    <rss version="2.0"><channel>
      <item>
        <title>Test Post</title>
        <link>https://example.com/p/1</link>
        <pubDate>Mon, 21 Apr 2026 00:00:00 GMT</pubDate>
        <guid>https://example.com/p/1</guid>
        <description>&lt;p&gt;Hello&lt;/p&gt;</description>
      </item>
    </channel></rss>"""
    root = ET.fromstring(xml)
    items = _iter_rss_items(root)
    assert len(items) == 1
    assert items[0]["title"] == "Test Post"
    assert items[0]["link"] == "https://example.com/p/1"


def test_atom_items() -> None:
    xml = b"""<?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Atom Title</title>
        <link href="https://example.com/a/2"/>
        <id>https://example.com/a/2</id>
        <updated>2026-04-22T10:00:00Z</updated>
        <summary type="html">Summary &lt;em&gt;text&lt;/em&gt;</summary>
      </entry>
    </feed>"""
    root = ET.fromstring(xml)
    items = _iter_rss_items(root)
    assert len(items) == 1
    assert items[0]["title"] == "Atom Title"
    assert items[0]["link"] == "https://example.com/a/2"


def test_threaded_raw_input_filename_same_pattern_all_experts() -> None:
    assert _threaded_raw_input_filename(air=date(2026, 4, 21), expert_id="mercouris") == (
        "2026-04-21-mercouris.md"
    )
    assert _threaded_raw_input_filename(air=date(2026, 4, 21), expert_id="simplicius") == (
        "2026-04-21-simplicius.md"
    )


def test_rss_no_thread_filename_stable() -> None:
    fname = _rss_no_thread_filename(
        slug_prefix="rss-test",
        air=date(2026, 4, 21),
        title="Hello World",
        guid="https://example.com/p/1",
    )
    assert fname.startswith("rss-test-2026-04-21-")
    assert fname.endswith(".md")


def test_build_rss_item_document_content() -> None:
    _guid, body = _build_rss_item_document(
        ingest_date=date(2026, 4, 25),
        pub_date=date(2026, 4, 21),
        feed_url="https://example.com/feed",
        item={
            "title": "Hello World",
            "link": "https://example.com/p/1",
            "pub_raw": None,
            "summary_html": "<p>Short</p>",
            "guid": "https://example.com/p/1",
        },
        thread=None,
    )
    assert "Hello World" in body
    assert "https://example.com/p/1" in body
    assert "ingest_date: 2026-04-25" in body
    assert "pub_date: 2026-04-21" in body


def test_build_rss_item_document_includes_optional_thread_in_yaml() -> None:
    _, body = _build_rss_item_document(
        ingest_date=date(2026, 4, 25),
        pub_date=date(2026, 4, 21),
        feed_url="https://example.com/feed",
        item={
            "title": "T",
            "link": "https://example.com/p/1",
            "pub_raw": None,
            "summary_html": None,
            "guid": "g",
        },
        thread="simplicius",
    )
    assert "thread: simplicius" in body
    fm_block = body.split("---", 2)[1]
    assert "guid:" in fm_block and "thread: simplicius" in fm_block


def test_load_config_example_exists() -> None:
    p = (
        Path(__file__).resolve().parent.parent
        / "docs/skill-work/work-strategy/strategy-notebook/raw-input/fetch-sources.example.json"
    )
    assert p.is_file()


def test_fetch_sources_json_substack_feeds() -> None:
    """Committed fetch-sources.json lists enabled Substack /feed URLs and slug_prefixes."""
    cfg = load_config(FETCH_SOURCES)
    assert cfg.get("version") == 1
    feeds = cfg.get("rss_feeds") or []
    enabled = [f for f in feeds if f.get("enabled", True) and f.get("url")]
    substack = [f for f in enabled if "substack.com/feed" in str(f.get("url", ""))]
    assert len(substack) == 5
    urls = {str(f["url"]) for f in substack}
    assert "https://simplicius76.substack.com/feed" in urls
    assert "https://bigserge.substack.com/feed" in urls
    assert "https://greenwald.substack.com/feed" in urls
    assert "https://scottritter.substack.com/feed" in urls
    assert "https://conflictsforum.substack.com/feed" in urls
    prefixes = {str(f.get("slug_prefix") or "") for f in substack}
    assert prefixes == {"rss-simplicius", "rss-bigserge", "rss-greenwald", "rss-ritter", "rss-conflictsforum"}
    threads = {str(f.get("thread") or "") for f in substack}
    assert threads == {"simplicius", "bigserge", "greenwald", "ritter", "crooke"}


def test_run_apply_writes_per_expert_daily_file_with_mock_fetch(
    tmp_path: Path, monkeypatch
) -> None:
    """Feeds with ``thread`` share one ``YYYY-MM-DD-<expert_id>.md`` per air date (no network)."""
    cfg_path = tmp_path / "fetch-sources.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": 1,
                "rss_feeds": [
                    {
                        "enabled": True,
                        "url": "https://simplicius76.substack.com/feed",
                        "slug_prefix": "rss-simplicius",
                        "max_items": 1,
                        "thread": "simplicius",
                    },
                    {
                        "enabled": True,
                        "url": "https://bigserge.substack.com/feed",
                        "slug_prefix": "rss-bigserge",
                        "max_items": 1,
                        "thread": "bigserge",
                    },
                    {
                        "enabled": True,
                        "url": "https://greenwald.substack.com/feed",
                        "slug_prefix": "rss-greenwald",
                        "max_items": 1,
                        "thread": "greenwald",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    raw_root = tmp_path / "raw-input"
    monkeypatch.setattr(
        "scripts.fetch_strategy_raw_input._fetch_url",
        lambda _url, timeout=45: _SUBSTACK_RSS_ONE_ITEM,
    )
    run(
        config_path=cfg_path,
        raw_root=raw_root,
        ingest_date=date(2026, 4, 25),
        apply=True,
        global_max=None,
    )
    mds = sorted(raw_root.rglob("*.md"))
    assert len(mds) == 3
    names = {p.name for p in mds}
    assert names == {
        "2026-04-21-simplicius.md",
        "2026-04-21-bigserge.md",
        "2026-04-21-greenwald.md",
    }
    for path in mds:
        t = path.read_text(encoding="utf-8")
        assert "kind: rss-item" in t
        assert "feed_url:" in t
        assert "thread:" in t


_SUBSTACK_RSS_TWO_ITEMS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item>
    <title>First</title>
    <link>https://example.com/p/a</link>
    <pubDate>Mon, 21 Apr 2026 00:00:00 GMT</pubDate>
    <guid>https://example.com/p/a</guid>
    <description>&lt;p&gt;A&lt;/p&gt;</description>
  </item>
  <item>
    <title>Second</title>
    <link>https://example.com/p/b</link>
    <pubDate>Mon, 21 Apr 2026 00:00:00 GMT</pubDate>
    <guid>https://example.com/p/b</guid>
    <description>&lt;p&gt;B&lt;/p&gt;</description>
  </item>
</channel></rss>"""


def test_run_appends_second_rss_item_into_same_expert_daily_file(
    tmp_path: Path, monkeypatch
) -> None:
    cfg_path = tmp_path / "fetch-sources.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": 1,
                "rss_feeds": [
                    {
                        "enabled": True,
                        "url": "https://simplicius76.substack.com/feed",
                        "slug_prefix": "rss-simplicius",
                        "max_items": 2,
                        "thread": "simplicius",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    raw_root = tmp_path / "raw-input"
    monkeypatch.setattr(
        "scripts.fetch_strategy_raw_input._fetch_url",
        lambda _url, timeout=45: _SUBSTACK_RSS_TWO_ITEMS,
    )
    run(
        config_path=cfg_path,
        raw_root=raw_root,
        ingest_date=date(2026, 4, 25),
        apply=True,
        global_max=None,
    )
    path = raw_root / "2026-04-21" / "2026-04-21-simplicius.md"
    assert path.is_file()
    t = path.read_text(encoding="utf-8")
    assert t.count("kind: rss-item") == 2
    assert "First" in t and "Second" in t
