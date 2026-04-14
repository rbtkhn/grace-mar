#!/usr/bin/env python3
"""
Create a pre-gate candidate draft from docs/templates/candidate-draft-template.md.

Human draft only — does not write recursion-gate.md or merge Record surfaces.
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
        description="Scaffold a candidate draft (non-canonical; does not stage the gate)."
    )
    ap.add_argument("--lane", required=True)
    ap.add_argument(
        "--target-surface",
        required=True,
        help="e.g. SELF, SKILLS, SELF-LIBRARY, EVIDENCE",
    )
    ap.add_argument("--title", required=True)
    ap.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "candidate-drafts",
        help="Output directory (default: artifacts/candidate-drafts/)",
    )
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--repo-root", type=Path, default=None)
    args = ap.parse_args()
    root = resolve_repo_root(args.repo_root)
    d = args.date or today_iso()
    slug = slugify(args.title)
    fn = f"{d}-{slug}.md"
    dest = write_from_template(
        template_rel="candidate-draft-template.md",
        output_dir=args.output,
        repo_root=root,
        filename=fn,
        fields=[
            ("Date", d),
            ("Lane", args.lane),
            ("Target surface", args.target_surface),
            ("Title", args.title),
        ],
    )
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
