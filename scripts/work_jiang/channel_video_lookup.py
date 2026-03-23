"""Resolve YouTube video_id and display title from Predictive History channel index.

Used by ingest_lecture.py. Parses CHANNEL-VIDEO-INDEX.md (markdown table).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX = (
    ROOT
    / "research"
    / "external"
    / "youtube-channels"
    / "predictive-history"
    / "CHANNEL-VIDEO-INDEX.md"
)

# Civilization #22: ... (ASCII or fullwidth colon; optional END, BONUS, etc.)
CIV_EP_RE = re.compile(r"^Civilization\s*#(\d+)\s*[:：]\s*", re.I)
# Geo-Strategy #N: — not "Geo-Strategy Update"
GEO_EP_RE = re.compile(r"^Geo-Strategy\s*#\s*(\d+)\s*[:：]\s*", re.I)
# Channel index uses "Geo-Strategy END:" for the finale (book line = #12).
GEO_END_RE = re.compile(r"^Geo-Strategy\s+END\s*[:：]\s*", re.I)


def parse_channel_index_rows(index_path: Path | None = None) -> list[tuple[str, str]]:
    """Return list of (video_id, title) from the channel index table."""
    path = index_path or DEFAULT_INDEX
    if not path.exists():
        return []
    rows: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # | # | `vid` | title | duration | url |
        if len(parts) < 5:
            continue
        vid_cell = parts[2].strip().strip("`")
        title = parts[3].strip()
        if len(vid_cell) != 11 or not title:
            continue
        rows.append((vid_cell, title))
    return rows


def _pick_best_duplicate(candidates: list[tuple[str, str]]) -> tuple[str, str]:
    """When multiple rows match one episode (e.g. re-upload), prefer AUDIO FIXED / Re-upload."""
    if len(candidates) == 1:
        return candidates[0]
    for pref in ("AUDIO FIXED", "Re-upload", "Re-Upload"):
        for vid, title in candidates:
            if pref in title:
                return (vid, title)
    return candidates[0]


def lookup_civilization(episode: int, *, index_path: Path | None = None) -> tuple[str, str] | None:
    """Return (video_id, youtube_title) for Civilization #episode, or None."""
    candidates: list[tuple[str, str]] = []
    for vid, title in parse_channel_index_rows(index_path):
        m = CIV_EP_RE.match(title)
        if m and int(m.group(1)) == episode:
            candidates.append((vid, title))
    if not candidates:
        return None
    return _pick_best_duplicate(candidates)


def lookup_geo_strategy(episode: int, *, index_path: Path | None = None) -> tuple[str, str] | None:
    """Return (video_id, youtube_title) for Geo-Strategy #episode (not Update series), or None."""
    candidates: list[tuple[str, str]] = []
    for vid, title in parse_channel_index_rows(index_path):
        if "Geo-Strategy Update" in title:
            continue
        t = title.strip()
        if episode == 12 and GEO_END_RE.match(t):
            candidates.append((vid, t))
            continue
        m = GEO_EP_RE.match(t)
        if m and int(m.group(1)) == episode:
            candidates.append((vid, t))
    if not candidates:
        return None
    return _pick_best_duplicate(candidates)


def lookup_series_episode(
    series: str, episode: int, *, index_path: Path | None = None
) -> tuple[str, str] | None:
    """
    series: 'civilization' | 'civ' | 'geo-strategy' | 'geo'
    """
    s = series.lower().replace("_", "-")
    if s in ("civilization", "civ"):
        return lookup_civilization(episode, index_path=index_path)
    if s in ("geo-strategy", "geo"):
        return lookup_geo_strategy(episode, index_path=index_path)
    raise ValueError(f"Unknown series: {series!r} (use civilization|civ|geo-strategy|geo)")


def youtube_title_to_heading(youtube_title: str, series: str, episode: int) -> str:
    """Strip redundant series prefix for curated # heading; keep rest as display title."""
    s = series.lower().replace("_", "-")
    if s in ("civilization", "civ"):
        m = CIV_EP_RE.match(youtube_title)
        if m:
            rest = youtube_title[m.end() :].strip()
            return f"Civilization #{episode}: {rest}" if rest else f"Civilization #{episode}"
    if s in ("geo-strategy", "geo"):
        if episode == 12:
            m_end = GEO_END_RE.match(youtube_title.strip())
            if m_end:
                rest = youtube_title.strip()[m_end.end() :].strip()
                return f"Geo-Strategy #12 (END): {rest}" if rest else "Geo-Strategy #12 (END)"
        m = GEO_EP_RE.match(youtube_title)
        if m:
            rest = youtube_title[m.end() :].strip()
            return f"Geo-Strategy #{episode}: {rest}" if rest else f"Geo-Strategy #{episode}"
    return youtube_title


_TRAILING_NOTE_PAREN = re.compile(
    r"\s*\([^)]*(?:re-?upload|AUDIO\s+FIXED|thanks\s+to\b)[^)]*\)\s*$",
    re.I,
)


def youtube_title_to_slug(youtube_title: str, series: str, episode: int) -> str:
    """Filesystem slug after civilization-NN- or geo-strategy-NN-."""
    heading = youtube_title_to_heading(youtube_title, series, episode)
    # Drop trailing YouTube/editor notes like "(Re-upload AUDIO FIXED …)"; keep
    # substantive parens e.g. "Psychohistory (The Science of …)" and "(END)" in prefix.
    base = heading.strip()
    while True:
        trimmed = _TRAILING_NOTE_PAREN.sub("", base).rstrip()
        if trimmed == base:
            break
        base = trimmed
    # Remove leading "Civilization #N:" / "Geo-Strategy #N:"
    base = re.sub(r"^Civilization\s*#\d+[A-Za-z]*\s*[:：]\s*", "", base, flags=re.I)
    base = re.sub(r"^Geo-Strategy\s*#\d+\s*\(END\)\s*[:：]\s*", "", base, flags=re.I)
    base = re.sub(r"^Geo-Strategy\s*#\d+\s*[:：]\s*", "", base, flags=re.I)
    base = base.strip()
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return slug or f"episode-{episode:02d}"
