#!/usr/bin/env python3
"""
OpenClaw oversight heartbeat — for long-running OpenClaw sessions.

Emits a short status: pending candidates, last evidence date, last session.
Run every N hours during a long OpenClaw session to keep human-in-the-loop.

Usage:
    python scripts/openclaw_heartbeat.py -u grace-mar
    python scripts/openclaw_heartbeat.py -u grace-mar --compact
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_review import split_gate_sections

DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _pending_count(pr_content: str) -> int:
    if "## Candidates" not in pr_content or "## Processed" not in pr_content:
        return 0
    candidates, _processed = split_gate_sections(pr_content)
    return len(re.findall(r"### CANDIDATE-\d+.*?status:\s*pending", candidates, re.DOTALL))


def _last_activity_date(evidence_content: str) -> str | None:
    if "## V. ACTIVITY LOG" not in evidence_content:
        return None
    matches = re.findall(r"date:\s*(\d{4}-\d{2}-\d{2})", evidence_content)
    return matches[-1] if matches else None


def _last_session_line(session_log: str) -> str | None:
    lines = [l.strip() for l in session_log.splitlines() if l.strip() and not l.strip().startswith("#")]
    return lines[-1][:120] if lines else None


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw oversight heartbeat")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument("--compact", action="store_true", help="Single-line output")
    args = parser.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    pr = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-archive.md") or _read(user_dir / "self-evidence.md")
    session = _read(user_dir / "session-log.md")

    pending = _pending_count(pr)
    last_act = _last_activity_date(evidence)
    last_session = _last_session_line(session)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    if args.compact:
        parts = [f"[{ts}] pending={pending}"]
        if last_act:
            parts.append(f"last_evidence={last_act}")
        if last_session:
            parts.append(f"session={last_session[:50]}...")
        print(" | ".join(parts))
    else:
        lines = [
            f"# Grace-Mar heartbeat — {ts}",
            "",
            f"- **Pending candidates:** {pending}",
            f"- **Last evidence date:** {last_act or 'unknown'}",
            "",
            "**Action:** Check RECURSION-GATE; run /review if candidates await approval.",
            "",
        ]
        if last_session:
            lines.extend(["**Last session:**", f"> {last_session}", ""])
        print("\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
