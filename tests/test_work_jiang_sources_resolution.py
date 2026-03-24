"""Smoke test: sources.yaml resolution for work-jiang generators."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
SOURCES_YAML = WORK_JIANG / "metadata" / "sources.yaml"


def test_sources_yaml_exists() -> None:
    assert SOURCES_YAML.exists(), f"sources.yaml not found: {SOURCES_YAML}"


def test_resolve_geo_12() -> None:
    import yaml

    with SOURCES_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    sources = data.get("sources", [])
    geo12 = next((s for s in sources if s.get("source_id") == "geo-12"), None)
    assert geo12 is not None, "geo-12 not found in sources.yaml"
    assert geo12.get("video_id"), "geo-12 missing video_id"
    assert geo12.get("lecture_path"), "geo12 missing lecture_path"
    lecture_path = WORK_JIANG / geo12["lecture_path"]
    assert lecture_path.exists(), f"geo-12 lecture file not found: {lecture_path}"


def test_resolve_civ_21() -> None:
    import yaml

    with SOURCES_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    sources = data.get("sources", [])
    civ21 = next((s for s in sources if s.get("source_id") == "civ-21"), None)
    assert civ21 is not None, "civ-21 not found in sources.yaml"
    assert civ21.get("video_id"), "civ-21 missing video_id"
    assert civ21.get("lecture_path"), "civ-21 missing lecture_path"
