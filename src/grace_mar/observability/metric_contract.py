"""
Comparable workflow metric keys for lane observability JSON (additive).

Field names align with JSON reporting (camelCase) for schema parity.
"""

from __future__ import annotations

from typing import Any

WORKFLOW_METRIC_CONTRACT_VERSION = "1.0.0"
WORKFLOW_METRIC_KEY = "workflowMetricContract"


def empty_contract(lane: str) -> dict[str, Any]:
    return {
        "schemaVersion": WORKFLOW_METRIC_CONTRACT_VERSION,
        "lane": lane,
        "workflowCount": 0,
        "acceptedCount": 0,
        "revisionCount": 0,
        "staleCount": 0,
        "medianContextTokens": None,
        "compressionRate": None,
        "retrievalMissRate": None,
        "medianReviewCycles": None,
        "partialMetrics": True,
        "notes": "Populated when lane emits comparable counters; else nulls.",
    }


def fill_contract(
    lane: str,
    *,
    workflow_count: int = 0,
    accepted_count: int = 0,
    revision_count: int = 0,
    stale_count: int = 0,
    median_context_tokens: float | None = None,
    compression_rate: float | None = None,
    retrieval_miss_rate: float | None = None,
    median_review_cycles: float | None = None,
    partial: bool = True,
) -> dict[str, Any]:
    return {
        "schemaVersion": WORKFLOW_METRIC_CONTRACT_VERSION,
        "lane": lane,
        "workflowCount": workflow_count,
        "acceptedCount": accepted_count,
        "revisionCount": revision_count,
        "staleCount": stale_count,
        "medianContextTokens": median_context_tokens,
        "compressionRate": compression_rate,
        "retrievalMissRate": retrieval_miss_rate,
        "medianReviewCycles": median_review_cycles,
        "partialMetrics": partial,
        "notes": "",
    }
