#!/usr/bin/env python3
"""
Advisory precheck before staging gate candidates — does not merge or block HTTP by default.

Exits 0 always unless --strict and promotion_recommendation is block.
Use --strict only when operator wants a hard stop in CI or local hooks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from policy_mode_config import (  # noqa: E402
    UnknownPolicyModeError,
    load_defaults,
    resolve_mode,
    staging_decision,
)
from observation_store import by_id  # noqa: E402
from uncertainty_envelope import (  # noqa: E402
    compute_envelope,
    envelope_to_json,
    synthetic_observation_from_text,
)


def main() -> int:
    p = argparse.ArgumentParser(description="Advisory uncertainty precheck for gate staging.")
    p.add_argument("--id", action="append", dest="ids", metavar="OBS_ID")
    p.add_argument(
        "--text",
        default="",
        help="Free text (synthetic observation) when no --id; for OpenClaw/handback preview",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if promotion_recommendation is block (operator/CI only)",
    )
    p.add_argument(
        "--force-override",
        action="store_true",
        help="With --strict, still exit 0 (document operator override)",
    )
    p.add_argument(
        "--policy-mode",
        default=None,
        help="Optional: tie stderr hints to policy envelope (GRACE_MAR_POLICY_MODE if unset)",
    )
    p.add_argument(
        "--target-surface",
        default=None,
        help="Target surface hint for staging_decision check (e.g. SELF, EVIDENCE)",
    )
    p.add_argument(
        "--policy-ack",
        action="store_true",
        help="Acknowledge policy warn/hold to proceed (matches stage_candidate behavior)",
    )
    args = p.parse_args()

    pdefs = load_defaults()
    try:
        pol = resolve_mode(args.policy_mode, pdefs, strict=True)
    except UnknownPolicyModeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    verb, reason = staging_decision(pol, args.target_surface, pdefs)
    print(f"policy_mode: {pol}", file=sys.stderr)
    print(f"staging_decision: {verb} — {reason}", file=sys.stderr)

    if verb == "blocked":
        print(f"error: policy mode {pol}: {reason}", file=sys.stderr)
        return 2
    if verb in ("warn", "hold_hint") and not args.policy_ack:
        print(
            f"error: policy mode {pol}: {reason} Pass --policy-ack to proceed.",
            file=sys.stderr,
        )
        return 2
    if verb in ("warn", "hold_hint") and args.policy_ack:
        print(f"warning: policy mode {pol} override acknowledged: {reason}", file=sys.stderr)

    rows: list[dict] = []
    if args.ids:
        for oid in args.ids:
            raw = by_id(oid)
            if raw is None:
                print(f"error: missing observation: {oid}", file=sys.stderr)
                return 2
            rows.append(raw)
    elif args.text.strip():
        rows = [synthetic_observation_from_text(args.text.strip())]
    else:
        print("error: provide --id (repeatable) or non-empty --text", file=sys.stderr)
        return 2

    env = compute_envelope(rows)
    print(envelope_to_json(env))
    promo = env.get("promotion_recommendation", "")
    blob = pdefs.get(pol) or {}
    if pol == "high_risk_abstention" or blob.get("abstention_level") == "very_strict":
        print(
            f"\nPOLICY_MODE: `{pol}` — pair envelope output with conservative promotion review; "
            "see docs/policy-modes.md and docs/abstention-policy.md.",
            file=sys.stderr,
        )
    if promo == "block":
        print(
            "\nABSTENTION_PRECHECK: promotion_recommendation=block (advisory). "
            "Review docs/abstention-policy.md. Override only with explicit operator decision.",
            file=sys.stderr,
        )
    if args.strict and not args.force_override and promo == "block":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
