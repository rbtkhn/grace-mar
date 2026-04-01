"""Deterministic reviewer functions for advisory swarm debate."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
SELF_PROPOSALS_DIR = REPO_ROOT / "auto-research" / "self-proposals"
path_str = str(SELF_PROPOSALS_DIR)
if path_str not in sys.path:
    sys.path.insert(0, path_str)

from proposal_io import PLACEHOLDER_GROUNDING_RE


def _proposal(artifact: dict[str, Any]) -> dict[str, Any]:
    return artifact.get("proposal") or {}


def _candidate_bundle(artifact: dict[str, Any]) -> dict[str, Any]:
    return _proposal(artifact).get("candidate_bundle") or {}


def _source_exchange(artifact: dict[str, Any]) -> dict[str, Any]:
    raw_source = artifact.get("raw_source_exchange")
    if isinstance(raw_source, dict) and raw_source:
        return raw_source
    return _candidate_bundle(artifact).get("source_exchange") or {}


def _summary(artifact: dict[str, Any]) -> str:
    candidate = _candidate_bundle(artifact)
    summary = str(candidate.get("summary") or "").strip()
    if summary:
        return summary
    projection = artifact.get("proposal_projection") or {}
    return str(projection.get("summary") or "").strip()


def run_grounding_review(artifact: dict[str, Any]) -> dict[str, Any]:
    source_exchange = _source_exchange(artifact)
    if not source_exchange:
        return {
            "verdict": "fail",
            "why": "Artifact has no grounded source exchange to justify promotion.",
            "risk_flags": ["missing_grounding"],
            "evidence_refs": [],
            "recommended_action": "request_more_grounding",
        }

    placeholder_keys = [
        f"raw_source_exchange.{key}"
        for key, value in source_exchange.items()
        if PLACEHOLDER_GROUNDING_RE.search(str(value))
    ]
    if placeholder_keys:
        return {
            "verdict": "fail",
            "why": "Artifact still contains placeholder grounding and is not ready for governed review.",
            "risk_flags": ["placeholder_grounding"],
            "evidence_refs": placeholder_keys,
            "recommended_action": "request_more_grounding",
        }

    return {
        "verdict": "pass",
        "why": "Grounding is present and concrete enough for advisory review.",
        "risk_flags": [],
        "evidence_refs": [f"raw_source_exchange.{key}" for key in sorted(source_exchange)],
        "recommended_action": "promote_candidate",
    }


def run_logic_review(artifact: dict[str, Any]) -> dict[str, Any]:
    hard_gates = artifact.get("hard_gates") or {}
    failed_gates = [key for key, value in hard_gates.items() if value is False]
    if failed_gates:
        return {
            "verdict": "fail",
            "why": "Artifact carries failed hard gates and should not advance as-is.",
            "risk_flags": ["failed_hard_gate"],
            "evidence_refs": [f"hard_gates.{key}" for key in failed_gates],
            "recommended_action": "reject_artifact",
        }

    proposal = _proposal(artifact)
    candidate = _candidate_bundle(artifact)
    missing_fields = [
        field
        for field in ("summary", "suggested_entry", "prompt_addition")
        if not str(candidate.get(field) or "").strip()
    ]
    if not str(proposal.get("hypothesis") or "").strip():
        missing_fields.append("hypothesis")
    if missing_fields:
        return {
            "verdict": "caution",
            "why": "Artifact is reviewable, but its reasoning projection is incomplete.",
            "risk_flags": ["incomplete_projection"],
            "evidence_refs": missing_fields,
            "recommended_action": "needs_operator_review",
        }

    return {
        "verdict": "pass",
        "why": "Artifact contains a coherent hypothesis and complete proposal projection.",
        "risk_flags": [],
        "evidence_refs": ["proposal.hypothesis", "proposal.candidate_bundle.summary"],
        "recommended_action": "promote_candidate",
    }


def run_critic_review(artifact: dict[str, Any]) -> dict[str, Any]:
    scalar = artifact.get("scalar_at_accept")
    if not isinstance(scalar, (int, float)):
        return {
            "verdict": "caution",
            "why": "Artifact lacks a transparent acceptance scalar, so confidence should stay advisory.",
            "risk_flags": ["missing_accept_scalar"],
            "evidence_refs": [],
            "recommended_action": "needs_operator_review",
        }

    if float(scalar) < 0.85:
        return {
            "verdict": "caution",
            "why": "Acceptance scalar is modest, so promotion should face stronger operator scrutiny.",
            "risk_flags": ["low_accept_score"],
            "evidence_refs": ["scalar_at_accept"],
            "recommended_action": "needs_operator_review",
        }

    if len(_summary(artifact)) < 25:
        return {
            "verdict": "caution",
            "why": "Artifact summary is too thin to trust as a strong promotion candidate.",
            "risk_flags": ["thin_summary"],
            "evidence_refs": ["proposal_projection.summary"],
            "recommended_action": "needs_operator_review",
        }

    return {
        "verdict": "pass",
        "why": "Critic found no strong rejection signal in the current artifact projection.",
        "risk_flags": [],
        "evidence_refs": ["scalar_at_accept", "proposal_projection.summary"],
        "recommended_action": "promote_candidate",
    }


def run_coordinator_review(
    artifact: dict[str, Any],
    *,
    grounding_review: dict[str, Any],
    logic_review: dict[str, Any],
    critic_review: dict[str, Any],
) -> dict[str, Any]:
    risk_flags = sorted(
        {
            *grounding_review.get("risk_flags", []),
            *logic_review.get("risk_flags", []),
            *critic_review.get("risk_flags", []),
        }
    )
    if "failed_hard_gate" in risk_flags:
        return {
            "verdict": "fail",
            "why": "Coordinator sees a failed hard gate and recommends stopping promotion.",
            "risk_flags": risk_flags,
            "evidence_refs": logic_review.get("evidence_refs", []),
            "recommended_action": "reject_artifact",
        }
    if "missing_grounding" in risk_flags or "placeholder_grounding" in risk_flags:
        return {
            "verdict": "fail",
            "why": "Coordinator sees grounding risk that should be repaired before promotion.",
            "risk_flags": risk_flags,
            "evidence_refs": grounding_review.get("evidence_refs", []),
            "recommended_action": "request_more_grounding",
        }
    if risk_flags:
        return {
            "verdict": "caution",
            "why": "Coordinator sees useful work, but still wants operator review before promotion.",
            "risk_flags": risk_flags,
            "evidence_refs": critic_review.get("evidence_refs", []),
            "recommended_action": "needs_operator_review",
        }

    return {
        "verdict": "pass",
        "why": "Coordinator sees aligned grounding, logic, and critic passes for advisory promotion readiness.",
        "risk_flags": [],
        "evidence_refs": ["proposal.hypothesis", "raw_source_exchange", "scalar_at_accept"],
        "recommended_action": "promote_candidate",
    }
