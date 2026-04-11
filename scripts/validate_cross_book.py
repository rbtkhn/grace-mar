#!/usr/bin/env python3
"""Validate cross-book coverage: Predictive History <-> History Notebook.

Reads:
  - HN cross-book-map.yaml   (sole SSOT for PH <-> HN links)
  - PH thesis-map.yaml       (8 theses — validates thesis_id refs)
  - PH concepts.yaml         (20 concepts — validates concept_id refs)
  - HN book-architecture.yaml (22 chapters — validates hn_chapter refs)

Reports:
  - Thesis coverage: X/8 with at least one HN chapter
  - Concept coverage: X/20 with at least one HN chapter
  - Coverage breakdown by status (full / partial / stub)
  - Orphan HN chapters: not referenced by any thesis or concept
  - Missing links: theses/concepts with no HN chapter
  - Dangling refs: chapter IDs in the map that don't exist in architecture,
    or thesis/concept IDs that don't exist in PH metadata

Exit code: 0 = full coverage (8/8, 20/20), 1 = gaps remain.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent

HN_DIR = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook"
PH_DIR = REPO / "research" / "external" / "work-jiang" / "metadata"

CROSS_MAP = HN_DIR / "cross-book-map.yaml"
HN_ARCH = HN_DIR / "book-architecture.yaml"
PH_THESES = PH_DIR / "thesis-map.yaml"
PH_CONCEPTS = PH_DIR / "concepts.yaml"


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress detailed output; exit code only")
    args = parser.parse_args()

    for p in (CROSS_MAP, HN_ARCH, PH_THESES, PH_CONCEPTS):
        if not p.exists():
            print(f"ERROR: missing file: {p}", file=sys.stderr)
            return 1

    cross = load_yaml(CROSS_MAP)
    arch = load_yaml(HN_ARCH)
    ph_thesis_data = load_yaml(PH_THESES)
    ph_concept_data = load_yaml(PH_CONCEPTS)

    hn_chapter_ids = {ch["id"] for ch in arch.get("chapters", [])}

    ph_thesis_ids = set()
    for sc in ph_thesis_data.get("thesis", {}).get("subclaims", []):
        ph_thesis_ids.add(sc["id"])

    ph_concept_ids = {c["concept_id"] for c in ph_concept_data.get("concepts", [])}

    errors: list[str] = []
    warnings: list[str] = []

    referenced_chapters: set[str] = set()

    # --- Theses ---
    map_theses = cross.get("theses", [])
    thesis_covered = 0
    thesis_stub = 0
    thesis_partial = 0
    thesis_full = 0
    thesis_missing: list[str] = []

    map_thesis_ids = set()
    for entry in map_theses:
        tid = entry["thesis_id"]
        map_thesis_ids.add(tid)

        if tid not in ph_thesis_ids:
            errors.append(f"Dangling thesis_id in cross-book-map: {tid} (not in PH thesis-map.yaml)")

        chapters = entry.get("hn_chapters", [])
        coverage = entry.get("coverage", "stub")

        for ch in chapters:
            if ch not in hn_chapter_ids:
                errors.append(f"Dangling chapter ref in thesis {tid}: {ch} (not in HN book-architecture.yaml)")
            referenced_chapters.add(ch)

        if chapters:
            thesis_covered += 1
        else:
            thesis_missing.append(tid)

        if coverage == "full":
            thesis_full += 1
        elif coverage == "partial":
            thesis_partial += 1
        else:
            thesis_stub += 1

    for tid in ph_thesis_ids - map_thesis_ids:
        errors.append(f"PH thesis {tid} not listed in cross-book-map.yaml")

    # --- Concepts ---
    map_concepts = cross.get("concepts", [])
    concept_covered = 0
    concept_stub = 0
    concept_partial = 0
    concept_full = 0
    concept_missing: list[str] = []

    map_concept_ids = set()
    for entry in map_concepts:
        cid = entry["concept_id"]
        map_concept_ids.add(cid)

        if cid not in ph_concept_ids:
            errors.append(f"Dangling concept_id in cross-book-map: {cid} (not in PH concepts.yaml)")

        chapters = entry.get("hn_chapters", [])
        coverage = entry.get("coverage", "stub")

        for ch in chapters:
            if ch not in hn_chapter_ids:
                errors.append(f"Dangling chapter ref in concept {cid}: {ch} (not in HN book-architecture.yaml)")
            referenced_chapters.add(ch)

        if chapters:
            concept_covered += 1
        else:
            concept_missing.append(cid)

        if coverage == "full":
            concept_full += 1
        elif coverage == "partial":
            concept_partial += 1
        else:
            concept_stub += 1

    for cid in ph_concept_ids - map_concept_ids:
        errors.append(f"PH concept {cid} not listed in cross-book-map.yaml")

    orphan_chapters = hn_chapter_ids - referenced_chapters

    # --- Report ---
    total_theses = len(ph_thesis_ids)
    total_concepts = len(ph_concept_ids)

    if not args.quiet:
        print("=" * 60)
        print("Cross-Book Coverage Report: Predictive History <-> History Notebook")
        print("=" * 60)
        print()
        print(f"THESIS COVERAGE: {thesis_covered}/{total_theses}")
        print(f"  full: {thesis_full}  partial: {thesis_partial}  stub: {thesis_stub}")
        if thesis_missing:
            print(f"  missing (no chapters): {', '.join(thesis_missing)}")
        print()
        print(f"CONCEPT COVERAGE: {concept_covered}/{total_concepts}")
        print(f"  full: {concept_full}  partial: {concept_partial}  stub: {concept_stub}")
        if concept_missing:
            print(f"  missing (no chapters): {', '.join(concept_missing)}")
        print()

        if orphan_chapters:
            print(f"ORPHAN CHAPTERS ({len(orphan_chapters)}):")
            print(f"  Not referenced by any thesis or concept: {', '.join(sorted(orphan_chapters))}")
            print()

        if errors:
            print(f"ERRORS ({len(errors)}):")
            for e in errors:
                print(f"  - {e}")
            print()

        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")
            print()

        if not errors and thesis_covered == total_theses and concept_covered == total_concepts:
            print("STATUS: All theses and concepts have at least one HN chapter link.")
        else:
            print("STATUS: Gaps remain — see missing/errors above.")

    has_gaps = (thesis_covered < total_theses or concept_covered < total_concepts or errors)
    return 1 if has_gaps else 0


if __name__ == "__main__":
    sys.exit(main())
