"""Normalize disparate runtime/lane sources into workflow-observability-event-shaped dicts."""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVENT_SCHEMA_VERSION = "1.0.0-workflow-event"


def new_event_id() -> str:
    return str(uuid.uuid4())


def workflow_id_from_parts(*parts: str) -> str:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"wf_{h}"


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def event_from_runtime_trace_line(
    obj: dict[str, Any],
    *,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    """Map runtime worker trace JSON line to a workflow event."""
    run_id = str(obj.get("run_id") or "unknown")
    prov = obj.get("provenance") if isinstance(obj.get("provenance"), dict) else {}
    wr = prov.get("worker_routing") if isinstance(prov.get("worker_routing"), dict) else {}
    task_type = wr.get("task_type") or "unknown"
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("trace", run_id),
        "workflowType": f"runtime_inspect_{task_type}",
        "lane": "runtime-worker",
        "phase": "inspect",
        "startedAt": str(obj.get("timestamp") or "") or None,
        "completedAt": str(obj.get("timestamp") or "") or None,
        "status": str(obj.get("status") or "unknown"),
        "artifactType": "trace",
        "targetSurface": "",
        "reviewStatus": "",
        "reviewCycles": 0,
        "contextTokensLoaded": None,
        "compressionInvoked": None,
        "retrievalHits": None,
        "retrievalMisses": None,
        "operatorActions": 0,
        "touchedSurfaces": [],
        "derivedFromReceipt": True,
        "sourceKind": "runtime_trace",
        "sourcePath": source_path,
        "partialConfidence": "full",
        "notes": f"task_mode={obj.get('task_mode')}",
    }


def event_from_change_proposal(
    proposal: dict[str, Any],
    *,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    """Map Change Proposal v1 JSON to a workflow event."""
    pid = str(proposal.get("proposalId") or Path(source_path).stem)
    status = str(proposal.get("status") or "unknown")
    stale_guess = status in ("proposed", "under_review")
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("proposal", pid),
        "workflowType": "change_proposal",
        "lane": "change-review",
        "phase": "review_queue",
        "startedAt": str(proposal.get("createdAt") or "") or None,
        "completedAt": None,
        "status": status,
        "artifactType": "change_proposal",
        "targetSurface": str(proposal.get("targetSurface") or ""),
        "reviewStatus": status,
        "reviewCycles": 0,
        "contextTokensLoaded": None,
        "compressionInvoked": None,
        "retrievalHits": None,
        "retrievalMisses": None,
        "operatorActions": 0,
        "touchedSurfaces": _touched_surfaces(proposal),
        "derivedFromReceipt": False,
        "sourceKind": "change_proposal",
        "sourcePath": source_path,
        "partialConfidence": "full" if not stale_guess else "partial",
        "notes": f"changeType={proposal.get('changeType')}",
    }


def _touched_surfaces(proposal: dict[str, Any]) -> list[str]:
    out: list[str] = []
    ts = proposal.get("targetSurface")
    if isinstance(ts, str) and ts:
        out.append(ts)
    for s in proposal.get("secondaryScopes") or []:
        if isinstance(s, str) and s:
            out.append(s)
    return out


def event_from_observability_report_aggregate(
    report: dict[str, Any],
    *,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    """Single aggregate pseudo-event when per-proposal files are absent."""
    stale = int(report.get("staleReviewCount") or 0)
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("obs_report", str(report.get("reviewRoot") or "unknown")),
        "workflowType": "change_proposal_aggregate",
        "lane": "change-review",
        "phase": "rollup",
        "startedAt": str(report.get("generatedAt") or "") or None,
        "completedAt": _iso_now(),
        "status": "aggregate_snapshot",
        "artifactType": "observability_report",
        "targetSurface": "",
        "reviewStatus": "",
        "reviewCycles": 0,
        "contextTokensLoaded": None,
        "compressionInvoked": None,
        "retrievalHits": None,
        "retrievalMisses": None,
        "operatorActions": 0,
        "touchedSurfaces": [],
        "derivedFromReceipt": False,
        "sourceKind": "observability_report_aggregate",
        "sourcePath": source_path,
        "partialConfidence": "aggregate_only",
        "notes": f"staleReviewCount={stale}; proposalCounts embedded in source report",
    }


