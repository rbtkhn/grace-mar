#!/usr/bin/env python3
"""
Create a new work domain following the uppercase DOMAIN.md convention.

Usage:
  python3 scripts/create-domain.py dev
  python3 scripts/create-domain.py politics
  python3 scripts/create-domain.py jiang

Creates:
  work-<lowercase>/<UPPERCASE>.md   (from _template/DOMAIN.md)
  work-<lowercase>/README.md       (minimal, if missing)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _domain_surface_links import (
    assert_domain_surface_links_rebased,
    rebase_domain_surface_markdown,
)

REPO_ROOT = _SCRIPT_DIR.parent
TEMPLATE_PATH = REPO_ROOT / "_template" / "DOMAIN.md"


def _validate_token(domain_raw: str) -> tuple[str, str, str] | None:
    """Return (lower, UPPER, Title) or None if invalid."""
    raw = domain_raw.strip()
    if not raw:
        return None
    if not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", raw):
        print(
            "Error: domain must be a single slug (letters, digits, optional internal hyphen).",
            file=sys.stderr,
        )
        return None
    domain_lower = raw.lower()
    domain_upper = domain_lower.upper()
    domain_title = raw.replace("-", " ").title()
    return domain_lower, domain_upper, domain_title


def create_domain(domain_raw: str) -> bool:
    parsed = _validate_token(domain_raw)
    if parsed is None:
        return False
    domain_lower, domain_upper, domain_title = parsed

    dir_path = REPO_ROOT / f"work-{domain_lower}"
    file_path = dir_path / f"{domain_upper}.md"

    if not TEMPLATE_PATH.is_file():
        print(f"Error: template not found: {TEMPLATE_PATH}", file=sys.stderr)
        return False

    if file_path.is_file():
        print(f"Error: already exists: {file_path}", file=sys.stderr)
        return False

    if not dir_path.is_dir():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path.relative_to(REPO_ROOT)}")

    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    content = content.replace("{{DOMAIN}}", domain_upper)
    content = content.replace("{{DOMAIN_LOWER}}", domain_lower)
    content = content.replace("{{DOMAIN_TITLE}}", domain_title)
    content = rebase_domain_surface_markdown(content, file_path, REPO_ROOT)
    assert_domain_surface_links_rebased(content, file_path)

    file_path.write_text(content, encoding="utf-8")
    print(f"Created: {file_path.relative_to(REPO_ROOT)}")

    readme = dir_path / "README.md"
    if not readme.is_file():
        readme.write_text(
            f"# work-{domain_lower}\n\n"
            f"Canonical wisdom surface: [`{domain_upper}.md`]({domain_upper}.md)\n",
            encoding="utf-8",
        )
        print(f"Created: {readme.relative_to(REPO_ROOT)}")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create work-<domain>/<DOMAIN>.md from _template/DOMAIN.md"
    )
    parser.add_argument("domain", help="e.g. dev, politics, jiang, strategy")
    args = parser.parse_args()
    return 0 if create_domain(args.domain) else 1


if __name__ == "__main__":
    raise SystemExit(main())
