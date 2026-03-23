#!/usr/bin/env python3
"""Delegate to fork_lifecycle.py end-session."""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "fork_lifecycle.py"), "end-session", *sys.argv[1:]]
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
