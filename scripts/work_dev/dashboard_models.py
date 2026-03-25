"""Data shapes for work-dev dashboard JSON (operator-facing)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DashboardSummary:
    generated_at: str
    integration_status_counts: dict[str, int]
    pipeline_event_counts: dict[str, int]
    provenance_completeness_score: float
    provenance_from_gate: bool
    lane_violation_count: int
    continuity_block_count: int
    gap_ids_open: list[str]
    notes: list[str] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)
