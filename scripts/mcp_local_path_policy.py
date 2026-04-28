"""
Shared path policy for local MCP adapters (allowlist + repo containment).

Used by mcp_local_readonly.py and mcp_local_index.py — keep rejection rules aligned.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any, Literal

Kind = Literal["file", "dir"]


def posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def validate_allowlist_schema(cfg: dict[str, Any]) -> None:
    for key in ("allowed_roots", "blocked_roots", "blocked_files", "blocked_name_patterns"):
        if key not in cfg:
            raise ValueError(f"allowlist missing {key!r}")
    if "max_file_bytes" not in cfg:
        raise ValueError("allowlist missing max_file_bytes")


def norm_segments(rel_posix: str) -> list[str]:
    parts = [p for p in rel_posix.replace("\\", "/").split("/") if p]
    if ".." in parts:
        raise ValueError("path must not contain .. segments")
    return parts


def resolve_target_under_allowlist(
    repo_root: Path,
    path_str: str,
    cfg: dict[str, Any],
    *,
    kind: Kind,
) -> Path:
    """
    Resolve repo-relative path_str under allowlist rules.

    Raises ValueError on policy violations.
    """
    raw = path_str.strip()
    if not raw:
        raise ValueError("path cannot be empty")

    if len(raw) >= 2 and raw[1] == ":":
        raise ValueError("absolute paths not allowed")
    if raw.startswith("/"):
        raise ValueError("absolute paths not allowed")

    norm = raw.replace("\\", "/").strip("/")
    parts = norm_segments(norm)
    rel_join = "/".join(parts) if parts else ""

    low_rel = rel_join.lower()
    if low_rel.startswith("users/grace-mar/") or low_rel == "users/grace-mar":
        raise ValueError("path cannot reference users/grace-mar")

    candidate = (repo_root / Path(*parts)) if parts else repo_root
    try:
        resolved = candidate.resolve()
    except OSError as e:
        raise ValueError(f"cannot resolve path: {e}") from e

    repo_abs = repo_root.resolve()
    try:
        resolved.relative_to(repo_abs)
    except ValueError as e:
        raise ValueError(f"path escapes repository root: {resolved}") from e

    rel_final = posix_under_repo(repo_root, resolved)

    blocked_roots = [str(x).replace("\\", "/").strip("/") for x in cfg["blocked_roots"]]
    for br in blocked_roots:
        br_prefix = br + "/" if br else ""
        if rel_final == br or (br_prefix and rel_final.startswith(br_prefix)):
            raise ValueError(f"path is under blocked root {br!r}")

    allowed = [str(x).replace("\\", "/") for x in cfg["allowed_roots"]]
    ok = False
    for root in allowed:
        prefix = root if root.endswith("/") else root + "/"
        if rel_final == root.rstrip("/") or rel_final.startswith(prefix):
            ok = True
            break
    if not ok:
        raise ValueError(f"path not under any allowed_roots (got {rel_final!r})")

    base = resolved.name
    blocked_files = {str(x).lower() for x in cfg["blocked_files"]}
    if base.lower() in blocked_files:
        raise ValueError(f"basename blocked by allowlist: {base!r}")

    for pat in cfg["blocked_name_patterns"]:
        if fnmatch.fnmatch(base.lower(), pat.lower()):
            raise ValueError(f"basename matches blocked_name_patterns: {base!r}")

    if kind == "file":
        if not resolved.is_file():
            raise ValueError(f"not a regular file: {resolved}")
    else:
        if not resolved.is_dir():
            raise ValueError(f"not a directory: {resolved}")

    return resolved


def basename_blocked(name: str, cfg: dict[str, Any]) -> bool:
    """True if basename matches blocked_files or blocked_name_patterns."""
    blocked_files = {str(x).lower() for x in cfg["blocked_files"]}
    if name.lower() in blocked_files:
        return True
    for pat in cfg["blocked_name_patterns"]:
        if fnmatch.fnmatch(name.lower(), pat.lower()):
            return True
    return False


def rel_under_blocked_root(rel_final: str, cfg: dict[str, Any]) -> bool:
    """True if rel_final is inside any blocked_roots prefix."""
    blocked_roots = [str(x).replace("\\", "/").strip("/") for x in cfg["blocked_roots"]]
    for br in blocked_roots:
        br_prefix = br + "/" if br else ""
        if rel_final == br or (br_prefix and rel_final.startswith(br_prefix)):
            return True
    return False


def rel_under_allowed_root(rel_final: str, cfg: dict[str, Any]) -> bool:
    allowed = [str(x).replace("\\", "/") for x in cfg["allowed_roots"]]
    for root in allowed:
        prefix = root if root.endswith("/") else root + "/"
        if rel_final == root.rstrip("/") or rel_final.startswith(prefix):
            return True
    return False
