"""Tests for lecture analysis JSON validation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WJ = ROOT / "scripts" / "work_jiang"
if str(WJ) not in sys.path:
    sys.path.insert(0, str(WJ))

from validate_lecture_analysis_json import validate_obj  # noqa: E402


def test_fixture_valid() -> None:
    p = ROOT / "research/external/work-jiang/fixtures/lecture_analysis_valid_min.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert validate_obj(data) == []


def test_missing_summary_errors() -> None:
    data = json.loads(
        (ROOT / "research/external/work-jiang/fixtures/lecture_analysis_valid_min.json").read_text(
            encoding="utf-8"
        )
    )
    del data["summary"]
    errs = validate_obj(data)
    assert any("summary" in e for e in errs)


def test_analysis_json_version_mismatch_errors() -> None:
    data = json.loads(
        (ROOT / "research/external/work-jiang/fixtures/lecture_analysis_valid_min.json").read_text(
            encoding="utf-8"
        )
    )
    data["analysis_json_version"] = "9.9"
    errs = validate_obj(data)
    assert any("analysis_json_version" in e for e in errs)


def test_extractor_registry_civ() -> None:
    from extractors.registry import get_extractor_class
    from extractors.civilization_extractor import CivilizationExtractor

    assert get_extractor_class(source_id="civ-01") is CivilizationExtractor
    assert get_extractor_class(source_id="geo-01").__name__ == "GeoStrategyExtractor"
