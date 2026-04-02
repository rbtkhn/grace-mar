#!/usr/bin/env python3
"""Deterministic execution paths for morning rotation (dream handoff). WORK-only hints."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


def build_execution_paths(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    integrity_ok: bool = True,
    governance_ok: bool = True,
    reviewable_count: int = 0,
    contradiction_count: int = 0,
    coffee_count_24h: int = 0,
) -> tuple[list[dict[str, Any]], int]:
    """
    Return (paths, suggested_index) where suggested_index is 0..2 for tomorrow (calendar).
    Paths are stable order: today_field, build, steward.
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)

    tomorrow = (now_utc.date() + timedelta(days=1))
    suggested_index = (tomorrow.timetuple().tm_yday - 1) % 3

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
            "title": "Today / field (brief + work-politics lane)",
            "first_move": f"python3 scripts/operator_coffee.py -u {user_id} — then coffee menu A — Today",
            "stop_rule": "One slice: brief path opened or KY-4 intel pass started — enough for first block.",
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

    return paths, suggested_index
