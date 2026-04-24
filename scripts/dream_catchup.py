#!/usr/bin/env python3
"""Since-previous-dream catch-up window for dream ritual (WORK only; not Record).

Computes which local calendar dates need strategy-notebook + cici-notebook production
when moving from the last successful dream handoff to now.

Semantics:
- Read ``users/<id>/last-dream.json`` ``generated_at`` **before** a new dream overwrites it.
- Local dates to cover: all dates **strictly after** the local calendar date of that
  timestamp, through **today** in the operator timezone (inclusive).
- If there is no prior handoff (first dream): **today only** in that timezone.

Timezone: ``DREAM_CATCHUP_TZ`` else ``TZ`` else ``UTC``.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

LAST_DREAM_FILENAME = "last-dream.json"


def read_previous_dream_generated_at(users_dir: Path, user_id: str) -> datetime | None:
    """Parse ``generated_at`` from existing last-dream.json, or None."""
    path = users_dir / user_id / LAST_DREAM_FILENAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    raw = data.get("generated_at")
    if not raw or not isinstance(raw, str):
        return None
    try:
        s = raw.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def resolve_catchup_tz_name() -> str:
    return os.environ.get("DREAM_CATCHUP_TZ") or os.environ.get("TZ") or "UTC"


def catch_up_local_dates(
    *,
    previous_dream_utc: datetime | None,
    now_utc: datetime,
    tz_name: str,
) -> list[date]:
    """Inclusive local dates to produce/verify after previous dream through today.

    Empty list only when previous local date equals today and same-day second dream
    (nothing new to backfill by day).
    """
    z = ZoneInfo(tz_name)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    now_local = now_utc.astimezone(z)
    d_end = now_local.date()

    if previous_dream_utc is None:
        return [d_end]

    if previous_dream_utc.tzinfo is None:
        previous_dream_utc = previous_dream_utc.replace(tzinfo=timezone.utc)
    prev_local = previous_dream_utc.astimezone(z)
    d_anchor = prev_local.date()

    out: list[date] = []
    d = d_anchor + timedelta(days=1)
    while d <= d_end:
        out.append(d)
        d += timedelta(days=1)
    return out


def catch_up_window_dict(
    *,
    users_dir: Path,
    user_id: str,
    now_utc: datetime | None = None,
    tz_name: str | None = None,
) -> dict[str, Any]:
    """Single blob for last-dream.json / auto_dream summary."""
    tz = tz_name or resolve_catchup_tz_name()
    prev = read_previous_dream_generated_at(users_dir, user_id)
    now = now_utc or datetime.now(timezone.utc)
    dates = catch_up_local_dates(previous_dream_utc=prev, now_utc=now, tz_name=tz)
    return {
        "semantics": "since_previous_dream",
        "timezone": tz,
        "previous_dream_generated_at": prev.isoformat() if prev else None,
        "local_calendar_dates": [d.isoformat() for d in dates],
    }


_DAYS_HEADER = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def parse_strategy_notebook_day_headers(days_md_text: str) -> set[str]:
    return set(_DAYS_HEADER.findall(days_md_text))


def strategy_notebook_month_paths(repo_root: Path, d0: date, d1: date) -> list[Path]:
    months: set[tuple[int, int]] = set()
    d = d0
    while d <= d1:
        months.add((d.year, d.month))
        d += timedelta(days=1)
    out: list[Path] = []
    for y, m in sorted(months):
        p = (
            repo_root
            / "docs"
            / "skill-work"
            / "work-strategy"
            / "strategy-notebook"
            / "chapters"
            / f"{y:04d}-{m:02d}"
            / "days.md"
        )
        out.append(p)
    return out


def missing_strategy_notebook_days(
    repo_root: Path,
    want: list[date],
) -> list[str]:
    """ISO dates in ``want`` that have no ``## YYYY-MM-DD`` section in the right month files."""
    if not want:
        return []
    d0, d1 = min(want), max(want)
    present: set[str] = set()
    for path in strategy_notebook_month_paths(repo_root, d0, d1):
        if path.is_file():
            present |= parse_strategy_notebook_day_headers(path.read_text(encoding="utf-8"))
    missing: list[str] = []
    for d in sorted(want):
        iso = d.isoformat()
        if iso not in present:
            missing.append(iso)
    return missing
