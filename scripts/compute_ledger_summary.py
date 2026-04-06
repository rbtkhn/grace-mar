#!/usr/bin/env python3
"""
Summarize compute-ledger.jsonl for companion transparency.

Groups rows by bucket, operation, task_type, or time period and prints
totals for tokens, wall time, byte volume, and outcome confidence.

Usage:
  python scripts/compute_ledger_summary.py -u grace-mar
  python scripts/compute_ledger_summary.py -u grace-mar --by task_type
  python scripts/compute_ledger_summary.py -u grace-mar --by date
  python scripts/compute_ledger_summary.py -u grace-mar --by task_id
  python scripts/compute_ledger_summary.py -u grace-mar --since 2026-04-01
  python scripts/compute_ledger_summary.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GROUP_KEYS = ("bucket", "operation", "task_type", "task_id", "date", "model")


@dataclass
class Bucket:
    rows: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    wall_ms: int = 0
    bytes_processed: int = 0
    successes: int = 0
    failures: int = 0
    outcome_confidences: list[float] = field(default_factory=list)

    def ingest(self, row: dict) -> None:
        self.rows += 1
        self.prompt_tokens += int(row.get("prompt_tokens") or 0)
        self.completion_tokens += int(row.get("completion_tokens") or 0)
        self.total_tokens += int(row.get("total_tokens") or 0)
        self.wall_ms += int(row.get("wall_ms") or 0)
        self.bytes_processed += int(row.get("bytes_processed") or 0)
        if row.get("success") is True:
            self.successes += 1
        elif row.get("success") is False:
            self.failures += 1
        oc = row.get("outcome_confidence")
        if oc is not None:
            self.outcome_confidences.append(float(oc))

    @property
    def mean_confidence(self) -> float | None:
        if not self.outcome_confidences:
            return None
        return sum(self.outcome_confidences) / len(self.outcome_confidences)

    def as_dict(self) -> dict:
        d = {
            "rows": self.rows,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "wall_ms": self.wall_ms,
            "bytes_processed": self.bytes_processed,
            "successes": self.successes,
            "failures": self.failures,
        }
        mc = self.mean_confidence
        if mc is not None:
            d["mean_outcome_confidence"] = round(mc, 3)
        return d


def _extract_key(row: dict, group_by: str) -> str:
    if group_by == "date":
        ts = row.get("ts", "")
        try:
            return datetime.fromisoformat(ts).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return "unknown"
    val = row.get(group_by, "")
    return str(val).strip() if val else "(empty)"


def summarize(
    ledger_path: Path,
    group_by: str = "bucket",
    since: str = "",
) -> dict[str, Bucket]:
    buckets: dict[str, Bucket] = defaultdict(Bucket)
    if not ledger_path.is_file():
        return dict(buckets)

    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            since_dt = datetime.fromisoformat(since + "T00:00:00")

    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue

        if since_dt:
            ts = row.get("ts", "")
            try:
                row_dt = datetime.fromisoformat(ts)
                if row_dt.tzinfo:
                    since_cmp = since_dt if since_dt.tzinfo else since_dt.replace(tzinfo=row_dt.tzinfo)
                else:
                    since_cmp = since_dt.replace(tzinfo=None) if since_dt.tzinfo else since_dt
                if row_dt < since_cmp:
                    continue
            except (ValueError, TypeError):
                pass

        key = _extract_key(row, group_by)
        buckets[key].ingest(row)

    return dict(buckets)


def _print_table(buckets: dict[str, Bucket], group_by: str) -> None:
    if not buckets:
        print("(no rows)")
        return
    header = f"{'Group':30s} {'Rows':>6s} {'Tokens':>10s} {'Wall(s)':>9s} {'Bytes':>12s} {'OK':>4s} {'Fail':>4s} {'Conf':>6s}"
    print(header)
    print("-" * len(header))
    for key in sorted(buckets):
        b = buckets[key]
        mc = b.mean_confidence
        conf_s = f"{mc:.2f}" if mc is not None else "-"
        print(
            f"{key:30s} {b.rows:6d} {b.total_tokens:10d} "
            f"{b.wall_ms / 1000:9.1f} {b.bytes_processed:12d} "
            f"{b.successes:4d} {b.failures:4d} {conf_s:>6s}"
        )
    print()
    total = Bucket()
    for b in buckets.values():
        total.rows += b.rows
        total.prompt_tokens += b.prompt_tokens
        total.completion_tokens += b.completion_tokens
        total.total_tokens += b.total_tokens
        total.wall_ms += b.wall_ms
        total.bytes_processed += b.bytes_processed
        total.successes += b.successes
        total.failures += b.failures
        total.outcome_confidences.extend(b.outcome_confidences)
    mc = total.mean_confidence
    conf_s = f"{mc:.2f}" if mc is not None else "-"
    print(
        f"{'TOTAL':30s} {total.rows:6d} {total.total_tokens:10d} "
        f"{total.wall_ms / 1000:9.1f} {total.bytes_processed:12d} "
        f"{total.successes:4d} {total.failures:4d} {conf_s:>6s}"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute ledger summary (companion transparency).")
    ap.add_argument("-u", "--user", default="grace-mar", help="User id")
    ap.add_argument(
        "--by",
        choices=GROUP_KEYS,
        default="bucket",
        help="Group rows by this field (default: bucket)",
    )
    ap.add_argument("--since", default="", metavar="DATE", help="Only include rows at or after this ISO date")
    ap.add_argument("--json", action="store_true", dest="emit_json", help="Output JSON instead of table")
    ap.add_argument("--ledger", type=Path, default=None, help="Path to ledger file (auto-detected if omitted)")
    args = ap.parse_args()

    ledger = args.ledger or (REPO_ROOT / "users" / args.user / "compute-ledger.jsonl")
    if not ledger.is_file():
        print(f"no ledger found at {ledger}", file=sys.stderr)
        return 2

    buckets = summarize(ledger, group_by=args.by, since=args.since)

    if args.emit_json:
        out = {k: v.as_dict() for k, v in sorted(buckets.items())}
        print(json.dumps(out, indent=2))
    else:
        print(f"Compute ledger: {ledger.relative_to(REPO_ROOT)}")
        print(f"Grouped by: {args.by}")
        if args.since:
            print(f"Since: {args.since}")
        print()
        _print_table(buckets, args.by)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
