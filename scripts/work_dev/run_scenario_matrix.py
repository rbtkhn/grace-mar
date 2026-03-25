#!/usr/bin/env python3
"""Map scenario matrix rows to suggested pytest commands (JSONL summary)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit scenario matrix run hints.")
    ap.add_argument("--write-jsonl", type=Path, default=None)
    args = ap.parse_args()
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    lines = []
    for row in data.get("rows") or []:
        hint = {
            "scenario_id": row["scenario_id"],
            "runtime": row["runtime"],
            "suggested_pytest": "pytest tests/test_continuity_receipts.py tests/test_lane_scope.py -q",
        }
        lines.append(json.dumps(hint))
    out = "\n".join(lines) + ("\n" if lines else "")
    if args.write_jsonl:
        args.write_jsonl.parent.mkdir(parents=True, exist_ok=True)
        args.write_jsonl.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
