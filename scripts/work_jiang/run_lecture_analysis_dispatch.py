#!/usr/bin/env python3
"""Print which extractor applies for a series_id or source_id (smoke test for registry)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_WJ = Path(__file__).resolve().parent
if str(_WJ) not in sys.path:
    sys.path.insert(0, str(_WJ))

from extractors.registry import get_extractor_class, list_registered_series


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series-id", default="")
    parser.add_argument("--source-id", default="")
    parser.add_argument("--list-series", action="store_true", help="Print registered series ids and exit.")
    args = parser.parse_args()
    if args.list_series:
        print("registered series:", ", ".join(list_registered_series()))
        return 0
    cls = get_extractor_class(series_id=args.series_id or None, source_id=args.source_id or None)
    inst = cls()
    print(f"extractor: {cls.__name__}")
    print(f"series_id: {inst.series_id}")
    print(f"schema_version: {inst.schema_version()}")
    print(f"prompt: {inst.prompt_system_path()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
