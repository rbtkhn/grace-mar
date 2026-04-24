#!/usr/bin/env python3
"""
Export a bounded inter-fork collaboration package.

The package is non-canonical transport material only. It does not authorize the
sender to write into another fork's namespace or bypass the recipient's gate.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional dependency
    jsonschema = None  # type: ignore[assignment]

try:
    from repo_io import DEFAULT_USER_ID, profile_dir
except ImportError:
    from scripts.repo_io import DEFAULT_USER_ID, profile_dir

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "inter-fork-package-envelope.v1.json"
BOUNDARY_NOTICE = (
    "This package is bounded inter-fork transport only. The recipient fork must import "
    "and review it locally; the sender has no recipient-side merge authority."
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _default_output_dir(
    sender_fork_id: str,
    *,
    profile_lookup: Callable[[str], Path] = profile_dir,
) -> Path:
    return profile_lookup(sender_fork_id) / "artifacts" / "inter-fork" / "packages"


def _default_routing_hint(package_kind: str) -> str:
    return "change_proposal_review" if package_kind == "change_proposal_review" else "candidate_import"


def _default_proposal_class(target_surface: str) -> str:
    return {
        "self": "identity",
        "self_library": "library",
        "civ_mem": "library",
        "skills": "skills",
        "evidence": "evidence",
        "work_layer": "policy",
    }.get(target_surface, "policy")


def _load_schema(repo_root: Path) -> dict:
    return json.loads((repo_root / "schema-registry" / "inter-fork-package-envelope.v1.json").read_text(encoding="utf-8"))


def build_inter_fork_package(
    *,
    sender_fork_id: str,
    intended_recipient_fork_id: str,
    package_kind: str,
    summary: str,
    body: str,
    supporting_refs: list[str],
    routing_hint: str,
    payload: dict,
) -> dict:
    package_id = f"ifpkg-{uuid.uuid4()}"
    return {
        "$schema": "schema-registry/inter-fork-package-envelope.v1.json",
        "schemaVersion": "1.0.0",
        "format": "grace-mar-inter-fork-package",
        "packageId": package_id,
        "createdAt": _utc_now_iso(),
        "senderForkId": sender_fork_id,
        "intendedRecipientForkId": intended_recipient_fork_id,
        "packageKind": package_kind,
        "routingHint": routing_hint,
        "summary": summary,
        "body": body,
        "boundaryNotice": BOUNDARY_NOTICE,
        "humanReviewRequired": True,
        "canonicalSurfacesTouched": False,
        "supportingRefs": supporting_refs,
        "payload": payload,
    }


def build_candidate_payload(
    *,
    suggested_target_surface: str,
    claim: str,
    review_notes: str,
) -> dict:
    return {
        "mode": "candidate_import",
        "suggestedTargetSurface": suggested_target_surface,
        "claim": claim,
        "reviewNotes": review_notes,
    }


def build_change_proposal_payload(
    *,
    primary_scope: str,
    secondary_scopes: list[str],
    change_type: str,
    target_surface: str,
    materiality: str,
    review_type: str,
    risk_level: str,
    prior_state_ref: str,
    proposed_state_ref: str,
    proposal_class: str | None,
    notes: str,
) -> dict:
    payload = {
        "mode": "change_proposal_review",
        "primaryScope": primary_scope,
        "secondaryScopes": secondary_scopes,
        "changeType": change_type,
        "targetSurface": target_surface,
        "materiality": materiality,
        "reviewType": review_type,
        "riskLevel": risk_level,
        "priorStateRef": prior_state_ref,
        "proposedStateRef": proposed_state_ref,
        "proposalClass": proposal_class or _default_proposal_class(target_surface),
    }
    if notes.strip():
        payload["notes"] = notes.strip()
    return payload


def export_inter_fork_package(
    *,
    sender_fork_id: str,
    intended_recipient_fork_id: str,
    package_kind: str,
    summary: str,
    body: str = "",
    supporting_refs: list[str] | None = None,
    routing_hint: str | None = None,
    payload: dict,
    output_dir: Path | None = None,
    repo_root: Path = REPO_ROOT,
    profile_lookup: Callable[[str], Path] = profile_dir,
    validate_schema: bool = True,
) -> Path:
    refs = [ref for ref in (supporting_refs or []) if ref.strip()]
    route = routing_hint or _default_routing_hint(package_kind)
    package = build_inter_fork_package(
        sender_fork_id=sender_fork_id,
        intended_recipient_fork_id=intended_recipient_fork_id,
        package_kind=package_kind,
        summary=summary,
        body=body,
        supporting_refs=refs,
        routing_hint=route,
        payload=payload,
    )

    if validate_schema and jsonschema is not None:
        jsonschema.Draft202012Validator(_load_schema(repo_root)).validate(package)

    out_dir = output_dir or _default_output_dir(sender_fork_id, profile_lookup=profile_lookup)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{package['packageId']}.json"
    out_path.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a bounded inter-fork collaboration package")
    parser.add_argument("-u", "--sender", default=DEFAULT_USER_ID, help="Sender fork id")
    parser.add_argument("--recipient", required=True, help="Intended recipient fork id")
    parser.add_argument(
        "--package-kind",
        required=True,
        choices=("evidence_share", "strategy_peer_review", "pointer_bundle", "change_proposal_review"),
    )
    parser.add_argument("--summary", required=True, help="Short recipient-facing summary")
    parser.add_argument("--body", default="", help="Optional body text")
    parser.add_argument("--supporting-ref", action="append", default=[], help="Supporting repo-relative ref")
    parser.add_argument(
        "--routing-hint",
        choices=("candidate_import", "change_proposal_review"),
        default=None,
        help="Override default recipient routing hint",
    )
    parser.add_argument(
        "--suggested-target-surface",
        default="work_layer",
        choices=("self", "self_library", "civ_mem", "skills", "evidence", "work_layer"),
        help="Suggested target surface for candidate import packages",
    )
    parser.add_argument("--claim", default="", help="Optional candidate-import claim")
    parser.add_argument("--review-notes", default="", help="Optional recipient review notes")
    parser.add_argument(
        "--primary-scope",
        choices=("identity", "curiosity", "pedagogy", "expression", "memory_governance", "safety", "preference", "upgrade_collision"),
        default="identity",
    )
    parser.add_argument(
        "--secondary-scope",
        action="append",
        default=[],
        dest="secondary_scopes",
        choices=("identity", "curiosity", "pedagogy", "expression", "memory_governance", "safety", "preference", "upgrade_collision"),
    )
    parser.add_argument(
        "--change-type",
        choices=("contradiction", "refinement", "expansion", "deprecation", "ambiguity", "policy_collision", "template_instance_collision"),
        default="refinement",
    )
    parser.add_argument(
        "--target-surface",
        choices=("self", "self_library", "civ_mem", "skills", "evidence", "work_layer"),
        default="self",
    )
    parser.add_argument("--materiality", choices=("low", "medium", "high", "critical"), default="medium")
    parser.add_argument("--review-type", choices=("routine", "extended", "boundary", "policy", "collision"), default="routine")
    parser.add_argument("--risk-level", choices=("low", "medium", "high"), default="low")
    parser.add_argument("--prior-state-ref", default="REPLACE_WITH_PRIOR_GOVERNED_STATE_REF")
    parser.add_argument("--proposed-state-ref", default="REPLACE_WITH_PROPOSED_STATE_REF")
    parser.add_argument(
        "--proposal-class",
        choices=("identity", "library", "skills", "evidence", "policy", "work_politics"),
        default=None,
    )
    parser.add_argument("--notes", default="", help="Optional change-proposal notes")
    parser.add_argument("-o", "--output-dir", default="", help="Output directory")
    args = parser.parse_args()

    route = args.routing_hint or _default_routing_hint(args.package_kind)
    if route == "change_proposal_review":
        payload = build_change_proposal_payload(
            primary_scope=args.primary_scope,
            secondary_scopes=list(dict.fromkeys(args.secondary_scopes)),
            change_type=args.change_type,
            target_surface=args.target_surface,
            materiality=args.materiality,
            review_type=args.review_type,
            risk_level=args.risk_level,
            prior_state_ref=args.prior_state_ref,
            proposed_state_ref=args.proposed_state_ref,
            proposal_class=args.proposal_class,
            notes=args.notes,
        )
    else:
        payload = build_candidate_payload(
            suggested_target_surface=args.suggested_target_surface,
            claim=args.claim,
            review_notes=args.review_notes,
        )

    out_dir = Path(args.output_dir) if args.output_dir else None
    out_path = export_inter_fork_package(
        sender_fork_id=args.sender,
        intended_recipient_fork_id=args.recipient,
        package_kind=args.package_kind,
        summary=args.summary,
        body=args.body,
        supporting_refs=args.supporting_ref,
        routing_hint=route,
        payload=payload,
        output_dir=out_dir,
    )
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
