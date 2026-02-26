#!/usr/bin/env python3
"""
Rotate ephemeral context files (MEMORY and SELF-ARCHIVE) for one user.

Usage:
  python scripts/rotate_context.py --user grace-mar          # dry run
  python scripts/rotate_context.py --user grace-mar --apply  # apply changes
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from rotate_telegram_archive import rotate_archive

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _parse_dated_line(line: str) -> tuple[datetime | None, str]:
    m = re.match(r"^(\s*[-*]\s*)\[(\d{4}-\d{2}-\d{2})\](.*)$", line)
    if not m:
        return None, line
    _, ts, _ = m.groups()
    try:
        return datetime.strptime(ts, "%Y-%m-%d"), line
    except ValueError:
        return None, line


def rotate_memory(user_id: str, ttl_days: int, apply: bool) -> dict:
    memory_path = REPO_ROOT / "users" / user_id / "memory.md"
    if not memory_path.exists():
        return {"ok": True, "memory_removed": 0, "reason": "memory_not_found"}

    content = memory_path.read_text(encoding="utf-8")
    cutoff = datetime.now() - timedelta(days=max(1, ttl_days))
    removed = 0
    out_lines: list[str] = []

    for line in content.splitlines():
        dt, raw = _parse_dated_line(line)
        if dt and dt < cutoff:
            removed += 1
            continue
        out_lines.append(raw)

    text = "\n".join(out_lines)
    today = date.today().isoformat()
    if re.search(r"^Last rotated:\s*\d{4}-\d{2}-\d{2}\s*$", text, re.MULTILINE):
        text = re.sub(
            r"^Last rotated:\s*\d{4}-\d{2}-\d{2}\s*$",
            f"Last rotated: {today}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    elif "Last rotated:" in text:
        text = re.sub(r"^Last rotated:.*$", f"Last rotated: {today}", text, count=1, flags=re.MULTILINE)

    if apply and text != content:
        memory_path.write_text(text.rstrip() + "\n", encoding="utf-8")

    return {
        "ok": True,
        "memory_removed": removed,
        "memory_updated": text != content,
        "applied": apply,
    }


def emit_maintenance_event(user_id: str, memory_stats: dict, archive_stats: dict, apply: bool) -> None:
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            user_id,
            "maintenance",
            "none",
            f"action=rotate_context",
            f"applied={str(apply).lower()}",
            f"memory_removed={memory_stats.get('memory_removed', 0)}",
            f"archive_rotated={archive_stats.get('rotated', 0)}",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Rotate MEMORY and SELF-ARCHIVE for one user.")
    parser.add_argument("--user", "-u", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry run)")
    parser.add_argument("--memory-ttl-days", type=int, default=7, help="Drop dated memory lines older than TTL")
    parser.add_argument("--archive-max-bytes", type=int, default=1_000_000, help="Archive size threshold in bytes")
    parser.add_argument("--archive-max-entries", type=int, default=2500, help="Archive entry count threshold")
    parser.add_argument("--archive-keep-recent", type=int, default=2000, help="Archive entries to keep in main file")
    args = parser.parse_args()

    memory_stats = rotate_memory(user_id=args.user, ttl_days=args.memory_ttl_days, apply=args.apply)
    archive_stats = rotate_archive(
        user_id=args.user,
        apply=args.apply,
        max_bytes=args.archive_max_bytes,
        max_entries=args.archive_max_entries,
        keep_recent=args.archive_keep_recent,
    )
    emit_maintenance_event(args.user, memory_stats, archive_stats, args.apply)

    if args.apply:
        print(
            "Context rotation applied: "
            f"memory_removed={memory_stats.get('memory_removed', 0)}, "
            f"archive_rotated={archive_stats.get('rotated', 0)}"
        )
    else:
        print(
            "Context rotation dry run: "
            f"memory_removed={memory_stats.get('memory_removed', 0)}, "
            f"archive_rotated={archive_stats.get('rotated', 0)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
