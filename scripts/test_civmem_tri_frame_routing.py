#!/usr/bin/env python3
"""
Smoke test for Grace-Mar tri-frame civ-mem routing (WORK).

Verifies upstream civilization_memory checkout has the expected spine files for a
default entity and that sample per-mind MEM paths exist — mirrors
docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md.

Usage:
  python3 scripts/test_civmem_tri_frame_routing.py
  python3 scripts/test_civmem_tri_frame_routing.py PERSIA
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CIV_ROOT = REPO_ROOT / "research" / "repos" / "civilization_memory" / "content" / "civilizations"


def main() -> int:
    entity = (sys.argv[1] if len(sys.argv) > 1 else "RUSSIA").strip().upper()
    base = CIV_ROOT / entity
    if not base.is_dir():
        print(f"FAIL: missing civilization folder: {base.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    spine = [
        base / f"MEM–RELEVANCE–{entity}.md",
        base / f"CIV–STATE–{entity}.md",
        base / f"CIV–SCHOLAR–{entity}.md",
        base / f"CIV–CORE–{entity}.md",
    ]
    missing = [p for p in spine if not p.is_file()]
    if missing:
        print("FAIL: spine files missing:", file=sys.stderr)
        for p in missing:
            print(f"  {p.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    # Per-mind sample MEMs (must exist on disk) — illustrative routing test
    samples: dict[str, Path] = {
        "mearsheimer_sample (geo / incentives)": base / f"MEM–{entity}–GEO–BLACK–SEA.md",
        "barnes_sample (mechanism / liability)": base / f"MEM–{entity}–LAW–SERFDOM.md",
        "shared_attrition_mem": base / f"MEM–{entity}–WAR–NAPOLEON.md",
    }
    bad = {k: v for k, v in samples.items() if not v.is_file()}
    if bad:
        print("FAIL: sample MEM files missing (adjust names if template differs):", file=sys.stderr)
        for k, v in bad.items():
            print(f"  {k}: {v.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    print(f"OK tri-frame civ-mem routing smoke test — entity={entity}")
    print(f"  spine: MEM–RELEVANCE, CIV–STATE, CIV–SCHOLAR, CIV–CORE")
    for k, v in samples.items():
        print(f"  {k}: {v.name}")
    print(f"  routing doc: docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
