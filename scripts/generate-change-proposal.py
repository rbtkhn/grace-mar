#!/usr/bin/env python3
"""
Emit a Change Proposal v1 JSON file under review-queue/proposals/.

Uses camelCase fields per schema-registry/change-proposal.v1.json.
Replace placeholder priorStateRef / proposedStateRef (and refine other fields)
before treating the proposal as merge-ready.

Validate with:
  python3 scripts/validate-change-review.py users/<id>/review-queue
"""

from __future__ import annotations

import argparse
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^proposal-[a-zA-Z0-9._-]+$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Change Proposal v1 JSON scaffold.")
    parser.add_argument(
        "--user-slug",
        default="demo",
        help="userSlug field (default: demo)",
    )
    parser.add_argument(
        "--proposal-id",
        default="",
        help="proposalId (default: proposal-<uuid>)",
    )
    parser.add_argument(
        "--primary-scope",
        required=True,
        choices=[
            "identity",
            "curiosity",
            "pedagogy",
            "expression",
            "memory_governance",
            "safety",
            "preference",
            "upgrade_collision",
        ],
    )
    parser.add_argument(
        "--secondary-scope",
        action="append",
        default=[],
        dest="secondary_scopes",
        choices=[
            "identity",
            "curiosity",
            "pedagogy",
            "expression",
            "memory_governance",
            "safety",
            "preference",
            "upgrade_collision",
        ],
    )
    parser.add_argument(
        "--change-type",
        required=True,
        choices=[
            "contradiction",
            "refinement",
            "expansion",
            "deprecation",
            "ambiguity",
            "policy_collision",
            "template_instance_collision",
        ],
    )
    parser.add_argument(
        "--queue-summary",
        required=True,
        help="Short narrative (maps to queueSummary; min substance for review)",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Path or id string to cite in supportingEvidence (repeatable)",
    )
    parser.add_argument(
        "--evidence-type",
        default="manual_note",
        choices=[
            "interaction",
            "seed_artifact",
            "template_upgrade",
            "manual_note",
            "policy_signal",
            "validation_output",
        ],
    )
    parser.add_argument(
        "--prior-state-ref",
        default="REPLACE_WITH_PRIOR_GOVERNED_STATE_REF",
        help="priorStateRef (placeholder default)",
    )
    parser.add_argument(
        "--proposed-state-ref",
        default="REPLACE_WITH_PROPOSED_STATE_REF",
        help="proposedStateRef (placeholder default)",
    )
    parser.add_argument(
        "--target-surface",
        default="self",
        choices=["self", "self_library", "civ_mem", "skills", "evidence", "work_layer"],
    )
    parser.add_argument(
        "--materiality",
        default="medium",
        choices=["low", "medium", "high", "critical"],
    )
    parser.add_argument(
        "--review-type",
        default="routine",
        choices=["routine", "extended", "boundary", "policy", "collision"],
    )
    parser.add_argument(
        "--risk-level",
        default="low",
        choices=["low", "medium", "high"],
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Directory for the JSON file (default: users/<user-slug>/review-queue/proposals)",
    )
    args = parser.parse_args()

    proposal_id = args.proposal_id.strip() or f"proposal-{uuid.uuid4()}"
    if not SAFE_ID.match(proposal_id):
        print("ERROR: proposalId must match ^proposal-[a-zA-Z0-9._-]+$", flush=True)
        return 1

    out_dir = Path(args.output_dir) if args.output_dir else ROOT / "users" / args.user_slug / "review-queue" / "proposals"
    out_dir.mkdir(parents=True, exist_ok=True)

    supporting: list[dict[str, str]] = []
    for ref in args.source:
        r = ref.strip()
        if not r:
            continue
        supporting.append(
            {
                "type": args.evidence_type,
                "ref": r,
                "summary": f"Cited from operator input: {r}",
            }
        )
    if not supporting:
        supporting.append(
            {
                "type": "manual_note",
                "ref": "no-source-provided",
                "summary": "Add real evidence refs before review; generated without --source.",
            }
        )

    proposal = {
        "schemaVersion": "1.0.0",
        "proposalId": proposal_id,
        "userSlug": args.user_slug,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "primaryScope": args.primary_scope,
        "secondaryScopes": list(dict.fromkeys(args.secondary_scopes)),
        "changeType": args.change_type,
        "priorStateRef": args.prior_state_ref,
        "proposedStateRef": args.proposed_state_ref,
        "supportingEvidence": supporting,
        "riskLevel": args.risk_level,
        "status": "proposed",
        "targetSurface": args.target_surface,
        "materiality": args.materiality,
        "reviewType": args.review_type,
        "queueSummary": args.queue_summary,
    }

    out_path = out_dir / f"{proposal_id}.json"
    out_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
