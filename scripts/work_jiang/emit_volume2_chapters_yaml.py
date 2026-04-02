#!/usr/bin/env python3
"""Emit full `volume_2_civilization` YAML block from civ-* rows in sources.yaml.

Usage:
  python3 scripts/work_jiang/emit_volume2_chapters_yaml.py > /tmp/v2.yaml
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
    civ = sorted(
        [s for s in sources if str(s.get("source_id", "")).startswith("civ-")],
        key=lambda x: x["source_id"],
    )
    chapters: list[dict] = []
    for s in civ:
        sid = s["source_id"]
        ep = int(sid.split("-")[1])
        cid = f"civ-ch{ep:02d}"
        chapters.append(
            {
                "id": cid,
                "title": s["title"],
                "purpose": (
                    f"Book chapter for Civilization lecture {ep} — Volume II Part I; "
                    "divergence end-box per CHAPTER-DIVERGENCE-BOX.md."
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
                "outline_path": f"chapters-volume-ii/{cid}/outline.md",
                "draft_path": f"chapters-volume-ii/{cid}/draft.md",
                "analysis_ready": False,
                "quotes_ready": False,
                "requires_prediction_review": False,
            }
        )

    block = {
        "volume_2_civilization": {
            "project": {
                "id": "work-jiang-volume-2",
                "series_title": "Predictive History",
                "volume": {"number": 2, "lecture_series": "Civilization"},
                "title": "Predictive History, Volume 2: Civilization",
                "thesis_one_sentence": (
                    "TBD — set when Volume II Part I book thesis is drafted "
                    "(lecture-faithful arc; see book/VOLUME-II-CIVILIZATION.md)."
                ),
                "promise_paragraph": (
                    "Part I follows Jiang's Civilization lectures in classroom order, "
                    "transcript-backed (`lectures/civilization-*.md`, registry `civ-*` in "
                    "`metadata/sources.yaml`). Each Part I chapter ends with a Divergence "
                    "box (not a prediction scorecard). Part II applies historiographic "
                    "divergence methods — see book/PART-II-CIVILIZATION-DIVERGENCE.md."
                ),
                "audience": {
                    "primary": (
                        "serious general readers interested in history, philosophy, "
                        "and civilizational argument"
                    ),
                    "secondary": [
                        "readers following the Civilization classroom series on @PredictiveHistory",
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
                "title": "Part II — Divergence (Civilization)",
                "after_chapter": "civ-ch60",
                "description": (
                    "Historiography and divergence — how Jiang's claims compare to named "
                    "mainstream or contested positions, using divergence-tracking and "
                    "book/PART-II-CIVILIZATION-DIVERGENCE.md. Not a forecast scorecard."
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
