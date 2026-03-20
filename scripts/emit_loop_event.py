#!/usr/bin/env python3
"""
Emit america-first-ky proactive-loop pipeline events by delegating to emit_pipeline_event.py.

Uses subprocess — does not import emit_pipeline_event as a library.

Usage:
  python scripts/emit_loop_event.py --phase started
  python scripts/emit_loop_event.py --phase staged territory=wap cycle=daily
  python scripts/emit_loop_event.py -u grace-mar --phase approved
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PHASE_TO_EVENT = {
    "started": "loop_cycle_started",
    "staged": "loop_cycle_staged",
    "approved": "loop_cycle_approved",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit loop_cycle_* pipeline events via scripts/emit_pipeline_event.py",
    )
    parser.add_argument(
        "--user",
        "-u",
        default=(os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"),
        help="User id (default: GRACE_MAR_USER_ID or grace-mar)",
    )
    parser.add_argument(
        "--phase",
        required=True,
        choices=sorted(PHASE_TO_EVENT.keys()),
        help="Maps to loop_cycle_started | loop_cycle_staged | loop_cycle_approved",
    )
    parser.add_argument(
        "extras",
        nargs="*",
        help="Extra key=value fields passed through to emit_pipeline_event.py",
    )
    args = parser.parse_args()

    event_type = PHASE_TO_EVENT[args.phase]
    emit_script = REPO_ROOT / "scripts" / "emit_pipeline_event.py"
    cmd: list[str] = [
        sys.executable,
        str(emit_script),
        "-u",
        args.user,
        event_type,
        "none",
        *args.extras,
    ]
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
