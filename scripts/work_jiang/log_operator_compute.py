#!/usr/bin/env python3
"""Append one JSON line to work-jiang operator compute ledger (tokens / API estimates).

Optional mirror to users/<id>/compute-ledger.jsonl (same shape as Voice/bot runs) for unified reporting.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "research" / "external" / "work-jiang" / "operator-compute-ledger.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", default="analysis_llm", help="event kind")
    parser.add_argument("--tokens", type=int, default=0)
    parser.add_argument("--usd-estimate", type=float, default=0.0, dest="usd")
    parser.add_argument("--backend", default="local", help="local|openai|other")
    parser.add_argument("--note", default="")
    parser.add_argument(
        "--mirror-grace-mar-ledger",
        action="store_true",
        help="Also append a line to users/grace-mar/compute-ledger.jsonl (operator:work-jiang channel_key).",
    )
    args = parser.parse_args()

    row = {
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": args.kind,
        "tokens": args.tokens,
        "usd_estimate": args.usd,
        "backend": args.backend,
        "note": args.note,
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=True) + "\n")
    print(f"Appended to {LEDGER}")

    if args.mirror_grace_mar_ledger:
        gm = ROOT / "users" / "grace-mar" / "compute-ledger.jsonl"
        gm_row = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "channel_key": "operator:work-jiang",
            "bucket": f"work_jiang:{args.kind}",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": args.tokens,
            "model": args.backend,
            "usd_estimate": args.usd,
            "note": args.note[:500] if args.note else "",
        }
        gm.parent.mkdir(parents=True, exist_ok=True)
        with gm.open("a", encoding="utf-8") as f:
            f.write(json.dumps(gm_row, ensure_ascii=True) + "\n")
        print(f"Mirrored to {gm}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
