"""
Shared rules for gated Record path checks (pre-commit commit-msg + CI PR).

Keep in sync: any change here affects scripts/check_gated_record_commit_msg.py
and scripts/check_gated_record_pr.py.
"""

from __future__ import annotations


def is_gated_record_path(rel: str) -> bool:
    rel = rel.replace("\\", "/").strip()
    if not rel:
        return False
    if rel == "bot/prompt.py" or rel == "grace-mar-llm.txt":
        return True
    parts = rel.split("/")
    if len(parts) < 3 or parts[0] != "users":
        return False
    name = parts[-1]
    if name in (
        "self.md",
        "self-evidence.md",
        "self-archive.md",
        "self-skills.md",
        "skills.md",
        "self-library.md",
        "merge-receipts.jsonl",
    ):
        return True
    if name.endswith("-llm.txt"):
        return True
    return False


def allowed_gated_commit_message(msg: str) -> bool:
    if "[gated-merge]" in msg:
        return True
    if "process_approved_candidates" in msg:
        return True
    if "MERGE-RECEIPT:" in msg:
        return True
    if "SNAPSHOT:" in msg:
        return True
    return False
