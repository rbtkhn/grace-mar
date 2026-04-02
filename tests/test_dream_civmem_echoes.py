"""Unit tests for dream_civmem_echoes query-side token helpers."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import dream_civmem_echoes as dce  # noqa: E402


def test_extract_interesting_query_tokens_drops_short_and_stopwords() -> None:
    q = "the constitution and rome trade war"
    toks = dce._extract_interesting_query_tokens(q)
    assert "constitution" in toks
    assert "trade" in toks
    assert "rome" not in toks
    assert "the" not in toks


def test_looks_specific_requires_intersection_when_tokens_present() -> None:
    interesting = ["constitution"]
    assert dce._looks_specific("docs/foo.md", "mentions constitution here", interesting) is True
    assert dce._looks_specific("docs/foo.md", "unrelated snippet", interesting) is False


def test_looks_specific_empty_interesting_always_true() -> None:
    assert dce._looks_specific("a.md", "body", []) is True
