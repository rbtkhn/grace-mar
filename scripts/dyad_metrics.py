#!/usr/bin/env python3
"""
Dyad metrics for Grace-Mar — tricameral mind (MIND, RECORD, VOICE).

Tracks MIND–RECORD/VOICE activity:
  - Consultations (lookup, grounded query) — Mind consulting Record/Voice
  - Activity reports — Mind feeding the Record ("we did X")
  - Integrations — applied events (conscious gate crossings)

Usage:
    python scripts/dyad_metrics.py [--user pilot-001] [--days 7] [--json]
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = "pilot-001"
DEFAULT_DAYS = 7

# Each lookup ends with lookup_rephrase; use that for 1:1 consultation count.
# library_lookup + lookup_factual are intermediate steps.
CONSULTATION_BUCKET = "lookup_rephrase"


def _parse_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().strip().splitlines():
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def _ts_in_window(ts_str: str, cutoff: datetime) -> bool:
    if not ts_str:
        return False
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.replace(tzinfo=None)
        return dt >= cutoff
    except (ValueError, TypeError):
        return False


def compute_dyad_metrics(profile_dir: Path, days: int) -> dict:
    """Compute dyad metrics from COMPUTE-LEDGER and PIPELINE-EVENTS."""
    cutoff = datetime.now() - timedelta(days=days)
    consultations_7d = 0
    integrations_7d = 0
    activity_reports_7d = 0
    dyad_lookups_7d = 0
    dyad_grounded_7d = 0

    ledger_path = profile_dir / "COMPUTE-LEDGER.jsonl"
    for row in _parse_jsonl(ledger_path):
        if not _ts_in_window(row.get("ts", ""), cutoff):
            continue
        if row.get("bucket") == CONSULTATION_BUCKET:
            consultations_7d += 1

    events_path = profile_dir / "PIPELINE-EVENTS.jsonl"
    for row in _parse_jsonl(events_path):
        if not _ts_in_window(row.get("ts", ""), cutoff):
            continue
        e = row.get("event", "")
        if e in ("applied", "approved"):
            integrations_7d += 1
        elif e == "dyad:activity_report":
            activity_reports_7d += 1
        elif e == "dyad:lookup":
            dyad_lookups_7d += 1
        elif e == "dyad:grounded_query":
            dyad_grounded_7d += 1

    # Use dyad events if present, else fall back to ledger consultations
    if dyad_lookups_7d or dyad_grounded_7d:
        consultations_7d = dyad_lookups_7d + dyad_grounded_7d

    dyad_score = consultations_7d + (2 * integrations_7d) + activity_reports_7d

    return {
        "consultations_7d": consultations_7d,
        "integrations_7d": integrations_7d,
        "activity_reports_7d": activity_reports_7d,
        "dyad_score": dyad_score,
    }


def report(metrics: dict, user: str, days: int) -> str:
    """Human-readable report."""
    return "\n".join(
        [
            "# Dyad Metrics",
            "",
            f"User: {user}",
            f"Window: last {days} days",
            "",
            "## Dyad Activity",
            f"  Consultations (7d):   {metrics['consultations_7d']}",
            f"  Integrations (7d):    {metrics['integrations_7d']}",
            f"  Activity reports (7d): {metrics['activity_reports_7d']}",
            "",
            f"  Dyad score:           {metrics['dyad_score']}",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Dyad metrics for Grace-Mar")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id")
    parser.add_argument("--days", "-d", type=int, default=DEFAULT_DAYS, help="Window in days")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    profile_dir = REPO_ROOT / "users" / args.user
    if not profile_dir.exists():
        print(f"Profile dir not found: {profile_dir}", file=__import__("sys").stderr)
        exit(1)

    metrics = compute_dyad_metrics(profile_dir, args.days)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print(report(metrics, args.user, args.days))


if __name__ == "__main__":
    main()