def event_from_workflow_depth_line(
    obj: dict[str, Any],
    *,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    """Map workflow-depth receipt JSON object."""
    rid = str(obj.get("run_id") or obj.get("receipt_id") or "unknown")
    mode = str(obj.get("effective_mode") or obj.get("workflow_depth") or "unknown")
    status = str(obj.get("status") or "unknown")
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("wf_depth", rid),
        "workflowType": "prepared_context_depth",
        "lane": str(obj.get("lane") or "prepared-context"),
        "phase": "budget",
        "startedAt": str(obj.get("timestamp") or "") or None,
        "completedAt": str(obj.get("timestamp") or "") or None,
        "status": status,
        "artifactType": "workflow_depth_receipt",
        "targetSurface": "",
        "reviewStatus": "",
        "reviewCycles": 0,
        "contextTokensLoaded": obj.get("tokens_loaded") if isinstance(obj.get("tokens_loaded"), int) else None,
        "compressionInvoked": bool(obj.get("compression")) if obj.get("compression") is not None else None,
        "retrievalHits": None,
        "retrievalMisses": None,
        "operatorActions": 0,
        "touchedSurfaces": [],
        "derivedFromReceipt": True,
        "sourceKind": "workflow_depth",
        "sourcePath": source_path,
        "partialConfidence": "partial",
        "notes": f"mode={mode}",
    }


def event_from_retrieval_miss_line(
    obj: dict[str, Any],
    *,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    ts = str(obj.get("timestamp") or "") or _iso_now()
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("ret_miss", ts, str(obj.get("query") or "")[:40]),
        "workflowType": "retrieval_miss",
        "lane": "retrieval",
        "phase": "retrieve",
        "startedAt": ts,
        "completedAt": ts,
        "status": "miss",
        "artifactType": "retrieval_miss",
        "targetSurface": "",
        "reviewStatus": "",
        "reviewCycles": 0,
        "contextTokensLoaded": None,
        "compressionInvoked": None,
        "retrievalHits": 0,
        "retrievalMisses": 1,
        "operatorActions": 0,
        "touchedSurfaces": [],
        "derivedFromReceipt": True,
        "sourceKind": "retrieval_miss",
        "sourcePath": source_path,
        "partialConfidence": "partial",
        "notes": "",
    }


def event_from_lane_observability(
    doc: dict[str, Any],
    *,
    lane: str,
    source_path: str,
    batch_id: str,
) -> dict[str, Any]:
    """Single summary event per lane observability JSON file."""
    return {
        "schemaVersion": EVENT_SCHEMA_VERSION,
        "eventId": new_event_id(),
        "batchId": batch_id,
        "workflowId": workflow_id_from_parts("lane_obs", lane, source_path),
        "workflowType": "lane_observability_snapshot",
        "lane": lane,
        "phase": "snapshot",
        "startedAt": str(doc.get("generatedAt") or "") or None,
        "completedAt": _iso_now(),
        "status": "ok",
        "artifactType": "lane_observability",
        "targetSurface": "",
        "reviewStatus": "",
        "reviewCycles": 0,
        "contextTokensLoaded": None,
        "compressionInvoked": None,
        "retrievalHits": None,
        "retrievalMisses": None,
        "operatorActions": 0,
        "touchedSurfaces": [],
        "derivedFromReceipt": False,
        "sourceKind": "lane_observability",
        "sourcePath": source_path,
        "partialConfidence": "aggregate_only",
        "notes": json.dumps({"keys": list(doc.keys())[:12]}),
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
