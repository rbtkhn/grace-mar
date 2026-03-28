#!/usr/bin/env python3
"""Print a GitHub compare URL for the current branch (no gh CLI required)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "git failed\n")
        raise SystemExit(1)
    return proc.stdout.strip()


def parse_github_owner_repo(remote_url: str) -> tuple[str, str]:
    """Return (owner, repo) from origin URL."""
    u = remote_url.strip()
    # git@github.com:owner/repo.git
    m = re.match(r"git@github\.com:([^/]+)/([^./]+)(?:\.git)?$", u)
    if m:
        return m.group(1), m.group(2)
    # https://github.com/owner/repo.git or .../repo
    m = re.match(r"https?://github\.com/([^/]+)/([^./]+)(?:\.git)?/?$", u)
    if m:
        return m.group(1), m.group(2)
    raise ValueError(f"Could not parse GitHub owner/repo from: {remote_url!r}")


def compare_url(owner: str, repo: str, base: str, head: str) -> str:
    return f"https://github.com/{owner}/{repo}/compare/{base}...{head}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print GitHub compare URL for current HEAD vs base branch."
    )
    parser.add_argument(
        "--base",
        "-b",
        default="main",
        help="Base branch name (default: main)",
    )
    parser.add_argument(
        "--head",
        default=None,
        help="Head branch or ref (default: current branch)",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name for URL parsing (default: origin)",
    )
    args = parser.parse_args()

    remote_url = _run_git("remote", "get-url", args.remote)
    owner, repo = parse_github_owner_repo(remote_url)
    head = args.head or _run_git("branch", "--show-current")
    if not head:
        sys.stderr.write("Detached HEAD: pass --head <branch>\n")
        return 1
    if head == args.base:
        sys.stderr.write(
            f"github_compare_url: current branch is '{head}' (same as --base). "
            "Checkout a feature branch or pass --head for a meaningful compare URL.\n"
        )
    url = compare_url(owner, repo, args.base, head)
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
