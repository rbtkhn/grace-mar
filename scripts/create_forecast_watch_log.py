#!/usr/bin/env python3
"""Append a forecast-informed entry to docs/skill-work/work-strategy/strategy-notebook/forecast-watch-log.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEMPLATE = """### {date} {title}

**Series:**  
{series_name}

**Forecast artifact:**  
{artifact_path}

**Receipt:**  
{receipt_path}

**What it suggests:**  
{suggestion}

**Why it matters:**  
{why_it_matters}

**Current status:**  
{status}

**Thresholds to watch next:**  
- {threshold_1}
- {threshold_2}

**Invalidators:**  
- {invalidator_1}
- {invalidator_2}

**Next review date:**  
{next_review_date}

**Boundary note:**  
Forecast artifact referenced for planning only. No Record update implied.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a forecast watch entry to the forecast watch log."
    )
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--suggestion", required=True)
    parser.add_argument("--why-it-matters", required=True)
    parser.add_argument("--status", default="weak signal")
    parser.add_argument("--threshold-1", default="no threshold set")
    parser.add_argument("--threshold-2", default="no threshold set")
    parser.add_argument("--invalidator-1", default="no invalidator set")
    parser.add_argument("--invalidator-2", default="no invalidator set")
    parser.add_argument("--next-review-date", required=True)
    parser.add_argument(
        "--out",
        default="docs/skill-work/work-strategy/strategy-notebook/forecast-watch-log.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    artifact = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
    series_name = artifact.get("series_name", "unknown_series")

    block = TEMPLATE.format(
        date=args.date,
        title=args.title,
        series_name=series_name,
        artifact_path=args.artifact,
        receipt_path=args.receipt,
        suggestion=args.suggestion,
        why_it_matters=args.why_it_matters,
        status=args.status,
        threshold_1=args.threshold_1,
        threshold_2=args.threshold_2,
        invalidator_1=args.invalidator_1,
        invalidator_2=args.invalidator_2,
        next_review_date=args.next_review_date,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists():
        existing = out_path.read_text(encoding="utf-8").rstrip()
        updated = existing + "\n\n" + block + "\n"
    else:
        updated = "# Forecast Watch Log\n\n" + block + "\n"

    out_path.write_text(updated, encoding="utf-8")
    print(f"Wrote watch entry: {out_path}")


if __name__ == "__main__":
    main()
