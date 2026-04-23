#!/usr/bin/env python3
"""Run import_runtime_observation.py for a Letta session summary (stdlib, subprocess).

All Letta-shaped JSON that returns into Grace-Mar should be imported only through
scripts/runtime/import_runtime_observation.py; this wrapper delegates to that script
with --source letta.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT = (
    REPO_ROOT / "bridges" / "runtime-complements" / "letta" / "letta-session-summary.example.json"
)
IMPORT_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "import_runtime_observation.py"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Import a Letta session summary JSON through the runtime complement membrane."
    )
    ap.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to session summary JSON (default: {DEFAULT_INPUT.relative_to(REPO_ROOT)}).",
    )
    args = ap.parse_args()

    in_path = args.input
    if not in_path.is_absolute():
        s = str(in_path)
        if ".." in s or not s.strip():
            print("error: invalid --input path", file=sys.stderr)
            return 1
        in_path = (REPO_ROOT / in_path).resolve()
    if not in_path.is_file():
        print(f"error: input is not a file: {in_path}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable,
        str(IMPORT_SCRIPT),
        "--source",
        "letta",
        "--input",
        str(in_path),
    ]
    p = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=False,
    )
    return int(p.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
