#!/usr/bin/env python3
"""
BUILD-AI-GAP-006 slice: consistency between handback text and constitution meta,
plus optional narrative vs structured risk tier when staged_risk_tier is supplied.

Validates that CONSTITUTION_ADVISORY embedded in content matches
constitution_check_status, and that advisory_flagged implies an advisory line is
present.

Optional: when staged_risk_tier is supplied, flag obvious narrative/structured
risk mismatches:
- approval-like tiers paired with high-concern phrasing
- manual/high tiers paired with approval-like phrasing

Usage:
  python scripts/work_dev/validate_handback_analysis.py --file payload.json
  echo '{"content":"...","constitution_check_status":"advisory_clear"}' | python scripts/work_dev/validate_handback_analysis.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_ADVISORY_RE = re.compile(
    r"CONSTITUTION_ADVISORY:\s*status\s*=\s*([^;\n]+)",
    re.IGNORECASE | re.MULTILINE,
)

# Heuristics: narrative signals that conflict with the structured staged_risk_tier.
_HIGH_CONCERN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bhigh risk\b", re.IGNORECASE),
    re.compile(r"\bdo not merge\b", re.IGNORECASE),
    re.compile(r"\bmust reject\b", re.IGNORECASE),
    re.compile(r"\bcannot approve\b", re.IGNORECASE),
    re.compile(r"\bsevere mismatch\b", re.IGNORECASE),
    re.compile(r"\bmanual(?:ly)? escalate\b", re.IGNORECASE),
    re.compile(r"\brequires? manual review\b", re.IGNORECASE),
    re.compile(r"\bnot safe to merge\b", re.IGNORECASE),
    re.compile(r"\breject this (?:candidate|change|merge)\b", re.IGNORECASE),
)

_APPROVAL_LIKE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\blow risk\b", re.IGNORECASE),
    re.compile(r"\bsafe to merge\b", re.IGNORECASE),
    re.compile(r"\bquick merge\b", re.IGNORECASE),
    re.compile(r"\bquick[-_ ]merge eligible\b", re.IGNORECASE),
    re.compile(r"\bready to merge\b", re.IGNORECASE),
    re.compile(r"\bapproved\b", re.IGNORECASE),
    re.compile(r"\bapprove (?:this|candidate|change)\b", re.IGNORECASE),
)

_APPROVAL_LIKE_TIERS = {"low", "medium", "quick_merge_eligible"}
_MANUAL_OR_HIGH_TIERS = {"high", "manual_escalate", "advisory_flagged", "reject", "blocked"}


def _narrative_text(payload: dict[str, Any]) -> str:
    """Collect free-text fields that may carry the handback reasoning narrative."""
    parts = []
    for key in ("content", "summary", "analysis", "reasoning"):
        value = str(payload.get(key) or "").strip()
        if value:
            parts.append(value)
    return "\n\n".join(parts)


def _narrative_suggests_high_concern(content: str) -> bool:
    return any(p.search(content) for p in _HIGH_CONCERN_PATTERNS)


def _narrative_suggests_approval(content: str) -> bool:
    return any(p.search(content) for p in _APPROVAL_LIKE_PATTERNS)


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    content = str(payload.get("content") or "")
    narrative = _narrative_text(payload)
    meta_status = str(payload.get("constitution_check_status") or "").strip()

    embedded_m = _ADVISORY_RE.search(content)
    embedded_status = embedded_m.group(1).strip() if embedded_m else ""

    if embedded_status and meta_status and embedded_status != meta_status:
        errors.append(
            f"embedded CONSTITUTION_ADVISORY status {embedded_status!r} != "
            f"constitution_check_status {meta_status!r}"
        )

    if meta_status == "advisory_flagged" and "CONSTITUTION_ADVISORY" not in content:
        errors.append("constitution_check_status is advisory_flagged but content has no CONSTITUTION_ADVISORY line")

    tier_raw = str(payload.get("staged_risk_tier") or "").strip().lower()
    if tier_raw in _APPROVAL_LIKE_TIERS and _narrative_suggests_high_concern(narrative):
        errors.append(
            f"narrative contains high-concern phrasing but staged_risk_tier is {tier_raw!r} "
            "(reasoning vs action - reconcile text and structured tier)"
        )
    if tier_raw in _MANUAL_OR_HIGH_TIERS and _narrative_suggests_approval(narrative):
        errors.append(
            f"narrative contains approval-like phrasing but staged_risk_tier is {tier_raw!r} "
            "(reasoning vs action - reconcile text and structured tier)"
        )

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate handback analysis vs constitution meta.")
    ap.add_argument("--file", "-f", type=Path, default=None, help="JSON file (default: stdin)")
    args = ap.parse_args()

    if args.file:
        raw = args.file.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"invalid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("JSON root must be an object", file=sys.stderr)
        return 2

    errs = validate_payload(payload)
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
