#!/usr/bin/env python3
"""
CI: for pull requests, every commit that touches gated Record paths must have an
allowed token in its commit message (same rule as check_gated_record_commit_msg.py).

Compare: git rev-list BASE..HEAD; for each commit, list files changed; if any are
gated and the message lacks a token, fail.

Emergency (repository secret or env in workflow): ALLOW_GATED_RECORD_EDIT=1

Usage (GitHub Actions):
  python scripts/check_gated_record_pr.py --base "$BASE_SHA" --head "$HEAD_SHA"

Requires full history: actions/checkout with fetch-depth: 0
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = _SCRIPT_DIR.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from gated_record_rules import allowed_gated_commit_message, is_gated_record_path


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def _commit_range_shas(base: str, head: str, cwd: Path) -> list[str]:
    r = _run_git(["rev-list", "--reverse", f"{base}..{head}"], cwd)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        sys.exit(2)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def _files_in_commit(commit: str, cwd: Path) -> list[str]:
    r = _run_git(["show", "--pretty=format:", "--name-only", commit], cwd)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return []
    return [ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()]


def _commit_message(commit: str, cwd: Path) -> str:
    r = _run_git(["log", "-1", "--format=%B", commit], cwd)
    if r.returncode != 0:
        return ""
    return r.stdout


def main() -> int:
    if os.environ.get("ALLOW_GATED_RECORD_EDIT", "").strip() in ("1", "yes", "true"):
        print("check_gated_record_pr: ALLOW_GATED_RECORD_EDIT set — skipping")
        return 0

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo",
        type=Path,
        default=REPO_ROOT,
        help="Git repository root (default: grace-mar root next to scripts/)",
    )
    p.add_argument("--base", required=True, help="Merge base / PR base SHA")
    p.add_argument("--head", required=True, help="PR head SHA")
    args = p.parse_args()

    cwd = args.repo.resolve()
    failures: list[tuple[str, list[str], str]] = []

    for commit in _commit_range_shas(args.base, args.head, cwd):
        files = _files_in_commit(commit, cwd)
        gated = [f for f in files if is_gated_record_path(f)]
        if not gated:
            continue
        msg = _commit_message(commit, cwd)
        if allowed_gated_commit_message(msg):
            continue
        short = _run_git(["rev-parse", "--short", commit], cwd)
        label = short.stdout.strip() if short.returncode == 0 else commit[:12]
        failures.append((label, gated, msg.strip()[:120]))

    if not failures:
        return 0

    print(
        "Gated Record paths changed in this PR, but one or more commits lack an allowed token.\n"
        "Allowed tokens in the commit message: [gated-merge], process_approved_candidates, "
        "MERGE-RECEIPT:, SNAPSHOT:\n\n"
        "Match local pre-commit: scripts/check_gated_record_commit_msg.py\n",
        file=sys.stderr,
    )
    for label, gated, preview in failures:
        print(f"  Commit {label} — gated files: {gated}", file=sys.stderr)
        print(f"    Message preview: {preview!r}\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
