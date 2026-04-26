#!/usr/bin/env python3
"""Parse work-cadence-events.md for coffee runs in a rolling UTC window.

Operator maintenance only — not Record truth. Used by auto_dream for last-dream.json.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"

# - **2026-04-02 20:46 UTC** — coffee (grace-mar) ok=true mode=work-start
_COFFEE_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — coffee \(([^)]+)\)\s*(.*)$"
)
# - **2026-04-02 20:46 UTC** — coffee_pick (grace-mar) picked=E steward=gate
_COFFEE_PICK_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — coffee_pick \(([^)]+)\)\s*(.*)$"
)


def _parse_trailing_kv(rest: str) -> tuple[bool | None, str | None, dict[str, str]]:
    ok: bool | None = None
    mode: str | None = None
    kv: dict[str, str] = {}
    for token in rest.split():
        if "=" not in token:
            continue
        key, _, val = token.partition("=")
        key, val = key.strip(), val.strip()
        if key == "ok":
            ok = val.lower() == "true"
        elif key == "mode":
            mode = val or None
        else:
            kv[key] = val
    return ok, mode, kv


def _parse_ts(date_part: str, time_part: str) -> datetime:
    dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    return dt


def parse_coffee_pick_cadence_lines(
    markdown: str,
    *,
    user_id: str,
    window_start: datetime,
    window_end: datetime,
    max_events: int = 40,
) -> list[dict[str, Any]]:
    """Return coffee_pick events for user_id with ts in [window_start, window_end], oldest first."""
    out: list[dict[str, Any]] = []
    for line in markdown.splitlines():
        m = _COFFEE_PICK_LINE.match(line.strip())
        if not m:
            continue
        uid = m.group(3).strip()
        if uid != user_id:
            continue
        ts = _parse_ts(m.group(1), m.group(2))
        if ts < window_start or ts > window_end:
            continue
        _ok, _mode, kv = _parse_trailing_kv(m.group(4).strip())
        raw_pick = (kv.get("picked") or "").strip()
        if not raw_pick:
            continue
        first = raw_pick[0].upper()
        if first not in {"A", "B", "C", "D", "E"}:
            continue
        picked = first
        steward = (kv.get("steward") or "").strip().lower() or None
        cond = (kv.get("conductor") or "").strip() or None
        row: dict[str, Any] = {
            "ts_iso": ts.isoformat(),
            "picked": picked,
            "menu_label": raw_pick,
        }
        if steward in {"gate", "template", "both"}:
            row["steward"] = steward
        if cond:
            row["conductor"] = cond
        out.append(row)
    out.sort(key=lambda r: r["ts_iso"])
    if len(out) > max_events:
        out = out[-max_events:]
    return out


def parse_coffee_cadence_lines(
    markdown: str,
    *,
    user_id: str,
    window_start: datetime,
    window_end: datetime,
    max_runs: int = 20,
) -> list[dict[str, Any]]:
    """Return coffee events for user_id with ts in [window_start, window_end], oldest first."""
    runs: list[dict[str, Any]] = []
    for line in markdown.splitlines():
        m = _COFFEE_LINE.match(line.strip())
        if not m:
            continue
        uid = m.group(3).strip()
        if uid != user_id:
            continue
        ts = _parse_ts(m.group(1), m.group(2))
        if ts < window_start or ts > window_end:
            continue
        ok, mode, kv = _parse_trailing_kv(m.group(4).strip())
        runs.append(
            {
                "ts_iso": ts.isoformat(),
                "ok": ok,
                "mode": mode or "unknown",
                "kv": kv,
            }
        )
    runs.sort(key=lambda r: r["ts_iso"])
    if len(runs) > max_runs:
        runs = runs[-max_runs:]
    return runs


def rollup_coffee_24h(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
    max_runs: int = 20,
) -> dict[str, Any]:
    """Aggregate coffee cadence in (now - window_hours, now] UTC."""
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    window_end = now_utc
    window_start = now_utc - timedelta(hours=window_hours)

    if not events_path.is_file():
        return {
            "window_start_utc": window_start.isoformat(),
            "window_end_utc": window_end.isoformat(),
            "window_hours": window_hours,
            "count": 0,
            "first_ts": None,
            "last_ts": None,
            "span_hours": None,
            "by_mode": {},
            "runs": [],
            "picks": [],
            "by_picked": {},
            "note": "no cadence file",
        }

    text = events_path.read_text(encoding="utf-8")
    runs = parse_coffee_cadence_lines(
        text,
        user_id=user_id,
        window_start=window_start,
        window_end=window_end,
        max_runs=max_runs,
    )
    picks = parse_coffee_pick_cadence_lines(
        text,
        user_id=user_id,
        window_start=window_start,
        window_end=window_end,
    )

    by_mode: dict[str, int] = {}
    for r in runs:
        m = r["mode"]
        by_mode[m] = by_mode.get(m, 0) + 1

    by_picked: dict[str, int] = {}
    for r in picks:
        letter = r["picked"]
        by_picked[letter] = by_picked.get(letter, 0) + 1

    first_ts = runs[0]["ts_iso"] if runs else None
    last_ts = runs[-1]["ts_iso"] if runs else None
    span_hours: float | None = None
    if len(runs) >= 2:
        t0 = datetime.fromisoformat(runs[0]["ts_iso"].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(runs[-1]["ts_iso"].replace("Z", "+00:00"))
        span_hours = round((t1 - t0).total_seconds() / 3600.0, 2)

    return {
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "window_hours": window_hours,
        "count": len(runs),
        "first_ts": first_ts,
        "last_ts": last_ts,
        "span_hours": span_hours,
        "by_mode": by_mode,
        "runs": runs,
        "picks": picks,
        "by_picked": by_picked,
    }


def _one_line_capped(s: str, max_len: int) -> str:
    t = " ".join(s.split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 1] + "…"


def build_last_coffee_echo(rollup: dict[str, Any]) -> dict[str, Any] | None:
    """Derive a compact, single-line echo from a 24h coffee rollup; no cadence re-parse.

    Returns None if there is no recent coffee *run* in the window (not Record).
    """
    runs = rollup.get("runs") or []
    if not runs or int(rollup.get("count") or 0) <= 0:
        return None
    last = runs[-1]
    ts = (last.get("ts_iso") or rollup.get("last_ts") or "") or None
    if not ts:
        return None
    mode = str(last.get("mode") or "unknown")
    picks = rollup.get("picks") or []
    last_pick = picks[-1] if picks else None
    conductor: str | None = None
    menu_letter: str | None = None
    if last_pick and isinstance(last_pick, dict):
        c = (last_pick.get("conductor") or "").strip()
        if c:
            conductor = c
        ml = (last_pick.get("menu_label") or last_pick.get("picked") or "").strip()
        if ml:
            menu_letter = ml
    # Warm, bounded one-liner (no raw event text)
    bits: list[str] = [f"Yesterday’s {mode} coffee is still the thread."]
    if menu_letter:
        bits.append(f"Menu pick: {menu_letter}.")
    if conductor:
        bits.append(f"Conductor line: {conductor}.")
    highlight = _one_line_capped(" ".join(bits), 160)
    return {
        "timestamp": ts,
        "conductor": conductor,
        "mode": mode,
        "menu_letter": menu_letter,
        "highlight": highlight,
        "source": "coffee_rollup_24h",
    }
