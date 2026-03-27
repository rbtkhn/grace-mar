#!/usr/bin/env python3
"""Optional YAML frontmatter on users/**/*.md — only files with --- block are checked."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED = frozenset({"core-truth", "operational", "transient", "evidence"})
REQUIRED = frozenset({"category", "intent", "last-reviewed"})
ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)


def parse_yamlish(blob: str) -> dict[str, str]:
    d: dict[str, str] = {}
    for line in blob.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, _, rest = line.partition(":")
        d[k.strip()] = rest.strip().strip('"\'')
    return d


def main() -> int:
    errors: list[str] = []
    users = ROOT / "users"
    if not users.is_dir():
        print("validate-record-boundaries: no users/; skip")
        return 0
    for md in users.rglob("*.md"):
        if "node_modules" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        m = FM.match(text)
        if not m:
            continue
        data = parse_yamlish(m.group(1))
        cat = data.get("category")
        if cat not in ALLOWED:
            errors.append(f"{md.relative_to(ROOT)}: bad category {cat!r}")
        miss = sorted(REQUIRED - set(data.keys()))
        if miss:
            errors.append(f"{md.relative_to(ROOT)}: missing {miss}")
    if errors:
        print("\n".join(errors))
        return 1
    print("validate-record-boundaries: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
