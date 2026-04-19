"""Load policy mode envelopes from config/policy_modes/defaults.json (operator governance, not Record truth)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
POLICY_DEFAULTS_PATH = REPO_ROOT / "config" / "policy_modes" / "defaults.json"
ENV_POLICY_MODE = "GRACE_MAR_POLICY_MODE"
DEFAULT_MODE = "operator_only"


def load_defaults(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Return mode name -> config dict (excludes schemaVersion)."""
    p = path or POLICY_DEFAULTS_PATH
    if not p.is_file():
        return {DEFAULT_MODE: _fallback_operator_only()}
    raw = json.loads(p.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    for k, v in raw.items():
        if k == "schemaVersion":
            continue
        if isinstance(v, dict) and "candidate_staging" in v:
            out[k] = v
    if not out:
        return {DEFAULT_MODE: _fallback_operator_only()}
    return out


def _fallback_operator_only() -> dict[str, Any]:
    return {
        "retrieval_scope": "lane_default",
        "candidate_staging": "allowed",
        "self_promotion_threshold": "standard",
        "abstention_level": "standard",
        "show_receipts": True,
    }


class UnknownPolicyModeError(ValueError):
    """Raised in strict mode when a policy mode name is not in defaults."""
    pass


def resolve_mode(
    name: str | None,
    defaults: dict[str, dict[str, Any]] | None = None,
    *,
    strict: bool = False,
) -> str:
    """Normalize mode key; unknown or empty -> operator_only.

    With strict=True, raises UnknownPolicyModeError instead of falling back
    when a non-empty mode name is not found in defaults.
    """
    modes = defaults if defaults is not None else load_defaults()
    raw = (name or "").strip() or os.environ.get(ENV_POLICY_MODE, "").strip()
    if not raw:
        return DEFAULT_MODE
    if raw in modes:
        return raw
    if strict:
        raise UnknownPolicyModeError(
            f"Unknown policy mode: {raw!r}. "
            f"Valid modes: {', '.join(sorted(modes))}. "
            f"Pass a valid mode or remove --policy-mode to use default ({DEFAULT_MODE})."
        )
    return DEFAULT_MODE


def staging_decision(
    mode_name: str,
    target_surface: str | None,
    defaults: dict[str, dict[str, Any]] | None = None,
) -> tuple[str, str]:
    """
    Return (verb, reason) where verb is:
    allowed | blocked | warn | hold_hint
    """
    modes = defaults if defaults is not None else load_defaults()
    m = modes.get(mode_name) or modes.get(DEFAULT_MODE) or {}
    cs = str(m.get("candidate_staging", "allowed"))
    ts = (target_surface or "").strip().upper()

    if cs == "blocked":
        return (
            "blocked",
            "This policy mode sets candidate_staging to blocked — automated gate staging is not allowed.",
        )
    if cs == "allowed":
        return ("allowed", "Policy mode allows staging; companion gate review is still required.")
    if cs == "allowed_with_strict_self_guard":
        if ts == "SELF":
            return (
                "warn",
                "identity_bound mode: SELF targets require --policy-ack (strict self guard).",
            )
        return ("allowed", "Policy mode allows staging for this target surface (non-SELF).")
    if cs == "hold_by_default":
        return (
            "hold_hint",
            "high_risk_abstention mode: staging defaults to hold — use --policy-ack to proceed with explicit override.",
        )
    return ("allowed", f"Unknown candidate_staging {cs!r}; treating as allowed.")


def mode_summary_lines(mode_name: str, defaults: dict[str, dict[str, Any]] | None = None) -> list[str]:
    """Short bullets for Markdown (review packet, etc.)."""
    modes = defaults if defaults is not None else load_defaults()
    m = modes.get(mode_name) or modes.get(DEFAULT_MODE) or {}
    lines = [
        f"- **retrieval_scope:** `{m.get('retrieval_scope', '')}`",
        f"- **candidate_staging:** `{m.get('candidate_staging', '')}`",
        f"- **self_promotion_threshold:** `{m.get('self_promotion_threshold', '')}`",
        f"- **abstention_level:** `{m.get('abstention_level', '')}`",
        f"- **show_receipts:** `{m.get('show_receipts', True)}`",
    ]
    return lines


def policy_mode_header_lines(mode_name: str, defaults: dict[str, dict[str, Any]] | None = None) -> list[str]:
    """Two-line header for budgeted context / artifacts."""
    modes = defaults if defaults is not None else load_defaults()
    m = modes.get(mode_name) or modes.get(DEFAULT_MODE) or {}
    return [
        f"Policy mode: {mode_name}",
        f"Envelope: candidate_staging={m.get('candidate_staging', '')}; abstention_level={m.get('abstention_level', '')}",
    ]
