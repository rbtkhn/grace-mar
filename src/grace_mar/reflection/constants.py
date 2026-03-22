"""Reflection cycle limits and identifiers."""

from __future__ import annotations

# Signal stored in recursion-gate YAML and used for dashboard filtering
SIGNAL_REFLECTION = "reflection-cycle"
CHANNEL_REFLECTION = "reflection-cycle"

DEFAULT_LOOKBACK_DAYS = 14
DEEP_LOOKBACK_DAYS = 45

MAX_PROPOSALS_PER_CYCLE = 5
DEFAULT_APPEND_TOP_N = 3
MAX_HIGH_RISK_PER_30_DAYS = 1
MAX_HIGH_RISK_PER_MONTH = 2

DEFAULT_TRANSCRIPT_TAIL_CHARS = 120_000
DEFAULT_MAX_JSONL_LINES = 400

# Bundle size caps (characters) for LLM context
MAX_NEGATIVE_EXAMPLES_CHARS = 4000
MAX_PROCESSED_GATE_CHARS = 80_000
