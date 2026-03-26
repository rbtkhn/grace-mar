#!/usr/bin/env python3
"""
Shared I/O and path helpers for Grace-Mar scripts.

Single place for REPO_ROOT, fork namespace (users/<id>), default fork id, and
optional per-fork config. Designed for multi-tenant boundaries: each fork is
isolated under its own directory; quotas, retention, and permissions are
per-fork. See docs/fork-isolation-and-multi-tenant.md.
"""

import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"
DEFAULT_USER_ID = (os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")

# Authoritative on-disk names under users/<id>/. Docs may say SELF/EVIDENCE as concepts;
# filenames are always these. See docs/canonical-paths.md.
CANONICAL_EVIDENCE_BASENAME = "self-archive.md"
CANONICAL_RECORD_FILES_REQUIRED: tuple[str, ...] = (
    "self.md",
    CANONICAL_EVIDENCE_BASENAME,
    "recursion-gate.md",
)


def read_path(path: Path) -> str:
    """Read path as utf-8; return '' if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def profile_dir(user_id: str) -> Path:
    """Return users/<user_id> directory under repo root (fork namespace root)."""
    return REPO_ROOT / "users" / user_id


def fork_root(fork_id: str) -> Path:
    """Alias for profile_dir: the filesystem root for this fork. All fork data lives under this path."""
    return profile_dir(fork_id)


def list_forks() -> list[str]:
    """
    Discover fork IDs by scanning users/ for directories that contain at least one
    canonical fork file (self.md or recursion-gate.md). Ignores non-directories and
    hidden dirs. Order is arbitrary.
    """
    if not USERS_DIR.exists():
        return []
    out = []
    for path in USERS_DIR.iterdir():
        if not path.is_dir() or path.name.startswith("."):
            continue
        if (path / "self.md").exists() or (path / "recursion-gate.md").exists():
            out.append(path.name)
    return sorted(out)


def fork_config_path(fork_id: str) -> Path:
    """Path to optional per-fork config (JSON). Schema: docs/fork-isolation-and-multi-tenant.md §7."""
    return fork_root(fork_id) / "fork-config.json"


def missing_canonical_record_files(user_id: str) -> list[str]:
    """
    Return basenames missing under users/<user_id>/. Empty list if all required exist.
    If the user directory does not exist, returns a single sentinel entry.
    """
    root = profile_dir(user_id)
    if not root.is_dir():
        return ["<users/{0}/ directory missing>".format(user_id)]
    return [name for name in CANONICAL_RECORD_FILES_REQUIRED if not (root / name).is_file()]


def assert_canonical_record_layout(user_id: str, *, context: str = "") -> None:
    """
    Fail loudly if required Record files are missing. Set GRACE_MAR_SKIP_PATH_CHECK=1 to skip.

    Raises:
        RuntimeError: missing files or missing user directory
    """
    if os.environ.get("GRACE_MAR_SKIP_PATH_CHECK", "").strip() == "1":
        return
    missing = missing_canonical_record_files(user_id)
    if missing:
        ctx = f" ({context})" if context else ""
        fix = (
            "See docs/canonical-paths.md. If you have legacy uppercase filenames, run:\n"
            f"  python scripts/migrate_legacy_user_filenames.py --user {user_id} --dry-run\n"
            f"  python scripts/migrate_legacy_user_filenames.py --user {user_id} --apply"
        )
        raise RuntimeError(
            f"Grace-Mar: canonical Record files missing for GRACE_MAR_USER_ID={user_id!r}: {missing}.{ctx}\n{fix}"
        )


def load_fork_config(fork_id: str) -> dict[str, Any] | None:
    """
    Load optional per-fork config from users/<fork_id>/fork-config.json.
    Returns None if file missing or invalid. Callers can use this for quotas,
    retention overrides, and display_name. Schema and defaults are in
    docs/fork-isolation-and-multi-tenant.md.
    """
    path = fork_config_path(fork_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
