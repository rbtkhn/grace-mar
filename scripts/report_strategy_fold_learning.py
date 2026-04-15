#!/usr/bin/env python3
"""
Read-only markdown report for strategy-fold-events.jsonl (fold learning ledger).

Legacy name; the current operator command is 'weave'. Script and JSONL field names
retain 'fold' for backward compatibility.

Usage:
  python3 scripts/report_strategy_fold_learning.py -u grace-mar --days 30
  python3 scripts/report_strategy_fold_learning.py -u grace-mar --days 90 --max-events 200
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir  # noqa: E402

LEDGER_NAME = "strategy-fold-events.jsonl"


def default_jsonl_path(user_id: str) -> Path:
    return profile_dir(user_id) / LEDGER_NAME


def parse_ts(raw: str) -> datetime | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def compression_proxy(row: dict) -> float | None:
    ic = row.get("inbox_chars")
    dd = row.get("days_delta_chars")
    if ic is None or dd is None:
        return None
    try:
        ic = int(ic)
        dd = int(dd)
    except (TypeError, ValueError):
        return None
    if ic <= 0:
        return None
    return dd / ic


def load_events(path: Path, *, since: datetime, max_events: int | None) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = parse_ts(str(row.get("ts", "")))
            if ts is None or ts < since:
                continue
            rows.append(row)
    rows.sort(key=lambda r: parse_ts(str(r.get("ts", ""))) or datetime.min.replace(tzinfo=timezone.utc))
    if max_events is not None and len(rows) > max_events:
        rows = rows[-max_events:]
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument("--days", type=int, default=30, help="Include events with ts in the last N days (default 30)")
    ap.add_argument("--max-events", type=int, default=None, help="Keep only the last M events after filter")
    ap.add_argument("--jsonl", type=Path, default=None, help="Override ledger path")
    args = ap.parse_args()
    uid = args.user.strip()
    path = args.jsonl if args.jsonl is not None else default_jsonl_path(uid)
    since = datetime.now(timezone.utc) - timedelta(days=max(0, args.days))

    rows = load_events(path, since=since, max_events=args.max_events)

    try:
        ledger_disp = path.relative_to(REPO_ROOT)
    except ValueError:
        ledger_disp = path
    lines_out: list[str] = []
    lines_out.append("# Strategy fold learning report\n")
    lines_out.append(f"- **Ledger:** `{ledger_disp}`\n")
    lines_out.append(f"- **Window:** last **{args.days}** days (ts ≥ UTC cutoff)\n")
    lines_out.append(f"- **Events in window:** {len(rows)}\n")

    if not rows:
        lines_out.append("\n_No events._\n")
        sys.stdout.write("".join(lines_out))
        return 0

    by_kind: dict[str, int] = {}
    proxies: list[tuple[float, dict]] = []
    for r in rows:
        k = str(r.get("fold_kind", "?"))
        by_kind[k] = by_kind.get(k, 0) + 1
        cp = compression_proxy(r)
        if cp is not None:
            proxies.append((cp, r))

    lines_out.append("\n## By fold_kind\n\n")
    for k in sorted(by_kind.keys()):
        lines_out.append(f"- **{k}:** {by_kind[k]}\n")

    if proxies:
        vals = [p[0] for p in proxies]
        lines_out.append("\n## Compression proxy (days_delta_chars / inbox_chars)\n\n")
        lines_out.append(f"- **Mean:** {statistics.mean(vals):.4f}\n")
        lines_out.append(f"- **Median:** {statistics.median(vals):.4f}\n")
        if len(vals) > 1:
            lines_out.append(f"- **Stdev:** {statistics.stdev(vals):.4f}\n")

        tight = sorted(proxies, key=lambda x: x[0])[:3]
        loose = sorted(proxies, key=lambda x: x[0], reverse=True)[:3]
        lines_out.append("\n### Tightest (lowest ratio — small page delta vs scratch)\n\n")
        for cp, r in tight:
            nd = r.get("notebook_date", "?")
            note = r.get("note", "")
            ts = r.get("ts", "")
            lines_out.append(f"- **{nd}** (`{ts}`) proxy={cp:.4f}" + (f" — {note}" if note else "") + "\n")
        lines_out.append("\n### Loosest (highest ratio — large page delta vs scratch)\n\n")
        for cp, r in loose:
            nd = r.get("notebook_date", "?")
            note = r.get("note", "")
            ts = r.get("ts", "")
            lines_out.append(f"- **{nd}** (`{ts}`) proxy={cp:.4f}" + (f" — {note}" if note else "") + "\n")

    lines_out.append("\n## All events (table)\n\n")
    lines_out.append("| ts | notebook_date | kind | inbox | delta | proxy | note |\n")
    lines_out.append("|---|-----|------|-------|-------|-------|------|\n")
    for r in rows:
        ts = r.get("ts", "")
        nd = r.get("notebook_date", "")
        k = r.get("fold_kind", "")
        ic = r.get("inbox_chars", "")
        dd = r.get("days_delta_chars", "")
        cp = compression_proxy(r)
        proxy_s = f"{cp:.4f}" if cp is not None else ""
        note = str(r.get("note", "")).replace("|", "\\|")[:80]
        lines_out.append(f"| {ts} | {nd} | {k} | {ic} | {dd} | {proxy_s} | {note} |\n")

    ratings_vd = [r["ratings"]["verify_depth"] for r in rows if isinstance(r.get("ratings"), dict) and "verify_depth" in r["ratings"]]
    ratings_jf = [r["ratings"]["judgment_freshness"] for r in rows if isinstance(r.get("ratings"), dict) and "judgment_freshness" in r["ratings"]]
    if ratings_vd or ratings_jf:
        lines_out.append("\n## Ratings (when present)\n\n")
        if ratings_vd:
            lines_out.append(f"- **verify_depth:** mean {statistics.mean(ratings_vd):.2f} (n={len(ratings_vd)})\n")
        if ratings_jf:
            lines_out.append(f"- **judgment_freshness:** mean {statistics.mean(ratings_jf):.2f} (n={len(ratings_jf)})\n")

    sys.stdout.write("".join(lines_out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
