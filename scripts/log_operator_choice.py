#!/usr/bin/env python3
"""
Append an operator menu choice to session-transcript.md (not MEMORY, not EVIDENCE).

Uses a stable ### [WORK-choice] block so scripts/menu_choice_evolution.py can aggregate.
Operator-invoked only — no automatic logging from Voice/analyst.

Usage:
  python3 scripts/log_operator_choice.py -u grace-mar --context WORK --picked A --tags "~15m,gate"
  python3 scripts/log_operator_choice.py -u grace-mar --context GOOD_MORNING --picked "2" --note "deep work"
  python3 scripts/log_operator_choice.py -u grace-mar --context COFFEE --picked E --tags "steward=gate"
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir  # noqa: E402

HEADER = (
    "# SESSION TRANSCRIPT\n\n"
    "> Raw conversation log for operator continuity. Not part of the Record. "
    "Approved content is written to SELF-ARCHIVE on merge.\n\n"
    "> Operator menu picks: blocks with heading level-3 tag **WORK-choice** — see "
    "docs/skill-work/work-menu-conventions.md\n\n---\n\n"
)


def append_work_choice(
    user_dir: Path,
    *,
    context: str,
    picked: str,
    tags: str,
    note: str,
) -> Path:
    path = user_dir / "session-transcript.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    block_lines = [
        f"\n### [WORK-choice] {ts}\n",
        f"- context: {context}\n",
        f"- picked: {picked}\n",
    ]
    if tags.strip():
        block_lines.append(f"- tags: {tags.strip()}\n")
    if note.strip():
        safe = note.strip().replace("\n", " ")[:500]
        block_lines.append(f"- note: {safe}\n")
    block = "".join(block_lines)

    if not path.is_file():
        path.write_text(HEADER + block, encoding="utf-8")
    else:
        raw = path.read_text(encoding="utf-8")
        if "SESSION TRANSCRIPT" not in raw[:200]:
            path.write_text(HEADER + raw + block, encoding="utf-8")
        else:
            with open(path, "a", encoding="utf-8") as f:
                f.write(block)
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument(
        "--context",
        required=True,
        choices=("WORK", "DAILY", "GOOD_MORNING", "COFFEE"),
        help="Menu family",
    )
    ap.add_argument("--picked", required=True, help="Label (e.g. A) or short text")
    ap.add_argument("--tags", default="", help="Comma-separated heuristic tags")
    ap.add_argument("--note", default="", help="Optional single-line note")
    args = ap.parse_args()
    uid = args.user.strip()
    user_dir = profile_dir(uid)
    out = append_work_choice(
        user_dir,
        context=args.context,
        picked=args.picked.strip(),
        tags=args.tags,
        note=args.note,
    )
    print(out.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
