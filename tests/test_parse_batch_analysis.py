"""Tests for scripts/parse_batch_analysis.py."""

from __future__ import annotations

from scripts.parse_batch_analysis import parse_inbox_text


def test_crosses_only_high_confidence() -> None:
    text = """
`batch-analysis | 2026-04-14 | Ritter × Davis | crosses:ritter+davis`
"""
    doc = parse_inbox_text(text)
    refs = doc["batch_analysis_refs"]
    assert len(refs) == 1
    r = refs[0]
    assert r["confidence"] == "high"
    assert set(r["expert_ids"]) == {"ritter", "davis"}
    assert r["sources"]["crosses"] == ["ritter", "davis"]


def test_merge_duplicate_label_unions_ids() -> None:
    text = """
`batch-analysis | 2026-04-14 | Ritter × Davis | short stub **crosses:ritter+davis**`
`batch-analysis | 2026-04-14 | Ritter × Davis | long prose without new crosses — padding padding padding padding padding padding padding padding padding padding`
"""
    doc = parse_inbox_text(text)
    refs = doc["batch_analysis_refs"]
    assert len(refs) == 1
    assert set(refs[0]["expert_ids"]) == {"ritter", "davis"}
    assert "long prose" in refs[0]["raw"]


def test_upstream_threads_medium() -> None:
    text = """
`X | cold: a // hook | https://x.com/a | verify:x | thread:davis`
`batch-analysis | 2026-04-16 | test batch | **Tension-first:** no crosses here`
"""
    doc = parse_inbox_text(text)
    refs = doc["batch_analysis_refs"]
    assert len(refs) == 1
    r = refs[0]
    assert r["confidence"] == "medium"
    assert r["sources"]["upstream_verify"] == ["davis"]
    assert "davis" in r["expert_ids"]


def test_thematic_none() -> None:
    text = """
`batch-analysis | 2026-04-15 | §1d Kremlin + §1h | **Tension-first:** wires only`
"""
    doc = parse_inbox_text(text)
    r = doc["batch_analysis_refs"][0]
    assert r["confidence"] == "none"
    assert r["expert_ids"] == []


def test_thread_on_batch_line_high() -> None:
    text = """
`batch-analysis | 2026-04-15 | Mercouris note | thread:mercouris **15 Apr** strand`
"""
    doc = parse_inbox_text(text)
    r = doc["batch_analysis_refs"][0]
    assert r["confidence"] == "high"
    assert r["sources"]["thread_in_line"] == ["mercouris"]
