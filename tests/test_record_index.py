"""Deterministic indexes for EVIDENCE (self-archive) and self-memory horizons."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from record_index import (  # noqa: E402
    ROMAN_TO_SECTION_LABEL,
    build_evidence_index,
    build_memory_horizon_index,
    evidence_section_for_offset,
    memory_buckets_from_index,
    slice_evidence_entry,
    slice_evidence_section,
)


def test_evidence_sections_and_activity_offset():
    md = """# E

## I. READING LIST
x
## V. ACTIVITY LOG
  - id: ACT-0001
    date: 2026-01-01
## VI. OTHER
"""
    idx = build_evidence_index(md)
    assert idx.section_spans["I"][0] < idx.section_spans["V"][0]
    assert "ACT-0001" in idx.entry_spans
    pos = md.index("ACT-0001")
    assert evidence_section_for_offset(idx, pos) == "V"
    assert "Reading" == ROMAN_TO_SECTION_LABEL.get("I")
    act = slice_evidence_section(md, idx, "V")
    assert "ACT-0001" in act
    assert "READ" not in act  # section I excluded
    entry = slice_evidence_entry(md, idx, "ACT-0001")
    assert "ACT-0001" in entry


def test_memory_horizon_index_buckets():
    md = """# MEMORY

pre

## Short-term

one

## Medium-term

two

## Long-term

three
"""
    idx = build_memory_horizon_index(md)
    assert idx.saw_horizon
    buckets, preamble = memory_buckets_from_index(idx)
    assert any("pre" in ln for ln in preamble)
    assert any("one" in ln for ln in buckets["short"])
    assert any("two" in ln for ln in buckets["medium"])
    assert any("three" in ln for ln in buckets["long"])


@pytest.mark.skipif(
    not (REPO / "users/grace-mar/self-archive.md").is_file(),
    reason="grace-mar EVIDENCE file not present",
)
def test_grace_mar_evidence_index_covers_main_sections():
    raw = (REPO / "users/grace-mar/self-archive.md").read_text(encoding="utf-8")
    idx = build_evidence_index(raw)
    for r in ("I", "II", "V", "VIII"):
        assert r in idx.section_spans, f"missing section {r}"
    # entry_spans may be empty after a reseed — presence of sections is the structural gate
    assert isinstance(idx.entry_spans, dict)


def test_grace_mar_recency_scan_regions():
    raw = (REPO / "users/grace-mar/self-archive.md").read_text(encoding="utf-8")
    idx = build_evidence_index(raw)
    frags = [slice_evidence_section(raw, idx, r) for r in ("II", "III", "V")]
    joined = "\n\n".join(f for f in frags if f.strip())
    # After reseed, sections may contain only empty entries: [] stubs
    has_entries = "WRITE-" in joined or "ACT-" in joined or "CREATE-" in joined
    has_stubs = "entries:" in joined
    assert has_entries or has_stubs, "evidence sections should have entries or at least yaml stubs"
