"""
Persisted boundary classification for recursion-gate candidates.

Builds schema-shaped artifacts (boundary-classification.v1) from parse_review_candidates
rows and optional boundary_review hints. See docs/boundary-review-queue.md.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Default proposal_class when reclassifying toward a record surface (ADD suffix).
_SURFACE_TO_ADD_CLASS: dict[tuple[str, str | None], str] = {
    ("self_knowledge", None): "SELF_KNOWLEDGE_ADD",
    ("self_library", None): "SELF_LIBRARY_ADD",
    ("self_library", "civ_mem"): "CIV_MEM_ADD",
    ("self_skills", None): "SELF_KNOWLEDGE_ADD",
    ("self_evidence", None): "SELF_KNOWLEDGE_ADD",
    ("work_layer", None): "META_INFRA",
}


def infer_surface_from_proposal_class(proposal_class: str) -> tuple[str, str | None]:
    """
    Map gate proposal_class to export-style surface + optional civ_mem subsurface.
    """
    pc = (proposal_class or "").strip().upper()
    if pc.startswith("CIV_MEM"):
        return "self_library", "civ_mem"
    if pc.startswith("SELF_LIBRARY"):
        return "self_library", None
    if pc.startswith("META_INFRA") or pc.startswith("SIMULATION_RESULT"):
        return "work_layer", None
    if "SKILL" in pc or pc.startswith("SKILLS"):
        return "self_skills", None
    if "EVIDENCE" in pc or "ACT-" in pc:
        return "self_evidence", None
    return "self_knowledge", None


def _display_to_artifact_surface(display: str | None) -> tuple[str, str | None]:
    """Map boundary_review display labels to (surface, subsurface)."""
    d = (display or "").strip().upper()
    if not d:
        return "self_knowledge", None
    if "WORK" in d and "LAYER" in d:
        return "work_layer", None
    if "CIV-MEM" in d:
        return "self_library", "civ_mem"
    if "SELF-LIBRARY" in d:
        return "self_library", None
    if d == "SELF-KNOWLEDGE":
        return "self_knowledge", None
    return "self_knowledge", None


def _boundary_status(misfiled: bool, surface_current: str, surface_suggested: str, sub_c: str | None, sub_s: str | None) -> str:
    if misfiled:
        return "misaligned"
    if surface_current != surface_suggested or sub_c != sub_s:
        return "ambiguous"
    return "clear"


def _confidence_score(band: str | None) -> float:
    return {"high": 0.85, "medium": 0.55, "low": 0.25}.get((band or "").lower(), 0.5)


def suggested_reclassify_proposal_class(
    surface_suggested: str,
    subsurface_suggested: str | None,
    current_proposal_class: str,
) -> str | None:
    """
    Proposal class for one-click reclassify toward the suggested surface.
    Uses ADD/REVISE to mirror the current row's verb when possible.
    """
    cur = (current_proposal_class or "").strip().upper()
    use_revise = "_REVISE" in cur
    key = (surface_suggested, subsurface_suggested)
    base = _SURFACE_TO_ADD_CLASS.get(key)
    if not base:
        return None
    if use_revise and base.endswith("_ADD"):
        rev = base.replace("_ADD", "_REVISE")
        if rev in ("SELF_KNOWLEDGE_REVISE", "SELF_LIBRARY_REVISE", "CIV_MEM_REVISE"):
            return rev
        return base
    return base


def review_surface_token_to_classifier_tuple(token: str) -> tuple[str, str | None]:
    """Map gate_review_normalize surface token to (surfaceSuggested, subsurfaceSuggested)."""
    x = (token or "").strip().lower()
    if x == "civ_mem":
        return "self_library", "civ_mem"
    if x == "self_library":
        return "self_library", None
    if x == "work_layer":
        return "work_layer", None
    if x in ("self", "self_knowledge"):
        return "self_knowledge", None
    if x == "skills":
        return "self_skills", None
    if x == "evidence":
        return "self_evidence", None
    return "self_knowledge", None


def build_boundary_classification(row: dict[str, Any], *, user_slug: str, source: str = "recursion_gate_review") -> dict[str, Any]:
    """Build a boundary-classification.v1 dict from a parse_review_candidates row."""
    br = row.get("boundary_review") if isinstance(row.get("boundary_review"), dict) else {}
    candidate_id = row["id"]
    pc_cur = (row.get("proposal_class") or "").strip() or "SELF_KNOWLEDGE_ADD"

    t_disp = br.get("target_surface")
    s_disp = br.get("suggested_surface") or t_disp
    surface_current, sub_c = _display_to_artifact_surface(t_disp)
    surface_suggested, sub_s = _display_to_artifact_surface(s_disp)

    misfiled = bool((br.get("misfiled_warning") or "").strip())
    reasons = list(br.get("hint_reasons") or [])
    if isinstance(reasons, list):
        why = [str(x) for x in reasons if str(x).strip()]
    else:
        why = []
    mw = (br.get("misfiled_warning") or "").strip()
    if mw:
        why.append(mw)
    band = (br.get("confidence") or "medium").strip().lower()
    if band not in ("high", "medium", "low"):
        band = "medium"

    prop_suggested = suggested_reclassify_proposal_class(surface_suggested, sub_s, pc_cur)

    status = _boundary_status(misfiled, surface_current, surface_suggested, sub_c, sub_s)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    out: dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "candidateId": candidate_id,
        "userSlug": user_slug,
        "proposalClassCurrent": pc_cur,
        "surfaceCurrent": surface_current,
        "surfaceSuggested": surface_suggested,
        "subsurfaceSuggested": sub_s,
        "boundaryStatus": status,
        "misfiled": misfiled,
        "why": why,
        "confidenceBand": band,
        "confidenceScore": _confidence_score(band),
        "createdAt": now,
        "source": source,
    }
    if prop_suggested:
        out["proposalClassSuggested"] = prop_suggested
    rel = f"review-queue/boundary-classifications/{_candidate_artifact_basename(candidate_id)}"
    out["artifactRelPath"] = rel
    return out


def _candidate_artifact_basename(candidate_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", candidate_id).strip("-") or "candidate"
    return safe if safe.endswith(".json") else f"{safe}.json"


def boundary_classification_path(user_slug: str, candidate_id: str, repo_root: Path) -> Path:
    base = repo_root / "users" / user_slug / "review-queue" / "boundary-classifications"
    return base / _candidate_artifact_basename(candidate_id)


def write_boundary_classification(user_slug: str, row: dict[str, Any], repo_root: Path) -> Path | None:
    """
    Write boundary-classification JSON for one row. Returns path or None if skipped.
    """
    if row.get("status") != "pending":
        return None
    data = build_boundary_classification(row, user_slug=user_slug)
    path = boundary_classification_path(user_slug, row["id"], repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def sync_boundary_classification_artifact(user_slug: str, row: dict[str, Any], *, repo_root: Path) -> Path | None:
    """Alias for write_boundary_classification (parse-time sync)."""
    return write_boundary_classification(user_slug, row, repo_root)


__all__ = [
    "boundary_classification_path",
    "build_boundary_classification",
    "infer_surface_from_proposal_class",
    "review_surface_token_to_classifier_tuple",
    "suggested_reclassify_proposal_class",
    "sync_boundary_classification_artifact",
    "write_boundary_classification",
]
