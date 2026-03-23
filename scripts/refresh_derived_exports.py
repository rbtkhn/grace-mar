#!/usr/bin/env python3
"""
Refresh all derived artifacts checked by validate-integrity.py (derived export freshness).

Run after Record/prompt edits when `validate-integrity.py` reports stale exports or runtime bundle.
Same order as `process_approved_candidates.py` post-merge exports.

  python3 scripts/refresh_derived_exports.py -u grace-mar
  python3 scripts/validate-integrity.py --user grace-mar
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _prp_output_path(user_id: str) -> Path:
    if user_id == "grace-mar":
        return REPO_ROOT / "grace-mar-llm.txt"
    return REPO_ROOT / "users" / user_id / f"{user_id}-llm.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate manifest, PRP, fork manifest, runtime bundle.")
    parser.add_argument("-u", "--user", default="grace-mar", help="User id")
    args = parser.parse_args()
    uid = args.user.strip() or "grace-mar"
    profile = REPO_ROOT / "users" / uid
    py = sys.executable

    steps: list[list[str]] = [
        [
            py,
            str(REPO_ROOT / "scripts" / "export_prp.py"),
            "-u",
            uid,
            "-n",
            "Abby",
            "-o",
            str(_prp_output_path(uid)),
        ],
        [py, str(REPO_ROOT / "scripts" / "export_manifest.py"), "-u", uid, "-o", str(profile)],
        [py, str(REPO_ROOT / "scripts" / "fork_checksum.py"), "-u", uid, "--manifest"],
        [
            py,
            str(REPO_ROOT / "scripts" / "export_runtime_bundle.py"),
            "-u",
            uid,
            "-o",
            str(profile / "runtime-bundle"),
        ],
    ]

    for cmd in steps:
        label = " ".join(cmd[-4:])
        print(f"Running: {label}", file=sys.stderr)
        r = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
        if r.returncode != 0:
            print(f"FAILED: {cmd}", file=sys.stderr)
            return r.returncode

    print("Derived exports refreshed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
