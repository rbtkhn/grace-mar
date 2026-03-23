"""Report missing analysis, unmapped sources, thin chapters. Use --strict for exit 1."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
SOURCES = WORK_DIR / "metadata" / "sources.yaml"
MAP = WORK_DIR / "metadata" / "source-map.yaml"

MIN_SOURCES_PER_CHAPTER = 1


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any issue is found.",
    )
    args = parser.parse_args()

    src = load(SOURCES).get("sources", [])
    mapping = load(MAP).get("chapter_map", {})
    appendix = load(MAP).get("appendix_map", {})

    mapped: set[str] = set()
    for ch, data in mapping.items():
        for sid in data.get("source_ids") or []:
            mapped.add(sid)
    for _k, data in appendix.items():
        for sid in data.get("source_ids") or []:
            mapped.add(sid)

    missing_analysis = [s["source_id"] for s in src if s["status"]["analysis"] != "complete"]
    unmapped = [s["source_id"] for s in src if s["source_id"] not in mapped]

    thin: list[str] = []
    for ch, data in mapping.items():
        n = len(data.get("source_ids") or [])
        if n < MIN_SOURCES_PER_CHAPTER:
            thin.append(f"{ch} ({n} sources)")

    issues = 0
    if missing_analysis:
        print("Missing analysis:", ", ".join(missing_analysis), file=sys.stderr)
        issues += 1
    if unmapped:
        print("Unmapped sources (not in any chapter_map or appendix_map):", ", ".join(unmapped), file=sys.stderr)
        issues += 1
    if thin:
        print("Chapters with fewer than", MIN_SOURCES_PER_CHAPTER, "sources:", ", ".join(thin), file=sys.stderr)
        issues += 1

    if not issues:
        print("Coverage OK: all sources mapped and analyzed (per rules).")
        return 0
    if args.strict:
        return 1
    print("(warnings only; use --strict to fail CI)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
