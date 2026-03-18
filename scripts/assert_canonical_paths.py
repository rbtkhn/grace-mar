#!/usr/bin/env python3
"""
Assert that a user directory has the canonical path layout (lowercase filenames).

Required: self.md, self-evidence.md, recursion-gate.md
Optional: self-archive.md (checked if --strict).

Usage:
  python scripts/assert_canonical_paths.py
  python scripts/assert_canonical_paths.py --user grace-mar
  python scripts/assert_canonical_paths.py --user grace-mar --strict

Exit: 0 if all required (and optional when --strict) paths exist; 1 otherwise.
Set GRACE_MAR_SKIP_PATH_CHECK=1 to skip (exit 0 without checking).
"""

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from repo_io import CANONICAL_RECORD_FILES_REQUIRED  # noqa: E402

REQUIRED = CANONICAL_RECORD_FILES_REQUIRED
OPTIONAL_STRICT = ("self-archive.md",)


def main() -> int:
    if os.environ.get("GRACE_MAR_SKIP_PATH_CHECK") == "1":
        return 0
    parser = argparse.ArgumentParser(description="Assert canonical user paths exist.")
    parser.add_argument("--user", default="grace-mar", help="User id under users/")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR, help="Users directory")
    parser.add_argument("--strict", action="store_true", help="Also require self-archive.md")
    args = parser.parse_args()
    user_dir = args.users_dir / args.user
    if not user_dir.is_dir():
        print(f"assert_canonical_paths: user dir not found: {user_dir}", file=sys.stderr)
        return 1
    missing = []
    for name in REQUIRED:
        if not (user_dir / name).is_file():
            missing.append(name)
    if args.strict:
        for name in OPTIONAL_STRICT:
            if not (user_dir / name).is_file():
                missing.append(name)
    if missing:
        print(f"assert_canonical_paths: missing under {user_dir}: {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
