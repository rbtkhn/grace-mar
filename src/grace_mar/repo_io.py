"""Repository root and path helpers aligned with docs/canonical-paths.md."""

from __future__ import annotations

from pathlib import Path

# src/grace_mar/repo_io.py -> repo root is three levels up
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def repo_root() -> Path:
    """Return the repository root (contains ``users/``, ``bot/``, ``scripts/``)."""
    return _REPO_ROOT


def users_dir(user_id: str = "grace-mar") -> Path:
    """Canonical ``users/<id>/`` directory."""
    return _REPO_ROOT / "users" / user_id
