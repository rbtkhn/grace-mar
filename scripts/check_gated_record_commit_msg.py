#!/usr/bin/env python3
"""
commit-msg hook: staged changes to gated Record paths require an explicit token.

Gated paths (pipeline merge targets + PRP anchor + canonical skills/library):
  users/*/self.md, self-evidence.md, self-archive.md, self-skills.md, skills.md, self-library.md, merge-receipts.jsonl
  bot/prompt.py
  grace-mar-llm.txt, users/*/*-llm.txt

Allow commit if message contains [gated-merge], process_approved_candidates, MERGE-RECEIPT:, or SNAPSHOT:.
Emergency: ALLOW_GATED_RECORD_EDIT=1

Install: pre-commit install --hook-type commit-msg
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from gated_record_rules import allowed_gated_commit_message, is_gated_record_path


def main() -> int:
    if os.environ.get("ALLOW_GATED_RECORD_EDIT", "").strip() in ("1", "yes", "true"):
        return 0
    if len(sys.argv) < 2:
        return 0
    msg_path = Path(sys.argv[1])
    if not msg_path.is_file():
        return 0
    msg = msg_path.read_text(encoding="utf-8", errors="replace")
    if allowed_gated_commit_message(msg):
        return 0

    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return 0
    gated = [f for f in r.stdout.splitlines() if is_gated_record_path(f)]
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
