#!/usr/bin/env python3
"""
Append or update a seed claim in users/<id>/seed-registry.jsonl.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/emit_seed_claim.py \\
    --claim "prefers emeralds over rubies" --category curiosity \\
    --source "session-2026-04-06"

  python3 scripts/emit_seed_claim.py \\
    --seed-id seed-0042 --observe --source "session-2026-04-07" \\
    --status recurring

  python3 scripts/emit_seed_claim.py \\
    --seed-id seed-0042 --set-status promoted
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"

STATUS_ORDER = [
    "observed", "weak_signal", "recurring", "candidate",
    "cross_evidenced", "stable", "promoted", "rejected", "expired",
]
CATEGORIES = [
    "identity", "curiosity", "pedagogy", "expression",
    "memory_governance", "safety", "preference",
]
SENSITIVITIES = ["standard", "elevated", "high"]


def registry_path(user_id: str = DEFAULT_USER_ID) -> Path:
    return REPO_ROOT / "users" / user_id / "seed-registry.jsonl"


def _load_latest(user_id: str) -> dict[str, dict[str, Any]]:
    """Load the latest snapshot per seed_id."""
    path = registry_path(user_id)
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


def _generate_seed_id(claim_text: str) -> str:
    h = hashlib.sha256(claim_text.encode()).hexdigest()[:8]
    return f"seed-{h}"


def compute_recurrence_score(
    observation_count: int,
    first_seen: str,
    last_seen: str,
    source_count: int | None = None,
) -> float:
    """Recurrence = f(observation_count, time_span, source_diversity).

    Uses a logarithmic curve that rewards early recurrence but saturates.
    """
    obs_factor = min(1.0, math.log2(max(observation_count, 1) + 1) / 4.0)

    try:
        fs = datetime.fromisoformat(first_seen)
        ls = datetime.fromisoformat(last_seen)
        days = max((ls - fs).days, 0)
    except (ValueError, TypeError):
        days = 0
    time_factor = min(1.0, days / 30.0)

    src = source_count if source_count is not None else observation_count
    diversity_factor = min(1.0, src / 5.0)

    return round(obs_factor * 0.4 + time_factor * 0.35 + diversity_factor * 0.25, 4)


def compute_confidence(recurrence_score: float, contradiction_count: int) -> float:
    penalty = min(0.5, contradiction_count * 0.15)
    return round(max(0.0, recurrence_score - penalty), 4)


def compute_promotion_readiness(
    confidence: float, recurrence_score: float, contradiction_count: int,
) -> float:
    if contradiction_count > 0:
        return round(max(0.0, confidence * 0.5), 4)
    return round((confidence + recurrence_score) / 2.0, 4)


def emit_seed_claim(
    user_id: str = DEFAULT_USER_ID,
    *,
    seed_id: str | None = None,
    claim_text: str | None = None,
    category: str | None = None,
    source_events: list[str] | None = None,
    status: str | None = None,
    sensitivity: str = "standard",
    notes: str | None = None,
    observe: bool = False,
    contradiction_ref: str | None = None,
    expiry_review_date: str | None = None,
) -> dict[str, Any]:
    """Emit or update a seed claim. Returns the emitted row."""
    now = datetime.now(timezone.utc).isoformat()
    latest = _load_latest(user_id)

    if seed_id and seed_id in latest and observe:
        existing = latest[seed_id]
        existing["observation_count"] += 1
        existing["last_seen"] = now
        if source_events:
            existing["source_events"] = list(
                dict.fromkeys(existing.get("source_events", []) + source_events)
            )
        if contradiction_ref:
            refs = existing.get("contradiction_refs", [])
            if contradiction_ref not in refs:
                refs.append(contradiction_ref)
            existing["contradiction_refs"] = refs
            existing["contradiction_count"] = len(refs)
        existing["recurrence_score"] = compute_recurrence_score(
            existing["observation_count"],
            existing["first_seen"],
            existing["last_seen"],
            len(existing.get("source_events", [])),
        )
        existing["confidence"] = compute_confidence(
            existing["recurrence_score"], existing.get("contradiction_count", 0),
        )
        existing["promotion_readiness"] = compute_promotion_readiness(
            existing["confidence"], existing["recurrence_score"],
            existing.get("contradiction_count", 0),
        )
        if status and status in STATUS_ORDER:
            existing["status"] = status
        if notes:
            existing["notes"] = notes
        if expiry_review_date:
            existing["expiry_review_date"] = expiry_review_date
        row = existing
    elif seed_id and seed_id in latest and status:
        existing = latest[seed_id]
        existing["status"] = status
        existing["last_seen"] = now
        if source_events:
            existing["source_events"] = list(
                dict.fromkeys(existing.get("source_events", []) + source_events)
            )
        if notes:
            existing["notes"] = notes
        if contradiction_ref:
            refs = existing.get("contradiction_refs", [])
            if contradiction_ref not in refs:
                refs.append(contradiction_ref)
            existing["contradiction_refs"] = refs
            existing["contradiction_count"] = len(refs)
            existing["confidence"] = compute_confidence(
                existing["recurrence_score"], existing["contradiction_count"],
            )
            existing["promotion_readiness"] = compute_promotion_readiness(
                existing["confidence"], existing["recurrence_score"],
                existing["contradiction_count"],
            )
        row = existing
    else:
        if not claim_text:
            raise ValueError("claim_text required for new seed claims")
        if not category or category not in CATEGORIES:
            raise ValueError(f"category must be one of {CATEGORIES}")
        if not source_events:
            raise ValueError("at least one source_event required")

        sid = seed_id or _generate_seed_id(claim_text)
        c_refs: list[str] = []
        if contradiction_ref:
            c_refs.append(contradiction_ref)

        rec = compute_recurrence_score(1, now, now, len(source_events))
        conf = compute_confidence(rec, len(c_refs))
        prom = compute_promotion_readiness(conf, rec, len(c_refs))

        row = {
            "seed_id": sid,
            "user_slug": user_id,
            "claim_text": claim_text,
            "category": category,
            "source_events": source_events,
            "first_seen": now,
            "last_seen": now,
            "observation_count": 1,
            "recurrence_score": rec,
            "contradiction_count": len(c_refs),
            "contradiction_refs": c_refs,
            "confidence": conf,
            "status": status or "observed",
            "promotion_readiness": prom,
            "sensitivity": sensitivity,
        }
        if notes:
            row["notes"] = notes
        if expiry_review_date:
            row["expiry_review_date"] = expiry_review_date

    path = registry_path(user_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")

    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit or update a seed claim.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--seed-id", help="Existing seed_id to update")
    parser.add_argument("--claim", help="Claim text (required for new claims)")
    parser.add_argument("--category", choices=CATEGORIES, help="Claim category")
    parser.add_argument("--source", action="append", dest="sources",
                        help="Source event ref (repeatable)")
    parser.add_argument("--status", choices=STATUS_ORDER, help="Set status")
    parser.add_argument("--set-status", dest="set_status", choices=STATUS_ORDER,
                        help="Change status on existing claim (alias for --status)")
    parser.add_argument("--sensitivity", choices=SENSITIVITIES, default="standard")
    parser.add_argument("--observe", action="store_true",
                        help="Increment observation_count on existing claim")
    parser.add_argument("--contradiction-ref", help="Ref to a conflicting claim or evidence")
    parser.add_argument("--expiry-review-date", help="YYYY-MM-DD review date")
    parser.add_argument("--notes", help="Optional notes")
    parser.add_argument("--json", action="store_true", help="Print emitted row as JSON")
    args = parser.parse_args()

    effective_status = args.set_status or args.status

    try:
        row = emit_seed_claim(
            args.user,
            seed_id=args.seed_id,
            claim_text=args.claim,
            category=args.category,
            source_events=args.sources,
            status=effective_status,
            sensitivity=args.sensitivity,
            observe=args.observe,
            contradiction_ref=args.contradiction_ref,
            expiry_review_date=args.expiry_review_date,
            notes=args.notes,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(f"{row['seed_id']}  [{row['status']}]  {row['claim_text'][:60]}  "
              f"(obs={row['observation_count']}, rec={row['recurrence_score']:.2f}, "
              f"conf={row['confidence']:.2f})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
