#!/usr/bin/env python3
"""Emit full `volume_6_interviews` YAML block from vi-* rows in sources.yaml.

Kind: exposition episodes 1–4; analysis 5–11. Priority: medium for all until
chapter-quote-links + counter-reading-links satisfy validate_comparative_layer.

Usage:
  python3 scripts/work_jiang/emit_volume6_chapters_yaml.py > /tmp/v6.yaml
  # Merge into metadata/book-architecture.yaml before `volume_7_essays`.

Operator lane — not Record.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research" / "external" / "work-jiang"

_KIND_EP: dict[int, str] = {i: "exposition" for i in range(1, 5)}
_KIND_EP.update({i: "analysis" for i in range(5, 100)})

_PRIORITY_EP: dict[int, str] = {i: "medium" for i in range(1, 100)}


def main() -> int:
    sources = yaml.safe_load((WORK / "metadata" / "sources.yaml").read_text(encoding="utf-8")).get(
        "sources", []
    )
    vi = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("vi-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in vi:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"vi-ch{ep:02d}"
        kind = _KIND_EP.get(ep, "analysis")
        priority = _PRIORITY_EP.get(ep, "medium")
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for Interviews episode {ep} — Volume VI Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md (Volume VI default)."
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
                "outline_path": f"chapters-volume-vi/{cid}/outline.md",
                "draft_path": f"chapters-volume-vi/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    last_cid = chapters[-1]["id"] if chapters else "vi-ch01"

    block = {
        "volume_6_interviews": {
            "project": {
                "id": "work-jiang-volume-6",
                "series_title": "Predictive History",
                "volume": {"number": 6, "lecture_series": "Interviews"},
                "title": "Predictive History, Volume 6: Interviews",
                "thesis_one_sentence": (
                    "TBD — set when Volume VI Part I book thesis is drafted "
                    "(interview-faithful arc; see book/VOLUME-VI-INTERVIEWS.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's long-form interview corpus in publication order, "
                    "transcript-backed (`lectures/interviews-*.md`, registry `vi-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box by default (Part II method operator-locked — see "
                    "book/VOLUME-VI-INTERVIEWS.md)."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in geopolitics, dialogue format, and cross-host comparison"
                    ),
                    "secondary": [
                        "listeners following Predictive History interview releases on YouTube",
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
                "title": "Part II — method TBD (Interviews)",
                "after_chapter": last_cid,
                "description": (
                    "Operator locks evaluation mode in book/VOLUME-VI-INTERVIEWS.md "
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
