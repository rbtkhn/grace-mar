#!/usr/bin/env python3
"""
Emit an identity-diff JSON when a seed claim changes status.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/emit_seed_diff.py -u demo --seed-id seed-demo-005 \\
    --from-status recurring --to-status candidate

  python3 scripts/emit_seed_diff.py -u demo --seed-id seed-demo-003 \\
    --from-status observed --to-status weak_signal --print-only
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


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


def _time_span_desc(claim: dict[str, Any]) -> str:
    try:
        fs = datetime.fromisoformat(claim.get("first_seen", ""))
        ls = datetime.fromisoformat(claim.get("last_seen", ""))
        days = (ls - fs).days
        return f"{days} days"
    except (ValueError, TypeError):
        return "unknown"


def _why_it_matters(from_status: str, to_status: str, claim: dict[str, Any]) -> str:
    if to_status == "candidate":
        return "ready for promotion review — may enter governed state after operator approval"
    if to_status == "recurring":
        return "pattern emerging — may influence soft exploration but not governed profile yet"
    if to_status == "weak_signal":
        return "interesting but immature — watching for recurrence"
    if to_status == "promoted":
        return "now part of governed state — identity claim is durable"
    if to_status == "rejected":
        return "operator decided against promotion — claim will not enter governed state"
    if to_status == "expired":
        return "insufficient recurrence — claim timed out without promotion"
    if to_status in ("cross_evidenced", "stable"):
        return "strengthening — multiple independent sources support this observation"
    return f"status changed from {from_status} to {to_status}"


def _recommended_action(to_status: str, claim: dict[str, Any]) -> str:
    if to_status == "candidate":
        return "accept"
    if to_status in ("recurring", "weak_signal", "cross_evidenced"):
        return "defer"
    if to_status == "stable":
        return "accept"
    if to_status in ("rejected", "expired"):
        return "reject"
    if to_status == "promoted":
        return "accept"
    return "defer"


def build_seed_diff(
    claim: dict[str, Any],
    from_status: str,
    to_status: str,
    diff_id: str | None = None,
) -> dict[str, Any]:
    """Build an identity-diff v1 JSON object for a seed status transition."""
    now = datetime.now(timezone.utc).isoformat()
    sid = claim["seed_id"]
    did = diff_id or f"diff-{sid}-{to_status}"

    obs = claim.get("observation_count", 1)
    span = _time_span_desc(claim)
    sessions = len(claim.get("source_events", []))

    return {
        "schemaVersion": "1.0.0",
        "diffId": did,
        "userSlug": claim.get("user_slug", ""),
        "category": "seed_transition",
        "sourceType": "seed",
        "before": {
            "status": from_status,
            "seed_id": sid,
            "claim_text": claim.get("claim_text", ""),
        },
        "after": {
            "status": to_status,
            "seed_id": sid,
            "claim_text": claim.get("claim_text", ""),
            "observation_count": obs,
            "recurrence_score": claim.get("recurrence_score", 0),
        },
        "changeSummary": (
            f"{from_status} -> {to_status}: "
            f"observed {obs} time(s) across {sessions} source(s) over {span}"
        ),
        "confidenceDelta": {
            "before": 0.0 if from_status == "observed" else claim.get("confidence", 0),
            "after": claim.get("confidence", 0),
        },
        "evidenceRefs": claim.get("source_events", [])[:10],
        "recommendedAction": _recommended_action(to_status, claim),
        "whyItMatters": _why_it_matters(from_status, to_status, claim),
    }


def write_diff(user_id: str, diff: dict[str, Any]) -> Path:
    """Write the diff JSON to the review-queue diffs directory."""
    diffs_dir = REPO_ROOT / "users" / user_id / "review-queue" / "diffs"
    diffs_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{diff['diffId']}.json"
    path = diffs_dir / filename
    path.write_text(json.dumps(diff, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a seed diff on status change.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--seed-id", required=True)
    parser.add_argument("--from-status", required=True, help="Previous status")
    parser.add_argument("--to-status", required=True, help="New status")
    parser.add_argument("--diff-id", help="Override diff ID")
    parser.add_argument("--print-only", action="store_true", help="Print without writing")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    latest = _load_latest(args.user)
    if args.seed_id not in latest:
        print(f"Seed claim {args.seed_id} not found.", file=sys.stderr)
        return 1

    claim = latest[args.seed_id]
    diff = build_seed_diff(claim, args.from_status, args.to_status, args.diff_id)

    if args.print_only or args.json:
        print(json.dumps(diff, indent=2))
    else:
        path = write_diff(args.user, diff)
        print(f"Wrote seed diff: {path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
