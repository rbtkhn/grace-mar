#!/usr/bin/env python3
"""
Verify a continuity receipt: schema shape, TTL, and file hashes vs working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def sha256_file_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_ts(s: str) -> datetime | None:
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def validate_receipt_shape(o: Any) -> tuple[bool, str]:
    if not isinstance(o, dict):
        return False, "receipt is not an object"
    if o.get("version") != 1:
        return False, "version must be 1"
    for k in ("session_id", "user_id", "runtime", "created_at"):
        if not o.get(k) or not isinstance(o.get(k), str):
            return False, f"missing or invalid {k}"
    rp = o.get("required_paths")
    if not isinstance(rp, list) or not rp:
        return False, "required_paths must be a non-empty array"
    for item in rp:
        if not isinstance(item, dict):
            return False, "required_paths item must be object"
        p = item.get("path")
        h = item.get("sha256")
        if not p or not isinstance(p, str):
            return False, "required_paths.path invalid"
        if not h or not isinstance(h, str) or len(h) != 64:
            return False, "required_paths.sha256 invalid"
    rd = o.get("reader")
    if not isinstance(rd, dict) or not rd.get("tool") or not rd.get("version"):
        return False, "reader.tool and reader.version required"
    return True, ""


def verify_receipt_file(
    receipt_path: Path,
    *,
    repo_root: Path,
    ttl_hours: float,
    now: datetime | None = None,
) -> tuple[bool, str]:
    if not receipt_path.is_file():
        return False, f"receipt not found: {receipt_path}"
    try:
        data = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return False, f"invalid JSON: {e}"
    ok, err = validate_receipt_shape(data)
    if not ok:
        return False, err
    created = _parse_ts(str(data["created_at"]))
    if created is None:
        return False, "invalid created_at"
    now = now or datetime.now(timezone.utc)
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    if now - created > timedelta(hours=ttl_hours):
        return False, f"receipt expired (TTL {ttl_hours}h)"

    for item in data["required_paths"]:
        rel = str(item["path"]).replace("\\", "/")
        want = str(item["sha256"])
        p = repo_root / rel
        if not p.is_file():
            return False, f"missing file: {rel}"
        got = sha256_file_bytes(p)
        if got != want:
            return False, f"hash mismatch: {rel}"
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify continuity receipt.")
    ap.add_argument("--receipt", "-r", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--ttl-hours", type=float, default=12.0)
    args = ap.parse_args()
    ok, msg = verify_receipt_file(args.receipt, repo_root=args.repo_root, ttl_hours=args.ttl_hours)
    if ok:
        print("verify_continuity_receipt: OK")
        return 0
    print(f"verify_continuity_receipt: FAIL — {msg}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
