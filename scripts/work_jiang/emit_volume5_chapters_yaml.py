#!/usr/bin/env python3
"""Emit full `volume_5_great_books` YAML block from gb-* rows in sources.yaml.

Kind: exposition episodes 1–4; analysis 5–8. Priority: medium for all until
chapter-quote-links + counter-reading-links satisfy validate_comparative_layer.

Usage:
  python3 scripts/work_jiang/emit_volume5_chapters_yaml.py > /tmp/v5.yaml
  # Merge into metadata/book-architecture.yaml before `volume_7_essays`.

Operator lane — not Record.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research" / "external" / "work-jiang"

_KIND_EP: dict[int, str] = {i: "exposition" for i in range(1, 5)}
# Episodes 5+ are lecture-analysis blocks (Great Books classroom depth).
_KIND_EP.update({i: "analysis" for i in range(5, 100)})

_PRIORITY_EP: dict[int, str] = {i: "medium" for i in range(1, 100)}


def main() -> int:
    sources = yaml.safe_load((WORK / "metadata" / "sources.yaml").read_text(encoding="utf-8")).get(
        "sources", []
    )
    gb = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("gb-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in gb:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"gb-ch{ep:02d}"
        kind = _KIND_EP.get(ep, "exposition")
        priority = _PRIORITY_EP.get(ep, "medium")
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for Great Books lecture {ep} — Volume V Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md (Volume V default)."
                ),
                "kind": kind,
                "priority": priority,
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
                "outline_path": f"chapters-volume-v/{cid}/outline.md",
                "draft_path": f"chapters-volume-v/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    last_cid = chapters[-1]["id"] if chapters else "gb-ch08"

    block = {
        "volume_5_great_books": {
            "project": {
                "id": "work-jiang-volume-5",
                "series_title": "Predictive History",
                "volume": {"number": 5, "lecture_series": "Great Books"},
                "title": "Predictive History, Volume 5: Great Books",
                "thesis_one_sentence": (
                    "TBD — set when Volume V Part I book thesis is drafted "
                    "(lecture-faithful arc; see book/VOLUME-V-GREAT-BOOKS.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's Great Books lectures in classroom order, "
                    "transcript-backed (`lectures/great-books-*.md`, registry `gb-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box by default (Part II method operator-locked — see "
                    "book/VOLUME-V-GREAT-BOOKS.md)."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in history, philosophy, literature, and consciousness"
                    ),
                    "secondary": [
                        "readers following the Great Books classroom series on @PredictiveHistory",
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
                    "where linked; not chapter_end_predictions (Volume I only) unless "
                    "Part II policy adopts prediction adjudication."
                ),
            },
            "part_2": {
                "title": "Part II — method TBD (Great Books)",
                "after_chapter": last_cid,
                "description": (
                    "Operator locks evaluation mode in book/VOLUME-V-GREAT-BOOKS.md "
                    "(divergence-first default for Part I boxes)."
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
