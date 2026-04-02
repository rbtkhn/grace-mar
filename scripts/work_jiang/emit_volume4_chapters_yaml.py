#!/usr/bin/env python3
"""Emit full `volume_4_game_theory` YAML block from gt-* rows in sources.yaml.

Kind: exposition 1–7, analysis 8–17; priority medium for all chapters until quote/counter-reading wiring (comparative validator).

Usage:
  python3 scripts/work_jiang/emit_volume4_chapters_yaml.py > /tmp/v4.yaml
  # Merge into metadata/book-architecture.yaml before `volume_7_essays`.

Operator lane — not Record.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research" / "external" / "work-jiang"

# Episodes 1–7 exposition; 8+ analysis. Priority: all analysis = medium until
# chapter-quote-links + counter-reading-links cover the chapter (validate_comparative_layer).
_KIND_EP: dict[int, str] = {i: "exposition" for i in range(1, 8)}
_KIND_EP.update({i: "analysis" for i in range(8, 18)})

_PRIORITY_EP: dict[int, str] = {i: "medium" for i in range(1, 18)}


def main() -> int:
    sources = yaml.safe_load((WORK / "metadata" / "sources.yaml").read_text(encoding="utf-8")).get(
        "sources", []
    )
    gt = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("gt-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in gt:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"gt-ch{ep:02d}"
        kind = _KIND_EP.get(ep, "exposition")
        priority = _PRIORITY_EP.get(ep, "medium")
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for Game Theory lecture {ep} — Volume IV Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md (Volume IV default)."
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
                "outline_path": f"chapters-volume-iv/{cid}/outline.md",
                "draft_path": f"chapters-volume-iv/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    last_cid = chapters[-1]["id"] if chapters else "gt-ch17"

    block = {
        "volume_4_game_theory": {
            "project": {
                "id": "work-jiang-volume-4",
                "series_title": "Predictive History",
                "volume": {"number": 4, "lecture_series": "Game Theory"},
                "title": "Predictive History, Volume 4: Game Theory",
                "thesis_one_sentence": (
                    "TBD — set when Volume IV Part I book thesis is drafted "
                    "(lecture-faithful arc; see book/VOLUME-IV-GAME-THEORY.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's Game Theory lectures in classroom order, "
                    "transcript-backed (`lectures/game-theory-*.md`, registry `gt-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box by default (Part II method operator-locked — see "
                    "book/VOLUME-IV-GAME-THEORY.md)."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in history, philosophy, strategy, and incentives"
                    ),
                    "secondary": [
                        "readers following the Game Theory classroom series on @PredictiveHistory",
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
                "title": "Part II — method TBD (Game Theory)",
                "after_chapter": last_cid,
                "description": (
                    "Operator locks evaluation mode in book/VOLUME-IV-GAME-THEORY.md "
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
