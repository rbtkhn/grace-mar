"""Validate work-jiang metadata consistency."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ANALYSIS = WORK_DIR / "analysis"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    raw = text[4:end]
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-analysis-frontmatter",
        action="store_true",
        help="Fail if any analysis memo lacks parseable YAML front matter.",
    )
    args = parser.parse_args()

    errors: list[str] = []

    arch_path = WORK_DIR / "metadata" / "book-architecture.yaml"
    if not arch_path.exists():
        errors.append("Missing metadata/book-architecture.yaml")
    architecture = load(arch_path) if arch_path.exists() else {}
    chapter_ids = {c["id"] for c in (architecture.get("book") or {}).get("chapters") or []}

    if not (architecture.get("project") or {}).get("thesis_one_sentence"):
        errors.append("Missing project.thesis_one_sentence")

    sm = load(WORK_DIR / "metadata" / "source-map.yaml")
    chapter_map = sm.get("chapter_map") or {}
    for ch in chapter_map:
        if ch not in chapter_ids:
            errors.append(f"source-map chapter_map references unknown chapter: {ch}")

    sources = load(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    source_ids = {s["source_id"] for s in sources}
    for ch, data in chapter_map.items():
        for sid in data.get("source_ids") or []:
            if sid not in source_ids:
                errors.append(f"Unknown source_id {sid} in chapter_map.{ch}")

    valid_ch = chapter_ids | set(chapter_map.keys())
    if args.require_analysis_frontmatter:
        for path in ANALYSIS.glob("*.md"):
            if path.name == ".gitkeep":
                continue
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if not fm:
                errors.append(f"Missing or invalid front matter: {path.name}")
                continue
            for cand in fm.get("chapter_candidates") or []:
                if cand not in valid_ch:
                    errors.append(f"{path.name}: invalid chapter_candidates entry {cand}")

    cq = load(WORK_DIR / "metadata" / "chapter-queue.yaml").get("chapter_queue") or []
    for item in cq:
        cid = item.get("chapter_id")
        if cid and cid not in chapter_ids:
            errors.append(f"chapter-queue references unknown chapter: {cid}")
        if (item.get("status") or "") == "research_ready":
            mapped = chapter_map.get(cid) or {}
            sids = mapped.get("source_ids") or []
            with_analysis = 0
            for s in sources:
                if s["source_id"] in sids and s["status"]["analysis"] == "complete":
                    with_analysis += 1
            if sids and with_analysis == 0:
                errors.append(
                    f"Chapter {cid} marked research_ready but no mapped source has complete analysis"
                )

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
