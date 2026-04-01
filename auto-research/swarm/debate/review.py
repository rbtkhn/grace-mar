"""Advisory debate review for swarm-visible accepted artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .roles import (
    run_coordinator_review,
    run_critic_review,
    run_grounding_review,
    run_logic_review,
)
from .schema import ARTIFACT_SCHEMA_VERSION, normalize_role_review, validate_debate_artifact

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_USER = "grace-mar"

_ACTION_ORDER = {
    "promote_candidate": 0,
    "needs_operator_review": 1,
    "request_more_grounding": 2,
    "reject_artifact": 3,
}


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def load_target_artifact(artifact_path: Path) -> dict[str, Any]:
    return json.loads(artifact_path.read_text(encoding="utf-8"))


def debate_output_dir(*, user_id: str = DEFAULT_USER, repo_root: Path = REPO_ROOT) -> Path:
    return repo_root / "users" / user_id / "derived" / "debate"


def _target_projection(artifact: dict[str, Any]) -> dict[str, Any]:
    proposal = artifact.get("proposal") or {}
    candidate = proposal.get("candidate_bundle") or {}
    projection = artifact.get("proposal_projection") or {}
    return {
        "hypothesis": str(proposal.get("hypothesis") or "").strip(),
        "summary": str(candidate.get("summary") or projection.get("summary") or "").strip(),
        "suggested_entry": str(candidate.get("suggested_entry") or projection.get("suggested_entry") or "").strip(),
        "prompt_addition": str(candidate.get("prompt_addition") or projection.get("prompt_addition") or "").strip(),
        "scalar_at_accept": artifact.get("scalar_at_accept"),
    }


def synthesize_debate_artifact(
    artifact: dict[str, Any],
    *,
    artifact_path: Path,
    user_id: str = DEFAULT_USER,
) -> dict[str, Any]:
    grounding = run_grounding_review(artifact)
    logic = run_logic_review(artifact)
    critic = run_critic_review(artifact)
    coordinator = run_coordinator_review(
        artifact,
        grounding_review=grounding,
        logic_review=logic,
        critic_review=critic,
    )
    role_reviews = [
        normalize_role_review("coordinator", coordinator),
        normalize_role_review("grounding", grounding),
        normalize_role_review("logic", logic),
        normalize_role_review("critic", critic),
    ]

    actions = [review["recommended_action"] for review in role_reviews]
    action_set = set(actions)
    blocking_flags = sorted({flag for review in role_reviews for flag in review.get("risk_flags", [])})
    if len(action_set) == 1:
        consensus_level = "aligned"
    elif "reject_artifact" in action_set and "promote_candidate" in action_set:
        consensus_level = "contested"
    else:
        consensus_level = "mixed"

    final_recommendation = max(actions, key=lambda action: _ACTION_ORDER[action])
    promotion_readiness = {
        "promote_candidate": "ready",
        "needs_operator_review": "review",
        "request_more_grounding": "blocked",
        "reject_artifact": "blocked",
    }[final_recommendation]

    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "review_type": "swarm_debate_review",
        "generated_at": _timestamp(),
        "user_id": user_id,
        "mode": "advisory",
        "target_kind": "accepted_artifact",
        "target_artifact": {
            "artifact_path": str(artifact_path.resolve()),
            "artifact_relpath": _safe_relpath(artifact_path),
            "artifact_name": artifact_path.name,
        },
        "target_projection": _target_projection(artifact),
        "role_reviews": role_reviews,
        "blocking_flags": blocking_flags,
        "consensus_level": consensus_level,
        "promotion_readiness": promotion_readiness,
        "final_recommendation": final_recommendation,
    }
    errors = validate_debate_artifact(payload)
    if errors:
        raise ValueError("Invalid debate artifact: " + "; ".join(errors))
    return payload


def _review_filename(artifact_path: Path) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"debate-{artifact_path.stem}-{ts}.json"


def run_debate_review(
    artifact_path: Path,
    *,
    user_id: str = DEFAULT_USER,
    write: bool = True,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    resolved_path = artifact_path.resolve()
    if not resolved_path.is_file():
        raise ValueError(f"No accepted artifact found for debate review: {artifact_path}")

    artifact = load_target_artifact(resolved_path)
    review = synthesize_debate_artifact(artifact, artifact_path=resolved_path, user_id=user_id)
    output_dir = debate_output_dir(user_id=user_id, repo_root=repo_root)
    review_path = output_dir / _review_filename(resolved_path)
    review["review_path"] = str(review_path)
    review["review_relpath"] = _safe_relpath(review_path)
    if write:
        output_dir.mkdir(parents=True, exist_ok=True)
        review_path.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    return review


def format_debate_summary(review: dict[str, Any]) -> str:
    target = review.get("target_artifact") or {}
    projection = review.get("target_projection") or {}
    lines = [
        "Swarm debate review",
        f"user: {review.get('user_id', DEFAULT_USER)}",
        f"target: {target.get('artifact_relpath') or target.get('artifact_path') or '(unknown)'}",
        f"summary: {projection.get('summary') or '(no summary)'}",
        f"blocking flags: {', '.join(review.get('blocking_flags') or []) or 'none'}",
        f"consensus: {review.get('consensus_level', 'unknown')}",
        f"promotion readiness: {review.get('promotion_readiness', 'unknown')}",
        f"recommendation: {review.get('final_recommendation', 'unknown')}",
    ]
    return "\n".join(lines)
