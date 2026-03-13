#!/usr/bin/env python3
"""
Check the repo for deprecated COG-EM naming.

Keeps the rule in one place so CI and local hooks enforce the same scan.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", ".cursor", "node_modules", "__pycache__"}
SKIP_FILES = {"check_deprecated_naming.py"}
SCAN_SUFFIXES = {".md", ".py", ".yml", ".yaml"}
PATTERN = re.compile(r"cog-em|COG-EM-CORE", re.IGNORECASE)


def _should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_SUFFIXES:
        return False
    if path.name in SKIP_FILES:
        return False
    return not any(part in SKIP_DIRS for part in path.parts)


def _scan_file(path: Path) -> list[tuple[int, str]]:
    matches: list[tuple[int, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return matches

    for line_num, line in enumerate(lines, 1):
        if PATTERN.search(line):
            matches.append((line_num, line.strip()))
    return matches


def main() -> int:
    violations: list[tuple[Path, int, str]] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or not _should_scan(path):
            continue
        rel = path.relative_to(REPO_ROOT)
        for line_num, line in _scan_file(path):
            violations.append((rel, line_num, line))

    if not violations:
        print("Naming check passed.")
        return 0

    print("Deprecated naming found. Use GRACE-MAR / GRACE-MAR-CORE instead.", file=sys.stderr)
    for path, line_num, line in violations:
        print(f"  {path}:{line_num}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
