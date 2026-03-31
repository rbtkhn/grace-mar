#!/usr/bin/env python3
"""Promote an accepted self-proposal artifact into the canonical gate."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SELF_PROPOSALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SELF_PROPOSALS_DIR.parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SELF_PROPOSALS_DIR) not in sys.path:
    sys.path.insert(0, str(SELF_PROPOSALS_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from emit_pipeline_event import append_pipeline_event
from proposal_io import PLACEHOLDER_GROUNDING_RE, validate_payload
from repo_io import profile_dir, read_path
from sandbox_merge import render_candidate_block
from stage_gate_candidate import insert_before_processed, next_candidate_id

ACCEPTED_DIR = SELF_PROPOSALS_DIR / "accepted"


def _load_artifact(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_promoted_candidate_block(artifact: dict, gate_text: str) -> tuple[str, str]:
    proposal = artifact.get("proposal")
    if not isinstance(proposal, dict):
        raise ValueError("accepted artifact missing proposal payload")

    errors = validate_payload(proposal)
    if errors:
        raise ValueError("accepted artifact proposal is no longer valid: " + "; ".join(errors))

    if artifact.get("promoted_to_gate_at"):
        raise ValueError("accepted artifact has already been promoted")
    if proposal.get("grounding_mode") == "scaffold":
        raise ValueError("scaffold-grounding artifacts may not be promoted")

    raw_source_exchange = artifact.get("raw_source_exchange") or proposal.get("candidate_bundle", {}).get("source_exchange") or {}
    if not isinstance(raw_source_exchange, dict) or not raw_source_exchange:
        raise ValueError("accepted artifact missing raw_source_exchange")
    for key, value in raw_source_exchange.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"accepted artifact raw_source_exchange.{key} is empty")
        if PLACEHOLDER_GROUNDING_RE.search(value):
            raise ValueError("accepted artifact still contains scaffold or placeholder grounding")

    candidate_id = next_candidate_id(gate_text)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    auto_meta = {
        "accepted_artifact": artifact.get("_artifact_relpath", "(unknown)"),
        "scalar_at_accept": artifact.get("scalar_at_accept", ""),
        "artifact_schema_version": artifact.get("artifact_schema_version", ""),
        "review_note": artifact.get("_promotion_review_note", ""),
    }
    candidate_block = render_candidate_block(
        proposal,
        candidate_id=candidate_id,
        timestamp=timestamp,
        status="pending",
        auto_research_metadata=auto_meta,
    )
    return candidate_id, candidate_block


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote an accepted self-proposal artifact into recursion-gate.md")
    parser.add_argument(
        "--artifact",
        type=Path,
        required=True,
        help="Accepted artifact JSON",
    )
    parser.add_argument("--user", "-u", default="grace-mar", help="User id (default: grace-mar)")
    parser.add_argument("--dry-run", action="store_true", help="Print the candidate block without writing the gate")
    parser.add_argument(
        "--review-note",
        default="",
        help="Required when writing to the gate; records the operator's reason for promotion",
    )
    args = parser.parse_args()

    artifact_path = args.artifact.resolve()
    if artifact_path is None or not artifact_path.is_file():
        raise SystemExit("No accepted artifact found to promote")
    if not args.dry_run and not args.review_note.strip():
        raise SystemExit("--review-note is required unless --dry-run is used")

    artifact = _load_artifact(artifact_path)
    artifact["_artifact_relpath"] = str(artifact_path.relative_to(REPO_ROOT))
    artifact["_promotion_review_note"] = args.review_note.strip()
    gate_path = profile_dir(args.user) / "recursion-gate.md"
    gate_text = read_path(gate_path)
    try:
        candidate_id, candidate_block = build_promoted_candidate_block(artifact, gate_text)
    except ValueError as exc:
        raise SystemExit(str(exc))

    if args.dry_run:
        print(candidate_block)
        return 0

    updated_gate = insert_before_processed(gate_text, candidate_block)
    gate_path.write_text(updated_gate, encoding="utf-8")
    append_pipeline_event(
        args.user,
        "staged",
        candidate_id,
        merge={
            "candidate_source": "auto-research/self-proposals",
            "accepted_artifact": str(artifact_path.relative_to(REPO_ROOT)),
            "scalar_at_accept": str(artifact.get("scalar_at_accept", "")),
            "artifact_schema_version": str(artifact.get("artifact_schema_version", "")),
            "review_note": args.review_note.strip(),
        },
    )
    artifact["promoted_to_gate_at"] = datetime.now(timezone.utc).isoformat()
    artifact["staged_candidate_id"] = candidate_id
    artifact["promotion_review_note"] = args.review_note.strip()
    artifact.pop("_artifact_relpath", None)
    artifact.pop("_promotion_review_note", None)
    artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"{gate_path}: inserted {candidate_id} from {artifact_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
