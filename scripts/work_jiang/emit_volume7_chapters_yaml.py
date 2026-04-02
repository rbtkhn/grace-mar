#!/usr/bin/env python3
"""Emit full `volume_7_essays` YAML block from es-* rows in sources.yaml.

Kind: analysis for all essays (Substack commentary arc). Priority: medium until
chapter-quote-links + counter-reading-links satisfy validate_comparative_layer.

Usage:
  python3 scripts/work_jiang/emit_volume7_chapters_yaml.py > /tmp/v7.yaml
  # Merge into metadata/book-architecture.yaml (replace `volume_7_essays` block).

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
    es_rows = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("es-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in es_rows:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"es-ch{ep:02d}"
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for essay {ep} — Volume VII Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md (Volume VII default)."
                ),
                "kind": "analysis",
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
                "outline_path": f"chapters-volume-vii/{cid}/outline.md",
                "draft_path": f"chapters-volume-vii/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    last_cid = chapters[-1]["id"] if chapters else "es-ch31"

    block = {
        "volume_7_essays": {
            "project": {
                "id": "work-jiang-volume-7",
                "series_title": "Predictive History",
                "volume": {
                    "number": 7,
                    "corpus": "Essays (Predictive History newsletter on Substack)",
                },
                "title": "Predictive History, Volume 7: Essays",
                "thesis_one_sentence": (
                    "TBD — set when Volume VII Part I book thesis is drafted "
                    "(essay-faithful arc; publication order; see book/VOLUME-VII-ESSAYS.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's Predictive History newsletter essays in publication order, "
                    "text-backed (`substack/essays/<slug>.md`; registry `es-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box by default (Part II method operator-locked — see "
                    "book/VOLUME-VII-ESSAYS.md)."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in history, philosophy, and geopolitics"
                    ),
                    "secondary": [
                        "readers following Predictive History on Substack",
                    ],
                },
                "channel_context": {
                    "platform": "Substack",
                    "publication": "https://predictivehistory.substack.com/",
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
                "title": "Part II — method TBD (Essays)",
                "after_chapter": last_cid,
                "description": (
                    "Operator locks evaluation mode in book/VOLUME-VII-ESSAYS.md "
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
