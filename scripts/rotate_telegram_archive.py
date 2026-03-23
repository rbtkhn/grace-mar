#!/usr/bin/env python3
"""
Rotate self-archive.md when it exceeds size or entry count.

SELF-ARCHIVE is gated (appended only on merge). This script rotates the main file
when it grows large; rotated chunks go to archives/SELF-ARCHIVE-YYYY-MM.md (or
``.md.gz`` when ``--compress``). Keeps the last KEEP_RECENT entries in the main file.

**Gzip:** Tools that read monthly archives must open ``.md.gz`` (e.g. ``gzip.open``)
or decompress first. Plain ``.md`` archives from older runs are unchanged.

Threshold defaults can be set in ``config/fork-config.json`` (see ``archive_*`` keys).

Usage:
    python scripts/rotate_telegram_archive.py          # Dry run (report only)
    python scripts/rotate_telegram_archive.py --apply  # Perform rotation
    python scripts/rotate_telegram_archive.py --apply --compress  # Rotated months as .md.gz
"""

import argparse
import gzip
import os
import re
from pathlib import Path

try:
    from fork_config import load_fork_config
except ImportError:
    from scripts.fork_config import load_fork_config

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

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


def rotate_archive(
    user_id: str,
    apply: bool,
    max_bytes: int = MAX_BYTES,
    max_entries: int = MAX_ENTRIES,
    keep_recent: int = KEEP_RECENT,
    compress: bool = False,
) -> dict:
    archive_path = REPO_ROOT / "users" / user_id / "self-archive.md"
    archives_dir = REPO_ROOT / "users" / user_id / "archives"

    if not archive_path.exists():
        return {"ok": True, "rotated": 0, "kept": 0, "reason": "archive_not_found"}

    content = archive_path.read_text(encoding="utf-8")
    size = len(content.encode("utf-8"))
    header, blocks = parse_archive(content)
    n = len(blocks)
    if n <= max_entries and size <= max_bytes:
        return {
            "ok": True,
            "rotated": 0,
            "kept": n,
            "size_bytes": size,
            "reason": "within_limits",
        }

    to_rotate = n - keep_recent
    if to_rotate <= 0:
        to_rotate = n // 2
    to_rotate = max(0, min(to_rotate, max(0, n - 1)))
    rotated = blocks[:to_rotate]
    kept = blocks[to_rotate:]

    if apply:
        archives_dir.mkdir(parents=True, exist_ok=True)
        by_month: dict[str, list[str]] = {}
        for block in rotated:
            ym = get_entry_ym(block) or "unknown"
            by_month.setdefault(ym, []).append(block)
        for ym, entries in by_month.items():
            header_ym = f"# SELF-ARCHIVE — {ym}\n\n> Rotated from main archive. Append-only.\n\n---\n\n"
            if compress:
                dest = archives_dir / f"SELF-ARCHIVE-{ym}.md.gz"
                if dest.exists():
                    with gzip.open(dest, "rt", encoding="utf-8") as zf:
                        existing = zf.read()
                    if not existing.rstrip().endswith("\n\n"):
                        existing += "\n\n"
                    body = existing + "\n\n".join(entries) + "\n\n"
                else:
                    body = header_ym + "\n\n".join(entries) + "\n\n"
                with gzip.open(dest, "wt", encoding="utf-8") as zf:
                    zf.write(body)
            else:
                dest = archives_dir / f"SELF-ARCHIVE-{ym}.md"
                if dest.exists():
                    existing = dest.read_text(encoding="utf-8")
                    if not existing.rstrip().endswith("\n\n"):
                        existing += "\n\n"
                    dest.write_text(existing + "\n\n".join(entries) + "\n\n", encoding="utf-8")
                else:
                    dest.write_text(header_ym + "\n\n".join(entries) + "\n\n", encoding="utf-8")
        new_body = "\n\n".join(kept) + ("\n\n" if kept else "")
        archive_path.write_text(header + new_body, encoding="utf-8")

    return {
        "ok": True,
        "rotated": len(rotated),
        "kept": len(kept),
        "size_bytes": size,
        "applied": apply,
        "compress": compress,
    }


def main() -> None:
    cfg = load_fork_config()
    parser = argparse.ArgumentParser(description="Rotate conversation archive when too large")
    parser.add_argument("--apply", "-a", action="store_true", help="Perform rotation (default: dry run)")
    parser.add_argument("--user", "-u", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=None,
        help=f"Archive size threshold in bytes (default: config or {MAX_BYTES})",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=None,
        help="Archive entry-count threshold (default: config archive_rotation_trigger_entries / archive_max_entries or "
        f"{MAX_ENTRIES})",
    )
    parser.add_argument(
        "--keep-recent",
        type=int,
        default=None,
        help=f"How many recent entries to keep (default: config or {KEEP_RECENT})",
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Write rotated monthly chunks as .md.gz under archives/ (smaller on disk; not plain-text in git)",
    )
    args = parser.parse_args()
    max_bytes = args.max_bytes if args.max_bytes is not None else int(cfg.get("archive_max_bytes", MAX_BYTES))
    max_entries = args.max_entries if args.max_entries is not None else int(
        cfg.get("archive_rotation_trigger_entries") or cfg.get("archive_max_entries") or MAX_ENTRIES
    )
    keep_recent = args.keep_recent if args.keep_recent is not None else int(cfg.get("archive_keep_recent", KEEP_RECENT))
    result = rotate_archive(
        user_id=args.user,
        apply=args.apply,
        max_bytes=max_bytes,
        max_entries=max_entries,
        keep_recent=keep_recent,
        compress=args.compress,
    )
    if result.get("reason") == "archive_not_found":
        print("Archive not found, nothing to do.")
        return
    if result.get("reason") == "within_limits":
        print(
            f"Archive OK: {result.get('kept', 0)} entries, {result.get('size_bytes', 0):,} bytes "
            f"(limit {args.max_entries} / {args.max_bytes:,})"
        )
        return
    if args.apply:
        print(f"Rotated {result.get('rotated', 0)} entries. Kept {result.get('kept', 0)} in main archive.")
    else:
        print(
            f"Would rotate {result.get('rotated', 0)} entries (keep {result.get('kept', 0)}). "
            "Run with --apply to perform."
        )


if __name__ == "__main__":
    main()
