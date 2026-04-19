"""Tests for scripts/tacit/generate_tacit_candidates.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

_GEN_SCRIPT = REPO_ROOT / "scripts" / "tacit" / "generate_tacit_candidates.py"
_spec = importlib.util.spec_from_file_location("generate_tacit_candidates", _GEN_SCRIPT)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
generate_from_normalized = _mod.generate_from_normalized

FIXTURE_NORM = REPO_ROOT / "tests" / "tacit" / "fixtures" / "expected" / "demo-note.normalized.json"


def test_generate_produces_moonshot_and_work_candidates() -> None:
    record = json.loads(FIXTURE_NORM.read_text(encoding="utf-8"))
    cands = generate_from_normalized(record)
    types = {c["candidate_type"] for c in cands}
    assert types == {"moonshot_insight_candidate", "work_doctrine_candidate"}
    assert all(c["provenance_tacit_id"] == record["id"] for c in cands)
    assert all("work-strategy" in c["proposed_destination_surface"] for c in cands if c["candidate_type"] == "work_doctrine_candidate")


def test_generate_empty_destinations_no_keyword_returns_empty() -> None:
    record = {
        "id": "tacit_20260101T000000Z_abcdef123456",
        "timestamp": "2026-01-01T00:00:00Z",
        "source": "t",
        "lane": "x",
        "raw_text": "plain note without triggers",
        "tags": [],
        "candidate_destinations": ["unknown"],
        "confidence": "low",
        "privacy": "private",
        "provenance_path": "p.md",
        "normalization_version": "1.0",
        "content_sha256": "0" * 64,
    }
    # unknown maps to no type; no moonshot keyword
    assert generate_from_normalized(record) == []
