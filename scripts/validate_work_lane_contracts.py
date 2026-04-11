#!/usr/bin/env python3
"""Lightweight check: work-layer hardening files exist (lane contract sanity).

Exits 0 if all required paths exist.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    REPO_ROOT / "docs/skill-work/WORK-LAYER-HARDENING-ROADMAP.md",
    REPO_ROOT / "docs/skill-work/work-lane-contract.md",
    REPO_ROOT / "docs/skill-work/work-strategy/promotion-ladder.md",
    REPO_ROOT / "docs/skill-work/work-strategy/authorized-sources.yaml",
    REPO_ROOT / "docs/skill-work/work-template/lane-contract.template.md",
    REPO_ROOT / "schemas/work_strategy/authorized_sources.schema.json",
]


def main() -> int:
    missing = [p for p in REQUIRED if not p.is_file()]
    for p in missing:
        print(f"missing: {p.relative_to(REPO_ROOT)}", file=sys.stderr)
    if missing:
        return 1
    print(f"ok: {len(REQUIRED)} contract paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
