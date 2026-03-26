#!/usr/bin/env python3
"""
SELF-KNOWLEDGE vs SELF-LIBRARY: IX-A must not hold domain/corpus dumps.

User-facing copy may say "Library" for SELF-LIBRARY; validators and file paths stay canonical.
See scripts/surface_aliases.py. See docs/boundary-self-knowledge-self-library.md

  python3 scripts/validate_identity_library_boundary.py -u grace-mar
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from identity_library_boundary_rules import collect_ix_a_violations_from_self_md

REPO = Path(__file__).resolve().parents[1]


def collect_identity_library_violations(
    user_dir: Path,
    *,
    repo_root: Path | None = None,
) -> list[str]:
    """
    Return human-readable violation strings for self.md IX-A in user_dir.
    Empty if OK.
    """
    repo_root = repo_root or REPO
    rel = lambda p: str(p.relative_to(repo_root)).replace("\\", "/")
    path = user_dir / "self.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return collect_ix_a_violations_from_self_md(text, rel_path=rel(path))


def collect_self_library_file_warnings(user_dir: Path, repo_root: Path) -> list[str]:
    """Warn when identity file exists but canonical SELF-LIBRARY file is missing."""
    self_p = user_dir / "self.md"
    lib_p = user_dir / "self-library.md"
    if not self_p.is_file() or lib_p.is_file():
        return []
    rel = str(user_dir.relative_to(repo_root)).replace("\\", "/")
    return [
        f"{rel}: self-library.md missing — SELF-LIBRARY surface absent; "
        "LIB→CMC routing requires LIB entries in self-library.md"
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default="grace-mar")
    args = ap.parse_args()
    ud = REPO / "users" / args.user
    viol = collect_identity_library_violations(ud)
    if not viol:
        print("Identity/library boundary scan: OK (no IX-A corpus-style violations).")
        return 0
    for v in viol:
        print(v, file=sys.stderr)
    print(
        f"Identity/library boundary: {len(viol)} violation(s). "
        "See docs/boundary-self-knowledge-self-library.md",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
