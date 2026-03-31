#!/usr/bin/env python3
"""Parse and validate the single editable proposal surface."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
PLACEHOLDER_GROUNDING_RE = re.compile(
    r"\b(synthetic|todo|replace|scaffold|validation only)\b",
    re.IGNORECASE,
)

REQUIRED_TOP_LEVEL = (
    "hypothesis",
    "expected_delta",
    "proposal_type",
    "target_surface",
    "candidate_bundle",
    "evaluation_notes",
)

REQUIRED_CANDIDATE_FIELDS = (
    "title",
    "summary",
    "source",
    "source_exchange",
    "mind_category",
    "signal_type",
    "priority_score",
    "profile_target",
    "suggested_entry",
    "prompt_section",
    "prompt_addition",
)

ALLOWED_PROPOSAL_TYPES = {"recursion_gate_candidate"}
ALLOWED_TARGET_SURFACES = {"self"}
ALLOWED_MIND_CATEGORIES = {"knowledge", "curiosity", "personality"}
ALLOWED_GROUNDING_MODES = {"scaffold", "strict"}


def extract_json_block(markdown: str) -> dict[str, Any]:
    match = JSON_BLOCK_RE.search(markdown)
    if not match:
        raise ValueError("train.md must contain exactly one fenced JSON block")
    return json.loads(match.group(1))


def load_train_payload(path: Path) -> dict[str, Any]:
    return extract_json_block(path.read_text(encoding="utf-8"))


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["proposal payload must be a JSON object"]

    for key in REQUIRED_TOP_LEVEL:
        if key not in payload:
            errors.append(f"missing top-level field: {key}")

    hypothesis = payload.get("hypothesis")
    if not isinstance(hypothesis, str) or not hypothesis.strip():
        errors.append("hypothesis must be a non-empty string")

    expected_delta = payload.get("expected_delta")
    if not isinstance(expected_delta, (int, float)):
        errors.append("expected_delta must be a number")

    proposal_type = payload.get("proposal_type")
    if proposal_type not in ALLOWED_PROPOSAL_TYPES:
        errors.append(f"proposal_type must be one of: {sorted(ALLOWED_PROPOSAL_TYPES)}")

    target_surface = payload.get("target_surface")
    if target_surface not in ALLOWED_TARGET_SURFACES:
        errors.append(f"target_surface must be one of: {sorted(ALLOWED_TARGET_SURFACES)}")

    grounding_mode = payload.get("grounding_mode")
    if grounding_mode is not None and grounding_mode not in ALLOWED_GROUNDING_MODES:
        errors.append(f"grounding_mode must be one of: {sorted(ALLOWED_GROUNDING_MODES)}")

    evaluation_notes = payload.get("evaluation_notes")
    if not isinstance(evaluation_notes, str) or not evaluation_notes.strip():
        errors.append("evaluation_notes must be a non-empty string")

    candidate = payload.get("candidate_bundle")
    if not isinstance(candidate, dict):
        errors.append("candidate_bundle must be a JSON object")
        return errors

    for key in REQUIRED_CANDIDATE_FIELDS:
        if key not in candidate:
            errors.append(f"candidate_bundle missing field: {key}")

    for key in (
        "title",
        "summary",
        "source",
        "signal_type",
        "profile_target",
        "suggested_entry",
        "prompt_section",
        "prompt_addition",
    ):
        value = candidate.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"candidate_bundle.{key} must be a non-empty string")

    source_exchange = candidate.get("source_exchange")
    if not isinstance(source_exchange, dict) or not source_exchange:
        errors.append("candidate_bundle.source_exchange must be a non-empty object")
    else:
        for key, value in source_exchange.items():
            if not isinstance(key, str) or not key.strip():
                errors.append("candidate_bundle.source_exchange keys must be non-empty strings")
            if not isinstance(value, str) or not value.strip():
                errors.append(f"candidate_bundle.source_exchange.{key} must be a non-empty string")

    mind_category = candidate.get("mind_category")
    if mind_category not in ALLOWED_MIND_CATEGORIES:
        errors.append(f"candidate_bundle.mind_category must be one of: {sorted(ALLOWED_MIND_CATEGORIES)}")

    priority = candidate.get("priority_score")
    if not isinstance(priority, int) or not (1 <= priority <= 5):
        errors.append("candidate_bundle.priority_score must be an integer between 1 and 5")

    proposal_class = candidate.get("proposal_class")
    if proposal_class is not None and (not isinstance(proposal_class, str) or not proposal_class.strip()):
        errors.append("candidate_bundle.proposal_class must be a non-empty string when present")

    territory = candidate.get("territory")
    if territory is not None and territory not in {"work-politics"}:
        errors.append("candidate_bundle.territory may only be omitted or set to 'work-politics'")

    for optional_key in ("new_vs_record", "suggested_followup", "channel_key"):
        value = candidate.get(optional_key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"candidate_bundle.{optional_key} must be a non-empty string when present")

    return errors


def validate_grounding(payload: dict[str, Any], *, strict: bool) -> list[str]:
    candidate = payload.get("candidate_bundle")
    if not isinstance(candidate, dict):
        return ["candidate_bundle must be a JSON object before grounding can be checked"]

    source_exchange = candidate.get("source_exchange")
    if not isinstance(source_exchange, dict) or not source_exchange:
        return ["candidate_bundle.source_exchange must be a non-empty object"]

    errors: list[str] = []
    grounding_mode = str(payload.get("grounding_mode") or "strict").strip().lower()
    enforce_strict = strict

    if strict and grounding_mode == "scaffold":
        errors.append("strict grounding does not allow grounding_mode=scaffold")

    longest_verbatim = 0
    found_non_placeholder = False
    for key, value in source_exchange.items():
        if not isinstance(value, str):
            continue
        cleaned = value.strip()
        if not cleaned:
            continue
        longest_verbatim = max(longest_verbatim, len(cleaned))
        if PLACEHOLDER_GROUNDING_RE.search(cleaned):
            if enforce_strict:
                errors.append(
                    f"candidate_bundle.source_exchange.{key} contains placeholder grounding markers"
                )
            continue
        found_non_placeholder = True

    if enforce_strict and not found_non_placeholder:
        errors.append("strict grounding requires at least one non-placeholder source_exchange value")
    if enforce_strict and longest_verbatim < 48:
        errors.append("strict grounding requires at least one sufficiently long verbatim source string")

    return errors
