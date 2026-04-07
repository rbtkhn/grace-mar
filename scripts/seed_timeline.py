#!/usr/bin/env python3
"""
Reconstruct the formation timeline for seed claims from the append-only registry.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/seed_timeline.py -u demo
  python3 scripts/seed_timeline.py -u demo --seed-id seed-demo-005
  python3 scripts/seed_timeline.py -u demo --json
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


def _load_all_snapshots(user_id: str) -> dict[str, list[dict[str, Any]]]:
    """Load ALL snapshots per seed_id (preserving append order for timeline)."""
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    if not path.exists():
        return {}
    history: dict[str, list[dict[str, Any]]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            sid = row.get("seed_id", "")
            if sid:
                history.setdefault(sid, []).append(row)
        except json.JSONDecodeError:
            continue
    return history


def build_timeline(snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build a timeline of events from a claim's snapshot history."""
    if not snapshots:
        return []

    events: list[dict[str, Any]] = []
    prev_status = None
    prev_obs = 0
    prev_confidence = 0.0
    prev_ctrds = 0

    for snap in snapshots:
        ts = snap.get("last_seen", snap.get("first_seen", ""))
        status = snap.get("status", "")
        obs = snap.get("observation_count", 1)
        conf = snap.get("confidence", 0)
        rec = snap.get("recurrence_score", 0)
        ctrds = snap.get("contradiction_count", 0)

        if prev_status is None:
            events.append({
                "timestamp": snap.get("first_seen", ts),
                "event": "first_observed",
                "detail": f"Claim first seen: \"{snap.get('claim_text', '')[:60]}\"",
                "status": status,
                "observation_count": obs,
                "confidence": conf,
                "recurrence_score": rec,
            })
        else:
            if status != prev_status:
                events.append({
                    "timestamp": ts,
                    "event": "status_change",
                    "detail": f"{prev_status} -> {status}",
                    "status": status,
                    "observation_count": obs,
                    "confidence": conf,
                    "recurrence_score": rec,
                })
            if obs > prev_obs:
                events.append({
                    "timestamp": ts,
                    "event": "new_observation",
                    "detail": f"observation #{obs}",
                    "status": status,
                    "observation_count": obs,
                    "confidence": conf,
                    "recurrence_score": rec,
                })
            if ctrds > prev_ctrds:
                new_refs = snap.get("contradiction_refs", [])[prev_ctrds:]
                events.append({
                    "timestamp": ts,
                    "event": "contradiction_appeared",
                    "detail": f"contradiction #{ctrds}: {', '.join(new_refs)}",
                    "status": status,
                    "observation_count": obs,
                    "confidence": conf,
                    "recurrence_score": rec,
                })
            if abs(conf - prev_confidence) >= 0.05 and status == prev_status and obs == prev_obs:
                direction = "rose" if conf > prev_confidence else "fell"
                events.append({
                    "timestamp": ts,
                    "event": f"confidence_{direction}",
                    "detail": f"{prev_confidence:.2f} -> {conf:.2f}",
                    "status": status,
                    "observation_count": obs,
                    "confidence": conf,
                    "recurrence_score": rec,
                })

        prev_status = status
        prev_obs = obs
        prev_confidence = conf
        prev_ctrds = ctrds

    return events


def _format_timeline(seed_id: str, events: list[dict[str, Any]], claim_text: str) -> str:
    lines: list[str] = []
    lines.append(f"  Timeline: {seed_id}")
    lines.append(f"  Claim: \"{claim_text[:70]}\"")
    lines.append("  " + "-" * 70)
    for ev in events:
        ts = ev["timestamp"][:19].replace("T", " ")
        icon = {
            "first_observed": "+",
            "new_observation": "o",
            "status_change": ">",
            "contradiction_appeared": "!",
            "confidence_rose": "^",
            "confidence_fell": "v",
        }.get(ev["event"], "?")
        lines.append(
            f"  {ts}  [{icon}] {ev['event']:<25} {ev['detail']}"
            f"  (conf={ev['confidence']:.2f} rec={ev['recurrence_score']:.2f})"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed claim formation timeline.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--seed-id", help="Show timeline for a specific claim")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    all_snapshots = _load_all_snapshots(args.user)
    if not all_snapshots:
        print("No seed claims found.", file=sys.stderr)
        return 0

    if args.seed_id:
        if args.seed_id not in all_snapshots:
            print(f"Seed claim {args.seed_id} not found.", file=sys.stderr)
            return 1
        targets = {args.seed_id: all_snapshots[args.seed_id]}
    else:
        targets = all_snapshots

    all_timelines: dict[str, Any] = {}
    for sid, snaps in sorted(targets.items()):
        events = build_timeline(snaps)
        claim_text = snaps[-1].get("claim_text", "") if snaps else ""
        all_timelines[sid] = {"claim_text": claim_text, "events": events}

    if args.json:
        print(json.dumps(all_timelines, indent=2))
    else:
        for sid, data in all_timelines.items():
            print(_format_timeline(sid, data["events"], data["claim_text"]))
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
