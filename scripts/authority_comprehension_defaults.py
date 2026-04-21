"""
Derive recommended Comprehension Envelope + Reflection Gate staging fields from
authority class (write-authority), aligned with docs/governance and
recursion_gate_review.reflection_gate (impact_tier → none|light|heavy).

Single SSOT for mapping logic; check-authority.py and tests import this module.
"""

from __future__ import annotations

# Normative mapping: authority class → staging hints (companion may override in YAML).
_AUTHORITY_CLASS_TO_STAGING: dict[str, tuple[str, str, str]] = {
    # (impact_tier, envelope_class, reflection_gate) — gate matches impact_tier per gate wiring v1
    "human_only": ("boundary", "required", "heavy"),
    "review_required": ("medium", "optional", "light"),
    "draftable": ("low", "none", "none"),
    "read_only": ("low", "none", "none"),
    "ephemeral_only": ("low", "none", "none"),
}

_RATIONALE: dict[str, str] = {
    "human_only": "High-trust surfaces: full comprehension proof and Heavy Gate before promotion.",
    "review_required": "Material changes: Light Gate and optional Comprehension Envelope.",
    "draftable": "Draft/prepared layers: fast path; envelope usually omitted unless complex.",
    "read_only": "No write path: minimal staging overhead.",
    "ephemeral_only": "Operational/ephemeral outputs: no Reflection Gate by default.",
}


def recommend_for_authority_class(authority_class: str) -> dict[str, str]:
    """
    Return recommended impact_tier, envelope_class, reflection_gate, rationale.

    Unknown authority_class returns empty strings and a generic rationale.
    """
    ac = (authority_class or "").strip()
    if ac not in _AUTHORITY_CLASS_TO_STAGING:
        return {
            "recommended_impact_tier": "",
            "recommended_envelope_class": "",
            "recommended_reflection_gate": "",
            "rationale": "Unknown authority class; set impact_tier and envelope_class manually.",
        }
    impact, env, gate = _AUTHORITY_CLASS_TO_STAGING[ac]
    return {
        "recommended_impact_tier": impact,
        "recommended_envelope_class": env,
        "recommended_reflection_gate": gate,
        "rationale": _RATIONALE.get(ac, ""),
    }


__all__ = ["recommend_for_authority_class", "_AUTHORITY_CLASS_TO_STAGING"]
