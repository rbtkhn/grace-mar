#!/usr/bin/env python3
"""
Summarize seed-registry.jsonl — list, filter, group seed claims.

Template-portable (companion-self + grace-mar).

Usage:
  python3 scripts/seed_registry_summary.py -u grace-mar
  python3 scripts/seed_registry_summary.py --status weak_signal
  python3 scripts/seed_registry_summary.py --category identity
  python3 scripts/seed_registry_summary.py --ready
  python3 scripts/seed_registry_summary.py --by status
  python3 scripts/seed_registry_summary.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


def load_latest(user_id: str) -> dict[str, dict[str, Any]]:
    """Load the latest snapshot per seed_id (last-write-wins in JSONL)."""
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            sid = row.get("seed_id", "")
            if sid:
                latest[sid] = row
        except json.JSONDecodeError:
            continue
    return latest


def _filter(
    claims: dict[str, dict[str, Any]],
    *,
    status: str | None = None,
    category: str | None = None,
    ready: bool = False,
    readiness_threshold: float = 0.6,
) -> list[dict[str, Any]]:
    result = list(claims.values())
    terminal = {"promoted", "rejected", "expired"}
    result = [c for c in result if c.get("status") not in terminal]
    if status:
        result = [c for c in result if c.get("status") == status]
    if category:
        result = [c for c in result if c.get("category") == category]
    if ready:
        result = [c for c in result if c.get("promotion_readiness", 0) >= readiness_threshold]
    return sorted(result, key=lambda c: c.get("promotion_readiness", 0), reverse=True)


def _group_by(claims: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in claims:
        groups[c.get(key) or "(none)"].append(c)
    return dict(groups)


def _format_claim(c: dict[str, Any]) -> str:
    ctrds = f"  ctrds={c.get('contradiction_count', 0)}" if c.get("contradiction_count") else ""
    return (
        f"  {c['seed_id']:<20} [{c['status']:<16}] "
        f"obs={c['observation_count']:<3} rec={c['recurrence_score']:.2f} "
        f"conf={c['confidence']:.2f} ready={c['promotion_readiness']:.2f}{ctrds}\n"
        f"  {'':20} {c['claim_text'][:70]}\n"
        f"  {'':20} cat={c['category']}  sens={c.get('sensitivity', 'standard')}"
    )


def _format_summary(claims: list[dict[str, Any]], label: str = "") -> str:
    lines: list[str] = []
    if label:
        lines.append(f"  Seed Registry — {label}")
    else:
        lines.append("  Seed Registry Summary")
    lines.append(f"  Active claims: {len(claims)}")
    lines.append("  " + "-" * 70)
    for c in claims:
        lines.append(_format_claim(c))
        lines.append("")
    return "\n".join(lines)


def _format_grouped(groups: dict[str, list[dict[str, Any]]], key: str) -> str:
    lines: list[str] = []
    lines.append(f"  Grouped by: {key}")
    lines.append("  " + "-" * 70)
    for group_key in sorted(groups.keys()):
        members = groups[group_key]
        lines.append(f"\n  {key}={group_key} ({len(members)} claims)")
        for c in members:
            lines.append(f"    {c['seed_id']:<18} [{c['status']:<14}] "
                         f"rec={c['recurrence_score']:.2f} "
                         f"ready={c['promotion_readiness']:.2f}  "
                         f"{c['claim_text'][:50]}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize the seed registry.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--ready", action="store_true", help="Show promotion-ready claims")
    parser.add_argument("--readiness-threshold", type=float, default=0.6)
    parser.add_argument("--by", choices=["status", "category", "sensitivity"],
                        help="Group by field")
    parser.add_argument("--all", action="store_true",
                        help="Include terminal statuses (promoted, rejected, expired)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    latest = load_latest(args.user)
    if not latest:
        print("No seed claims found.", file=sys.stderr)
        return 0

    if args.all:
        filtered = sorted(latest.values(),
                          key=lambda c: c.get("promotion_readiness", 0), reverse=True)
    else:
        filtered = _filter(
            latest,
            status=args.status,
            category=args.category,
            ready=args.ready,
            readiness_threshold=args.readiness_threshold,
        )

    if not filtered:
        print("No matching claims.", file=sys.stderr)
        return 0

    if args.by:
        groups = _group_by(filtered, args.by)
        if args.json:
            print(json.dumps({k: v for k, v in groups.items()}, indent=2))
        else:
            print(_format_grouped(groups, args.by))
        return 0

    if args.json:
        print(json.dumps(filtered, indent=2))
    else:
        label_parts = []
        if args.status:
            label_parts.append(f"status={args.status}")
        if args.category:
            label_parts.append(f"category={args.category}")
        if args.ready:
            label_parts.append(f"ready (>={args.readiness_threshold})")
        print(_format_summary(filtered, " | ".join(label_parts)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
