#!/usr/bin/env python3
"""Append a THINK update receipt (JSON line) — WORK audit only.

Usage:
  python3 scripts/record_think_update.py --trigger "post READ-0042" --read-ids READ-0042 \\
    --think-ids THINK-001 --ix-candidate false --note "optional"
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "artifacts/skill-think/update-receipts/think-updates.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trigger", required=True, help="What caused the update")
    ap.add_argument("--read-ids", default="", help="Comma-separated READ-* ids")
    ap.add_argument("--think-ids", default="", help="Comma-separated THINK-* ids touched")
    ap.add_argument("--ix-candidate", choices=("true", "false"), default="false")
    ap.add_argument("--note", default="")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "trigger": args.trigger,
        "read_ids": [x.strip() for x in args.read_ids.split(",") if x.strip()],
        "think_ids": [x.strip() for x in args.think_ids.split(",") if x.strip()],
        "ix_promotion_candidate_staged": args.ix_candidate == "true",
        "operator_note": args.note,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"appended to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
