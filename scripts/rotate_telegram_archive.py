#!/usr/bin/env python3
"""
Rotate TELEGRAM-ARCHIVE.md when it exceeds size or entry count.

Moves oldest entries to users/pilot-001/archives/TELEGRAM-ARCHIVE-YYYY-MM.md.
Keeps the last KEEP_RECENT entries in the main file. Run manually or via cron.

Thresholds:
  - MAX_BYTES: 1 MB
  - MAX_ENTRIES: 2500
  - KEEP_RECENT: 2000 entries

Usage:
    python scripts/rotate_telegram_archive.py          # Dry run (report only)
    python scripts/rotate_telegram_archive.py --apply  # Perform rotation
"""

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_PATH = REPO_ROOT / "users" / "pilot-001" / "TELEGRAM-ARCHIVE.md"
ARCHIVES_DIR = REPO_ROOT / "users" / "pilot-001" / "archives"

MAX_BYTES = 1_000_000
MAX_ENTRIES = 2500
KEEP_RECENT = 2000


def parse_archive(content: str) -> tuple[str, list[str]]:
    """Split archive into header and list of entry blocks."""
    parts = content.split("\n---\n\n", 1)
    if len(parts) == 1:
        return "", []
    header = parts[0] + "\n---\n\n"
    body = parts[1]
    # Each entry is `**[ts]** ...\n> lines\n`; entries separated by \n\n
    blocks = [b.strip() for b in body.split("\n\n") if b.strip() and b.strip().startswith("**[")]
    return header, blocks


def get_entry_ym(block: str) -> str | None:
    """Extract YYYY-MM from first line of block."""
    m = re.match(r"\*\*\[(\d{4}-\d{2})-\d{2}", block)
    return m.group(1) if m else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Rotate Telegram archive when too large")
    parser.add_argument("--apply", "-a", action="store_true", help="Perform rotation (default: dry run)")
    args = parser.parse_args()

    if not ARCHIVE_PATH.exists():
        print("Archive not found, nothing to do.")
        return

    content = ARCHIVE_PATH.read_text()
    size = len(content.encode("utf-8"))
    header, blocks = parse_archive(content)
    n = len(blocks)

    if n <= MAX_ENTRIES and size <= MAX_BYTES:
        print(f"Archive OK: {n} entries, {size:,} bytes (limit {MAX_ENTRIES} / {MAX_BYTES:,})")
        return

    to_rotate = n - KEEP_RECENT
    if to_rotate <= 0:
        to_rotate = n // 2  # Rotate half if over size but under entry count
    to_rotate = min(to_rotate, n - 1)

    rotated = blocks[:to_rotate]
    kept = blocks[to_rotate:]

    if args.apply:
        ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
        # Group rotated by YYYY-MM and append to corresponding files
        by_month: dict[str, list[str]] = {}
        for b in rotated:
            ym = get_entry_ym(b) or "unknown"
            by_month.setdefault(ym, []).append(b)
        for ym, entries in by_month.items():
            dest = ARCHIVES_DIR / f"TELEGRAM-ARCHIVE-{ym}.md"
            header_ym = f"# TELEGRAM ARCHIVE — {ym}\n\n> Rotated from main archive. Append-only.\n\n---\n\n"
            if dest.exists():
                existing = dest.read_text()
                if not existing.rstrip().endswith("\n\n"):
                    existing += "\n\n"
                dest.write_text(existing + "\n\n".join(entries) + "\n\n")
            else:
                dest.write_text(header_ym + "\n\n".join(entries) + "\n\n")
        # Rewrite main archive
        new_body = "\n\n".join(kept) + ("\n\n" if kept else "")
        ARCHIVE_PATH.write_text(header + new_body)
        print(f"Rotated {to_rotate} entries to {ARCHIVES_DIR}. Kept {len(kept)} in main archive.")
    else:
        print(f"Would rotate {to_rotate} entries (keep {len(kept)}). Run with --apply to perform.")


if __name__ == "__main__":
    main()
