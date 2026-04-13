#!/usr/bin/env python3
"""
Smoke test for Grace-Mar tri-frame civ-mem routing (WORK).

Verifies upstream civilization_memory checkout has the expected spine files for a
default entity and that sample per-mind MEM paths exist — mirrors
docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md.

Usage:
  python3 scripts/test_civmem_tri_frame_routing.py
  python3 scripts/test_civmem_tri_frame_routing.py RUSSIA
  python3 scripts/test_civmem_tri_frame_routing.py ROME
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CIV_ROOT = REPO_ROOT / "research" / "repos" / "civilization_memory" / "content" / "civilizations"


def _full_spine(entity: str, base: Path) -> list[Path]:
    return [
        base / f"MEM–RELEVANCE–{entity}.md",
        base / f"CIV–STATE–{entity}.md",
        base / f"CIV–SCHOLAR–{entity}.md",
        base / f"CIV–CORE–{entity}.md",
    ]


def run_russia() -> int:
    """Default entity: full spine + RUSSIA-shaped sample MEM names."""
    entity = "RUSSIA"
    base = CIV_ROOT / entity
    if not base.is_dir():
        print(f"FAIL: missing civilization folder: {base.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    spine = _full_spine(entity, base)
    missing = [p for p in spine if not p.is_file()]
    if missing:
        print("FAIL: spine files missing:", file=sys.stderr)
        for p in missing:
            print(f"  {p.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

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


def run_rome() -> int:
    """
    ROME at current upstream pin may omit MEM–RELEVANCE–ROME.md; assert partial spine +
    real Barnes / Mearsheimer / war MEM paths for Trump–Leo drill receipts.
    """
    entity = "ROME"
    base = CIV_ROOT / entity
    if not base.is_dir():
        print(f"FAIL: missing civilization folder: {base.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    relevance = base / f"MEM–RELEVANCE–{entity}.md"
    if relevance.is_file():
        spine = _full_spine(entity, base)
        note = "full spine including MEM–RELEVANCE"
    else:
        spine = [
            base / f"CIV–STATE–{entity}.md",
            base / f"CIV–SCHOLAR–{entity}.md",
            base / f"CIV–CORE–{entity}.md",
        ]
        note = "partial spine (no MEM–RELEVANCE–ROME.md — manual MEM picks; see TRUMP-LEO-CIV-MEM-BARNES-DRILL.md)"

    missing = [p for p in spine if not p.is_file()]
    if missing:
        print("FAIL: ROME spine files missing:", file=sys.stderr)
        for p in missing:
            print(f"  {p.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    samples: dict[str, Path] = {
        "mearsheimer_sample (geo / incentives)": base / "MEM–ROME–GEO–MEDITERRANEAN–SEA.md",
        "barnes_sample (mechanism / liability / law)": base / "MEM–ROME–LAW–CITIZENSHIP.md",
        "barnes_alt (papacy / legitimacy register)": base / "MEM–ROME–PAPACY.md",
        "shared_attrition_mem": base / "MEM–ROME–WAR–ACTIUM.md",
    }
    bad = {k: v for k, v in samples.items() if not v.is_file()}
    if bad:
        print("FAIL: ROME sample MEM files missing:", file=sys.stderr)
        for k, v in bad.items():
            print(f"  {k}: {v.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    print(f"OK tri-frame civ-mem routing smoke test — entity={entity} ({note})")
    for p in spine:
        print(f"  spine: {p.name}")
    for k, v in samples.items():
        print(f"  {k}: {v.name}")
    print("  drill doc: docs/skill-work/work-strategy/strategy-notebook/TRUMP-LEO-CIV-MEM-BARNES-DRILL.md")
    return 0


def main() -> int:
    if len(sys.argv) > 1:
        ent = sys.argv[1].strip().upper()
        if ent == "ROME":
            return run_rome()
        if ent == "RUSSIA":
            return run_russia()
        print(
            "FAIL: unsupported entity (use RUSSIA or ROME, or no argument for both).",
            file=sys.stderr,
        )
        return 1
    r = run_russia()
    if r != 0:
        return r
    print("")
    return run_rome()


if __name__ == "__main__":
    sys.exit(main())
