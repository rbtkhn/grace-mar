#!/usr/bin/env python3
"""Emit full `volume_3_secret_history` YAML block from sh-* rows in sources.yaml.

Usage:
  python3 scripts/work_jiang/emit_volume3_chapters_yaml.py > /tmp/v3.yaml
  # Merge into metadata/book-architecture.yaml before `volume_4_game_theory`.

Operator lane — not Record.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research" / "external" / "work-jiang"


def main() -> int:
    sources = yaml.safe_load((WORK / "metadata" / "sources.yaml").read_text(encoding="utf-8")).get(
        "sources", []
    )
    sh = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("sh-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in sh:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"sh-ch{ep:02d}"
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for Secret History lecture {ep} — Volume III Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md (Volume III policy)."
                ),
                "kind": "exposition",
                "priority": "medium",
                "target_words": 2800,
                "source_ids": [sid],
                "analysis_ids": [],
                "prediction_ids": [],
                "divergence_ids": [],
                "applications": [],
                "status": "outline_pending",
                "owner": "operator",
                "sprint": "TBD",
                "blocking": [],
                "next_action": f"Complete analysis memo for {sid}; then draft chapter outline",
                "outline_path": f"chapters-volume-iii/{cid}/outline.md",
                "draft_path": f"chapters-volume-iii/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    block = {
        "volume_3_secret_history": {
            "project": {
                "id": "work-jiang-volume-3",
                "series_title": "Predictive History",
                "volume": {"number": 3, "lecture_series": "Secret History"},
                "title": "Predictive History, Volume 3: Secret History",
                "thesis_one_sentence": (
                    "TBD — set when Volume III Part I book thesis is drafted "
                    "(lecture-faithful arc; see book/VOLUME-III-SECRET-HISTORY.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's Secret History lectures in classroom order, "
                    "transcript-backed (`lectures/secret-history-*.md`, registry `sh-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box (mirrors Volume II; not a Geo-style prediction scorecard). "
                    "Part II method remains operator-chosen — see book/VOLUME-III-SECRET-HISTORY.md."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in history, philosophy, power, and narrative"
                    ),
                    "secondary": [
                        "readers following the Secret History classroom series on @PredictiveHistory",
                    ],
                },
                "channel_context": {
                    "platform": "YouTube",
                    "handle": "@PredictiveHistory",
                    "status": "book_track_wired",
                },
            },
            "chapter_end_divergence": {
                "registry_path": "divergence-tracking/registry/divergences.jsonl",
                "instruction": (
                    "End each Part I chapter with a boxed subsection per "
                    "CHAPTER-DIVERGENCE-BOX.md — divergence IDs from divergences.jsonl "
                    "where linked; not chapter_end_predictions (Volume I only)."
                ),
            },
            "part_2": {
                "title": "Part II — method TBD (Secret History)",
                "after_chapter": "sh-ch28",
                "description": (
                    "Operator locks evaluation mode in book/VOLUME-III-SECRET-HISTORY.md "
                    "(divergence-first default for Part I boxes; Part II may add adjudication or hybrid)."
                ),
            },
            "book": {"chapters": chapters},
        }
    }

    print(
        yaml.dump(
            block,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
