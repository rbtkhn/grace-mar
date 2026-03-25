"""Shared ASR light-cleaning for work-jiang transcript text (curated or raw caption body).

Civilization lectures use common + civilization replacement tiers; geo-strategy uses common
only; **secret-history** uses common + ``SECRET_HISTORY_REPLACEMENTS`` (Roman/SH Volume III);
**game-theory** uses common + ``GAME_THEORY_REPLACEMENTS`` (Volume IV; table may start empty);
**great-books** uses common + ``GREAT_BOOKS_REPLACEMENTS`` (Volume V; table may start empty)."""

from __future__ import annotations

import re
from pathlib import Path

from asr_transcript_replacements import (
    CIVILIZATION_REPLACEMENTS,
    COMMON_REPLACEMENTS,
    GAME_THEORY_REPLACEMENTS,
    GREAT_BOOKS_REPLACEMENTS,
    SECRET_HISTORY_REPLACEMENTS,
)


def detect_series_from_basename(name: str) -> str | None:
    """Return series key for replacement tier from a lecture or verbatim filename."""
    n = name.lower()
    if n.startswith("civilization-"):
        return "civilization"
    if n.startswith("geo-strategy-"):
        return "geo-strategy"
    if n.startswith("secret-history-"):
        return "secret-history"
    if n.startswith("game-theory-"):
        return "game-theory"
    if n.startswith("great-books-"):
        return "great-books"
    return None


def detect_series(path: Path) -> str | None:
    return detect_series_from_basename(path.name)


def _sort_by_length(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return sorted(pairs, key=lambda x: len(x[0]), reverse=True)


def apply_ordered_replacements(text: str, pairs: list[tuple[str, str]]) -> tuple[str, int]:
    """Return (new_text, number of substring replacements)."""
    count = 0
    ordered = _sort_by_length(pairs)
    for old, new in ordered:
        if not old:
            continue
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n
    return text, count


def fix_civilization_thieves(text: str) -> tuple[str, int]:
    """Map ASR 'thieves' → Thebes without leaving 'the Thebes'."""
    count = 0
    for pat, repl in (
        (r"(?i)\bthe thieves\b", "Thebes"),
        (r"(?i)\bthieves\b", "Thebes"),
    ):
        n = len(re.findall(pat, text))
        if n:
            text = re.sub(pat, repl, text)
            count += n
    return text, count


def normalize_transcript_text(
    text: str,
    *,
    series: str | None,
) -> tuple[str, int]:
    """Apply systematic spelling / ASR fixes; return (text, substitution_count)."""
    total = 0
    text, n = apply_ordered_replacements(text, COMMON_REPLACEMENTS)
    total += n
    if series == "civilization":
        text, n = apply_ordered_replacements(text, CIVILIZATION_REPLACEMENTS)
        total += n
        text, n = fix_civilization_thieves(text)
        total += n
    elif series == "secret-history":
        text, n = apply_ordered_replacements(text, SECRET_HISTORY_REPLACEMENTS)
        total += n
    elif series == "game-theory":
        text, n = apply_ordered_replacements(text, GAME_THEORY_REPLACEMENTS)
        total += n
    elif series == "great-books":
        text, n = apply_ordered_replacements(text, GREAT_BOOKS_REPLACEMENTS)
        total += n
    return text, total
