#!/usr/bin/env python3
"""Expand baseline scenarios × runtimes into a JSON matrix (BUILD-AI-GAP-005)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BASE = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "scenarios" / "baseline_scenarios"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate scenario matrix rows.")
    ap.add_argument("--scenario", default="", help="Filter by scenario_id prefix")
    ap.add_argument(
        "--runtimes",
        default="openclaw,cursor,claude-code",
        help="Comma-separated runtime labels",
    )
    ap.add_argument("--formats", default="json", choices=["json", "markdown"])
    args = ap.parse_args()
    rts = [x.strip() for x in args.runtimes.split(",") if x.strip()]
    rows: list[dict] = []
    for path in sorted(BASE.glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        sid = str(raw.get("scenario_id") or path.stem)
        if args.scenario and not sid.startswith(args.scenario):
            continue
        for rt in rts:
            rows.append(
                {
                    "scenario_id": sid,
                    "runtime": rt,
                    "variation": "default",
                    "expected_failure_mode": raw.get("failure_family"),
                    "required_checks": raw.get("required_checks") or [],
                    "severity": raw.get("severity") or "medium",
                }
            )
    rows.sort(key=lambda r: (r["scenario_id"], r["runtime"]))
    if args.formats == "json":
        print(json.dumps({"version": 1, "rows": rows}, indent=2))
    else:
        for r in rows:
            print(f"- **{r['scenario_id']}** / {r['runtime']}: {r['expected_failure_mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
