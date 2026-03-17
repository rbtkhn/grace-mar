#!/usr/bin/env python3
"""
Shared I/O and path helpers for Grace-Mar scripts.

Single place for REPO_ROOT, reading files (utf-8), profile dir, and default user id.
Reduces duplicate _read/REPO_ROOT/DEFAULT_USER across 25+ scripts.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = (os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")


def read_path(path: Path) -> str:
    """Read path as utf-8; return '' if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def profile_dir(user_id: str) -> Path:
    """Return users/<user_id> directory under repo root."""
    return REPO_ROOT / "users" / user_id
