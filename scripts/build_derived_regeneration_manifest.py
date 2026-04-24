#!/usr/bin/env python3
"""Build the derived regeneration manifest for repo-owned rebuild targets."""

from __future__ import annotations

import argparse
from pathlib import Path

from derived_regeneration import REPO_ROOT, build_manifest_payload, write_receipt

DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev" / "derived-regeneration-manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="output JSON path (default: artifacts/work-dev/derived-regeneration-manifest.json)",
    )
    args = parser.parse_args()

    out = args.output
    if not out.is_absolute():
        out = (REPO_ROOT / out).resolve()

    payload = build_manifest_payload()
    write_receipt(out, payload)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
