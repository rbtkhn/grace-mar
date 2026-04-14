"""
Derive uncertainty envelope from runtime observation dicts (single pipeline).

All scores are computed only from fields present on observations plus optional
staging text (precheck). See docs/abstention-policy.md.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Identity / biographical cues without evidence — fabricated-history screening (not accusation).
_IDENTITY_HISTORY_PATTERNS = (
    re.compile(r"\b(born|childhood|grew up|always knew|never told anyone)\b", re.I),
    re.compile(r"\b(19|20)\d{2}\b.*\b(in|at)\b", re.I),
    re.compile(r"\b(remember when we|first met|years ago)\b", re.I),
)
_OVERLY_SPECIFIC = re.compile(
    r"\b(exactly|precisely|definitely)\b.+\b(on \d{4}-\d{2}-\d{2}|at \d{1,2}:\d{2})\b", re.I
)


def _text_blob(observations: list[dict]) -> str:
    parts: list[str] = []
    for o in observations:
        parts.append((o.get("title") or "") + " " + (o.get("summary") or ""))
    return " ".join(parts)


def _has_identity_history_like(text: str) -> bool:
    return any(p.search(text) for p in _IDENTITY_HISTORY_PATTERNS)


def _overly_specific_without_refs(observations: list[dict], has_refs: bool) -> bool:
    if has_refs:
        return False
    blob = _text_blob(observations)
    return bool(_OVERLY_SPECIFIC.search(blob)) or len(blob) > 400 and not has_refs


def compute_fabricated_history_risk(observations: list[dict]) -> tuple[str, list[str]]:
    """Return (low|medium|high, reason strings)."""
    reasons: list[str] = []
    if not observations:
        return "low", ["No observations to assess."]

    union_refs: list[str] = []
    for o in observations:
        union_refs.extend(o.get("source_refs") or [])
    has_refs = len(union_refs) > 0

    record_mut = any(o.get("record_mutation_candidate") for o in observations)
    blob = _text_blob(observations)

    if len(observations) == 1 and record_mut and not has_refs:
        reasons.append(
            "Single observation proposes durable Record change without source references."
        )
        return "high", reasons

    if _has_identity_history_like(blob) and not has_refs:
        reasons.append("History- or identity-like wording without evidence references.")
        if record_mut:
            return "high", reasons
        return "medium", reasons

    if _overly_specific_without_refs(observations, has_refs):
        reasons.append("Highly specific claims without supporting references.")
        return "medium", reasons

    if record_mut and not has_refs and len(observations) < 2:
        reasons.append("Durable-change flag without corroborating references.")
        return "medium", reasons

    reasons.append("No strong fabricated-history pattern detected in heuristics.")
    return "low", reasons


def compute_evidence_state(observations: list[dict]) -> tuple[str, list[str], list[str], list[str]]:
    """
    Return (evidence_state, reasons, missing_evidence_refs, conflicting_refs).
    Derives from source_refs, contradiction_refs, confidence, source_kind, counts.
    """
    reasons: list[str] = []
    conflicting: list[str] = []
    seen: set[str] = set()
    for o in observations:
        for c in o.get("contradiction_refs") or []:
            if c and c not in seen:
                seen.add(c)
                conflicting.append(c)

    if conflicting:
        reasons.append("Contradiction reference(s) present; evidence is not mutually consistent.")

    n = len(observations)
    n_with_refs = sum(1 for o in observations if (o.get("source_refs") or []))
    all_refs = [r for o in observations for r in (o.get("source_refs") or [])]
    evidence_ref_kind = sum(1 for o in observations if o.get("source_kind") == "evidence_ref")

    low_conf = sum(
        1
        for o in observations
        if isinstance(o.get("confidence"), (int, float)) and float(o["confidence"]) < 0.4
    )

    if conflicting:
        return "conflicted", reasons, [], conflicting

    if n == 0:
        reasons.append("No observations supplied.")
        return "insufficient", reasons, ["(no observations)"], []

    if not all_refs and n == 1:
        s = (observations[0].get("summary") or "").strip()
        if len(s) < 80 and not (observations[0].get("source_path")):
            reasons.append("Single short observation with no source_refs or source_path.")
            return "insufficient", reasons, ["source_refs", "primary citation"], []

    if not all_refs:
        reasons.append("No source_refs across the selection; support is thin.")
        return "insufficient", reasons, ["source_refs"], []

    if n_with_refs >= 2 or (n_with_refs >= 1 and evidence_ref_kind >= 1 and n >= 1):
        if low_conf:
            reasons.append("References present but at least one observation has low confidence.")
            return "partial", reasons, [], []
        reasons.append("Multiple supporting observations with references, or evidence_ref kind with refs.")
        return "sufficient", reasons, [], []

    if n_with_refs == 1 and n >= 2:
        reasons.append("Only one observation carries explicit refs among several.")
        return "partial", reasons, [], []

    reasons.append("Some evidence references present; gaps may remain.")
    return "partial", reasons, [], []


def promotion_recommendation(evidence_state: str, fabricated_history_risk: str) -> str:
    """First-pass rule from docs/abstention-policy.md."""
    if evidence_state == "conflicted" or fabricated_history_risk == "high":
        return "block"
    if evidence_state == "insufficient":
        return "hold"
    if evidence_state == "partial" and fabricated_history_risk in ("low", "medium"):
        return "allow_with_review"
    if evidence_state == "sufficient" and fabricated_history_risk == "low":
        return "allow"
    if evidence_state == "sufficient" and fabricated_history_risk == "medium":
        return "allow_with_review"
    if evidence_state == "partial" and fabricated_history_risk == "high":
        return "block"
    return "allow_with_review"


def compute_envelope(observations: list[dict]) -> dict[str, Any]:
    """
    Build a full uncertainty envelope dict from runtime observation rows.
    Observations should match schema-registry/runtime-observation.v1.json shape.
    """
    ev_state, ev_reasons, missing, conflicting = compute_evidence_state(observations)
    fh_risk, fh_reasons = compute_fabricated_history_risk(observations)

    reasons = list(ev_reasons)
    for r in fh_reasons:
        if r not in reasons:
            reasons.append(r)
    if not reasons:
        reasons.append("Heuristic assessment complete.")

    promo = promotion_recommendation(ev_state, fh_risk)

    return {
        "evidence_state": ev_state,
        "fabricated_history_risk": fh_risk,
        "reasons": reasons,
        "missing_evidence_refs": missing,
        "conflicting_refs": conflicting,
        "promotion_recommendation": promo,
    }


def synthetic_observation_from_text(text: str, record_mutation_candidate: bool = True) -> dict:
    """Minimal shape for gate precheck on free text (not a persisted observation)."""
    # Matches runtime-observation obs_id pattern (8-char suffix).
    stub = "obs_20260101T000000Z_prchkfff"
    return {
        "obs_id": stub,
        "timestamp": "1970-01-01T00:00:00Z",
        "lane": "precheck",
        "source_kind": "agent_output",
        "title": "precheck",
        "summary": (text or "")[:1200],
        "record_mutation_candidate": record_mutation_candidate,
        "source_path": None,
        "source_refs": [],
        "tags": ["precheck_synthetic"],
        "confidence": None,
        "contradiction_refs": [],
        "notes": None,
    }


def envelope_to_markdown_block(env: dict[str, Any]) -> str:
    """Human-readable section for prepared context / briefs."""
    lines = [
        "## Uncertainty envelope",
        "",
        f"- **Evidence state:** `{env['evidence_state']}`",
        f"- **Fabricated-history risk:** `{env['fabricated_history_risk']}` (screening, not attribution)",
        f"- **Promotion recommendation:** `{env.get('promotion_recommendation', '')}`",
        "",
        "**Reasons:**",
    ]
    for r in env.get("reasons") or []:
        lines.append(f"- {r}")
    cr = env.get("conflicting_refs") or []
    if cr:
        lines.extend(["", "**Conflicting refs:**", *[f"- `{c}`" for c in cr]])
    me = env.get("missing_evidence_refs") or []
    if me:
        lines.extend(["", "**Missing evidence (kinds):**", *[f"- {m}" for m in me]])
    lines.extend(
        [
            "",
            "_Advisory only. Companion approval still required for Record merges._",
        ]
    )
    return "\n".join(lines) + "\n"


def envelope_to_json(env: dict[str, Any]) -> str:
    return json.dumps(env, ensure_ascii=True, indent=2)


def load_prepared_context_obs_ids(path: Path) -> list[str]:
    """Extract obs_id tokens from a prepared-context markdown file."""
    text = path.read_text(encoding="utf-8")
    return list(
        dict.fromkeys(re.findall(r"\b(obs_\d{8}T\d{6}Z_[a-z0-9]{8})\b", text))
    )
