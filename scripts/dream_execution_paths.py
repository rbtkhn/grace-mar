#!/usr/bin/env python3
"""Deterministic execution paths for morning rotation (dream handoff). WORK-only hints."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

# Stable order from build_execution_paths — maps first three hub letters A/B/C (see coffee SKILL).
_COFFEE_LETTER_AND_LABEL: dict[str, tuple[str, str]] = {
    "today_field": ("C", "Historian"),
    "build": ("B", "Engineer"),
    "steward": ("A", "Steward"),
}


def coffee_menu_hint_from_dream(dream: dict[str, Any]) -> str | None:
    """
    One-line hint for the next coffee Step 2 menu from last-dream.json.

    Maps execution_paths[suggested_execution_path_index] to **A / B / C** only
    (Historian, Engineer, Steward). Operational hint — not policy or Record.
    """
    paths = dream.get("execution_paths")
    if not isinstance(paths, list) or not paths:
        return None
    idx = int(dream.get("suggested_execution_path_index") or 0)
    idx = max(0, min(idx, len(paths) - 1))
    raw = paths[idx]
    if not isinstance(raw, dict):
        return None
    pid = str(raw.get("id") or "").strip()
    letter, label = _COFFEE_LETTER_AND_LABEL.get(pid, ("?", "?"))
    if letter == "?":
        # Fallback: positional 0/1/2 matches build_execution_paths order.
        fallbacks = (("C", "Historian"), ("B", "Engineer"), ("A", "Steward"))
        letter, label = fallbacks[idx] if idx < len(fallbacks) else ("A", "Steward")

    reason = str(dream.get("execution_path_suggestion_reason") or "").strip()
    if reason == "integrity_or_governance_fail":
        why = "integrity/governance did not fully pass this dream"
    elif reason == "gate_backlog":
        why = "gate backlog over `max_pending_candidates`"
    else:
        why = "calendar rotation"

    return (
        f"- **Dream → coffee menu:** lean **{letter} — {label}** — {why}; "
        "operational hint only (not policy or Record)."
    )


def build_execution_paths(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    integrity_ok: bool = True,
    governance_ok: bool = True,
    reviewable_count: int = 0,
    contradiction_count: int = 0,
    coffee_count_24h: int = 0,
    gate_pending_count: int = 0,
    max_pending_candidates: int | None = None,
) -> tuple[list[dict[str, Any]], int, str]:
    """
    Return (paths, suggested_index, suggestion_reason).

    suggested_index is 0..2. Paths are stable order: today_field, build, steward.

    Suggestion rule (deterministic): if integrity or governance failed this run,
    suggest Steward path index 2 (`steward`). Else if gate pending exceeds max_pending_candidates (when
    configured), suggest Steward (2). Else use calendar mod-3 on tomorrow's yearday.
    suggestion_reason is one of: integrity_or_governance_fail, gate_backlog, calendar_mod3.
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)

    tomorrow = now_utc.date() + timedelta(days=1)
    suggested_index = (tomorrow.timetuple().tm_yday - 1) % 3
    suggestion_reason = "calendar_mod3"

    if not integrity_ok or not governance_ok:
        suggested_index = 2
        suggestion_reason = "integrity_or_governance_fail"
    elif max_pending_candidates is not None and gate_pending_count > int(max_pending_candidates):
        suggested_index = 2
        suggestion_reason = "gate_backlog"

    signals_field: list[str] = []
    if coffee_count_24h >= 5:
        signals_field.append("reentry_heavy")

    first_build = (
        f"python3 scripts/validate-integrity.py --user {user_id} --json"
    )
    stop_build = "Integrity passes; then optional: python3 scripts/refresh_derived_exports.py -u {uid}".format(
        uid=user_id
    )
    if not integrity_ok:
        signals_build = ["integrity_fail"]
        first_build = f"python3 scripts/validate-integrity.py --user {user_id} --json"
        stop_build = "Fix reported integrity errors before shipping."
    else:
        signals_build = []

    if not governance_ok:
        signals_build.append("governance_fail")
        stop_build = "Read governance_checker.py stdout from dream JSON; fix blocking issues."

    first_steward = f"Read users/{user_id}/recursion-gate.md; optional: python3 scripts/operator_gate_review_pass.py -u {user_id}"
    stop_steward = "Top 1–3 candidates reviewed or explicitly deferred."
    signals_steward: list[str] = []
    if reviewable_count > 0 or contradiction_count > 0:
        signals_steward.append("digest_hot")
        first_steward = (
            f"python3 scripts/operator_gate_review_pass.py -u {user_id} "
            f"(digest: reviewable={reviewable_count}, contradiction={contradiction_count})"
        )

    paths: list[dict[str, Any]] = [
        {
            "id": "today_field",
            "title": "Daily Brief (generator + watch slices; optional KY-4 intel when chosen)",
            "first_move": f"python3 scripts/operator_coffee.py -u {user_id} — then coffee menu C — Historian",
            "stop_rule": "One slice: daily brief path opened or optional intel pass started — enough for first block.",
            "signals_used": signals_field,
        },
        {
            "id": "build",
            "title": "Build / integrate (repo + work-dev)",
            "first_move": first_build,
            "stop_rule": stop_build,
            "signals_used": signals_build,
        },
        {
            "id": "steward",
            "title": "Steward / membrane (gate + template parity)",
            "first_move": first_steward,
            "stop_rule": stop_steward,
            "signals_used": signals_steward,
        },
    ]

    return paths, suggested_index, suggestion_reason


def format_tomorrow_inherits_line(
    paths: list[dict[str, Any]],
    suggested_index: int,
    suggestion_reason: str,
) -> str:
    """Single-line handoff for morning warmup (collapsed dream block)."""
    idx = max(0, min(suggested_index, len(paths) - 1)) if paths else 0
    p = paths[idx] if paths else {}
    title = str(p.get("title") or p.get("id") or "execution path")
    if suggestion_reason == "integrity_or_governance_fail":
        return (
            f"Tomorrow inherits (hint): **{title}** — integrity or governance did not fully pass this dream; "
            "not policy or Record."
        )
    if suggestion_reason == "gate_backlog":
        return (
            f"Tomorrow inherits (hint): **{title}** — gate backlog over `max_pending_candidates`; "
            "not policy or Record."
        )
    return (
        f"Tomorrow inherits (hint): **{title}** — calendar rotation; not policy or Record."
    )
