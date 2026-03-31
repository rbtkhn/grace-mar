#!/usr/bin/env python3
"""
Normalize RECURSION-GATE candidate rows (from parse_review_candidates) for review UIs
and change-review queue-shaped exports. See docs/identity-fork-protocol.md — canonical
change review object.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_GRACE_SRC = Path(__file__).resolve().parents[1] / "src"
if _GRACE_SRC.is_dir() and str(_GRACE_SRC) not in sys.path:
    sys.path.insert(0, str(_GRACE_SRC))

from grace_mar.merge.boundary_classifier import (  # noqa: E402
    review_surface_token_to_classifier_tuple,
    suggested_reclassify_proposal_class,
)


def _map_boundary_surface_to_token(display: str | None) -> str:
    """Map boundary_review display labels to schema surface tokens (review UI / queue)."""
    s = (display or "").strip().upper()
    if s in ("WORK-LAYER", "WORK LAYER"):
        return "work_layer"
    if "CIV-MEM" in s:
        return "civ_mem"
    if "SELF-LIBRARY" in s:
        return "self_library"
    if s == "SELF-KNOWLEDGE":
        return "self"
    return "self"


def _risk_tier_to_queue_risk(tier: str | None) -> str:
    t = (tier or "").strip()
    if t == "quick_merge_eligible":
        return "low"
    if t == "manual_escalate":
        return "high"
    return "medium"


def _materiality_from_row(row: dict[str, Any]) -> str:
    m = row.get("materiality")
    if m in ("low", "medium", "high", "critical"):
        return str(m)
    return _risk_tier_to_materiality(row.get("risk_tier"))


def _risk_tier_to_materiality(tier: str | None) -> str:
    t = (tier or "").strip()
    if t == "quick_merge_eligible":
        return "low"
    if t == "manual_escalate":
        return "high"
    return "medium"


def _evidence_count_from_row(row: dict[str, Any]) -> int:
    refs = row.get("evidence_refs")
    if isinstance(refs, list):
        return len(refs)
    raw = row.get("raw_block") or ""
    return len(re.findall(r"^evidence_id:\s*\S", raw, re.MULTILINE))


def normalize_review_item(row: dict[str, Any]) -> dict[str, Any]:
    """
    Build a unified review-shaped dict from one parse_review_candidates row.
    Keys use snake_case for JSON/HTML consumption.
    """
    boundary = row.get("boundary_review") or {}
    if not isinstance(boundary, dict):
        boundary = {}
    target_surface = _map_boundary_surface_to_token(boundary.get("target_surface"))
    suggested_raw = boundary.get("suggested_surface") or boundary.get("target_surface")
    suggested_surface = _map_boundary_surface_to_token(suggested_raw)
    misfiled = bool((boundary.get("misfiled_warning") or "").strip())
    requires_reclassification = misfiled or (suggested_surface != target_surface)
    review_type = "boundary" if requires_reclassification else "routine"
    risk_level = _risk_tier_to_queue_risk(row.get("risk_tier"))
    materiality = _materiality_from_row(row)
    pc = (row.get("proposal_class") or "").strip() or "SELF_KNOWLEDGE_ADD"
    band = (boundary.get("confidence") or "medium").strip().lower()
    if band not in ("high", "medium", "low"):
        band = "medium"
    band_to_score = {"high": 0.85, "medium": 0.55, "low": 0.25}
    surf_s, sub_s = review_surface_token_to_classifier_tuple(suggested_surface)
    sug_pc = suggested_reclassify_proposal_class(surf_s, sub_s, pc)
    misfiled_warning = (boundary.get("misfiled_warning") or "").strip()
    hint_reasons = boundary.get("hint_reasons") if isinstance(boundary.get("hint_reasons"), list) else []
    hint_reasons = [str(x) for x in hint_reasons if str(x).strip()]
    return {
        "candidate_id": row["id"],
        "summary": row.get("summary") or "(no summary)",
        "proposal_class": pc,
        "target_surface": target_surface,
        "suggested_surface": suggested_surface,
        "materiality": materiality,
        "review_type": review_type,
        "risk_level": risk_level,
        "status": row.get("status") or "pending",
        "requires_reclassification": requires_reclassification,
        "canonical_path": (row.get("canonical_path") or "").strip(),
        "confidence_after": row.get("confidence_after"),
        "boundary_confidence": band,
        "boundary_confidence_score": band_to_score.get(band, 0.5),
        "boundary_misfiled_warning": misfiled_warning,
        "boundary_hint_reasons": hint_reasons,
        "suggested_reclassify_proposal_class": sug_pc,
        "evidence_count": _evidence_count_from_row(row),
        "ready_for_quick_merge": bool(row.get("ready_for_quick_merge")),
        "territory_label": row.get("territory_label") or "",
        "channel_key": row.get("channel_key") or "—",
        "timestamp": row.get("timestamp") or "—",
        "age_days": row.get("age_days"),
        "territory": row.get("territory") or "",
        "signal_type": (row.get("signal_type") or "").strip(),
        "duplicate_hints": row.get("duplicate_hints") or [],
    }


__all__ = ["normalize_review_item"]
