"""Schema helpers for advisory swarm debate artifacts."""

from __future__ import annotations

from typing import Any

ARTIFACT_SCHEMA_VERSION = 1
ROLE_NAMES = ("coordinator", "grounding", "logic", "critic")
ROLE_VERDICTS = {"pass", "caution", "fail"}
FINAL_RECOMMENDATIONS = {
    "promote_candidate",
    "needs_operator_review",
    "request_more_grounding",
    "reject_artifact",
}


def normalize_role_review(role: str, payload: dict[str, Any]) -> dict[str, Any]:
    verdict = str(payload.get("verdict") or "caution").strip().lower()
    if verdict not in ROLE_VERDICTS:
        verdict = "caution"

    recommended_action = str(payload.get("recommended_action") or "needs_operator_review").strip().lower()
    if recommended_action not in FINAL_RECOMMENDATIONS:
        recommended_action = "needs_operator_review"

    risk_flags = payload.get("risk_flags") or []
    evidence_refs = payload.get("evidence_refs") or []
    return {
        "role": role,
        "verdict": verdict,
        "why": str(payload.get("why") or "").strip(),
        "risk_flags": [str(flag).strip() for flag in risk_flags if str(flag).strip()],
        "evidence_refs": [str(ref).strip() for ref in evidence_refs if str(ref).strip()],
        "recommended_action": recommended_action,
    }


def validate_debate_artifact(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("artifact_schema_version") != ARTIFACT_SCHEMA_VERSION:
        errors.append("artifact_schema_version must equal 1")
    if payload.get("review_type") != "swarm_debate_review":
        errors.append("review_type must equal swarm_debate_review")
    if str(payload.get("user_id") or "").strip() == "":
        errors.append("user_id is required")
    target = payload.get("target_artifact") or {}
    if str(target.get("artifact_path") or "").strip() == "":
        errors.append("target_artifact.artifact_path is required")
    if payload.get("final_recommendation") not in FINAL_RECOMMENDATIONS:
        errors.append("final_recommendation must be a valid recommendation")

    role_reviews = payload.get("role_reviews")
    if not isinstance(role_reviews, list) or len(role_reviews) != len(ROLE_NAMES):
        errors.append("role_reviews must contain exactly four reviewer outputs")
    else:
        seen_roles = {str(review.get("role") or "") for review in role_reviews}
        if seen_roles != set(ROLE_NAMES):
            errors.append("role_reviews must contain coordinator, grounding, logic, and critic")
    return errors
