#!/usr/bin/env python3
"""
Run both CIV-MEM and PSY-HIST generators for given source(s).
CIV-MEM = structure/seams; PSY-HIST = prediction/steering.
Together they feed the Integrated Operator Thesis (see CHAPTER-SCAFFOLD-DUAL-LENS.md).

Usage:
    python3 scripts/work_jiang/generate_dual_lenses.py --lecture geo-12
    python3 scripts/work_jiang/generate_dual_lenses.py --batch civ-60 civ-06 --delay 3
    python3 scripts/work_jiang/generate_dual_lenses.py --lecture civ-21 --dry-run
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CIVMEM_SCRIPT = ROOT / "scripts/work_jiang/generate_civmem_memo.py"
PSYHIST_SCRIPT = ROOT / "scripts/work_jiang/generate_psy_hist_memo.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate both CIV-MEM and PSY-HIST memos")
    parser.add_argument("--lecture", type=str, help="Source ID, e.g. civ-21, geo-12")
    parser.add_argument("--batch", nargs="*", help="Multiple source IDs")
    parser.add_argument("--dry-run", action="store_true", help="Pass through to both generators")
    parser.add_argument("--delay", type=float, default=2.5, help="Seconds between batch items (default 2.5)")
    args = parser.parse_args()

    ids = []
    if args.batch:
        ids = args.batch
    elif args.lecture:
        ids = [args.lecture]
    else:
        print("Error: Provide --lecture or --batch", file=sys.stderr)
        return 1

    extra = []
    if args.dry_run:
        extra.append("--dry-run")
    extra.extend(["--delay", str(args.delay)])

    failed = 0
    for script in (CIVMEM_SCRIPT, PSYHIST_SCRIPT):
        if len(ids) == 1:
            cmd = [sys.executable, str(script), "--lecture", ids[0]] + extra
        else:
            cmd = [sys.executable, str(script), "--batch"] + ids + extra
        r = subprocess.run(cmd, cwd=str(ROOT))
        if r.returncode != 0:
            failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
