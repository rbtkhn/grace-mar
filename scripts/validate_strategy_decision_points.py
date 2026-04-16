#!/usr/bin/env python3
"""Validate work-strategy decision point files (light checks).

WORK only. Exits 0 if all checks pass, 1 otherwise.

Usage:
  python3 scripts/validate_strategy_decision_points.py
  python3 scripts/validate_strategy_decision_points.py --root docs/skill-work/work-strategy/decision-points
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "## Decision point",
    "## Perspectives",
    "## Options",
    "## Recommendation",
    "## Downstream lane impact",
)

FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][-a-z0-9]*\.md$")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    name = path.name
    if name == "README.md":
        return errors
    if "template" in name.lower():
        return errors
    if not FILENAME_RE.match(name):
        errors.append(f"{path}: filename must match YYYY-MM-DD-slug.md (lowercase slug)")
    text = path.read_text(encoding="utf-8", errors="replace")
    if "example-stub" in name and "Replace" in text:
        return errors
    for h in REQUIRED_HEADINGS:
        if h not in text:
            errors.append(f"{path}: missing heading {h!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("docs/skill-work/work-strategy/decision-points"),
        help="Directory containing decision point markdown files",
    )
    args = parser.parse_args()
    root = args.root
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1
    all_errors: list[str] = []
    for p in sorted(root.glob("*.md")):
        if p.name == "README.md":
            continue
        all_errors.extend(validate_file(p))
    for e in all_errors:
        print(e, file=sys.stderr)
    if all_errors:
        return 1
    print(f"ok: {root} — {len(list(root.glob('*.md'))) - 1} decision file(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
