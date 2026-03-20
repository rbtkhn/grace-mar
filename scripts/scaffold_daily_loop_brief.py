#!/usr/bin/env python3
"""
Copy the America First KY daily-loop brief template to a dated WORK file.

Writes under docs/skill-work/work-politics/america-first-ky/ only.
Does not touch users/, self-evidence, or Record files.

Usage:
  python scripts/scaffold_daily_loop_brief.py
  python scripts/scaffold_daily_loop_brief.py morning
  python scripts/scaffold_daily_loop_brief.py war-powers-scan --date 2026-03-21
  python scripts/scaffold_daily_loop_brief.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_REL = Path(
    "docs/skill-work/work-politics/america-first-ky/templates/daily-loop-brief.md"
)
OUT_DIR_REL = Path("docs/skill-work/work-politics/america-first-ky")


def sanitize_slug(raw: str) -> str:
    s = raw.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "cycle"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a dated daily-loop brief from the WORK template.",
    )
    parser.add_argument(
        "slug",
        nargs="?",
        default="",
        help="Optional slug for filename (e.g. morning, war-powers-scan). Omit for date-only name.",
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        default=None,
        help="Date for filename and Cycle line (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print target path and exit without writing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite if the output file already exists",
    )
    args = parser.parse_args()

    if args.date:
        try:
            d = date.fromisoformat(args.date)
        except ValueError:
            print("--date must be YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        d = date.today()

    slug = sanitize_slug(args.slug) if args.slug.strip() else ""

    template_path = REPO_ROOT / TEMPLATE_REL
    if not template_path.is_file():
        print(f"Template missing: {template_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = REPO_ROOT / OUT_DIR_REL
    if slug:
        out_name = f"daily-loop-brief-{d.isoformat()}-{slug}.md"
    else:
        out_name = f"daily-loop-brief-{d.isoformat()}.md"
    out_path = out_dir / out_name

    if out_path.exists() and not args.force:
        print(f"Refusing to overwrite (use --force): {out_path}", file=sys.stderr)
        sys.exit(1)

    body = template_path.read_text(encoding="utf-8")
    # Pre-fill Cycle line with date (operator still fills time / timezone). Trailing two spaces = markdown line break.
    cycle_line = f"**Cycle:** {d.isoformat()} — [time / local — fill in]  \n"
    body, n = re.subn(
        r"^\*\*Cycle:\*\* \[Date \+ time UTC or local\][ \t]*\r?\n",
        cycle_line,
        body,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        print("Warning: Cycle placeholder not found; copied template unchanged.", file=sys.stderr)

    if args.dry_run:
        print(out_path)
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
