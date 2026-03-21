#!/usr/bin/env python3
"""
Verify an atomic integration receipt against the repo working tree or a git revision.

Receipts are written by scripts/atomic_integrate.py (JSON under users/<id>/integration-receipts/).
Each receipt stores before_hashes and after_hashes: maps of repo-relative POSIX paths to sha256
of UTF-8 file contents (same convention as atomic_integrate).

Usage:
  python scripts/verify_integration_receipt.py --receipt users/grace-mar/integration-receipts/integration-receipt-....json
  python scripts/verify_integration_receipt.py --receipt path/to/receipt.json --expect before
  python scripts/verify_integration_receipt.py --receipt path/to/receipt.json --git-ref HEAD

Exit:
  0 — all listed paths match
  1 — mismatch or error
  2 — receipt cannot be verified (e.g. empty after_hashes when mode=after)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_worktree(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_git_show(ref: str, rel_posix: str, repo_root: Path) -> str:
    spec = f"{ref}:{rel_posix}"
    proc = subprocess.run(
        ["git", "show", spec],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        raise FileNotFoundError(proc.stderr.strip() or f"git show {spec} failed")
    return proc.stdout


def verify_hashes(
    expected: dict[str, str],
    *,
    repo_root: Path,
    git_ref: str | None,
) -> tuple[bool, list[str]]:
    """
    Compare expected path -> sha256 to current worktree or git blob.

    Returns (ok, messages) where messages list errors or a single success line.
    """
    errors: list[str] = []
    for rel, want in sorted(expected.items()):
        path = repo_root / rel
        try:
            if git_ref:
                content = _read_git_show(git_ref, rel, repo_root)
            else:
                if not path.is_file():
                    errors.append(f"{rel}: missing on disk (expected {want[:12]}…)")
                    continue
                content = _read_worktree(path)
        except FileNotFoundError as e:
            errors.append(f"{rel}: {e}")
            continue
        got = sha256_text(content)
        if got != want:
            errors.append(f"{rel}: sha256 mismatch (want {want[:16]}… got {got[:16]}…)")
    if errors:
        return False, errors
    return True, [f"OK: {len(expected)} path(s) match"]


def load_receipt(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("receipt must be a JSON object")
    return data


def main() -> int:
    p = argparse.ArgumentParser(description="Verify integration receipt hashes.")
    p.add_argument("--receipt", "-r", required=True, type=Path, help="Path to integration-receipt JSON")
    p.add_argument(
        "--expect",
        choices=("after", "before"),
        default="after",
        help="Which hash map to verify (default: after merge state)",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--git-ref",
        default="",
        help="If set, compare hashes to `git show <ref>:path` instead of working tree",
    )
    args = p.parse_args()
    repo_root = args.repo_root.resolve()

    if not args.receipt.is_file():
        print(f"receipt not found: {args.receipt}", file=sys.stderr)
        return 1

    try:
        receipt = load_receipt(args.receipt)
    except (json.JSONDecodeError, OSError, ValueError) as e:
        print(f"invalid receipt: {e}", file=sys.stderr)
        return 1

    key = "after_hashes" if args.expect == "after" else "before_hashes"
    raw = receipt.get(key)
    if not isinstance(raw, dict):
        print(f"receipt missing {key} object", file=sys.stderr)
        return 1
    expected: dict[str, str] = {str(k): str(v) for k, v in raw.items()}

    if not expected:
        print(
            f"Cannot verify: {key} is empty (dry-run receipts or preflight-only receipts have no {key}).",
            file=sys.stderr,
        )
        return 2

    git_ref = args.git_ref.strip() or None
    if git_ref:
        proc = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode != 0:
            print("--git-ref requires a git checkout at repo-root", file=sys.stderr)
            return 1

    ok, lines = verify_hashes(expected, repo_root=repo_root, git_ref=git_ref)
    for line in lines:
        print(line)
    if not ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
