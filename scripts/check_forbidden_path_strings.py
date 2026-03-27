#!/usr/bin/env python3
"""
Scan text files for forbidden substrings (cross-fork / cross-repo leakage).

Typical use on an external instance repo (not grace-mar):
  python3 scripts/check_forbidden_path_strings.py --preset isolate-external-instance --under users

Optional docs pass (may need --exclude for files that cite the rule):
  python3 scripts/check_forbidden_path_strings.py --preset isolate-external-instance --under users --under docs \\
      --exclude docs/cross-instance-boundary.md

Exit 1 if any forbidden substring appears in a scanned line.
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git",
    ".github",
    ".cursor",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "companion-self",
}
SCAN_SUFFIXES = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".txt",
    ".mdc",
}

PRESETS: dict[str, list[str]] = {
    "isolate-external-instance": ["users/grace-mar/"],
}


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fail if forbidden path strings appear under scanned paths.")
    p.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: grace-mar root relative to this script).",
    )
    p.add_argument(
        "--forbid",
        action="append",
        default=[],
        metavar="SUBSTRING",
        help="Forbidden substring (repeatable). Case-sensitive.",
    )
    p.add_argument(
        "--preset",
        choices=sorted(PRESETS.keys()),
        help="Add preset forbidden substrings (e.g. isolate-external-instance).",
    )
    p.add_argument(
        "--under",
        action="append",
        dest="under_dirs",
        metavar="REL_DIR",
        help="Relative directory under root to scan (repeatable). Default: users if it exists.",
    )
    p.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="Relative path glob to skip (fnmatch, e.g. docs/policy/*.md). Repeatable.",
    )
    p.add_argument(
        "--exclude-this-script",
        action="store_true",
        help="Exclude scripts/check_forbidden_path_strings.py from scan (for --under scripts).",
    )
    return p.parse_args()


def _should_scan_file(path: Path, root: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix not in SCAN_SUFFIXES:
        return False
    try:
        if path.stat().st_size > 2_000_000:
            return False
    except OSError:
        return False
    if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
        return False
    return True


def _excluded(rel: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, f"**/{pat}"):
            return True
    return False


def _iter_scan_files(root: Path, under: list[Path], exclude_globs: list[str]) -> list[Path]:
    out: list[Path] = []
    for base in under:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not _should_scan_file(path, root):
                continue
            rel = path.relative_to(root).as_posix()
            if _excluded(rel, exclude_globs):
                continue
            out.append(path)
    return sorted(out)


def _scan_file(path: Path, forbidden: list[str]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return hits
    for i, line in enumerate(lines, 1):
        for sub in forbidden:
            if sub in line:
                hits.append((i, line.strip()))
                break
    return hits


def main() -> int:
    args = _parse_args()
    root = args.root.resolve()
    forbidden: list[str] = list(args.forbid)
    if args.preset:
        forbidden.extend(PRESETS[args.preset])
    if not forbidden:
        print("check_forbidden_path_strings: nothing to forbid (--forbid or --preset)", file=sys.stderr)
        return 2

    # dedupe preserve order
    seen: set[str] = set()
    deduped: list[str] = []
    for s in forbidden:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    forbidden = deduped

    exclude = list(args.exclude)
    if args.exclude_this_script:
        exclude.append("scripts/check_forbidden_path_strings.py")

    if args.under_dirs:
        under = [root / d for d in args.under_dirs]
    else:
        default_users = root / "users"
        if default_users.is_dir():
            under = [default_users]
        else:
            print(
                "check_forbidden_path_strings: no --under given and users/ missing; specify --under",
                file=sys.stderr,
            )
            return 2

    files = _iter_scan_files(root, under, exclude)
    if not files:
        print("check_forbidden_path_strings: no files matched scan (check --under paths)", file=sys.stderr)
        return 0

    violations: list[tuple[Path, int, str]] = []
    for path in files:
        rel = path.relative_to(root)
        for line_num, line in _scan_file(path, forbidden):
            violations.append((rel, line_num, line))

    if not violations:
        print(f"check_forbidden_path_strings OK (no forbidden strings under {len(files)} files).")
        return 0

    print("check_forbidden_path_strings FAILED:", file=sys.stderr)
    for sub in forbidden:
        print(f"  forbidden: {sub!r}", file=sys.stderr)
    for rel, line_num, line in violations:
        print(f"  {rel}:{line_num}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
