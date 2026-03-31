#!/usr/bin/env python3
"""Normalize repo-native metrics into one bounded score bundle."""

from __future__ import annotations

import re
from typing import Any


def tokenize_text(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) >= 3}


def parse_measure_uniqueness_output(text: str) -> dict[str, float]:
    out: dict[str, float] = {}
    patterns = {
        "abstention_score": r"Abstention score:\s+\d+/\d+\s+=\s+([0-9.]+)",
        "divergence_score": r"Divergence score:\s+([0-9.]+)",
        "readability_gap": r"Readability gap:\s+([+-]?[0-9.]+)",
        "composite_uniqueness": r"Composite uniqueness:\s+([0-9.]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            out[key] = float(match.group(1))
    return out


def parse_growth_density_output(text: str) -> dict[str, float]:
    out: dict[str, float] = {}
    patterns = {
        "entries_per_day": r"Entries per day:\s+([0-9.]+)",
        "words_per_entry": r"Words per entry:\s+([0-9.]+)",
        "evidence_backing_pct": r"Evidence backing:\s+\d+/\d+\s+\(([0-9.]+)%\)",
        "topic_diversity": r"Topic diversity:\s+([0-9.]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            out[key] = float(match.group(1))
    return out


def score_metrics_health(metrics_json: dict[str, Any]) -> float:
    pipeline = metrics_json.get("pipeline_health", {})
    completeness = metrics_json.get("record_completeness", {})
    drift = metrics_json.get("intent_drift", {})

    approval_rate = pipeline.get("approval_rate")
    if not isinstance(approval_rate, (int, float)):
        approval_rate = 0.5
    pending = pipeline.get("pending_count")
    pending_penalty = 0.0
    if isinstance(pending, (int, float)):
        pending_penalty = min(float(pending) / 250.0, 1.0)

    total_ix = completeness.get("total_ix")
    record_fullness = min(float(total_ix or 0) / 100.0, 1.0)

    conflicts = drift.get("total_conflicts")
    conflict_penalty = min(float(conflicts or 0) / 10.0, 1.0)

    score = (
        (0.45 * float(approval_rate))
        + (0.35 * record_fullness)
        + (0.20 * (1.0 - conflict_penalty))
    )
    score *= 1.0 - (0.20 * pending_penalty)
    return max(0.0, min(score, 1.0))


def score_source_proposal_alignment(candidate: dict[str, Any]) -> dict[str, float]:
    source_text = " ".join(str(value) for value in (candidate.get("source_exchange") or {}).values())
    proposal_text = " ".join(
        str(candidate.get(key, ""))
        for key in ("summary", "suggested_entry", "prompt_addition")
    )

    source_tokens = tokenize_text(source_text)
    proposal_tokens = tokenize_text(proposal_text)
    if not proposal_tokens:
        return {
            "source_overlap": 0.0,
            "novel_term_ratio": 1.0,
            "drift_penalty": 1.0,
            "alignment_score": 0.0,
        }

    overlap_count = len(source_tokens & proposal_tokens)
    source_overlap = overlap_count / len(proposal_tokens)
    novel_term_ratio = max(0.0, min((len(proposal_tokens - source_tokens) / len(proposal_tokens)), 1.0))
    drift_penalty = max(0.0, min((novel_term_ratio * 0.7) + (max(0.0, 0.5 - source_overlap) * 0.6), 1.0))
    alignment_score = max(0.0, min((source_overlap * 1.1) - (novel_term_ratio * 0.35), 1.0))
    return {
        "source_overlap": round(source_overlap, 4),
        "novel_term_ratio": round(novel_term_ratio, 4),
        "drift_penalty": round(drift_penalty, 4),
        "alignment_score": round(alignment_score, 4),
    }


def score_proposal_quality(payload: dict[str, Any], candidate_block: str) -> dict[str, float]:
    candidate = payload["candidate_bundle"]
    required_fields = (
        "title",
        "summary",
        "source",
        "source_exchange",
        "mind_category",
        "signal_type",
        "profile_target",
        "suggested_entry",
        "prompt_section",
        "prompt_addition",
    )
    present = 0
    for key in required_fields:
        value = candidate.get(key)
        if isinstance(value, dict):
            present += 1 if value else 0
        elif isinstance(value, str):
            present += 1 if value.strip() else 0
        elif value is not None:
            present += 1
    completeness = present / len(required_fields)

    source_exchange = candidate.get("source_exchange", {})
    grounded_sources = 0
    total_sources = 0
    for value in source_exchange.values():
        total_sources += 1
        if isinstance(value, str) and value.strip() and "TODO" not in value:
            grounded_sources += 1
    groundedness = grounded_sources / total_sources if total_sources else 0.0

    reviewability = 1.0
    summary = str(candidate.get("summary", ""))
    if len(summary) < 20 or len(summary) > 240:
        reviewability -= 0.25
    if not candidate.get("new_vs_record"):
        reviewability -= 0.15
    if not candidate.get("proposal_class"):
        reviewability -= 0.10
    reviewability = max(0.0, reviewability)

    prompt_alignment = 1.0
    prompt_addition = str(candidate.get("prompt_addition", ""))
    if not prompt_addition or prompt_addition.lower() == "none":
        prompt_alignment -= 0.35
    if "training data" in prompt_addition.lower():
        prompt_alignment -= 0.30
    if "wikipedia" in candidate_block.lower():
        prompt_alignment -= 0.30
    prompt_alignment = max(0.0, prompt_alignment)
    source_alignment = score_source_proposal_alignment(candidate)

    quality = (
        (0.28 * completeness)
        + (0.24 * groundedness)
        + (0.16 * reviewability)
        + (0.12 * prompt_alignment)
        + (0.20 * source_alignment["alignment_score"])
    )
    quality = max(0.0, min(quality - (0.12 * source_alignment["drift_penalty"]), 1.0))

    return {
        "quality": round(max(0.0, min(quality, 1.0)), 4),
        "completeness": round(completeness, 4),
        "groundedness": round(groundedness, 4),
        "reviewability": round(reviewability, 4),
        "prompt_alignment": round(prompt_alignment, 4),
        "source_overlap": source_alignment["source_overlap"],
        "novel_term_ratio": source_alignment["novel_term_ratio"],
        "drift_penalty": source_alignment["drift_penalty"],
        "alignment_score": source_alignment["alignment_score"],
    }


def build_score_bundle(
    *,
    integrity_json: dict[str, Any],
    governance_ok: bool,
    metrics_json: dict[str, Any],
    proposal_quality: dict[str, float],
    uniqueness: dict[str, float] | None = None,
    growth_density: dict[str, float] | None = None,
    baseline_scalar: float | None = None,
) -> dict[str, Any]:
    integrity_ok = bool(integrity_json.get("ok"))
    metrics_health = score_metrics_health(metrics_json)

    component_values: dict[str, tuple[float, float]] = {
        "proposal_quality": (proposal_quality["quality"], 0.65),
        "metrics_health": (metrics_health, 0.25),
    }
    if uniqueness and "composite_uniqueness" in uniqueness:
        component_values["uniqueness_proxy"] = (
            max(0.0, min(float(uniqueness["composite_uniqueness"]), 1.0)),
            0.05,
        )
    if growth_density:
        evidence_pct = growth_density.get("evidence_backing_pct")
        diversity = growth_density.get("topic_diversity")
        if evidence_pct is not None and diversity is not None:
            growth_score = min(max((float(evidence_pct) / 100.0) * 0.7 + float(diversity) * 0.3, 0.0), 1.0)
            component_values["growth_density_proxy"] = (growth_score, 0.05)

    if not integrity_ok or not governance_ok:
        scalar = 0.0
    else:
        weight_total = sum(weight for _, weight in component_values.values())
        scalar = sum(value * weight for value, weight in component_values.values()) / weight_total

    delta = None if baseline_scalar is None else round(scalar - baseline_scalar, 4)
    return {
        "ok": integrity_ok and governance_ok,
        "scalar": round(float(scalar), 4),
        "comparison": {
            "baseline_scalar": baseline_scalar,
            "delta_from_baseline": delta,
        },
        "hard_gates": {
            "integrity_ok": integrity_ok,
            "governance_ok": governance_ok,
        },
        "components": {
            "proposal_quality": round(proposal_quality["quality"], 4),
            "metrics_health": round(metrics_health, 4),
            "proposal_quality_detail": proposal_quality,
        },
        "optional_metrics": {
            "uniqueness": uniqueness or {},
            "growth_density": growth_density or {},
        },
    }
