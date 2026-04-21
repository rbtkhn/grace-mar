"""Shared reduce helpers for workflow observability reports (batch-only)."""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from typing import Any


def median_or_none(values: list[float]) -> float | None:
    nums = [float(v) for v in values if isinstance(v, (int, float))]
    if not nums:
        return None
    return float(statistics.median(nums))


def aggregate_events(events: list[dict[str, Any]], *, batch_id: str, sources_used: list[str]) -> dict[str, Any]:
    """Build workflow-observability-report-shaped dict."""
    from datetime import datetime, timezone

    by_wf: Counter[str] = Counter()
    by_lane: Counter[str] = Counter()
    acceptance = 0
    revision = 0
    stale = 0
    review_cycles: list[float] = []
    tokens: list[float] = []
    miss_flags: list[float] = []

    for e in events:
        wt = str(e.get("workflowType") or "unknown")
        by_wf[wt] += 1
        by_lane[str(e.get("lane") or "unknown")] += 1
        st = str(e.get("status") or "").lower()
        if st in ("approved", "accepted", "superseded"):
            acceptance += 1
        elif st in ("rejected", "partial", "error"):
            revision += 1
        if st in ("stale", "stuck") or (
            e.get("partialConfidence") == "partial" and st in ("proposed", "under_review")
        ):
            stale += 1
        rc = e.get("reviewCycles")
        if isinstance(rc, (int, float)):
            review_cycles.append(float(rc))
        ct = e.get("contextTokensLoaded")
        if isinstance(ct, (int, float)):
            tokens.append(float(ct))
        rm = e.get("retrievalMisses")
        if isinstance(rm, (int, float)) and rm > 0:
            miss_flags.append(1.0)
        elif isinstance(rm, (int, float)):
            miss_flags.append(0.0)

    retrieval_miss_rate = (
        sum(miss_flags) / len(miss_flags) if miss_flags else (len([e for e in events if e.get("workflowType") == "retrieval_miss"]) / max(len(events), 1))
    )

    # Friction hotspots: lanes with highest median reviewCycles (or event volume)
    lane_rc: dict[str, list[float]] = defaultdict(list)
    for e in events:
        lane = str(e.get("lane") or "unknown")
        rc = e.get("reviewCycles")
        if isinstance(rc, (int, float)):
            lane_rc[lane].append(float(rc))
    hotspots: list[dict[str, Any]] = []
    for lane, rcs in lane_rc.items():
        if rcs:
            hotspots.append(
                {
                    "label": f"{lane}_median_rc",
                    "lane": lane,
                    "workflowType": "",
                    "score": float(statistics.median(rcs)),
                }
            )
    hotspots.sort(key=lambda x: -x["score"])
    if not hotspots:
        for lane, n in by_lane.most_common(5):
            hotspots.append({"label": f"{lane}_volume", "lane": lane, "workflowType": "", "score": float(n)})

    leverage: list[dict[str, Any]] = []
    for e in events:
        if str(e.get("workflowType") or "") == "change_proposal" and str(e.get("status") or "").lower() in (
            "approved",
            "superseded",
        ):
            leverage.append(
                {
                    "label": str(e.get("workflowId") or ""),
                    "lane": str(e.get("lane") or ""),
                    "workflowType": "change_proposal",
                    "score": 1.0,
                }
            )
    leverage.sort(key=lambda x: -x["score"])
    leverage = leverage[:5]

    partial = any(
        e.get("partialConfidence") in ("partial", "inferred", "aggregate_only") for e in events
    )

    return {
        "schemaVersion": "1.0.0-workflow-report",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "batchId": batch_id,
        "partialMetrics": partial,
        "eventCount": len(events),
        "totalsByWorkflowType": dict(by_wf),
        "totalsByLane": dict(by_lane),
        "acceptanceCount": acceptance,
        "revisionCount": revision,
        "staleCount": stale,
        "medianTimeToFirstReviewSeconds": None,
        "medianTimeToMergeSeconds": None,
        "medianContextTokensLoaded": median_or_none(tokens),
        "compressionRate": None,
        "retrievalMissRate": float(retrieval_miss_rate) if retrieval_miss_rate is not None else None,
        "medianReviewCycles": median_or_none(review_cycles),
        "reviewFrictionHotspots": hotspots[:5],
        "leverageCandidates": leverage[:5],
        "sourcesUsed": sources_used,
        "notes": [],
    }
