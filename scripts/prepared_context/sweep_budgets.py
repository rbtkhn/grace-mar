#!/usr/bin/env python3
"""
Sweep all lane × mode combinations and report benchmark scores.

Runs build_budgeted_context for each (lane, mode) pair and collects
utilization, coverage, and mean_included_rank into a comparison table.
Output: markdown table (default) or JSON (--json).

Usage:
  python3 scripts/prepared_context/sweep_budgets.py
  python3 scripts/prepared_context/sweep_budgets.py --json
  python3 scripts/prepared_context/sweep_budgets.py --lanes work-strategy work-dev
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "prepared_context" / "build_budgeted_context.py"
LANE_DEFAULTS = REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"
MODES = ("compact", "medium", "deep")


def _load_lanes(budgets_file: Path) -> list[str]:
    if not budgets_file.is_file():
        return ["default"]
    data = json.loads(budgets_file.read_text(encoding="utf-8"))
    return [k for k in data if k != "default"] or ["default"]


def _run_one(
    lane: str,
    mode: str,
    query: str,
    budgets_file: Path,
    tmp_dir: Path,
    env: dict[str, str],
) -> dict | None:
    out_path = tmp_dir / f"{lane}_{mode}.md"
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--lane", lane,
        "--mode", mode,
        "--query", query,
        "-o", str(out_path),
        "--repo-root", str(tmp_dir),
        "--budgets-file", str(budgets_file),
        "--score",
    ]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FAIL {lane}/{mode}: {r.stderr.strip()}", file=sys.stderr)
        return None
    for line in r.stdout.strip().splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass
    body = r.stdout.strip()
    if body.startswith("{"):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Sweep budget lanes × modes and report scores.")
    ap.add_argument("--lanes", nargs="*", default=None, help="Lanes to sweep (default: all from lane-defaults.json)")
    ap.add_argument("--query", "-q", default="", help="Search query for ranking")
    ap.add_argument("--budgets-file", type=Path, default=LANE_DEFAULTS)
    ap.add_argument("--observations", type=Path, default=None, help="Path to observations JSONL (overrides GRACE_MAR_RUNTIME_LEDGER_ROOT)")
    ap.add_argument("--json", action="store_true", default=False, help="Output JSON instead of markdown table")
    args = ap.parse_args()

    lanes = args.lanes or _load_lanes(args.budgets_file)
    results: list[dict] = []

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        obs_dir = tmp / "runtime" / "observations"
        obs_dir.mkdir(parents=True)

        if args.observations and args.observations.is_file():
            (obs_dir / "index.jsonl").write_text(
                args.observations.read_text(encoding="utf-8"), encoding="utf-8"
            )
        else:
            default_obs = REPO_ROOT / "runtime" / "observations" / "index.jsonl"
            seed_obs = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"
            src = default_obs if default_obs.is_file() else seed_obs
            if src.is_file():
                (obs_dir / "index.jsonl").write_text(
                    src.read_text(encoding="utf-8"), encoding="utf-8"
                )

        (tmp / "prepared-context").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp)}

        for lane in lanes:
            for mode in MODES:
                row = _run_one(lane, mode, args.query, args.budgets_file, tmp, env)
                if row:
                    results.append(row)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("| Lane | Mode | Budget | Util | Coverage | Mean Rank | Incl | Excl |")
        print("|------|------|--------|------|----------|-----------|------|------|")
        for r in results:
            receipt_path = tmp / "prepared-context" / "last-budget-builds.json"
            print(
                f"| {r.get('lane', '?')} "
                f"| {r.get('mode', '?')} "
                f"| - "
                f"| {r.get('utilization', 0):.2%} "
                f"| {r.get('coverage', 0):.2%} "
                f"| {r.get('mean_included_rank', 0):.3f} "
                f"| {r.get('included_count', 0)} "
                f"| {r.get('excluded_count', 0)} |"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
