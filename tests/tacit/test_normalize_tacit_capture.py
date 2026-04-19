"""Tests for scripts/tacit/normalize_tacit_capture.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

_TACIT_SCRIPT = REPO_ROOT / "scripts" / "tacit" / "normalize_tacit_capture.py"
_spec = importlib.util.spec_from_file_location("normalize_tacit_capture", _TACIT_SCRIPT)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
sys.modules["normalize_tacit_capture"] = _mod
_spec.loader.exec_module(_mod)
parse_and_normalize = _mod.parse_and_normalize

FIXTURE_IN = REPO_ROOT / "tests" / "tacit" / "fixtures" / "inbox" / "demo-note.md"
FIXTURE_EXPECTED = REPO_ROOT / "tests" / "tacit" / "fixtures" / "expected" / "demo-note.normalized.json"


def test_normalize_demo_fixture_matches_golden() -> None:
    raw = FIXTURE_IN.read_text(encoding="utf-8")
    got = parse_and_normalize(raw, provenance_path="tests/tacit/fixtures/inbox/demo-note.md")
    expected = json.loads(FIXTURE_EXPECTED.read_text(encoding="utf-8"))
    assert got == expected


def test_malformed_missing_raw_section() -> None:
    bad = "# Tacit Capture\nlane: x\ntimestamp: 2026-01-01T00:00:00Z\nsource: t\n"
    with pytest.raises(ValueError, match="Raw note"):
        parse_and_normalize(bad, provenance_path="x.md")


def test_malformed_missing_lane() -> None:
    bad = """# Tacit Capture
timestamp: 2026-01-01T00:00:00Z
source: t

## Raw note

body
"""
    with pytest.raises(ValueError, match="lane"):
        parse_and_normalize(bad, provenance_path="x.md")


@pytest.mark.skipif(
    __import__("importlib.util").util.find_spec("jsonschema") is None,
    reason="jsonschema not installed",
)
def test_golden_validates_against_schema() -> None:
    import jsonschema

    schema = json.loads(
        (REPO_ROOT / "schema-registry" / "tacit-capture-normalized.v1.json").read_text(
            encoding="utf-8"
        )
    )
    instance = json.loads(FIXTURE_EXPECTED.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
