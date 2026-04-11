#!/usr/bin/env python3
"""Compare URL coverage: work-strategy-sources.md vs authorized-sources.yaml.

Read-only. Exits 0 always unless --strict and counts mismatch.

Usage:
  python3 scripts/sync_strategy_sources.py
  python3 scripts/sync_strategy_sources.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_PATH = REPO_ROOT / "docs/skill-work/work-strategy/work-strategy-sources.md"
YAML_PATH = REPO_ROOT / "docs/skill-work/work-strategy/authorized-sources.yaml"

_URL_RE = re.compile(r"https?://[^\s\)|]+")


def count_urls(text: str) -> int:
    return len(set(_URL_RE.findall(text)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="Exit 1 if URL counts differ")
    args = ap.parse_args()

    md_urls = 0
    if MD_PATH.is_file():
        md_urls = count_urls(MD_PATH.read_text(encoding="utf-8"))

    yaml_urls = 0
    if YAML_PATH.is_file():
        try:
            import yaml  # type: ignore[import-untyped]

            data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
            for s in data.get("sources", []):
                u = s.get("url")
                if u:
                    yaml_urls += 1
        except ImportError:
            print("warn: PyYAML not installed; skipping yaml count", file=sys.stderr)

    print(f"work-strategy-sources.md distinct URL-like strings: {md_urls}")
    print(f"authorized-sources.yaml entries with url: {yaml_urls}")
    print("hint: migrate incrementally; goal is parity with markdown table rows.")
    if args.strict and md_urls and yaml_urls and md_urls != yaml_urls:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
