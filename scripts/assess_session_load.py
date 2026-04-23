#!/usr/bin/env python3
"""
Session load assessment — aggregate cadence, gate, capture gap, and dream
quality signals into a cognitive load level for the operator.

Designed to annotate the coffee **A–D2–E** menu with per-option cost hints and a
recommended pick (A / B / C only — not D1 / D2 / E).

Exposes assess_load() for import by operator_coffee.py.

Usage:
    python scripts/assess_session_load.py -u grace-mar
    python scripts/assess_session_load.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

DEFAULT_USER = "grace-mar"


# ---------------------------------------------------------------------------
# Signal collectors (each returns a partial signal dict or None)
# ---------------------------------------------------------------------------

def _collect_cadence_today(user_id: str) -> dict | None:
    """Count and categorize today's cadence events."""
    try:
        from audit_cadence_rhythm import parse_events
    except ImportError:
        try:
            from scripts.audit_cadence_rhythm import parse_events
        except ImportError:
            return None

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    all_events = parse_events(user_id)
    today_events = [e for e in all_events if e["dt"] >= today_start]

    by_kind: dict[str, int] = {}
    for e in today_events:
        by_kind[e["kind"]] = by_kind.get(e["kind"], 0) + 1

    return {
        "total": len(today_events),
        "coffees": by_kind.get("coffee", 0),
        "bridges": by_kind.get("bridge", 0),
        "harvests": by_kind.get("harvest", 0),
        "dreams": by_kind.get("dream", 0),
        "thanks": by_kind.get("thanks", 0),
        "by_kind": by_kind,
    }


def _collect_gate_depth(user_id: str) -> dict | None:
    """Count pending candidates in the gate."""
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.is_file():
        return None
    content = gate_path.read_text(encoding="utf-8")
    processed = re.search(r"^## Processed\s*$", content, re.MULTILINE)
    section = content[:processed.start()] if processed else content
    pending = len(re.findall(r"status:\s*pending", section))
    return {"pending": pending}


def _collect_capture_gap(user_id: str) -> dict | None:
    """Get capture gap result."""
    try:
        from detect_capture_gap import detect_gap
    except ImportError:
        try:
            from scripts.detect_capture_gap import detect_gap
        except ImportError:
            return None
    return detect_gap(user_id)


def _collect_dream_quality(user_id: str) -> dict | None:
    """Read last-dream.json for quality signals."""
    dream_path = REPO_ROOT / "users" / user_id / "last-dream.json"
    if not dream_path.is_file():
        return None
    try:
        data = json.loads(dream_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return {
        "integrity_ok": data.get("integrity_ok", True),
        "governance_ok": data.get("governance_ok", True),
        "contradiction_count": data.get("contradiction_count", 0),
        "reviewable_count": data.get("reviewable_count", 0),
        "followup_count": len(data.get("followups", [])),
        "ok": data.get("ok", True),
    }


def _collect_branch_count() -> int:
    """Count non-main git branches."""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "branch"], capture_output=True, text=True,
            cwd=str(REPO_ROOT), timeout=5,
        )
        branches = [
            line.strip() for line in r.stdout.splitlines()
            if line.strip() and not line.strip().lstrip("* ").startswith("main")
        ]
        return len(branches)
    except Exception:
        return 0


