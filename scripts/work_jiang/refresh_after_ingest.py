#!/usr/bin/env python3
"""Light post-ingest refresh: registry, analysis backlog, status dashboard.

Does not run full rebuild_all.py — use after adding or replacing a lecture .md.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_STEPS = (
    "scripts/work_jiang/build_source_registry.py",
    "scripts/work_jiang/render_analysis_backlog.py",
    "scripts/work_jiang/render_status_dashboard.py",
)


def main() -> int:
    for rel in _STEPS:
        script = ROOT / rel
        if not script.is_file():
            print(f"Missing script: {script}", file=sys.stderr)
            return 1
        print(f"Running {rel} …", file=sys.stderr)
        subprocess.check_call([sys.executable, str(script)], cwd=str(ROOT))
    print("refresh_after_ingest: done.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
