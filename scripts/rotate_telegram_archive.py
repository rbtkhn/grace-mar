#!/usr/bin/env python3
"""
Rotate the gated approved log when it exceeds size or entry count.

**Primary:** `self-evidence.md` § **## VIII. GATED APPROVED LOG (SELF-ARCHIVE)** (merge script appends here).

**Legacy:** If § VIII is absent, falls back to standalone `self-archive.md` (pre-migration instances).

Rotated chunks go to `archives/SELF-ARCHIVE-YYYY-MM.md` (or `.md.gz` with ``--compress``).

**Gzip:** Tools that read monthly archives must open ``.md.gz`` (e.g. ``gzip.open``)
or decompress first.

Threshold defaults: ``config/fork-config.json`` (``archive_*`` keys).

Usage:
    python scripts/rotate_telegram_archive.py          # Dry run (report only)
    python scripts/rotate_telegram_archive.py --apply  # Perform rotation
    python scripts/rotate_telegram_archive.py --apply --compress
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

GATED_LOG_SECTION = "## VIII. GATED APPROVED LOG (SELF-ARCHIVE)"
_END_FILE = re.compile(r"(?m)^END OF FILE.*$")


def parse_archive(content: str) -> tuple[str, list[str]]:
    """Split archive into header and list of entry blocks."""
    parts = content.split("\n---\n\n", 1)
    if len(parts) == 1:
        return "", []
    header = parts[0] + "\n---\n\n"
    body = parts[1]
    blocks = [b.strip() for b in body.split("\n\n") if b.strip() and b.strip().startswith("**[")]
    return header, blocks


def get_entry_ym(block: str) -> str | None:
    """Extract YYYY-MM from first line of block."""
    m = re.match(r"\*\*\[(\d{4}-\d{2})-\d{2}", block)
    return m.group(1) if m else None


def _rotate_embedded_gated_log(
    evidence_path: Path,
    archives_dir: Path,
    apply: bool,
    max_bytes: int,
    max_entries: int,
    keep_recent: int,
    compress: bool,
) -> dict:
    content = evidence_path.read_text(encoding="utf-8")
    if GATED_LOG_SECTION not in content:
        return {"ok": False, "rotated": 0, "kept": 0, "reason": "no_gated_section"}

    m_end = _END_FILE.search(content)
    viii = content.index(GATED_LOG_SECTION)
    end_idx = m_end.start() if m_end else len(content)
    prefix = content[:viii]
    gated_region = content[viii:end_idx]
    suffix = content[end_idx:] if m_end else ""

    size = len(gated_region.encode("utf-8"))
    header, blocks = parse_archive(gated_region)
    n = len(blocks)
    if n <= max_entries and size <= max_bytes:
        return {
            "ok": True,
            "rotated": 0,
            "kept": n,
            "size_bytes": size,
            "reason": "within_limits",
            "source": "self-evidence",
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
            header_ym = f"# SELF-ARCHIVE — {ym}\n\n> Rotated from self-evidence § VIII. Append-only.\n\n---\n\n"
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
        new_gated = header + new_body
        new_full = prefix + new_gated.rstrip() + ("\n\n" if suffix.strip() else "\n") + suffix.lstrip("\n")
        evidence_path.write_text(new_full, encoding="utf-8")

    return {
        "ok": True,
        "rotated": len(rotated),
        "kept": len(kept),
        "size_bytes": size,
        "applied": apply,
        "compress": compress,
        "source": "self-evidence",
    }


def _rotate_legacy_standalone(
    archive_path: Path,
    archives_dir: Path,
    apply: bool,
    max_bytes: int,
    max_entries: int,
    keep_recent: int,
    compress: bool,
) -> dict:
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
            "source": "self-archive.md",
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
        "source": "self-archive.md",
    }


def rotate_archive(
    user_id: str,
    apply: bool,
    max_bytes: int = MAX_BYTES,
    max_entries: int = MAX_ENTRIES,
    keep_recent: int = KEEP_RECENT,
    compress: bool = False,
) -> dict:
    ud = REPO_ROOT / "users" / user_id
    evidence_path = ud / "self-evidence.md"
    archive_path = ud / "self-archive.md"
    archives_dir = ud / "archives"

    if evidence_path.exists():
        ev_text = evidence_path.read_text(encoding="utf-8")
        if GATED_LOG_SECTION in ev_text:
            return _rotate_embedded_gated_log(
                evidence_path,
                archives_dir,
                apply,
                max_bytes,
                max_entries,
                keep_recent,
                compress,
            )

    if archive_path.exists():
        txt = archive_path.read_text(encoding="utf-8").strip()
        if txt.startswith("# self-archive.md (deprecated)"):
            return {"ok": True, "rotated": 0, "kept": 0, "reason": "archive_stub_only"}
        if "**[" in txt or txt.startswith("# SELF-ARCHIVE"):
            return _rotate_legacy_standalone(
                archive_path,
                archives_dir,
                apply,
                max_bytes,
                max_entries,
                keep_recent,
                compress,
            )

    return {"ok": True, "rotated": 0, "kept": 0, "reason": "archive_not_found"}


def main() -> None:
    cfg = load_fork_config()
    parser = argparse.ArgumentParser(description="Rotate gated approved log (self-evidence § VIII or legacy self-archive)")
    parser.add_argument("--apply", "-a", action="store_true", help="Perform rotation (default: dry run)")
    parser.add_argument("--user", "-u", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=None,
        help=f"Size threshold in bytes (default: config or {MAX_BYTES})",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=None,
        help="Entry-count threshold (default: config archive_rotation_trigger_entries / archive_max_entries or "
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
        help="Write rotated monthly chunks as .md.gz under archives/",
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
        print("No gated log (§ VIII) or legacy archive found, nothing to do.")
        return
    if result.get("reason") == "archive_stub_only":
        print("self-archive.md is a deprecation stub; gated log is in self-evidence § VIII.")
        return
    if result.get("reason") == "within_limits":
        src = result.get("source", "archive")
        print(
            f"{src} OK: {result.get('kept', 0)} entries, {result.get('size_bytes', 0):,} bytes "
            f"(limit {max_entries} / {max_bytes:,})"
        )
        return
    if args.apply:
        print(
            f"Rotated {result.get('rotated', 0)} entries from {result.get('source', 'archive')}. "
            f"Kept {result.get('kept', 0)}."
        )
    else:
        print(
            f"Would rotate {result.get('rotated', 0)} entries (keep {result.get('kept', 0)}). "
            "Run with --apply to perform."
        )


if __name__ == "__main__":
    main()
