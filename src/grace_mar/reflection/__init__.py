"""Reflection cycle: evidence-grounded gate proposals."""

from grace_mar.reflection.collect import ReflectionBundle, collect_bundle
from grace_mar.reflection.constants import (
    CHANNEL_REFLECTION,
    DEFAULT_APPEND_TOP_N,
    DEFAULT_LOOKBACK_DAYS,
    DEEP_LOOKBACK_DAYS,
    MAX_PROPOSALS_PER_CYCLE,
    SIGNAL_REFLECTION,
)
from grace_mar.reflection.engine import ReflectionResult, run_reflection_engine
from grace_mar.reflection.format_gate import build_reflection_candidate_block

__all__ = [
    "CHANNEL_REFLECTION",
    "DEFAULT_APPEND_TOP_N",
    "DEFAULT_LOOKBACK_DAYS",
    "DEEP_LOOKBACK_DAYS",
    "MAX_PROPOSALS_PER_CYCLE",
    "SIGNAL_REFLECTION",
    "ReflectionBundle",
    "ReflectionResult",
    "build_reflection_candidate_block",
    "collect_bundle",
    "run_reflection_engine",
]
