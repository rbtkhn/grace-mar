#!/usr/bin/env python3
"""Warn on unknown History Notebook chapter ids cited in strategy-notebook.

Scans markdown under docs/skill-work/work-strategy/strategy-notebook/ for tokens
matching ``hn-`` + slug segments (same convention as book-architecture.yaml).
Compares against ``chapters[].id`` in history-notebook/book-architecture.yaml.

Exit 0 always unless --strict (then exit 1 if any unknown id).

WORK-only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
HN_ARCH = REPO / "docs/skill-work/work-strategy/history-notebook/book-architecture.yaml"
STRATEGY_NB = REPO / "docs/skill-work/work-strategy/strategy-notebook"

# hn-i-v1-04, hn-app-method, hn-v-america-hegemonic
RE_HN_ID = re.compile(r"\b(hn(?:-[a-z0-9]+)+)\b")


def load_valid_ids(path: Path) -> set[str]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    chapters = data.get("chapters") or []
    return {c["id"] for c in chapters if isinstance(c, dict) and "id" in c}


def iter_markdown_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.md"):
        if p.is_file():
            out.append(p)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any unknown hn-* token is found",
    )
    args = ap.parse_args()

    if not HN_ARCH.exists():
        print(f"ERROR: missing {HN_ARCH}", file=sys.stderr)
        return 1

    valid = load_valid_ids(HN_ARCH)
    unknown: list[tuple[str, Path, int]] = []

    for path in iter_markdown_files(STRATEGY_NB):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"WARN: could not read {path}: {e}", file=sys.stderr)
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for m in RE_HN_ID.finditer(line):
                token = m.group(1)
                if token not in valid:
                    unknown.append((token, path, line_no))

    if not unknown:
        print("ok: no unknown hn-* chapter ids in strategy-notebook")
        return 0

    print("Unknown hn-* tokens (not in book-architecture.yaml chapters):", file=sys.stderr)
    for token, path, line_no in unknown:
        rel = path.relative_to(REPO)
        print(f"  {token} — {rel}:{line_no}", file=sys.stderr)
    if args.strict:
        return 1
    print(
        f"\n({len(unknown)} finding(s); exit 0 — use --strict to fail CI)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
