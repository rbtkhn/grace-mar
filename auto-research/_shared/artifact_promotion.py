#!/usr/bin/env python3
"""Shared accepted-artifact promotion helpers for auto-research lanes."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SHARED_DIR = Path(__file__).resolve().parent
AUTO_RESEARCH_DIR = SHARED_DIR.parent
REPO_ROOT = AUTO_RESEARCH_DIR.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SELF_PROPOSALS_DIR = AUTO_RESEARCH_DIR / "self-proposals"

for path in (SCRIPTS_DIR, SELF_PROPOSALS_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from emit_pipeline_event import append_pipeline_event
from proposal_io import PLACEHOLDER_GROUNDING_RE, validate_payload
from repo_io import profile_dir, read_path
from sandbox_merge import render_candidate_block
from stage_gate_candidate import insert_before_processed, next_candidate_id


def load_artifact(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def build_promoted_candidate_block(
    artifact: dict[str, Any],
    gate_text: str,
    *,
    lane_name: str = "self-proposals",
    candidate_source: str = "auto-research/self-proposals",
    extra_auto_research_metadata: dict[str, Any] | None = None,
) -> tuple[str, str]:
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

    raw_source_exchange = (
        artifact.get("raw_source_exchange")
        or proposal.get("candidate_bundle", {}).get("source_exchange")
        or {}
    )
    if not isinstance(raw_source_exchange, dict) or not raw_source_exchange:
        raise ValueError("accepted artifact missing raw_source_exchange")
    for key, value in raw_source_exchange.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"accepted artifact raw_source_exchange.{key} is empty")
        if PLACEHOLDER_GROUNDING_RE.search(value):
            raise ValueError("accepted artifact still contains scaffold or placeholder grounding")

    candidate_id = next_candidate_id(gate_text)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    auto_meta: dict[str, Any] = {
        "lane": lane_name,
        "candidate_source": candidate_source,
        "accepted_artifact": artifact.get("_artifact_relpath", "(unknown)"),
        "scalar_at_accept": artifact.get("scalar_at_accept", ""),
        "artifact_schema_version": artifact.get("artifact_schema_version", ""),
        "review_note": artifact.get("_promotion_review_note", ""),
    }
    if extra_auto_research_metadata:
        auto_meta.update(extra_auto_research_metadata)
    candidate_block = render_candidate_block(
        proposal,
        candidate_id=candidate_id,
        timestamp=timestamp,
        status="pending",
        auto_research_metadata=auto_meta,
    )
    return candidate_id, candidate_block


def promote_artifact_to_gate(
    artifact_path: Path,
    *,
    user_id: str = "grace-mar",
    review_note: str = "",
    dry_run: bool = False,
    lane_name: str = "self-proposals",
    candidate_source: str = "auto-research/self-proposals",
    extra_auto_research_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    artifact_path = artifact_path.resolve()
    if not artifact_path.is_file():
        raise ValueError("No accepted artifact found to promote")
    if not dry_run and not review_note.strip():
        raise ValueError("--review-note is required unless --dry-run is used")

    artifact = load_artifact(artifact_path)
    artifact_relpath = _safe_relpath(artifact_path)
    artifact["_artifact_relpath"] = artifact_relpath
    artifact["_promotion_review_note"] = review_note.strip()

    gate_path = profile_dir(user_id) / "recursion-gate.md"
    gate_text = read_path(gate_path)
    candidate_id, candidate_block = build_promoted_candidate_block(
        artifact,
        gate_text,
        lane_name=lane_name,
        candidate_source=candidate_source,
        extra_auto_research_metadata=extra_auto_research_metadata,
    )
    result: dict[str, Any] = {
        "artifact_path": str(artifact_path),
        "artifact_relpath": artifact_relpath,
        "gate_path": str(gate_path),
        "candidate_id": candidate_id,
        "candidate_block": candidate_block,
        "lane_name": lane_name,
        "candidate_source": candidate_source,
    }
    if dry_run:
        return result

    updated_gate = insert_before_processed(gate_text, candidate_block)
    gate_path.write_text(updated_gate, encoding="utf-8")
    append_pipeline_event(
        user_id,
        "staged",
        candidate_id,
        merge={
            "candidate_source": candidate_source,
            "candidate_lane": lane_name,
            "accepted_artifact": artifact_relpath,
            "scalar_at_accept": str(artifact.get("scalar_at_accept", "")),
            "artifact_schema_version": str(artifact.get("artifact_schema_version", "")),
            "review_note": review_note.strip(),
        },
    )
    artifact["promoted_to_gate_at"] = datetime.now(timezone.utc).isoformat()
    artifact["staged_candidate_id"] = candidate_id
    artifact["promotion_review_note"] = review_note.strip()
    artifact["promotion_lane"] = lane_name
    artifact.pop("_artifact_relpath", None)
    artifact.pop("_promotion_review_note", None)
    artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    result["promoted_to_gate_at"] = artifact["promoted_to_gate_at"]
    return result
