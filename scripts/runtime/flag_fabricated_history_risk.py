#!/usr/bin/env python3
"""Narrow fabricated-history risk heuristics on runtime observations (not general confidence)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from observation_store import by_id  # noqa: E402
from uncertainty_envelope import compute_fabricated_history_risk  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(
        description="Flag fabricated-history risk (low|medium|high) for observation IDs."
    )
    p.add_argument("--id", action="append", dest="ids", required=True, metavar="OBS_ID")
    p.add_argument("--json", action="store_true", help="Emit JSON with risk and reasons")
    args = p.parse_args()

    rows: list[dict] = []
    for oid in args.ids:
        raw = by_id(oid)
        if raw is None:
            print(f"error: missing observation: {oid}", file=sys.stderr)
            return 2
        rows.append(raw)

    risk, reasons = compute_fabricated_history_risk(rows)
    out = {"fabricated_history_risk": risk, "reasons": reasons}
    if args.json:
        print(json.dumps(out, ensure_ascii=True, indent=2))
    else:
        print(f"fabricated_history_risk: {risk}")
        for r in reasons:
            print(f"  - {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
