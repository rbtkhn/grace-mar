#!/usr/bin/env python3
"""
Capture gap detector — checks whether new Evidence is being recorded.

Parses the Evidence file (self-archive.md or self-evidence.md) for the
latest entry date and compares to today.  Also checks pipeline-events.jsonl
for the last merge date.

Thresholds (configurable):
  7 days  — notice  ("Record hasn't grown in a week")
  14 days — warning ("Two weeks without new Evidence")
  30 days — alert   ("Record capture may have stalled")

Exposes detect_gap() for import by auto_dream.py, harness_warmup.py, and
assess_session_load.py.

Usage:
    python scripts/detect_capture_gap.py -u grace-mar
    python scripts/detect_capture_gap.py -u grace-mar --json
    python scripts/detect_capture_gap.py -u grace-mar --notice 5 --warning 10 --alert 21
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_USER = "grace-mar"
DEFAULT_NOTICE = 7
DEFAULT_WARNING = 14
DEFAULT_ALERT = 30


def _find_evidence_path(user_id: str) -> Path | None:
    """Auto-detect Evidence file: self-archive.md (grace-mar) or self-evidence.md."""
    user_dir = REPO_ROOT / "users" / user_id
    for name in ("self-archive.md", "self-evidence.md"):
        p = user_dir / name
        if p.is_file():
            return p
    return None


def _parse_latest_evidence(evidence_path: Path) -> tuple[str | None, str | None]:
    """Extract the latest Evidence entry ID and date from the file.

    Returns (last_id, last_date_str) or (None, None) if no entries found.
    """
    content = evidence_path.read_text(encoding="utf-8")

    last_id: str | None = None
    last_date: str | None = None

    for m in re.finditer(
        r"- id:\s*((?:ACT|READ|WRITE|CREATE|MEDIA|LEARN|CUR|PER)-\d+)",
        content,
    ):
        entry_id = m.group(1)
        date_match = re.search(
            r"date:\s*(\d{4}-\d{2}-\d{2})",
            content[m.end(): m.end() + 500],
        )
        if date_match:
            entry_date = date_match.group(1)
            if last_date is None or entry_date > last_date:
                last_date = entry_date
                last_id = entry_id

    return last_id, last_date


def _parse_last_merge(user_id: str) -> str | None:
    """Find the most recent 'applied' event date in pipeline-events.jsonl."""
    events_path = REPO_ROOT / "users" / user_id / "pipeline-events.jsonl"
    if not events_path.is_file():
        return None

    last_date: str | None = None
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") == "applied" or event.get("action") == "applied":
            ts = event.get("timestamp", event.get("ts", ""))
            d = str(ts)[:10]
            if re.match(r"\d{4}-\d{2}-\d{2}", d):
                if last_date is None or d > last_date:
                    last_date = d

    return last_date


def _pending_count(user_id: str) -> int:
    """Count pending candidates in recursion-gate.md."""
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    if not gate_path.is_file():
        return 0
    content = gate_path.read_text(encoding="utf-8")
    processed_match = re.search(r"^## Processed\s*$", content, re.MULTILINE)
    candidates_section = content[:processed_match.start()] if processed_match else content
    return len(re.findall(r"status:\s*pending", candidates_section))


def detect_gap(
    user_id: str,
    *,
    notice_days: int = DEFAULT_NOTICE,
    warning_days: int = DEFAULT_WARNING,
    alert_days: int = DEFAULT_ALERT,
    today: date | None = None,
) -> dict:
    """Detect capture gaps in the Record.

    Returns a structured dict compatible with the capability_shift pattern.
    """
    today = today or date.today()

    evidence_path = _find_evidence_path(user_id)
    if evidence_path is None:
        return {
            "last_evidence_date": None,
            "last_evidence_id": None,
            "days_since_evidence": None,
            "last_merge_date": None,
            "days_since_merge": None,
            "pending_count": _pending_count(user_id),
            "level": "unknown",
            "message": f"No Evidence file found for {user_id}",
        }

    last_id, last_date_str = _parse_latest_evidence(evidence_path)
    last_merge_str = _parse_last_merge(user_id)

    days_since_evidence: int | None = None
    if last_date_str:
        try:
            last_dt = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            days_since_evidence = (today - last_dt).days
        except ValueError:
            pass

    days_since_merge: int | None = None
    if last_merge_str:
        try:
            merge_dt = datetime.strptime(last_merge_str, "%Y-%m-%d").date()
            days_since_merge = (today - merge_dt).days
        except ValueError:
            pass

    gap_days = days_since_evidence if days_since_evidence is not None else None

    if gap_days is None:
        level = "unknown"
    elif gap_days >= alert_days:
        level = "alert"
    elif gap_days >= warning_days:
        level = "warning"
    elif gap_days >= notice_days:
        level = "notice"
    else:
        level = "ok"

    if gap_days is not None and level != "ok":
        message = f"Record hasn't grown in {gap_days} days (last: {last_id}, {last_date_str})"
    elif gap_days is not None:
        message = f"Record healthy — last entry {gap_days}d ago ({last_id}, {last_date_str})"
    else:
        message = "No Evidence entries found"

    return {
        "last_evidence_date": last_date_str,
        "last_evidence_id": last_id,
        "days_since_evidence": days_since_evidence,
        "last_merge_date": last_merge_str,
        "days_since_merge": days_since_merge,
        "pending_count": _pending_count(user_id),
        "level": level,
        "message": message,
    }


def format_gap_one_liner(result: dict) -> str:
    """One-line summary for warmup/dream integration."""
    level = result.get("level", "unknown")
    days = result.get("days_since_evidence")
    eid = result.get("last_evidence_id", "?")
    pending = result.get("pending_count", 0)

    if level == "ok":
        return f"Capture health: OK ({days}d since {eid}, {pending} pending)"
    if level == "unknown":
        return "Capture health: unknown (no Evidence file or entries)"
    return f"Capture health: {level.upper()} — {days}d since {eid} ({pending} pending)"


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect capture gaps in Evidence.")
    ap.add_argument(
        "-u", "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER,
    )
    ap.add_argument("--notice", type=int, default=DEFAULT_NOTICE)
    ap.add_argument("--warning", type=int, default=DEFAULT_WARNING)
    ap.add_argument("--alert", type=int, default=DEFAULT_ALERT)
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    result = detect_gap(
        args.user,
        notice_days=args.notice,
        warning_days=args.warning,
        alert_days=args.alert,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_gap_one_liner(result))
        if result["level"] not in ("ok", "unknown"):
            print(f"  Last Evidence: {result['last_evidence_id']} on {result['last_evidence_date']}")
            print(f"  Last merge:    {result['last_merge_date'] or 'unknown'}")
            print(f"  Pending:       {result['pending_count']} candidate(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
