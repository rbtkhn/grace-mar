#!/usr/bin/env python3
"""
Evaluate seed claims against promotion rules and report readiness.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/evaluate_seed_promotion.py -u grace-mar
  python3 scripts/evaluate_seed_promotion.py --advance
  python3 scripts/evaluate_seed_promotion.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"

PROMOTABLE_STATUSES = {"recurring", "candidate", "cross_evidenced", "stable"}
TERMINAL_STATUSES = {"promoted", "rejected", "expired"}


def _load_rules(rules_path: Path | None = None) -> dict[str, Any]:
    path = rules_path or (REPO_ROOT / "config" / "seed-promotion-rules.json")
    if not path.exists():
        return {"defaults": {"min_observations": 2, "min_sessions": 2,
                             "min_time_span_days": 7, "recurrence_score_threshold": 0.6,
                             "contradiction_policy": "block_until_resolved"},
                "sensitivity_overrides": {}, "category_overrides": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_latest(user_id: str) -> dict[str, dict[str, Any]]:
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            sid = row.get("seed_id", "")
            if sid:
                latest[sid] = row
        except json.JSONDecodeError:
            continue
    return latest


def _effective_rules(
    claim: dict[str, Any], rules: dict[str, Any],
) -> dict[str, Any]:
    """Merge defaults, sensitivity overrides, and category overrides."""
    defaults = dict(rules.get("defaults", {}))
    sensitivity = claim.get("sensitivity", "standard")
    category = claim.get("category", "")

    cat_overrides = rules.get("category_overrides", {}).get(category, {})
    if "sensitivity_floor" in cat_overrides:
        floor = cat_overrides["sensitivity_floor"]
        floors = {"standard": 0, "elevated": 1, "high": 2}
        if floors.get(floor, 0) > floors.get(sensitivity, 0):
            sensitivity = floor

    sens_overrides = rules.get("sensitivity_overrides", {}).get(sensitivity, {})
    effective = {**defaults, **sens_overrides, **cat_overrides}
    effective.pop("sensitivity_floor", None)
    return effective


def _count_sessions(source_events: list[str]) -> int:
    sessions = {s for s in source_events if s.startswith("session-")}
    return max(len(sessions), len(source_events))


def _time_span_days(first_seen: str, last_seen: str) -> int:
    try:
        fs = datetime.fromisoformat(first_seen)
        ls = datetime.fromisoformat(last_seen)
        return max((ls - fs).days, 0)
    except (ValueError, TypeError):
        return 0


def evaluate_claim(
    claim: dict[str, Any], rules: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate a single claim against promotion rules.

    Returns dict with keys: seed_id, verdict, blockers, approaching, met.
    """
    eff = _effective_rules(claim, rules)
    blockers: list[str] = []
    approaching: list[str] = []
    met: list[str] = []

    obs = claim.get("observation_count", 1)
    min_obs = eff.get("min_observations", 2)
    if obs < min_obs:
        diff = min_obs - obs
        if diff == 1:
            approaching.append(f"observations: {obs}/{min_obs} (need {diff} more)")
        else:
            blockers.append(f"observations: {obs}/{min_obs}")
    else:
        met.append(f"observations: {obs}/{min_obs}")

    sessions = _count_sessions(claim.get("source_events", []))
    min_sessions = eff.get("min_sessions", 2)
    if sessions < min_sessions:
        diff = min_sessions - sessions
        if diff == 1:
            approaching.append(f"sessions: {sessions}/{min_sessions} (need {diff} more)")
        else:
            blockers.append(f"sessions: {sessions}/{min_sessions}")
    else:
        met.append(f"sessions: {sessions}/{min_sessions}")

    span = _time_span_days(claim.get("first_seen", ""), claim.get("last_seen", ""))
    min_span = eff.get("min_time_span_days", 7)
    if span < min_span:
        blockers.append(f"time_span: {span}d/{min_span}d")
    else:
        met.append(f"time_span: {span}d/{min_span}d")

    rec = claim.get("recurrence_score", 0)
    rec_thresh = eff.get("recurrence_score_threshold", 0.6)
    if rec < rec_thresh:
        if rec >= rec_thresh - 0.1:
            approaching.append(f"recurrence: {rec:.2f}/{rec_thresh}")
        else:
            blockers.append(f"recurrence: {rec:.2f}/{rec_thresh}")
    else:
        met.append(f"recurrence: {rec:.2f}/{rec_thresh}")

    ctrds = claim.get("contradiction_count", 0)
    policy = eff.get("contradiction_policy", "block_until_resolved")
    if ctrds > 0 and policy == "block_until_resolved":
        blockers.append(f"contradictions: {ctrds} (policy: block_until_resolved)")

    if eff.get("requires_operator_approval"):
        blockers.append("requires explicit operator approval")
    elif eff.get("requires_operator_flag"):
        approaching.append("requires operator flag before promotion")

    if blockers:
        verdict = "blocked"
    elif approaching:
        verdict = "approaching"
    else:
        verdict = "ready"

    return {
        "seed_id": claim["seed_id"],
        "claim_text": claim.get("claim_text", ""),
        "status": claim.get("status", ""),
        "category": claim.get("category", ""),
        "sensitivity": claim.get("sensitivity", "standard"),
        "verdict": verdict,
        "blockers": blockers,
        "approaching": approaching,
        "met": met,
    }


