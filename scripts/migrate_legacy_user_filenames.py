#!/usr/bin/env python3
"""
One-time migration: rename legacy per-user filenames to canonical lowercase paths.

Legacy (wrong)          -> Canonical (authoritative)
  SELF.md               -> self.md
  EVIDENCE.md           -> self-evidence.md
  ARCHIVE.md            -> self-archive.md
  SKILLS.md             -> skills.md
  skills.md             -> self-skills.md (capability index; if self-skills.md absent)
  memory.md             -> self-memory.md (self-memory; if self-memory.md absent)
  PENDING-REVIEW.md     -> recursion-gate.md (only if recursion-gate.md absent;
                          if both exist, abort unless --merge-pending-review)

Default: --dry-run (print planned renames). Use --apply to perform.

See docs/canonical-paths.md.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (legacy_name, canonical_name) — applied only if legacy exists and canonical missing.
RENAMES: list[tuple[str, str]] = [
    ("SELF.md", "self.md"),
    ("EVIDENCE.md", "self-evidence.md"),
    ("ARCHIVE.md", "self-archive.md"),
    ("SKILLS.md", "skills.md"),
    ("skills.md", "self-skills.md"),
    ("memory.md", "self-memory.md"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate legacy user filenames to canonical paths.")
    parser.add_argument("--user", required=True, help="User id under users/")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform renames (default without this flag: dry-run only)",
    )
    parser.add_argument(
        "--merge-pending-review",
        action="store_true",
        help="If PENDING-REVIEW.md and recursion-gate.md both exist, append pending to gate then remove pending",
    )
    args = parser.parse_args()
    dry = not args.apply
    user_dir = REPO_ROOT / "users" / args.user
    if not user_dir.is_dir():
        print(f"error: {user_dir} is not a directory", file=sys.stderr)
        return 1

    actions: list[str] = []
    for legacy, canonical in RENAMES:
        lp, cp = user_dir / legacy, user_dir / canonical
        if not lp.exists():
            continue
        if cp.exists():
            try:
                if lp.samefile(cp):
                    # Case-insensitive FS: SELF.md and self.md are the same path
                    continue
            except OSError:
                pass
            actions.append(f"SKIP {legacy} -> {canonical}: target exists (resolve manually)")
            continue
        actions.append(f"RENAME {legacy} -> {canonical}")
        if not dry:
            lp.rename(cp)

    pending = user_dir / "PENDING-REVIEW.md"
    gate = user_dir / "recursion-gate.md"
    if pending.exists():
        if not gate.exists():
            actions.append("RENAME PENDING-REVIEW.md -> recursion-gate.md")
            if not dry:
                pending.rename(gate)
        elif args.merge_pending_review:
            actions.append("MERGE PENDING-REVIEW.md into recursion-gate.md (append), delete pending")
            if not dry:
                sep = "\n\n<!-- merged from PENDING-REVIEW.md -->\n\n"
                gate.write_text(gate.read_text(encoding="utf-8") + sep + pending.read_text(encoding="utf-8"), encoding="utf-8")
                pending.unlink()
        else:
            actions.append(
                "SKIP PENDING-REVIEW.md: recursion-gate.md exists (use --merge-pending-review to append)"
            )

    if not actions:
        print("No legacy files found; nothing to do.")
        return 0

    mode = "dry-run" if dry else "APPLIED"
    print(f"[{mode}] users/{args.user}/")
    for a in actions:
        print(f"  {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
