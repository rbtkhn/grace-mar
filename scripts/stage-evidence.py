#!/usr/bin/env python3
"""
Starter staging: copy a text file into a JSON stub under prepared-context/.

Prepared context is not governed state. See docs/prepared-context-doctrine.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREPARED_DIR = REPO_ROOT / "prepared-context"


def stage_text_file(source: Path) -> Path:
    PREPARED_DIR.mkdir(parents=True, exist_ok=True)
    out = PREPARED_DIR / f"{source.stem}.prepared.json"
    text = source.read_text(encoding="utf-8", errors="replace")
    try:
        rel_src = str(source.resolve().relative_to(REPO_ROOT))
    except ValueError:
        rel_src = str(source.resolve())
    payload = {
        "source_path": rel_src,
        "prepared_type": "plain_text",
        "content": text,
        "notes": [
            "Starter staging artifact",
            "Prepared context is not governed state",
        ],
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage a text file into prepared-context/*.prepared.json")
    parser.add_argument("source", type=Path, help="Path to evidence file (often under evidence/)")
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        print("Not a file:", source, file=sys.stderr)
        return 1
    try:
        source.relative_to(REPO_ROOT)
    except ValueError:
        print("Source must be inside repository root:", REPO_ROOT, file=sys.stderr)
        return 1

    staged = stage_text_file(source)
    print(staged.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