def evaluate_all(
    user_id: str, rules: dict[str, Any],
) -> list[dict[str, Any]]:
    latest = _load_latest(user_id)
    results = []
    for claim in latest.values():
        if claim.get("status") in TERMINAL_STATUSES:
            continue
        results.append(evaluate_claim(claim, rules))
    return sorted(results, key=lambda r: (
        {"ready": 0, "approaching": 1, "blocked": 2}[r["verdict"]],
        r["seed_id"],
    ))


def advance_claims(user_id: str, rules: dict[str, Any]) -> list[str]:
    """Auto-advance claims whose status can be upgraded based on evaluation."""
    latest = _load_latest(user_id)
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    advanced: list[str] = []
    for claim in latest.values():
        if claim.get("status") in TERMINAL_STATUSES:
            continue
        result = evaluate_claim(claim, rules)
        current = claim.get("status", "observed")
        new_status = current
        if result["verdict"] == "ready" and current in ("observed", "weak_signal", "recurring"):
            new_status = "candidate"
        elif current == "observed" and claim.get("observation_count", 1) >= 2:
            new_status = "weak_signal"

        if new_status != current:
            claim["status"] = new_status
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(claim) + "\n")
            advanced.append(f"{claim['seed_id']}: {current} -> {new_status}")
    return advanced


def _format_results(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("  Seed Promotion Evaluation")
    lines.append("  " + "-" * 70)

    for verdict_group in ("ready", "approaching", "blocked"):
        group = [r for r in results if r["verdict"] == verdict_group]
        if not group:
            continue
        label = {"ready": "READY FOR PROMOTION", "approaching": "APPROACHING",
                 "blocked": "BLOCKED"}[verdict_group]
        lines.append(f"\n  [{label}] ({len(group)} claims)")
        for r in group:
            lines.append(f"    {r['seed_id']:<20} [{r['status']}] {r['claim_text'][:50]}")
            if r["met"]:
                lines.append(f"      met: {', '.join(r['met'])}")
            if r["approaching"]:
                lines.append(f"      approaching: {', '.join(r['approaching'])}")
            if r["blockers"]:
                lines.append(f"      blocked: {', '.join(r['blockers'])}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate seed promotion readiness.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--rules", help="Path to promotion rules JSON")
    parser.add_argument("--advance", action="store_true",
                        help="Auto-advance statuses based on evaluation")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rules_path = Path(args.rules) if args.rules else None
    rules = _load_rules(rules_path)

    if args.advance:
        advanced = advance_claims(args.user, rules)
        if advanced:
            for line in advanced:
                print(f"  Advanced: {line}")
        else:
            print("  No claims advanced.")
        return 0

    results = evaluate_all(args.user, rules)
    if not results:
        print("No active seed claims to evaluate.", file=sys.stderr)
        return 0

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(_format_results(results))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
