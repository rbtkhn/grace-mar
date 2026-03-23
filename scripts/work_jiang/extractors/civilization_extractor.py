"""Civilization lecture series (source_id civ-*) — shares prompts with Predictive History until a dedicated prompt exists."""
from __future__ import annotations

from extractors.predictive_history_extractor import PredictiveHistoryExtractor


class CivilizationExtractor(PredictiveHistoryExtractor):
    series_id = "civilization"
