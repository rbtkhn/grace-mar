#!/usr/bin/env python3
"""
Hash continuity contract files and write a JSON receipt under runtime/continuity/receipts/.

Does not modify the Record. See schemas/work_dev/continuity_receipt.schema.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPTS_DIR = REPO_ROOT / "runtime" / "continuity" / "receipts"
READER_TOOL = "continuity_preflight.py"
READER_VERSION = "1.0.0"


def sha256_file_text(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha256(raw).hexdigest()


def build_receipt(
    *,
    user_id: str,
    runtime: str,
    session_id: str,
    repo_root: Path,
    receipts_rel_base: str = "runtime/continuity/receipts",
) -> tuple[dict, list[str]]:
    """Return receipt dict and list of error strings (empty if ok)."""
    errors: list[str] = []
    user_dir = repo_root / "users" / user_id
    required_names = ("session-log.md", "recursion-gate.md", "self-archive.md")
    entries: list[dict[str, str]] = []
    for name in required_names:
        rel = f"users/{user_id}/{name}"
        p = repo_root / rel
        if not p.is_file():
            errors.append(f"missing: {rel}")
            continue
        entries.append({"path": rel.replace("\\", "/"), "sha256": sha256_file_text(p)})
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    receipt = {
        "version": 1,
        "session_id": session_id,
        "user_id": user_id,
        "runtime": runtime,
        "created_at": ts,
        "required_paths": entries,
        "reader": {"tool": READER_TOOL, "version": READER_VERSION},
    }
    return receipt, errors


def write_receipt(
    receipt: dict,
    *,
    out_path: Path,
    repo_root: Path | None = None,
) -> str:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    root = (repo_root or REPO_ROOT).resolve()
    try:
        rel = out_path.resolve().relative_to(root)
        return str(rel).replace("\\", "/")
    except ValueError:
        return str(out_path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description="Write continuity hash receipt for handback preflight.")
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork / user id")
    ap.add_argument("-r", "--runtime", default="openclaw", help="Runtime label (e.g. openclaw)")
    ap.add_argument(
        "-s",
        "--session-id",
        default="",
        help="Session id (default: timestamp_openclaw)",
    )
    ap.add_argument(
        "--receipts-dir",
        type=Path,
        default=DEFAULT_RECEIPTS_DIR,
        help="Directory for receipt JSON (default: runtime/continuity/receipts)",
    )
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file (default: auto under receipts-dir)",
    )
    ap.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit non-zero if any required file is missing",
    )
    args = ap.parse_args()
    uid = args.user.strip()
    rt = args.runtime.strip()
    sid = (args.session_id or "").strip() or f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}_{rt}"

    receipt, errs = build_receipt(user_id=uid, runtime=rt, session_id=sid, repo_root=args.repo_root)
    if errs and args.fail_on_missing:
        for e in errs:
            print(f"error: {e}")
        return 1

    out = args.output
    if out is None:
        safe = sid.replace(":", "-").replace("/", "-")
        out = args.receipts_dir / f"continuity-{uid}-{rt}-{safe}.json"

    rel_written = write_receipt(receipt, out_path=out, repo_root=args.repo_root)
    print(rel_written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
