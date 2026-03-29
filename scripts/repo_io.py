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


def resolve_surface_markdown_path(
    user_dir: Path,
    canonical_key: str,
    *,
    prefer_existing: bool = True,
) -> Path:
    """
    Resolve the Path for a Record surface markdown file under user_dir.

    Conflict rule (self_skills and similar): if both the canonical file
    (e.g. self-skills.md) and a legacy file (e.g. skills.md) exist, the
    canonical path wins — prefer_existing returns the canonical file when it
    is present.

    self_evidence: canonical body is self-archive.md. If it is missing but
    self-evidence.md exists (optional pointer / compat), returns
    self-evidence.md for read scenarios when prefer_existing is True; if
    neither exists, returns self-archive.md as the intended canonical target.

    Raises:
        ValueError: unknown canonical_key or logical-only surface (e.g. self_knowledge).
    """
    from surface_aliases import get_surface_by_key

    surface = get_surface_by_key(canonical_key)
    if surface is None:
        raise ValueError(f"unknown surface key: {canonical_key!r}")
    if surface.canonical_file_stem is None:
        raise ValueError(f"surface {surface.canonical_key!r} has no on-disk markdown file")

    canon = user_dir / f"{surface.canonical_file_stem}.md"

    if surface.canonical_key == "self_evidence":
        if prefer_existing:
            if canon.is_file():
                return canon
            fe = user_dir / "self-evidence.md"
            if fe.is_file():
                return fe
        return canon

    if not prefer_existing:
        return canon

    if canon.is_file():
        return canon
    for leg in surface.legacy_file_stems:
        p = user_dir / f"{leg}.md"
        if p.is_file():
            return p
    return canon


def resolve_self_memory_path(user_dir: Path) -> Path:
    """
    Canonical continuity file: self-memory.md. Legacy memory.md is still read if present
    and self-memory.md is absent (same pattern as skills.md → self-skills.md).
    """
    return resolve_surface_markdown_path(user_dir, "self_memory", prefer_existing=True)


def read_surface_markdown(user_dir: Path, canonical_key: str) -> str:
    """Read UTF-8 content for a surface; empty string if resolved path missing."""
    try:
        path = resolve_surface_markdown_path(user_dir, canonical_key, prefer_existing=True)
    except ValueError:
        return ""
    return read_path(path)


def self_skills_layout_warnings(user_dir: Path) -> list[str]:
    """
    Phase A (advisory): warn on legacy skills.md or duplicate capability index files.

    Canonical capability index: self-skills.md. See docs/canonical-paths.md.
    """
    if not user_dir.is_dir():
        return []
    legacy = user_dir / "skills.md"
    canon = user_dir / "self-skills.md"
    rel = user_dir.name
    out: list[str] = []
    if legacy.is_file() and canon.is_file():
        out.append(
            f"users/{rel}: both skills.md and self-skills.md exist; readers prefer self-skills.md. "
            "Remove skills.md after confirming content is merged."
        )
    elif legacy.is_file() and not canon.is_file():
        out.append(
            f"users/{rel}: legacy skills.md present; rename to self-skills.md "
            f"(e.g. python scripts/migrate_legacy_user_filenames.py --user {rel} --apply)."
        )
    return out


def enforce_canonical_self_skills_layout(user_dir: Path) -> None:
    """
    Phase B: when GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS=1, fail if only legacy
    skills.md exists (canonical self-skills.md required when a capability index file is present).
    """
    if os.environ.get("GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS", "").strip() != "1":
        return
    if not user_dir.is_dir():
        return
    legacy = user_dir / "skills.md"
    canon = user_dir / "self-skills.md"
    if legacy.is_file() and not canon.is_file():
        raise RuntimeError(
            f"Grace-Mar: GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS=1 but users/{user_dir.name}/ "
            "has skills.md without self-skills.md. Migrate: "
            f"python scripts/migrate_legacy_user_filenames.py --user {user_dir.name} --apply"
        )


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
    enforce_canonical_self_skills_layout(profile_dir(user_id))


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
