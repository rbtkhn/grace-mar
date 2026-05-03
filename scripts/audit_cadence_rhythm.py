#!/usr/bin/env python3
"""
Cadence rhythm auditor — read-only discipline audit of cadence events.

Parses work-cadence-events.md and reports dream frequency, bridge coverage,
coffee cadence, and longest gap.  Exposes compute_rhythm_summary() for
import by harness_warmup.py.

Read-only operator tooling — no file writes.

Usage:
  python scripts/audit_cadence_rhythm.py -u grace-mar
  python scripts/audit_cadence_rhythm.py -u grace-mar --days 14 --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"
DEFAULT_GATE_PATH = REPO_ROOT / "users" / "grace-mar" / "recursion-gate.md"

import re

_EVENT_LINE_RE = re.compile(
    r"- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — (\w+) \(([^)]+)\)"
)


_KV_RE = re.compile(r"(\w+)=(\S+)")
KNOWN_CONDUCTOR_SLUGS = frozenset(
    {"toscanini", "furtwangler", "karajan", "kleiber", "bernstein"}
)
CONDUCTOR_PICKED_VALUES = frozenset(
    {"conductor", "E", "D", "D1", "D2", "D3", "D4", "D5"}
)


def parse_events(
    user_id: str,
    *,
    events_path: Path = EVENTS_PATH,
) -> list[dict]:
    """Parse cadence events for a user. Returns list of {dt, kind, user, line, kv}."""
    if not events_path.is_file():
        return []
    events: list[dict] = []
    for line in events_path.read_text(encoding="utf-8").splitlines():
        m = _EVENT_LINE_RE.match(line.strip())
        if not m:
            continue
        date_str, time_str, kind, user = m.group(1), m.group(2), m.group(3), m.group(4).strip()
        if user != user_id:
            continue
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        kv = dict(_KV_RE.findall(line.strip()))
        events.append({"dt": dt, "kind": kind, "user": user, "line": line.strip(), "kv": kv})
    return events


def _normalize_conductor_slug(value: str | None) -> str:
    if value is None:
        return ""
    slug = str(value).strip()
    if "+" in slug:
        slug = slug.split("+", 1)[0].strip()
    return slug


def _is_explicit_conductor_pick(event: dict) -> bool:
    if event.get("kind") != "coffee_pick":
        return False
    kv = event.get("kv") or {}
    picked = str(kv.get("picked", "")).strip()
    conductor = _normalize_conductor_slug(kv.get("conductor"))
    return picked in CONDUCTOR_PICKED_VALUES and conductor in KNOWN_CONDUCTOR_SLUGS


def _is_legacy_partial_conductor_pick(event: dict) -> bool:
    if event.get("kind") != "coffee_pick":
        return False
    kv = event.get("kv") or {}
    conductor = _normalize_conductor_slug(kv.get("conductor"))
    if conductor not in KNOWN_CONDUCTOR_SLUGS:
        return False
    picked = str(kv.get("picked", "")).strip()
    return picked not in CONDUCTOR_PICKED_VALUES


def compute_rhythm_summary(
    user_id: str,
    days: int = 14,
    *,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
) -> dict:
    """Compute cadence discipline summary. Returns a dict suitable for JSON or display."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)

    all_events = parse_events(user_id, events_path=events_path)
    events = [e for e in all_events if e["dt"] >= cutoff]

    if not events:
        return {
            "user_id": user_id,
            "days": days,
            "event_count": 0,
            "discipline": "NO_DATA",
            "detail": "No cadence events found in window.",
        }

    by_kind: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        by_kind[e["kind"]].append(e)

    active_dates: set[str] = set()
    for e in events:
        active_dates.add(e["dt"].strftime("%Y-%m-%d"))
    active_day_count = len(active_dates)

    dream_events = by_kind.get("dream", [])
    bridge_events = by_kind.get("bridge", [])
    coffee_events = by_kind.get("coffee", [])

    last_dream = max((e["dt"] for e in dream_events), default=None)
    last_bridge = max((e["dt"] for e in bridge_events), default=None)

    dream_days_ago = (now - last_dream).days if last_dream else None
    bridge_days_ago = (now - last_bridge).days if last_bridge else None

    coffee_per_active_day = len(coffee_events) / max(1, active_day_count)

    sorted_events = sorted(events, key=lambda e: e["dt"])
    longest_gap_hours = 0.0
    gap_start = gap_end = None
    for i in range(1, len(sorted_events)):
        gap = (sorted_events[i]["dt"] - sorted_events[i - 1]["dt"]).total_seconds() / 3600
        if gap > longest_gap_hours:
            longest_gap_hours = gap
            gap_start = sorted_events[i - 1]["dt"]
            gap_end = sorted_events[i]["dt"]

    days_without_dream_since_last_active = 0
    if dream_events and active_dates:
        sorted_active = sorted(active_dates)
        last_dream_date = last_dream.strftime("%Y-%m-%d") if last_dream else ""
        for d in reversed(sorted_active):
            if d <= last_dream_date:
                break
            days_without_dream_since_last_active += 1

    sessions_without_bridge = 0
    if coffee_events:
        sorted_coffee = sorted(coffee_events, key=lambda e: e["dt"])
        bridge_dts = {e["dt"] for e in bridge_events}
        for i in range(len(sorted_coffee) - 1):
            session_start = sorted_coffee[i]["dt"]
            session_end = sorted_coffee[i + 1]["dt"]
            has_bridge = any(session_start <= bdt <= session_end for bdt in bridge_dts)
            if not has_bridge:
                sessions_without_bridge += 1

    issues: list[str] = []
    if days_without_dream_since_last_active > 2:
        issues.append(f"{days_without_dream_since_last_active} active days without dream")
    if longest_gap_hours > 48:
        issues.append(f"longest gap {longest_gap_hours:.0f}h")
    if coffee_per_active_day < 1.0 and active_day_count > 1:
        issues.append(f"coffee avg {coffee_per_active_day:.1f}/active-day")

    tier_counts: dict[str, int] = defaultdict(int)
    for e in events:
        tier = e["kv"].get("model_tier", "unknown")
        tier_counts[tier] += 1
    tier_total = sum(tier_counts.values())
    tier_pcts = {k: round(100 * v / max(1, tier_total), 1) for k, v in sorted(tier_counts.items())}

    discipline = "DRIFT" if issues else "HEALTHY"

    return {
        "user_id": user_id,
        "days": days,
        "event_count": len(events),
        "active_day_count": active_day_count,
        "discipline": discipline,
        "issues": issues,
        "dream": {
            "count": len(dream_events),
            "last": last_dream.isoformat() if last_dream else None,
            "days_ago": dream_days_ago,
            "ok": days_without_dream_since_last_active <= 2,
        },
        "bridge": {
            "count": len(bridge_events),
            "last": last_bridge.isoformat() if last_bridge else None,
            "days_ago": bridge_days_ago,
            "sessions_without": sessions_without_bridge,
        },
        "coffee": {
            "count": len(coffee_events),
            "per_active_day": round(coffee_per_active_day, 1),
            "ok": coffee_per_active_day >= 1.0 or active_day_count <= 1,
        },
        "longest_gap": {
            "hours": round(longest_gap_hours, 1),
            "start": gap_start.isoformat() if gap_start else None,
            "end": gap_end.isoformat() if gap_end else None,
            "ok": longest_gap_hours <= 48,
        },
        "model_tier": {
            "counts": dict(tier_counts),
            "pcts": tier_pcts,
            "total": tier_total,
        },
    }


