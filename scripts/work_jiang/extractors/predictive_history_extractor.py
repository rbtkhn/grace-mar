"""Umbrella Predictive History channel — same JSON schema as Geo-Strategy by default."""
from __future__ import annotations

from pathlib import Path

from extractors.base import LectureExtractor

ROOT = Path(__file__).resolve().parents[3]


class PredictiveHistoryExtractor(LectureExtractor):
    """Umbrella channel / Civilization (`civ-*`) — same JSON schema as Geo-Strategy until prompts split."""

    series_id = "predictive-history"

    def prompt_system_path(self) -> Path:
        return ROOT / "scripts" / "work_jiang" / "prompts" / "lecture_analysis_json_system.md"

    def schema_version(self) -> str:
        return "1.0"

    def json_schema_variant(self) -> str | None:
        return "default"
