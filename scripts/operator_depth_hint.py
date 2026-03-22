#!/usr/bin/env python3
"""
Operator "trap door" hint: when pipeline velocity (approvals / merges) crosses tiers,
emit a single harness-events line pointing at work-dev depth docs.

Reads users/<id>/pipeline-events.jsonl (event approved | applied). Deduplicates via
users/<id>/.operator_depth_hint_state.json so we only escalate when tier *increases*
(L1 → L2 → L3), not on every run.

Not part of the Record. Operator / work-dev surface only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from harness_events import append_harness_event  # noqa: E402
from repo_io import profile_dir  # noqa: E402

UTC = timezone.utc

# Tiers: higher = more "whale" velocity in the rolling window (power-law tail).
# applied = merged candidates; approved = gate approvals (may precede merge).
TIER_THRESHOLDS: tuple[tuple[int, int, int], ...] = (
    # (tier, min_applied, min_approved) — tier activates if either count meets threshold
    (1, 3, 5),
    (2, 8, 12),
    (3, 20, 25),
)

HINT_BODY = (
    "High pipeline velocity — consider work-dev operator depth: "
    "`docs/skill-work/work-dev/workspace.md`, `bootstrap/grace-mar-bootstrap.md` (merge ritual + receipts), "
    "`scripts/operator_merge_once.sh`, `docs/skill-work/work-dev/README.md` § Operator path."
)


@dataclass(frozen=True)
class VelocitySnapshot:
    window_days: int
    applied: int
    approved: int
    tier: int  # 0 = below L1


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _parse_line_ts(line: str) -> datetime | None:
    line = line.strip()
    if not line:
        return None
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        return None
    ts = o.get("ts")
    if not ts or not isinstance(ts, str):
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def _event_name(line: str) -> str | None:
    try:
        o = json.loads(line.strip())
        ev = o.get("event")
        return str(ev) if ev is not None else None
    except json.JSONDecodeError:
        return None


def analyze_velocity(
    user_id: str,
    *,
    window_days: int = 7,
    now: datetime | None = None,
) -> VelocitySnapshot:
    """Count approved / applied events in pipeline-events.jsonl within the rolling window."""
    path = profile_dir(user_id) / "pipeline-events.jsonl"
    if not path.is_file():
        return VelocitySnapshot(window_days=window_days, applied=0, approved=0, tier=0)
    now = now or datetime.now(UTC)
    cutoff = now - timedelta(days=window_days)
    applied = 0
    approved = 0
    cutoff = _to_utc(cutoff)
    for line in path.read_text(encoding="utf-8").splitlines():
        ts = _parse_line_ts(line)
        if ts is None:
            continue
        if _to_utc(ts) < cutoff:
            continue
        ev = _event_name(line)
        if ev == "applied":
            applied += 1
        elif ev == "approved":
            approved += 1
    tier = _tier_from_counts(applied, approved)
    return VelocitySnapshot(window_days=window_days, applied=applied, approved=approved, tier=tier)


def _tier_from_counts(applied: int, approved: int) -> int:
    best = 0
    for tier, min_a, min_p in TIER_THRESHOLDS:
        if applied >= min_a or approved >= min_p:
            best = max(best, tier)
    return best


def _state_path(user_id: str) -> Path:
    return profile_dir(user_id) / ".operator_depth_hint_state.json"


def _load_state(user_id: str) -> dict[str, Any]:
    p = _state_path(user_id)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(user_id: str, data: dict[str, Any]) -> None:
    p = _state_path(user_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def maybe_emit_tier_hint(
    user_id: str,
    snap: VelocitySnapshot,
    *,
    dry_run: bool,
) -> tuple[bool, str]:
    """
    If snap.tier exceeds last emitted tier, emit harness event and update state.

    Returns (emitted, message).
    """
    if snap.tier <= 0:
        return False, "tier 0 — no hint (velocity below L1 thresholds)"

    state = _load_state(user_id)
    last = int(state.get("last_emitted_tier") or 0)

    if snap.tier <= last:
        return (
            False,
            f"no new tier (current={snap.tier}, last_emitted={last}); thresholds already signaled",
        )

    msg = (
        f"tier {snap.tier}: {snap.applied} applied, {snap.approved} approved "
        f"in last {snap.window_days}d — {HINT_BODY}"
    )

    if dry_run:
        return True, f"[dry-run] would emit harness event: {msg}"

    append_harness_event(
        user_id,
        "operator_depth_hint",
        "tier_reveal",
        tier=snap.tier,
        last_emitted_tier_before=last,
        applied_in_window=snap.applied,
        approved_in_window=snap.approved,
        window_days=snap.window_days,
        hint=HINT_BODY,
    )
    state["last_emitted_tier"] = snap.tier
    state["last_emit_ts"] = datetime.now(UTC).isoformat()
    state["last_snapshot"] = {
        "applied": snap.applied,
        "approved": snap.approved,
        "tier": snap.tier,
        "window_days": snap.window_days,
    }
    _save_state(user_id, state)
    return True, msg


def velocity_oneliner(user_id: str, *, window_days: int = 7) -> str:
    """Short line for operator_daily_warmup (no side effects)."""
    snap = analyze_velocity(user_id, window_days=window_days)
    if snap.tier <= 0:
        return (
            f"Pipeline velocity ({window_days}d): {snap.applied} merge(s) (`applied`), "
            f"{snap.approved} approval(s) — below operator-depth tier (run `python3 scripts/operator_depth_hint.py -u {user_id}`)."
        )
    return (
        f"Pipeline velocity ({window_days}d): {snap.applied} merge(s), {snap.approved} approval(s) — "
        f"tier L{snap.tier} active; depth docs: `docs/skill-work/work-dev/workspace.md` "
        f"(run `python3 scripts/operator_depth_hint.py -u {user_id}` to emit harness hint on tier increases)."
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit operator depth harness hint when pipeline tier increases.")
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork id")
    ap.add_argument("--window-days", type=int, default=7, help="Rolling window for counts (default 7)")
    ap.add_argument("--dry-run", action="store_true", help="Print actions without writing state or harness")
    ap.add_argument(
        "--reset-state",
        action="store_true",
        help="Delete .operator_depth_hint_state.json so tiers can re-fire from scratch",
    )
    args = ap.parse_args()
    uid = args.user.strip()
    if args.reset_state:
        p = _state_path(uid)
        if p.is_file():
            p.unlink()
            print(f"Removed {p}")
        else:
            print(f"No state file at {p}")
    snap = analyze_velocity(uid, window_days=args.window_days)
    emitted, message = maybe_emit_tier_hint(uid, snap, dry_run=args.dry_run)
    print(f"tier={snap.tier} applied={snap.applied} approved={snap.approved} window={snap.window_days}d")
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
