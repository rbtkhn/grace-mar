"""Join predictions/divergences/influence JSONL to source_id and chapter_id; write metadata/*-links.yaml.

Predictions/divergences load from canonical JSONL by default. Set WORK_JIANG_REGISTRY_PREFER_SQLITE=1
(after rebuild_registry_db.py) to read the materialized SQLite payloads instead — same row shape.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"

_SCRIPTS_WJ = ROOT / "scripts" / "work_jiang"
if str(_SCRIPTS_WJ) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_WJ))

from registry_db import load_divergences_for_link, load_predictions_for_link


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def source_indexes():
    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    by_video = {s["video_id"]: s for s in sources if s.get("video_id")}
    by_lecture = {}
    for s in sources:
        lp = s.get("lecture_path")
        if lp:
            by_lecture[lp.replace("\\", "/")] = s
            by_lecture[Path(lp).name] = s
    sm = load_yaml(WORK_DIR / "metadata" / "source-map.yaml")
    source_to_chapters: dict[str, list[str]] = {}
    for ch, data in (sm.get("chapter_map") or {}).items():
        for sid in data.get("source_ids") or []:
            source_to_chapters.setdefault(sid, []).append(ch)
    return by_video, by_lecture, source_to_chapters


def resolve_source(row: dict, by_video: dict, by_lecture: dict):
    vid = row.get("video_id")
    if vid and vid in by_video:
        return by_video[vid]["source_id"]
    ref = row.get("lecture_ref") or ""
    ref = ref.replace("\\", "/")
    if ref in by_lecture:
        return by_lecture[ref]["source_id"]
    base = Path(ref).name
    if base in by_lecture:
        return by_lecture[base]["source_id"]
    return None


def main() -> int:
    by_video, by_lecture, source_to_chapters = source_indexes()

    predictions = load_jsonl(WORK_DIR / "prediction-tracking" / "registry" / "predictions.jsonl")
    out_pred = []
    for row in predictions:
        sid = resolve_source(row, by_video, by_lecture)
        chs = source_to_chapters.get(sid, []) if sid else []
        out_pred.append(
            {
                **row,
                "source_id": sid,
                "chapter_ids": chs,
            }
        )

    divergences = load_divergences_for_link()
    out_div = []
    for row in divergences:
        sid = resolve_source(row, by_video, by_lecture)
        chs = source_to_chapters.get(sid, []) if sid else []
        out_div.append({**row, "source_id": sid, "chapter_ids": chs})

    influence = load_jsonl(WORK_DIR / "influence-tracking" / "snapshots" / "video-metrics.jsonl")
    out_inf = []
    for row in influence:
        sid = resolve_source(row, by_video, by_lecture)
        chs = source_to_chapters.get(sid, []) if sid else []
        out_inf.append({**row, "source_id": sid, "chapter_ids": chs})

    meta = WORK_DIR / "metadata"
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "prediction-links.yaml").write_text(
        yaml.safe_dump({"prediction_links": out_pred}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (meta / "divergence-links.yaml").write_text(
        yaml.safe_dump({"divergence_links": out_div}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (meta / "influence-links.yaml").write_text(
        yaml.safe_dump({"influence_links": out_inf}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(
        f"Wrote prediction-links ({len(out_pred)}), divergence-links ({len(out_div)}), "
        f"influence-links ({len(out_inf)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
