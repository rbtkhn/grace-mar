#!/usr/bin/env python3
"""
Fail if grace-mar Record paths appear under companion-xavier instance tree.

Scans: docs/skill-work/work-xavier/companion-xavier/users/xavier/
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
    REPO_ROOT
    / "docs"
    / "skill-work"
    / "work-xavier"
    / "companion-xavier"
    / "users"
    / "xavier"
)
FORBIDDEN = "users/grace-mar/"


def main() -> int:
    if not TARGET.is_dir():
        print(f"check_companion_xavier_leakage: skip (missing {TARGET.relative_to(REPO_ROOT)})")
        return 0
    bad: list[str] = []
    for path in sorted(TARGET.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            bad.append(f"{path.relative_to(REPO_ROOT)}: read error: {e}")
            continue
        if FORBIDDEN in text:
            bad.append(f"{path.relative_to(REPO_ROOT)}: contains {FORBIDDEN!r}")
    if bad:
        print("companion-xavier leakage check FAILED:\n", file=sys.stderr)
        for line in bad:
            print(line, file=sys.stderr)
        return 1
    print("companion-xavier leakage check OK (no users/grace-mar/ under instance tree).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
