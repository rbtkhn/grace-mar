#!/usr/bin/env python3
"""
Library: require a fresh continuity receipt before OpenClaw /stage handback.

Used by scripts/handback_server.py. See continuity_preflight.py.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPTS_DIR = REPO_ROOT / "runtime" / "continuity" / "receipts"

from verify_continuity_receipt import verify_receipt_file


def list_receipt_paths(receipts_dir: Path) -> list[Path]:
    if not receipts_dir.is_dir():
        return []
    out: list[Path] = []
    for p in receipts_dir.iterdir():
        if p.is_file() and p.suffix.lower() == ".json":
            out.append(p)
    return sorted(out, key=lambda x: x.stat().st_mtime, reverse=True)


def load_receipt_meta(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def find_valid_receipt(
    user_id: str,
    runtime: str,
    *,
    receipts_dir: Path | None = None,
    repo_root: Path | None = None,
    ttl_hours: float = 12.0,
    explicit_path: Path | None = None,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Return (ok, error_message, meta).

    meta includes receipt_path (repo-relative posix), receipt_valid, continuity_checked_at.
    """
    repo_root = repo_root or REPO_ROOT
    receipts_dir = receipts_dir or DEFAULT_RECEIPTS_DIR
    env_path = (os.getenv("GRACE_MAR_CONTINUITY_RECEIPT") or "").strip()
    candidates: list[Path] = []
    if explicit_path is not None:
        candidates.append(explicit_path)
    elif env_path:
        candidates.append(Path(env_path))
    else:
        for p in list_receipt_paths(receipts_dir):
            meta = load_receipt_meta(p)
            if not meta:
                continue
            if str(meta.get("user_id") or "") != user_id:
                continue
            if str(meta.get("runtime") or "") != runtime:
                continue
            candidates.append(p)

    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not candidates:
        return (
            False,
            "no valid continuity receipt; run: python scripts/continuity_preflight.py -u "
            f"{user_id} -r {runtime} --fail-on-missing",
            {},
        )

    last_err = "no valid continuity receipt"
    for path in candidates:
        ok, err = verify_receipt_file(path, repo_root=repo_root, ttl_hours=ttl_hours)
        try:
            rel = path.resolve().relative_to(repo_root.resolve())
            rel_s = str(rel).replace("\\", "/")
        except ValueError:
            rel_s = str(path)
        if ok:
            return True, "", {
                "continuity_receipt_path": rel_s,
                "continuity_receipt_valid": True,
                "continuity_checked_at": checked_at,
            }
        last_err = err

    return False, last_err, {}


def assert_continuity_ok(
    user_id: str,
    runtime: str,
    *,
    ttl_hours: float = 12.0,
    receipts_dir: Path | None = None,
    repo_root: Path | None = None,
    explicit_receipt: Path | None = None,
) -> tuple[bool, str, dict[str, Any]]:
    return find_valid_receipt(
        user_id,
        runtime,
        receipts_dir=receipts_dir,
        repo_root=repo_root,
        ttl_hours=ttl_hours,
        explicit_path=explicit_receipt,
    )


def append_continuity_block_event(
    repo_root: Path,
    *,
    user_id: str,
    reason: str,
    source: str = "openclaw_stage",
) -> None:
    """Append one structured continuity_block line for dashboards (non-fatal if IO fails)."""
    try:
        p = repo_root / "runtime" / "observability" / "continuity_blocks.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        event: dict[str, Any] = {
            "event": "continuity_block",
            "user_id": user_id,
            "reason": reason,
            "source": source,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError:
        pass