def _time_of_day_energy() -> str:
    """Simple time-of-day proxy for energy level."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    return "evening"


# ---------------------------------------------------------------------------
# Load computation
# ---------------------------------------------------------------------------

def _compute_load_level(
    cadence: dict | None,
    gate: dict | None,
    gap: dict | None,
    dream: dict | None,
) -> tuple[str, list[str]]:
    """Compute load level and signal descriptions."""
    weight = 0
    signals: list[str] = []

    if cadence:
        coffees = cadence.get("coffees", 0)
        if coffees >= 4:
            weight += 3
            signals.append(f"{coffees} coffees today (frequent reorientation)")
        elif coffees >= 2:
            weight += 1
            signals.append(f"{coffees} coffees today")
        bridges = cadence.get("bridges", 0)
        if bridges >= 1:
            weight += 1
            signals.append(f"{bridges} bridge(s) today (context transfer cost)")

    if gate:
        pending = gate.get("pending", 0)
        if pending >= 5:
            weight += 2
            signals.append(f"{pending} pending gate candidates (cognitive debt)")
        elif pending >= 2:
            weight += 1
            signals.append(f"{pending} pending gate candidates")

    if gap:
        gap_level = gap.get("level", "ok")
        days = gap.get("days_since_evidence")
        if gap_level == "alert":
            weight += 3
            signals.append(f"capture gap: {days}d since last Evidence (alert)")
        elif gap_level == "warning":
            weight += 2
            signals.append(f"capture gap: {days}d since last Evidence (warning)")
        elif gap_level == "notice":
            weight += 1
            signals.append(f"capture gap: {days}d since last Evidence")

    if dream:
        if not dream.get("integrity_ok", True):
            weight += 2
            signals.append("dream integrity issue (unresolved)")
        if not dream.get("governance_ok", True):
            weight += 2
            signals.append("dream governance issue (unresolved)")
        followups = dream.get("followup_count", 0)
        if followups >= 2:
            weight += 1
            signals.append(f"{followups} dream followups pending")

    tod = _time_of_day_energy()
    if tod == "evening":
        weight += 1
        signals.append("evening session (energy proxy: lower)")

    if weight >= 5:
        return "heavy", signals
    if weight >= 2:
        return "moderate", signals
    return "light", signals


def _compute_option_weights(
    load_level: str,
    gate: dict | None,
    branch_count: int,
) -> dict[str, dict[str, str]]:
    """Assign cost and note to each A–D2–E option (coffee six-line menu)."""
    pending = gate.get("pending", 0) if gate else 0

    weights: dict[str, dict[str, str]] = {
        "A": {"cost": "moderate", "note": "Build — work-dev + skills"},
        "B": {"cost": "light", "note": "Steward — gate / template / integrity / git"},
        "C": {"cost": "light", "note": "Strategy — daily brief + tri-frame"},
        "D1": {"cost": "moderate", "note": "Conductor — continue last emphasis (notebook)"},
        "D2": {"cost": "moderate", "note": "Conductor — system-recommended stack (notebook)"},
        "E": {"cost": "moderate", "note": "System choice — xavier / dev / jiang / rome slice"},
    }

    if branch_count >= 3:
        weights["A"]["cost"] = "heavy"
        weights["A"]["note"] = f"Build; {branch_count} branches to review"
    elif branch_count >= 1:
        weights["A"]["note"] = f"Build; {branch_count} non-main branch(es)"

    if pending >= 5:
        weights["B"]["note"] = f"Steward; {pending} pending — heavier gate pass"
        weights["B"]["cost"] = "moderate"
    elif pending >= 1:
        weights["B"]["note"] = f"Steward; {pending} pending candidate(s)"

    return weights


def _pick_recommendation(
    load_level: str,
    weights: dict[str, dict[str, str]],
    signals: list[str],
) -> tuple[str, str]:
    """Select the recommended option and reason (A / B / C only; see menu skill)."""
    w = {k: weights[k] for k in ("A", "B", "C") if k in weights}
    if load_level == "heavy":
        return "C", "heavy load — strategy / daily brief pass is highest leverage"
    if load_level == "moderate":
        light_options = [k for k, v in w.items() if v["cost"] == "light"]
        if "B" in light_options:
            return "B", "moderate load — bounded steward pass clears cognitive debt"
        return "C", "moderate load — strategy pass matches current pace"
    moderate_options = [k for k, v in w.items() if v["cost"] in ("light", "moderate")]
    if "C" in moderate_options:
        return "C", "light load — good conditions for strategy / daily brief"
    return "A", "light load — good conditions for build work"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def assess_load(user_id: str) -> dict:
    """Compute session load assessment. Returns structured dict."""
    cadence = _collect_cadence_today(user_id)
    gate = _collect_gate_depth(user_id)
    gap = _collect_capture_gap(user_id)
    dream = _collect_dream_quality(user_id)
    branch_count = _collect_branch_count()

    load_level, signals = _compute_load_level(cadence, gate, gap, dream)
    weights = _compute_option_weights(load_level, gate, branch_count)
    recommended, reason = _pick_recommendation(load_level, weights, signals)

    return {
        "load_level": load_level,
        "signals": signals,
        "option_weights": weights,
        "recommended": recommended,
        "recommendation_reason": reason,
        "time_of_day": _time_of_day_energy(),
        "branch_count": branch_count,
    }


def format_load_one_liner(result: dict) -> str:
    """One-line summary for coffee Step 1 output."""
    level = result.get("load_level", "unknown")
    signals = result.get("signals", [])
    rec = result.get("recommended", "?")
    summary_parts = signals[:3] if signals else ["no signals"]
    return (
        f"Session load: {level.upper()} — "
        + ", ".join(summary_parts)
        + f" (recommended: {rec})"
    )


def format_annotated_menu(result: dict) -> str:
    """Format the A–D2–E coffee menu with load annotations (optional; not printed by default)."""
    weights = result.get("option_weights", {})
    rec = result.get("recommended", "")

    labels = {
        "A": "Build",
        "B": "Steward",
        "C": "Strategy (daily brief)",
        "D1": "Conductor — continue",
        "D2": "Conductor — system",
        "E": "System choice",
    }

    lines = []
    for letter in ("A", "B", "C", "D1", "D2", "E"):
        w = weights.get(letter, {"cost": "?", "note": ""})
        label = labels[letter]
        tag = f"({w['cost']})"
        note = w["note"]
        rec_tag = " recommended" if letter == rec else ""
        lines.append(f"**{letter}. {label}** — {tag}{rec_tag}: {note}")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Assess operator session cognitive load.")
    ap.add_argument(
        "-u", "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER,
    )
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    result = assess_load(args.user)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_load_one_liner(result))
        print()
        print("Annotated menu:")
        print(format_annotated_menu(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
