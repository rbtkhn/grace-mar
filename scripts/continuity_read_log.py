#!/usr/bin/env python3
"""
Session continuity proof-of-read — log that recommended Grace-Mar files were read at startup.

Run before or at the start of an OpenClaw (or other harness) session. Appends one JSONL line
to users/[id]/continuity-log.jsonl with timestamp and which files were read. Does not modify
the Record; the log is for audit and verification only.

Usage:
    python scripts/continuity_read_log.py -u grace-mar
    python scripts/continuity_read_log.py -u grace-mar --dry-run

See docs/openclaw-integration.md § Session continuity — Proof-of-read.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

FILES = ["session-log.md", "recursion-gate.md", "self-archive.md"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Log proof-of-read for session continuity (SESSION-LOG, RECURSION-GATE, EVIDENCE)."
    )
    parser.add_argument("-u", "--user", default=DEFAULT_USER, help="User id")
    parser.add_argument("--dry-run", action="store_true", help="Print payload only; do not write log")
    args = parser.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    read_ok: list[str] = []
    missing: list[str] = []
    for name in FILES:
        p = user_dir / name
        if p.exists():
            read_ok.append(name)
        else:
            missing.append(name)

    ts = datetime.now(timezone.utc).isoformat()
    payload = {
        "ts": ts,
        "user_id": args.user,
        "purpose": "openclaw_startup",
        "files_read": read_ok,
    }
    if missing:
        payload["missing"] = missing

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=True))
        return 0

    log_path = user_dir / "continuity-log.jsonl"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=True) + "\n")
    except OSError as e:
        print(f"Could not write {log_path}: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
