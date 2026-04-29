"""Shared helpers for work-strategy carry harness and validators (stdlib only)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = frozenset({".md", ".txt", ".markdown"})
MIN_WORDS_NON_TRIVIAL = 50


def safe_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def word_count(text: str) -> int:
    parts = re.split(r"\s+", text.strip())
    return len([p for p in parts if p])


def is_forbidden_record_path(path: Path, repo_root: Path) -> bool:
    """True if path must not be used as harness or validator derived outputs."""
    try:
        resolved = path.resolve()
        root = repo_root.resolve()
    except OSError:
        return True
    try:
        resolved.relative_to(root / "users")
        return True
    except ValueError:
        pass
    try:
        rel = resolved.relative_to(root)
    except ValueError:
        return False
    rel_s = rel.as_posix()
    forbidden_exact = {"bot/prompt.py", "bot/bot.py", "bot/wechat_bot.py"}
    if rel_s in forbidden_exact:
        return True
    return False


def is_text_like(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def inspect_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    """Portable artifact probe for carry harness receipts."""
    rel = ""
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()
    out: dict[str, Any] = {"path": rel, "exists": False, "notes": ""}
    if not path.is_file():
        out["notes"] = "not a file or missing"
        return out
    out["exists"] = True
    try:
        st = path.stat()
        out["size_bytes"] = int(st.st_size)
    except OSError as e:
        out["notes"] = f"stat failed: {e}"
        return out
    if is_text_like(path):
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            out["word_count"] = word_count(raw)
        except OSError as e:
            out["notes"] = f"read failed: {e}"
    else:
        out["notes"] = "non-text suffix; word_count not applied"
    return out
