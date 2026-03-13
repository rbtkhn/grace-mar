#!/usr/bin/env python3
"""
commit-msg hook: staged changes to gated Record paths require an explicit token.

Gated paths (pipeline merge targets + PRP anchor):
  users/*/self.md, self-evidence.md, self-archive.md, merge-receipts.jsonl
  bot/prompt.py
  grace-mar-llm.txt, users/*/*-llm.txt

Allow commit if message contains [gated-merge] or merge via process_approved_candidates.
Emergency: ALLOW_GATED_RECORD_EDIT=1

Install: pre-commit install --hook-type commit-msg
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _is_gated(rel: str) -> bool:
    rel = rel.replace("\\", "/").strip()
    if not rel:
        return False
    if rel == "bot/prompt.py" or rel == "grace-mar-llm.txt":
        return True
    parts = rel.split("/")
    if len(parts) < 3 or parts[0] != "users":
        return False
    name = parts[-1]
    if name in ("self.md", "self-evidence.md", "self-archive.md", "merge-receipts.jsonl"):
        return True
    if name.endswith("-llm.txt"):
        return True
    return False


def _allowed_message(msg: str) -> bool:
    if "[gated-merge]" in msg:
        return True
    if "process_approved_candidates" in msg:
        return True
    return False


def main() -> int:
    if os.environ.get("ALLOW_GATED_RECORD_EDIT", "").strip() in ("1", "yes", "true"):
        return 0
    if len(sys.argv) < 2:
        return 0
    msg_path = Path(sys.argv[1])
    if not msg_path.is_file():
        return 0
    msg = msg_path.read_text(encoding="utf-8", errors="replace")
    if _allowed_message(msg):
        return 0

    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return 0
    gated = [f for f in r.stdout.splitlines() if _is_gated(f)]
    if not gated:
        return 0

    print(
        "Gated Record paths are staged but commit message lacks [gated-merge].\n"
        "These files should change only via the approved pipeline "
        "(process_approved_candidates.py --apply), then commit with [gated-merge] in the message.\n"
        "\n"
        f"Staged gated files:\n  " + "\n  ".join(gated) + "\n"
        "\n"
        "Fix: add [gated-merge] to the commit message, or run the merge script and commit its result.\n"
        "Emergency only: ALLOW_GATED_RECORD_EDIT=1 git commit ...\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
