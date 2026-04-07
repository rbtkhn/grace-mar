#!/usr/bin/env python3
"""
Generate the Weak Signal Nursery report: 'why still a seed' and 'what would mature this'.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/seed_nursery_report.py -u demo
  python3 scripts/seed_nursery_report.py --seed-id seed-demo-003
  python3 scripts/seed_nursery_report.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"

NURSERY_STATUSES = {"observed", "weak_signal", "recurring"}
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


def _effective_rules(claim: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    defaults = dict(rules.get("defaults", {}))
    sensitivity = claim.get("sensitivity", "standard")
    category = claim.get("category", "")
    cat_overrides = rules.get("category_overrides", {}).get(category, {})
    if "sensitivity_floor" in cat_overrides:
        floors = {"standard": 0, "elevated": 1, "high": 2}
        floor = cat_overrides["sensitivity_floor"]
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


def nursery_card(claim: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    """Build a nursery report card for a single claim."""
    eff = _effective_rules(claim, rules)
    obs = claim.get("observation_count", 1)
    sessions = _count_sessions(claim.get("source_events", []))
    span = _time_span_days(claim.get("first_seen", ""), claim.get("last_seen", ""))
    ctrds = claim.get("contradiction_count", 0)

    why_interesting: list[str] = []
    why_interesting.append(f"Observed {obs} time(s) in {claim.get('category', 'unknown')} category")
    if obs > 1:
        why_interesting.append(f"Recurring across {sessions} session(s) over {span} day(s)")
    if claim.get("notes"):
        why_interesting.append(f"Note: {claim['notes']}")

    still_seed: list[str] = []
    min_obs = eff.get("min_observations", 2)
    if obs < min_obs:
        still_seed.append(f"insufficient recurrence ({obs} observation(s), need {min_obs})")
    min_sess = eff.get("min_sessions", 2)
    if sessions < min_sess:
        still_seed.append(f"insufficient session diversity ({sessions} session(s), need {min_sess})")
    min_span = eff.get("min_time_span_days", 7)
    if span < min_span:
        still_seed.append(f"insufficient time stability ({span} day(s), need {min_span})")
    rec_thresh = eff.get("recurrence_score_threshold", 0.6)
    rec = claim.get("recurrence_score", 0)
    if rec < rec_thresh:
        still_seed.append(f"recurrence score below threshold ({rec:.2f}, need {rec_thresh})")
    if ctrds > 0 and eff.get("contradiction_policy") == "block_until_resolved":
        still_seed.append(f"conflicting evidence ({ctrds} contradiction(s))")
    if eff.get("requires_operator_approval"):
        still_seed.append("sensitivity tier requires explicit operator approval")
    elif eff.get("requires_operator_flag"):
        still_seed.append("sensitivity tier requires operator flag")
    if not still_seed:
        still_seed.append("meets all thresholds — may be ready for promotion")

    would_mature: list[str] = []
    if obs < min_obs:
        would_mature.append(f"{min_obs - obs} more observation(s)")
    if sessions < min_sess:
        would_mature.append(f"evidence from {min_sess - sessions} more distinct session(s)")
    if span < min_span:
        would_mature.append(f"time stability: {min_span - span} more day(s) between first and last observation")
    if eff.get("requires_operator_flag") or eff.get("requires_operator_approval"):
        would_mature.append("explicit operator confirmation")
    if ctrds > 0:
        would_mature.append("contradiction resolution or preservation note")
    if not would_mature:
        would_mature.append("ready for promotion review")

    would_falsify: list[str] = []
    if ctrds > 0:
        refs = claim.get("contradiction_refs", [])
        would_falsify.append(f"existing contradictions: {', '.join(refs)}")
    would_falsify.append("explicit statement contradicting this claim")
    would_falsify.append("evidence from a different context opposing this pattern")

    affects_behavior = claim.get("status") in ("recurring", "candidate", "cross_evidenced", "stable")

    review_date = claim.get("expiry_review_date")
    if not review_date:
        try:
            ls = datetime.fromisoformat(claim.get("last_seen", ""))
            review_date = (ls + timedelta(days=30)).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            review_date = "unknown"

    return {
        "seed_id": claim["seed_id"],
        "claim_text": claim.get("claim_text", ""),
        "status": claim.get("status", ""),
        "category": claim.get("category", ""),
        "sensitivity": claim.get("sensitivity", "standard"),
        "why_interesting": why_interesting,
        "still_seed_because": still_seed,
        "would_mature_with": would_mature,
        "would_falsify_with": would_falsify,
        "affects_behavior": affects_behavior,
        "review_by": review_date,
    }


def _format_card(card: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"{card['seed_id']}: \"{card['claim_text']}\" ({card['category']})")
    lines.append(f"  Status: {card['status']}")
    lines.append(f"  Why interesting: {'; '.join(card['why_interesting'])}")
    lines.append(f"  Still a seed because: {'; '.join(card['still_seed_because'])}")
    lines.append(f"  Would mature with: {'; '.join(card['would_mature_with'])}")
    lines.append(f"  Would falsify with: {'; '.join(card['would_falsify_with'])}")
    affects = "yes (may influence soft exploration)" if card["affects_behavior"] else "no (not yet influencing recommendations)"
    lines.append(f"  Affects behavior: {affects}")
    lines.append(f"  Review by: {card['review_by']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Weak Signal Nursery report.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--seed-id", help="Report on a specific claim")
    parser.add_argument("--rules", help="Path to promotion rules JSON")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rules = _load_rules(Path(args.rules) if args.rules else None)
    latest = _load_latest(args.user)

    if not latest:
        print("No seed claims found.", file=sys.stderr)
        return 0

    if args.seed_id:
        if args.seed_id not in latest:
            print(f"Seed claim {args.seed_id} not found.", file=sys.stderr)
            return 1
        cards = [nursery_card(latest[args.seed_id], rules)]
    else:
        nursery = {sid: c for sid, c in latest.items()
                   if c.get("status") not in TERMINAL_STATUSES}
        cards = [nursery_card(c, rules) for c in
                 sorted(nursery.values(), key=lambda c: c.get("promotion_readiness", 0), reverse=True)]

    if not cards:
        print("No nursery-resident claims.", file=sys.stderr)
        return 0

    if args.json:
        print(json.dumps(cards, indent=2))
    else:
        print(f"  Weak Signal Nursery — {args.user}")
        print("  " + "-" * 70)
        for card in cards:
            print()
            print(_format_card(card))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
