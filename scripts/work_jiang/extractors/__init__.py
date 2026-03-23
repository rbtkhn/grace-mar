"""Pluggable lecture analysis extractors (work-jiang)."""

from .base import LectureExtractor
from .civilization_extractor import CivilizationExtractor
from .geo_strategy_extractor import GeoStrategyExtractor
from .predictive_history_extractor import PredictiveHistoryExtractor
from .registry import (
    get_extractor,
    get_extractor_class,
    instantiate_extractor,
    list_registered_series,
    register_extractor,
)

__all__ = [
    "LectureExtractor",
    "GeoStrategyExtractor",
    "PredictiveHistoryExtractor",
    "CivilizationExtractor",
    "get_extractor",
    "get_extractor_class",
    "instantiate_extractor",
    "list_registered_series",
    "register_extractor",
]
