#!/usr/bin/env python3
"""
Create an evidence stub from docs/templates/evidence-stub-template.md.

Pre-canonical capture only — not governed EVIDENCE. Does not write recursion-gate.md.
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
        description="Scaffold an evidence stub (non-canonical; not governed EVIDENCE yet)."
    )
    ap.add_argument("--source", required=True, help='e.g. "operator note"')
    ap.add_argument("--type", required=True, help="e.g. analysis, session, artifact")
    ap.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "evidence-stubs",
        help="Output directory (default: artifacts/evidence-stubs/)",
    )
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--status", default="unreviewed", help="Stub status line (default: unreviewed)")
    ap.add_argument("--title", default="", help="Optional short label for filename (default: type-source slug)")
    ap.add_argument("--repo-root", type=Path, default=None, help="Repo root (default: inferred)")
    args = ap.parse_args()
    root = resolve_repo_root(args.repo_root)
    d = args.date or today_iso()
    label = args.title.strip() or f"{args.type}-{args.source}"
    slug = slugify(label)
    fn = f"{d}-{slug}.md"
    dest = write_from_template(
        template_rel="evidence-stub-template.md",
        output_dir=args.output,
        repo_root=root,
        filename=fn,
        fields=[
            ("Date", d),
            ("Source", args.source),
            ("Type", args.type),
            ("Status", args.status),
        ],
    )
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