def compute_conductor_audit(
    user_id: str,
    days: int = 7,
    *,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
) -> dict:
    """Compute a conductor-specific audit for a rolling look-back window."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    all_events = parse_events(user_id, events_path=events_path)
    events = [e for e in all_events if e["dt"] >= cutoff]
    events.sort(key=lambda e: e["dt"])

    explicit_picks_by_conductor: dict[str, int] = defaultdict(int)
    explicit_outcomes_by_conductor: dict[str, int] = defaultdict(int)
    inferred_outcomes_by_conductor: dict[str, int] = defaultdict(int)
    legacy_partial_picks_by_conductor: dict[str, int] = defaultdict(int)
    per_day: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"picks": 0, "explicit_outcomes": 0, "inferred_outcomes": 0})
    )
    evidence_richness = {"verdict": 0, "action": 0, "notebook_ref": 0, "falsify": 0}
    open_picks: list[dict] = []
    explicit_closed = 0
    inferred_closed = 0
    unattributed_outcomes = 0
    outcomes_without_matching_pick = 0

    for event in events:
        day = event["dt"].strftime("%Y-%m-%d")
        kv = event.get("kv") or {}

        if _is_explicit_conductor_pick(event):
            conductor = _normalize_conductor_slug(kv.get("conductor"))
            explicit_picks_by_conductor[conductor] += 1
            per_day[day][conductor]["picks"] += 1
            open_picks.append(
                {
                    "conductor": conductor,
                    "dt": event["dt"],
                    "line": event["line"],
                }
            )
            continue

        if _is_legacy_partial_conductor_pick(event):
            conductor = _normalize_conductor_slug(kv.get("conductor"))
            legacy_partial_picks_by_conductor[conductor] += 1
            continue

        if event.get("kind") != "coffee_conductor_outcome":
            continue

        for key in evidence_richness:
            if str(kv.get(key, "")).strip():
                evidence_richness[key] += 1

        explicit_conductor = _normalize_conductor_slug(kv.get("conductor"))
        if explicit_conductor in KNOWN_CONDUCTOR_SLUGS:
            explicit_outcomes_by_conductor[explicit_conductor] += 1
            per_day[day][explicit_conductor]["explicit_outcomes"] += 1
            match_index = next(
                (
                    idx
                    for idx in range(len(open_picks) - 1, -1, -1)
                    if open_picks[idx]["conductor"] == explicit_conductor
                ),
                None,
            )
            if match_index is not None:
                explicit_closed += 1
                open_picks.pop(match_index)
            else:
                outcomes_without_matching_pick += 1
            continue

        if open_picks:
            inferred_conductor = open_picks[-1]["conductor"]
            inferred_outcomes_by_conductor[inferred_conductor] += 1
            per_day[day][inferred_conductor]["inferred_outcomes"] += 1
            inferred_closed += 1
            open_picks.pop()
        else:
            unattributed_outcomes += 1

    explicit_pick_count = sum(explicit_picks_by_conductor.values())
    explicit_outcome_count = sum(explicit_outcomes_by_conductor.values())
    inferred_outcome_count = sum(inferred_outcomes_by_conductor.values())
    total_closed = explicit_closed + inferred_closed
    closure_rate = round(total_closed / explicit_pick_count, 3) if explicit_pick_count else 0.0

    return {
        "user_id": user_id,
        "days": days,
        "window_start": cutoff.isoformat(),
        "window_end": now.isoformat(),
        "event_count": len(events),
        "explicit_pick_count": explicit_pick_count,
        "explicit_outcome_count": explicit_outcome_count,
        "inferred_outcome_count": inferred_outcome_count,
        "explicit_picks_by_conductor": dict(explicit_picks_by_conductor),
        "explicit_outcomes_by_conductor": dict(explicit_outcomes_by_conductor),
        "inferred_outcomes_by_conductor": dict(inferred_outcomes_by_conductor),
        "legacy_partial_picks_by_conductor": dict(legacy_partial_picks_by_conductor),
        "closure": {
            "explicit_closed": explicit_closed,
            "inferred_closed": inferred_closed,
            "total_closed": total_closed,
            "open_pick_count": len(open_picks),
            "closure_rate": closure_rate,
            "outcomes_without_matching_pick": outcomes_without_matching_pick,
            "unattributed_outcomes": unattributed_outcomes,
        },
        "evidence_richness": evidence_richness,
        "open_picks": [
            {
                "conductor": row["conductor"],
                "ts": row["dt"].isoformat(),
                "line": row["line"],
            }
            for row in open_picks
        ],
        "per_day": {
            day: {conductor: counts for conductor, counts in sorted(day_counts.items())}
            for day, day_counts in sorted(per_day.items())
        },
    }


def format_summary(s: dict) -> str:
    lines = [f"Cadence rhythm ({s['user_id']}) — last {s['days']} days"]

    if s["event_count"] == 0:
        lines.append("  (no cadence events in window)")
        return "\n".join(lines)

    d = s["dream"]
    dream_line = f"  dream: {d['count']} runs"
    if d["last"]:
        dream_line += f", last {d['last'][:10]} ({d['days_ago']}d ago)"
    dream_line += " — " + ("OK" if d["ok"] else "DRIFT")
    lines.append(dream_line)

    b = s["bridge"]
    bridge_line = f"  bridge: {b['count']} runs"
    if b["last"]:
        bridge_line += f", last {b['last'][:10]} ({b['days_ago']}d ago)"
    if b["sessions_without"]:
        bridge_line += f", {b['sessions_without']} sessions without"
    lines.append(bridge_line)

    c = s["coffee"]
    coffee_line = f"  coffee: {c['count']} runs, avg {c['per_active_day']}/active-day"
    coffee_line += " — " + ("OK" if c["ok"] else "LOW")
    lines.append(coffee_line)

    g = s["longest_gap"]
    gap_line = f"  longest gap: {g['hours']}h"
    if g["start"] and g["end"]:
        gap_line += f" ({g['start'][:10]} to {g['end'][:10]})"
    gap_line += " — " + ("OK" if g["ok"] else "LONG")
    lines.append(gap_line)

    mt = s.get("model_tier", {})
    if mt.get("total", 0) > 0:
        tier_parts = [f"{k}: {mt['counts'][k]} ({mt['pcts'][k]}%)" for k in sorted(mt["pcts"])]
        lines.append(f"  model tier: {', '.join(tier_parts)}")

    lines.append(f"  discipline: {s['discipline']}")
    if s["issues"]:
        for issue in s["issues"]:
            lines.append(f"    - {issue}")

    return "\n".join(lines)


def format_discipline_one_liner(s: dict) -> str:
    """One-line summary for warmup integration."""
    if s["event_count"] == 0:
        return f"Cadence discipline ({s['days']}d): NO_DATA"
    if s["discipline"] == "HEALTHY":
        return f"Cadence discipline ({s['days']}d): HEALTHY"
    issues_str = "; ".join(s["issues"][:3])
    return f"Cadence discipline ({s['days']}d): {issues_str} — DRIFT"


def format_conductor_audit(summary: dict) -> str:
    lines = [f"5-conductor audit ({summary['user_id']}) â€” last {summary['days']} days"]
    if summary["event_count"] == 0:
        lines.append("  (no cadence events in window)")
        return "\n".join(lines)

    lines.append(
        "  explicit picks/outcomes/inferred outcomes: "
        f"{summary['explicit_pick_count']}/{summary['explicit_outcome_count']}/{summary['inferred_outcome_count']}"
    )
    closure = summary["closure"]
    lines.append(
        "  closure: "
        f"{closure['total_closed']} closed, {closure['open_pick_count']} open, "
        f"rate {closure['closure_rate']:.1%}"
    )
    if closure["unattributed_outcomes"] or closure["outcomes_without_matching_pick"]:
        lines.append(
            "  audit gaps: "
            f"{closure['unattributed_outcomes']} unattributed outcomes, "
            f"{closure['outcomes_without_matching_pick']} outcomes without matching pick"
        )

    for conductor in sorted(KNOWN_CONDUCTOR_SLUGS):
        picks = summary["explicit_picks_by_conductor"].get(conductor, 0)
        outcomes = summary["explicit_outcomes_by_conductor"].get(conductor, 0)
        inferred = summary["inferred_outcomes_by_conductor"].get(conductor, 0)
        legacy = summary["legacy_partial_picks_by_conductor"].get(conductor, 0)
        if picks or outcomes or inferred or legacy:
            lines.append(
                f"  {conductor}: picks={picks} explicit_outcomes={outcomes} "
                f"inferred_outcomes={inferred} legacy_partial={legacy}"
            )

    ev = summary["evidence_richness"]
    lines.append(
        "  evidence richness: "
        f"verdict={ev['verdict']}, action={ev['action']}, "
        f"notebook_ref={ev['notebook_ref']}, falsify={ev['falsify']}"
    )

    if summary["open_picks"]:
        lines.append("  open picks:")
        for row in summary["open_picks"][:5]:
            lines.append(f"    - {row['ts'][:16]} {row['conductor']}")

    return "\n".join(lines)


def count_gate_pending_substrings(gate_path: Path) -> int:
    """Count `status: pending` occurrences in gate file (companion queue signal)."""
    if not gate_path.is_file():
        return 0
    text = gate_path.read_text(encoding="utf-8", errors="replace")
    return text.count("status: pending")


def compute_cadence_pressure_report(
    user_id: str,
    days: int = 14,
    *,
    events_path: Path = EVENTS_PATH,
    gate_path: Path | None = None,
    now: datetime | None = None,
) -> dict:
    """Combine rhythm summary with lightweight governance pressure signals."""
    now = now or datetime.now(timezone.utc)
    rhythm = compute_rhythm_summary(user_id, days, events_path=events_path, now=now)
    pending = count_gate_pending_substrings(gate_path) if gate_path else 0
    signals: list[str] = []
    if rhythm.get("discipline") == "DRIFT":
        signals.append("cadence_drift")
    if pending > 5:
        signals.append("high_gate_pending")
    ce = rhythm.get("coffee", {}).get("count", 0)
    if isinstance(ce, int) and ce > 25:
        signals.append("high_coffee_volume")
    return {
        "schemaVersion": "1.0.0-cadence-pressure",
        "generatedAt": now.isoformat(),
        "user_id": user_id,
        "days": days,
        "rhythm_summary": rhythm,
        "governance": {
            "recursion_gate_pending_status_count": pending,
            "gate_path": str(gate_path) if gate_path else None,
        },
        "pressure_signals": signals,
    }


def format_tier_report(s: dict) -> str:
    """Standalone model-tier distribution report."""
    mt = s.get("model_tier", {})
    lines = [f"Model tier distribution ({s['user_id']}) — last {s['days']} days"]
    if mt.get("total", 0) == 0:
        lines.append("  (no events in window)")
        return "\n".join(lines)
    lines.append(f"  total events: {mt['total']}")
    for tier in ("frontier", "fast", "unknown"):
        count = mt["counts"].get(tier, 0)
        pct = mt["pcts"].get(tier, 0.0)
        bar = "#" * int(pct / 2)
        lines.append(f"  {tier:10s}  {count:4d}  ({pct:5.1f}%)  {bar}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Cadence rhythm auditor — discipline summary.")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    ap.add_argument("--days", type=int, default=14, help="Look-back window in days (default 14)")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")
    ap.add_argument("--tier-report", action="store_true", help="Standalone model-tier distribution")
    ap.add_argument("--conductor-report", action="store_true", help="5-conductor audit for the look-back window")
    ap.add_argument(
        "--pressure-report",
        type=Path,
        nargs="?",
        const=REPO_ROOT / "artifacts/work-cadence/cadence-pressure-report.json",
        metavar="OUT",
        help="Write cadence pressure JSON (default: artifacts/work-cadence/cadence-pressure-report.json)",
    )
    ap.add_argument(
        "--gate-path",
        type=Path,
        default=DEFAULT_GATE_PATH,
        help="recursion-gate.md path for pending count (default: users/grace-mar/recursion-gate.md)",
    )
    args = ap.parse_args()

    if args.pressure_report is not None:
        rep = compute_cadence_pressure_report(
            args.user, args.days, gate_path=args.gate_path
        )
        args.pressure_report.parent.mkdir(parents=True, exist_ok=True)
        args.pressure_report.write_text(
            json.dumps(rep, indent=2, default=str) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.pressure_report}")
        return 0

    if args.conductor_report:
        summary = compute_conductor_audit(args.user, args.days)
        if args.json:
            print(json.dumps(summary, indent=2, default=str))
        else:
            print(format_conductor_audit(summary))
        return 0

    summary = compute_rhythm_summary(args.user, args.days)

    if args.tier_report:
        print(format_tier_report(summary))
    elif args.json:
        print(json.dumps(summary, indent=2, default=str))
    else:
        print(format_summary(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
