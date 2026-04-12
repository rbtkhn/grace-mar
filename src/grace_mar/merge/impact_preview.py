"""Predict which files and sections a candidate will touch on merge.

Pure function over candidate metadata — no file I/O, no side effects.
Mirrors the routing logic in process_approved_candidates.merge_candidate_in_memory
so the operator can see impact *before* approving.
"""

from __future__ import annotations


def _classify_surface(mind_category: str, profile_target: str) -> str:
    cat = (mind_category or "").lower()
    pt = (profile_target or "").upper()
    if "knowledge" in cat or "IX-A" in pt:
        return "IX-A"
    if "curiosity" in cat or "IX-B" in pt:
        return "IX-B"
    return "IX-C"


def _prompt_effect(candidate: dict) -> str:
    mode = (candidate.get("prompt_merge_mode") or "").strip().lower()
    if mode == "rebuild_ix":
        return "rebuild"
    addition = (candidate.get("prompt_addition") or "").strip().lower()
    if addition and addition != "none":
        return "append"
    return "none"


def _prompt_section_label(candidate: dict, surface: str) -> str:
    section = (candidate.get("prompt_section") or "").strip()
    if section:
        return section
    if surface == "IX-A":
        return "YOUR KNOWLEDGE"
    if surface == "IX-B":
        return "YOUR CURIOSITY"
    return "YOUR PERSONALITY"


def preview_candidate_impact(
    candidate: dict,
    user_id: str = "grace-mar",
) -> dict:
    """Predict which files a candidate will touch on merge.

    Args:
        candidate: Dict with at least mind_category, profile_target, and
            the optional prompt/evidence fields from get_approved_in_candidates.
        user_id: Instance user id for path construction.

    Returns a dict with:
        candidate_id, surface, files_touched, sections_touched,
        prompt_effect, prompt_section, boundary_flags, risk_factors.
    """
    cid = candidate.get("id") or "(unknown)"
    cat = (candidate.get("mind_category") or "knowledge").strip().lower()
    pt = (candidate.get("profile_target") or "IX-A. KNOWLEDGE").strip()
    evidence_type = (candidate.get("evidence_record_type") or "act").strip().lower()
    proposal_class = (candidate.get("proposal_class") or "").strip().upper()

    surface = _classify_surface(cat, pt)
    prompt_eff = _prompt_effect(candidate)

    base = f"users/{user_id}"
    files: list[str] = []
    sections: list[str] = []

    files.append(f"{base}/self.md")
    sections.append(surface)

    files.append(f"{base}/self-archive.md")
    sections.append("ACT log")
    if evidence_type == "read":
        sections.append("Reading list")
    elif evidence_type == "write":
        sections.append("Writing log")

    if prompt_eff != "none":
        files.append("bot/prompt.py")
        p_section = _prompt_section_label(candidate, surface)
        if prompt_eff == "rebuild":
            sections.append(f"prompt (rebuild from IX)")
        else:
            sections.append(f"prompt ({p_section})")

    files.append(f"{base}/recursion-gate.md")
    sections.append("Candidates → Processed")

    files.append(f"{base}/session-log.md")
    sections.append("Session log entry")

    if any(tok in proposal_class for tok in ("SELF_LIBRARY", "CIV_MEM", "LIBRARY_")):
        files.append(f"{base}/self-library.md")
        sections.append("Self-library")

    if "SKILLS" in proposal_class:
        files.append(f"{base}/self-skills.md")
        sections.append("Skills")

    boundary_flags: list[str] = []
    risk_factors: list[str] = []

    boundary = candidate.get("boundary_review")
    if isinstance(boundary, dict):
        target_surf = (boundary.get("target_surface") or "").strip().upper()
        suggested_surf = (boundary.get("suggested_surface") or "").strip().upper()
        if suggested_surf and target_surf and suggested_surf != target_surf:
            boundary_flags.append("reclassification_needed")
            risk_factors.append("boundary_reclassification")
        if (boundary.get("misfiled_warning") or "").strip():
            boundary_flags.append("misfiled_warning")
            risk_factors.append("misfiled")

    if prompt_eff == "rebuild":
        risk_factors.append("prompt_rebuild")
    if len(files) > 4:
        risk_factors.append("multi_surface")

    return {
        "candidate_id": cid,
        "surface": surface,
        "files_touched": files,
        "sections_touched": sections,
        "prompt_effect": prompt_eff,
        "prompt_section": _prompt_section_label(candidate, surface) if prompt_eff != "none" else None,
        "boundary_flags": boundary_flags,
        "risk_factors": risk_factors,
    }


def format_impact_summary(impact: dict) -> str:
    """One-line human-readable summary of an impact preview."""
    cid = impact["candidate_id"]
    surface = impact["surface"]
    n_files = len(impact["files_touched"])
    prompt = impact["prompt_effect"]
    flags = impact["boundary_flags"]

    parts = [f"{cid}: {surface}, {n_files} files"]
    if prompt != "none":
        parts.append(f"prompt={prompt}")
    if flags:
        parts.append(f"flags={','.join(flags)}")
    return " | ".join(parts)
