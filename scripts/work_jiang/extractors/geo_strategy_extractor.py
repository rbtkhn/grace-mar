"""Geo-Strategy series (source_id geo-*)."""
from __future__ import annotations

from pathlib import Path

from extractors.base import LectureExtractor

ROOT = Path(__file__).resolve().parents[3]


class GeoStrategyExtractor(LectureExtractor):
    series_id = "geo-strategy"

    def prompt_system_path(self) -> Path:
        return ROOT / "scripts" / "work_jiang" / "prompts" / "lecture_analysis_json_system.md"

    def schema_version(self) -> str:
        return "1.0"

    def json_schema_variant(self) -> str | None:
        return "default"
