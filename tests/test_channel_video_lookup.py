"""Tests for Predictive History channel index → video_id resolution."""

from __future__ import annotations

import sys
from pathlib import Path

_WJ = Path(__file__).resolve().parents[1] / "scripts" / "work_jiang"
sys.path.insert(0, str(_WJ))

from channel_video_lookup import (  # noqa: E402
    lookup_civilization,
    lookup_geo_strategy,
    lookup_series_episode,
    parse_channel_index_rows,
    youtube_title_to_heading,
    youtube_title_to_slug,
)

INDEX = (
    Path(__file__).resolve().parents[1]
    / "research"
    / "external"
    / "youtube-channels"
    / "predictive-history"
    / "CHANNEL-VIDEO-INDEX.md"
)


def test_index_file_exists() -> None:
    assert INDEX.is_file(), "CHANNEL-VIDEO-INDEX.md missing — run fetch --index-only"


def test_parse_rows_nonempty() -> None:
    rows = parse_channel_index_rows(INDEX)
    assert len(rows) >= 10
    assert all(len(v) == 11 for v, _ in rows)


def test_civilization_57_prefers_audio_fixed() -> None:
    vid, title = lookup_civilization(57, index_path=INDEX)
    assert vid == "cylkQPsfFRY"
    assert "AUDIO FIXED" in title


def test_geo_strategy_12_resolves_end_row() -> None:
    vid, title = lookup_geo_strategy(12, index_path=INDEX)
    assert vid == "s_k6esWheqA"
    assert "END" in title
    assert "Psychohistory" in title


def test_geo_strategy_skips_update() -> None:
    # Episode 1 should be the lecture, not an "Update" row.
    vid, title = lookup_geo_strategy(1, index_path=INDEX)
    assert "Update" not in title
    assert vid


def test_lookup_series_episode_aliases() -> None:
    a = lookup_series_episode("civ", 1, index_path=INDEX)
    b = lookup_series_episode("civilization", 1, index_path=INDEX)
    assert a and a == b


def test_youtube_title_to_heading_geo_end() -> None:
    yt = "Geo-Strategy END:  Psychohistory (The Science of Imagining the Future)"
    h = youtube_title_to_heading(yt, "geo-strategy", 12)
    assert h.startswith("Geo-Strategy #12 (END):")
    assert "Psychohistory" in h


def test_youtube_title_to_slug_geo_end() -> None:
    yt = "Geo-Strategy END:  Psychohistory (The Science of Imagining the Future)"
    slug = youtube_title_to_slug(yt, "geo-strategy", 12)
    assert "psychohistory" in slug
