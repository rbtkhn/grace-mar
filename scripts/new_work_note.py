#!/usr/bin/env python3
"""
Create a dated work note from docs/templates/work-note-template.md.

Non-canonical operator capture only. Does not write Record surfaces or recursion-gate.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from capture_scaffold_common import (
    REPO_ROOT,
    resolve_repo_root,
    slugify,
    today_iso,
    write_from_template,
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Scaffold a work note (non-canonical; does not stage the gate)."
    )
    ap.add_argument("--lane", required=True, help="Work lane (e.g. work-strategy)")
    ap.add_argument("--title", required=True, help="Short title for filename and header")
    ap.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "work-notes",
        help="Output directory (default: artifacts/work-notes/)",
    )
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today local)")
    ap.add_argument("--repo-root", type=Path, default=None, help="Repo root (default: inferred)")
    args = ap.parse_args()
    root = resolve_repo_root(args.repo_root)
    d = args.date or today_iso()
    slug = slugify(args.title)
    fn = f"{d}-{slug}.md"
    dest = write_from_template(
        template_rel="work-note-template.md",
        output_dir=args.output,
        repo_root=root,
        filename=fn,
        fields=[
            ("Date", d),
            ("Lane", args.lane),
            ("Title", args.title),
        ],
    )
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
