"""Tests for ASR transcript normalization (work-jiang ingest helper)."""

from __future__ import annotations

import textwrap

# Import from scripts path
import sys
from pathlib import Path

_WJ = Path(__file__).resolve().parents[1] / "scripts" / "work_jiang"
sys.path.insert(0, str(_WJ))

from asr_light_clean import fix_civilization_thieves, normalize_transcript_text  # noqa: E402
from normalize_lecture_transcript_asr import (  # noqa: E402
    FULL_TRANSCRIPT_HEADING,
    run_file,
    split_full_transcript,
)


def test_split_full_transcript() -> None:
    md = f"# Title\n\n{FULL_TRANSCRIPT_HEADING}\n\nhello\n"
    head, body, _ = split_full_transcript(md)
    assert FULL_TRANSCRIPT_HEADING in head
    assert body == "\nhello\n"


def test_fix_civilization_thieves_article() -> None:
    text, n = fix_civilization_thieves("He marched against the thieves and thieves fled.")
    assert "the Thebes" not in text
    assert "Thebes" in text
    assert n >= 1


def test_normalize_civilization_replaces_granicus() -> None:
    raw = "at the battle of granticus in 334"
    out, n = normalize_transcript_text(raw, series="civilization")
    assert "Granicus" in out
    assert "granticus" not in out.lower()
    assert n >= 1


def test_normalize_geo_does_not_apply_thieves_to_thebes(tmp_path: Path) -> None:
    """Geo uses common tier only — 'thieves' is not bulk-replaced."""
    p = tmp_path / "geo-strategy-99-test.md"
    p.write_text(
        textwrap.dedent(
            f"""
            # T

            {FULL_TRANSCRIPT_HEADING}

            the thieves of Baghdad
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    assert run_file(p, whole_file=False, series="geo-strategy", dry_run=True) == 0
    text = p.read_text(encoding="utf-8")
    assert "thieves" in text  # unchanged for geo
