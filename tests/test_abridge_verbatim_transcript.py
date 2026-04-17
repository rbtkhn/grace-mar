"""Tests for scripts/abridge_verbatim_transcript.py — sentence-only abridgment."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from abridge_verbatim_transcript import (  # noqa: E402
    abridge_sentences,
    sentence_drop_score,
    split_sentences,
)


def test_split_sentences_does_not_glue_title_lines_to_next_without_punctuation() -> None:
    """Title lines without terminal .!? must not swallow following lines."""
    text = """strategy ; Short Title
Alexander Mercouris – April 16, 2026
Good day. Today is Thursday.
Over the last 24 hours, news happened."""
    sents = split_sentences(text)
    assert any(s.strip() == "Good day." for s in sents)
    assert sentence_drop_score("Good day.") >= 45
    assert not any("Good day" in s and "Over the last" in s for s in sents)


def test_abridge_under_max_words() -> None:
    text = " ".join(f"Sentence {i} has five words here." for i in range(80))
    sents = split_sentences(text)
    kept, _ = abridge_sentences(sents, max_words=50)
    wc = sum(len(s.split()) for s in kept)
    assert wc <= 50
