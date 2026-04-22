#!/usr/bin/env python3
"""Fail if manifest-listed Ritter primaries lack refined page files or transcript backlinks."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
RITTER = NOTEBOOK / "experts" / "ritter"
MANIFEST_PATH = RITTER / "ritter-pages-manifest.yaml"
TRANSCRIPT_PATH = RITTER / "transcript.md"


def main() -> int:
    if yaml is None:
        print("verify_ritter_refined_pages: need PyYAML", file=sys.stderr)
        return 1
    if not MANIFEST_PATH.is_file():
        print(f"verify_ritter_refined_pages: missing {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    pages = manifest.get("pages") or []
    transcript = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    errors: list[str] = []

    for entry in pages:
        raw_rel = entry.get("raw_input_relative", "")
        page_fn = entry.get("page_filename", "")
        raw_path = NOTEBOOK / raw_rel
        page_path = RITTER / page_fn
        if not raw_path.is_file():
            errors.append(f"missing raw-input: {raw_rel}")
        if not page_path.is_file():
            errors.append(f"missing refined page: {page_fn}")
        if page_fn and page_fn not in transcript:
            errors.append(f"transcript.md missing backlink for {page_fn}")

    if errors:
        print("verify_ritter_refined_pages: FAILED", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("verify_ritter_refined_pages: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
