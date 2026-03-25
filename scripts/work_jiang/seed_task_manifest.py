#!/usr/bin/env python3
"""
Seed tasks.jsonl from book-architecture.yaml.

For each chapter in the YAML, emits three tasks (unless they already exist):
  - analysis-chNN   (chapter_analysis)
  - draft-chNN      (chapter_draft, depends on analysis)
  - predictions-chNN (prediction_score, depends on draft)

Usage:
    python3 scripts/work_jiang/seed_task_manifest.py
    python3 scripts/work_jiang/seed_task_manifest.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_JIANG = REPO_ROOT / "research" / "external" / "work-jiang"
ARCH_PATH = WORK_JIANG / "metadata" / "book-architecture.yaml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from emit_task_event import append_task_event, read_task_states


def lecture_glob_from_source_id(source_id: str) -> str:
    """Convert source_id like 'geo-01' to a lecture glob."""
    parts = source_id.split("-")
    if len(parts) == 2:
        prefix, num = parts
        prefix_map = {
            "geo": "geo-strategy",
            "civ": "civilization",
            "sh": "secret-history",
            "gt": "game-theory",
            "gb": "great-books",
            "vi": "interviews",
        }
        series = prefix_map.get(prefix, prefix)
        return f"lectures/{series}-{num}-*.md"
    return f"lectures/*{source_id}*.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed task manifest from book architecture.")
    parser.add_argument("--dry-run", action="store_true", help="Print tasks without writing")
    args = parser.parse_args()

    if not ARCH_PATH.exists():
        print(f"Architecture file not found: {ARCH_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(ARCH_PATH, encoding="utf-8") as f:
        arch = yaml.safe_load(f)

    chapters = arch.get("book", {}).get("chapters", [])
    if not chapters:
        print("No chapters found in architecture.", file=sys.stderr)
        sys.exit(1)

    existing = read_task_states()
    created = 0

    for ch in chapters:
        ch_id = ch["id"]
        source_ids = ch.get("source_ids", [])
        outline = ch.get("outline_path", f"chapters/{ch_id}/outline.md")
        draft = ch.get("draft_path", f"chapters/{ch_id}/draft.md")
        pred_ids = ch.get("prediction_ids", [])

        lecture_globs = [lecture_glob_from_source_id(s) for s in source_ids]

        tasks = [
            {
                "task_id": f"analysis-{ch_id}",
                "type": "chapter_analysis",
                "scope": ch_id,
                "depends_on": None,
                "context_files": lecture_globs + [outline],
            },
            {
                "task_id": f"draft-{ch_id}",
                "type": "chapter_draft",
                "scope": ch_id,
                "depends_on": [f"analysis-{ch_id}"],
                "context_files": lecture_globs + [
                    outline,
                    "prediction-tracking/registry/predictions.jsonl",
                    "divergence-tracking/registry/divergences.jsonl",
                ],
            },
            {
                "task_id": f"predictions-{ch_id}",
                "type": "prediction_score",
                "scope": ch_id,
                "depends_on": [f"draft-{ch_id}"],
                "context_files": [
                    draft,
                    "prediction-tracking/registry/predictions.jsonl",
                ],
            },
        ]

        for t in tasks:
            if t["task_id"] in existing:
                continue
            if args.dry_run:
                print(f"  [dry-run] would create: {t['task_id']}  type={t['type']}  scope={t['scope']}")
            else:
                append_task_event(
                    t["task_id"],
                    "created",
                    task_type=t["type"],
                    scope=t["scope"],
                    depends_on=t["depends_on"],
                    context_files=t["context_files"],
                )
                print(f"  created: {t['task_id']}")
            created += 1

    print(f"\n{created} task(s) {'would be ' if args.dry_run else ''}created.")


if __name__ == "__main__":
    main()
