#!/usr/bin/env python3
"""Assistive: suggest THINK claim stubs from READ ids found in self-archive.md.

Does NOT write to skill-think.md, think-claims.json, or self.md — stdout only.
Operator copies or adapts; gate rules unchanged for IX promotion.

Usage:
  python3 scripts/propose_think_claims_from_read.py
  python3 scripts/propose_think_claims_from_read.py --archive users/grace-mar/self-archive.md --max-ids 5
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
READ_RE = re.compile(r"\b(READ-[0-9]{4})\b")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--archive",
        type=Path,
        default=REPO_ROOT / "users/grace-mar/self-archive.md",
    )
    ap.add_argument("--max-ids", type=int, default=8)
    args = ap.parse_args()

    if not args.archive.is_file():
        print(f"error: {args.archive} not found", file=sys.stderr)
        return 1

    text = args.archive.read_text(encoding="utf-8", errors="replace")
    seen: list[str] = []
    for m in READ_RE.finditer(text):
        rid = m.group(1)
        if rid not in seen:
            seen.append(rid)

    tail = seen[-args.max_ids :] if args.max_ids else seen

    proposals = []
    for i, rid in enumerate(tail):
        proposals.append(
            {
                "status": "proposed_only",
                "suggested_id": f"THINK-{i + 1:03d}_draft",
                "topic": "(fill from READ title)",
                "capability_type": "topic_familiarity",
                "level": "exposed",
                "evidence_refs": [rid],
                "note": "Assistive stub — assign real THINK id and merge manually into think-claims.json",
            }
        )

    print(
        json.dumps(
            {"proposed_think_claims": proposals, "source_read_ids_found": tail},
            indent=2,
            ensure_ascii=False,
        )
    )
    print(
        "\n# Reminder: do not auto-merge. IX promotion still requires RECURSION-GATE + companion approval.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
