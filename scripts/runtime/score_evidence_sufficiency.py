#!/usr/bin/env python3
"""Compute uncertainty envelope from runtime observation IDs or prepared-context file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from observation_store import by_id  # noqa: E402
from uncertainty_envelope import (  # noqa: E402
    compute_envelope,
    envelope_to_json,
    load_prepared_context_obs_ids,
)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Score evidence sufficiency → uncertainty envelope (derived from observations)."
    )
    p.add_argument("--id", action="append", dest="ids", metavar="OBS_ID", help="Runtime observation id (repeatable)")
    p.add_argument(
        "--prepared-context",
        type=Path,
        default=None,
        help="Prepared-context markdown; extracts obs_* ids and scores those observations",
    )
    p.add_argument("--json", action="store_true", help="Print envelope JSON only")
    args = p.parse_args()

    ids = list(args.ids or [])
    if args.prepared_context is not None:
        ids.extend(load_prepared_context_obs_ids(args.prepared_context))
        ids = list(dict.fromkeys(ids))

    if not ids:
        print("error: provide --id and/or --prepared-context", file=sys.stderr)
        return 2

    rows: list[dict] = []
    for oid in ids:
        raw = by_id(oid)
        if raw is None:
            print(f"error: missing observation: {oid}", file=sys.stderr)
            return 2
        rows.append(raw)

    env = compute_envelope(rows)
    if args.json:
        print(envelope_to_json(env))
    else:
        print(envelope_to_json(env))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
