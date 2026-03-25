"""Map series_id or source_id prefix -> extractor class."""
from __future__ import annotations

import os
from typing import Type

from extractors.base import LectureExtractor
from extractors.civilization_extractor import CivilizationExtractor
from extractors.geo_strategy_extractor import GeoStrategyExtractor
from extractors.predictive_history_extractor import PredictiveHistoryExtractor

_EXTRACTORS: dict[str, Type[LectureExtractor]] = {
    "geo-strategy": GeoStrategyExtractor,
    "predictive-history": PredictiveHistoryExtractor,
    "civilization": CivilizationExtractor,
}


def register_extractor(series_id: str, cls: Type[LectureExtractor]) -> None:
    _EXTRACTORS[series_id] = cls


def list_registered_series() -> list[str]:
    return sorted(_EXTRACTORS.keys())


def get_extractor_class(*, series_id: str | None = None, source_id: str | None = None) -> Type[LectureExtractor]:
    if series_id and series_id in _EXTRACTORS:
        return _EXTRACTORS[series_id]
    if source_id:
        if source_id.startswith("geo-"):
            return GeoStrategyExtractor
        if source_id.startswith("civ-"):
            return CivilizationExtractor
        if source_id.startswith("vi-"):
            return PredictiveHistoryExtractor
    override = os.environ.get("WORK_JIANG_EXTRACTOR_SERIES", "").strip()
    if override and override in _EXTRACTORS:
        return _EXTRACTORS[override]
    return PredictiveHistoryExtractor


def get_extractor(*, series_id: str | None = None, source_id: str | None = None) -> Type[LectureExtractor]:
    """Backward-compatible alias: returns the extractor *class*."""
    return get_extractor_class(series_id=series_id, source_id=source_id)


def instantiate_extractor(*, series_id: str | None = None, source_id: str | None = None) -> LectureExtractor:
    cls = get_extractor_class(series_id=series_id, source_id=source_id)
    return cls()
