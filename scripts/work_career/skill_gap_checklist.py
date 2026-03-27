#!/usr/bin/env python3
"""
Read-only: scan skill-demo-worksheet.md for markdown links (...)(path) and verify paths exist from repo root.

Paths in the worksheet may be relative to the worksheet file (../...). Resolves against repo root.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"\]\(([^)]+)\)")


def resolve_link(worksheet_dir: Path, target: str) -> Path | None:
    t = target.strip()
    if t.startswith(("http://", "https://", "mailto:")):
        return None
    p = (worksheet_dir / t).resolve()
    try:
        p.relative_to(ROOT)
    except ValueError:
        return None
    return p


def main() -> int:
    parser = argparse.ArgumentParser(description="Check worksheet markdown links exist on disk.")
    parser.add_argument(
        "--worksheet",
        type=Path,
        default=ROOT / "docs/skill-work/work-career/skill-demo-worksheet.md",
    )
    args = parser.parse_args()

    if not args.worksheet.is_file():
        print(f"Missing worksheet: {args.worksheet}", file=sys.stderr)
        return 2

    text = args.worksheet.read_text(encoding="utf-8")
    base = args.worksheet.parent
    missing = []
    skipped = []
    ok = []

    for m in LINK_RE.finditer(text):
        raw = m.group(1).strip()
        if raw.startswith("#"):
            continue
        if "://" in raw.split("/")[0]:
            skipped.append(raw)
            continue
        path = resolve_link(base, raw)
        if path is None:
            skipped.append(raw)
            continue
        try:
            rel = str(path.relative_to(ROOT))
        except ValueError:
            skipped.append(raw)
            continue
        if path.is_file() or path.is_dir():
            ok.append(rel)
        else:
            missing.append((raw, rel))

    for r in ok:
        print(f"ok\t{r}")
    for raw, resolved in missing:
        print(f"MISSING\t{raw}\t-> {resolved}")
    print(f"# ok={len(ok)} missing={len(missing)} skipped_url={len(skipped)}", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
