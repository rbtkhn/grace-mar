#!/usr/bin/env python3
"""
Copy the America First KY stress-test brief template to a dated WORK file.

Writes under docs/skill-work/work-politics/america-first-ky/ only.
Does not touch users/, self-evidence, or Record files.

Usage:
  python scripts/scaffold_stress_test_brief.py war-powers-vote
  python scripts/scaffold_stress_test_brief.py ethics-thread --date 2026-03-21
  python scripts/scaffold_stress_test_brief.py my-issue --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_REL = Path("docs/skill-work/work-politics/america-first-ky/stress-test-brief-template.md")
OUT_DIR_REL = Path("docs/skill-work/work-politics/america-first-ky")


def sanitize_slug(raw: str) -> str:
    s = raw.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "issue"


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a dated stress-test brief from the WORK template.",
    )
    parser.add_argument("slug", help="Issue slug (e.g. war-powers-vote)")
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        default=None,
        help="Date for filename (default: today)",
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

    slug = sanitize_slug(args.slug)
    if args.date:
        try:
            d = date.fromisoformat(args.date)
        except ValueError:
            print("--date must be YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        d = date.today()

    template_path = REPO_ROOT / TEMPLATE_REL
    if not template_path.is_file():
        print(f"Template missing: {template_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = REPO_ROOT / OUT_DIR_REL
    out_name = f"stress-test-brief-{d.isoformat()}-{slug}.md"
    out_path = out_dir / out_name

    if out_path.exists() and not args.force:
        print(f"Refusing to overwrite (use --force): {out_path}", file=sys.stderr)
        sys.exit(1)

    body = template_path.read_text(encoding="utf-8")
    # Replace H1 placeholder [Issue] with slug-based title
    first_line = body.split("\n", 1)[0]
    if first_line.startswith("# Stress-test brief — "):
        rest = body.split("\n", 1)[1] if "\n" in body else ""
        title = title_from_slug(slug)
        body = f"# Stress-test brief — {title} — America First Kentucky\n" + rest

    if args.dry_run:
        print(out_path)
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
