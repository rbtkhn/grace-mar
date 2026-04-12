"""
Shared rejection taxonomy and categorization for recursion-gate YAML (WORK layer; not Record).

Used by analyze_rejection_feedback.py. Categories align with docs/governance-unbundling.md.
"""

from __future__ import annotations

import re
from typing import Any

import yaml

REJECTION_CATEGORIES: dict[str, str] = {
    "routing_error": "Signal misclassified, low quality, or duplicate",
    "sensemaking_mismatch": "Does not align with lived context, mind model (IX-A/B/C), or long-term trajectory",
    "accountability_violation": "Would override user intent, create drift, or violate sovereign merge rule",
    "ethics_boundary": "Violates condition-derived ethics or trust boundaries",
    "evidence_weak": "Insufficient evidence or poor grounding",
    "other": "Custom / uncategorized reason",
}

_ALLOWED = frozenset(REJECTION_CATEGORIES)


def _yaml_safe(blob: str) -> dict[str, Any]:
    try:
        data = yaml.safe_load(blob) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def infer_rejection_category(yaml_body: str) -> str:
    """
    Return a category key: optional rejection_category field, else heuristics on rejection_reason/summary.
    """
    data = _yaml_safe(yaml_body)
    raw = data.get("rejection_category")
    if isinstance(raw, str) and raw.strip():
        cat = raw.strip().lower()
        if cat in _ALLOWED:
            return cat
    reason = str(data.get("rejection_reason") or "").lower()
    summary = str(data.get("summary") or "").lower()
    text = f"{reason} {summary}"

    if re.search(r"\bduplicate\b", text):
        return "routing_error"
    if "weak" in text or "insufficient" in text or "grounding" in text:
        return "evidence_weak"
    if "ethic" in text or "trust boundary" in text:
        return "ethics_boundary"
    if "intent" in text or "drift" in text or "override" in text:
        return "accountability_violation"
    if "context" in text or "ix-" in text or "mind" in text or "trajectory" in text:
        return "sensemaking_mismatch"
    if "misclassif" in text or "low quality" in text or "signal" in text:
        return "routing_error"

    return "other"
