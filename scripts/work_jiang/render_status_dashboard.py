"""Render STATUS.md — corpus, book, registries, next actions."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
OUT = WORK_DIR / "STATUS.md"


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


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


def count_geo_lectures() -> int:
    return len(list((WORK_DIR / "lectures").glob("geo-strategy-*.md")))


def count_civilization_lectures() -> int:
    return len(list((WORK_DIR / "lectures").glob("civilization-*.md")))


def main() -> int:
    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    arch = load_yaml(WORK_DIR / "metadata" / "book-architecture.yaml")
    chapters = (arch.get("book") or {}).get("chapters") or []
    pred_links = load_yaml(WORK_DIR / "metadata" / "prediction-links.yaml")
    div_links = load_yaml(WORK_DIR / "metadata" / "divergence-links.yaml")
    infl_links = load_yaml(WORK_DIR / "metadata" / "influence-links.yaml")

    lecture_count = count_geo_lectures()
    civ_lecture_count = count_civilization_lectures()
    analysis_count = len(list((WORK_DIR / "analysis").glob("*.md")))
    # exclude .gitkeep if counted as file - glob *.md only real files
    missing_analysis = [s["source_id"] for s in sources if s["status"]["analysis"] != "complete"]

    preds_raw = load_jsonl(WORK_DIR / "prediction-tracking" / "registry" / "predictions.jsonl")
    divs_raw = load_jsonl(WORK_DIR / "divergence-tracking" / "registry" / "divergences.jsonl")
    infl_raw = load_jsonl(WORK_DIR / "influence-tracking" / "snapshots" / "video-metrics.jsonl")

    pl = pred_links.get("prediction_links") if isinstance(pred_links, dict) else None
    pred_linked = len(pl) if isinstance(pl, list) else len(preds_raw)

    unresolved = sum(
        1
        for p in preds_raw
        if (p.get("resolution_status") or "") in ("pending", "not_evaluable", "")
        or p.get("resolved_at_utc") is None
    )

    dl = div_links.get("divergence_links") if isinstance(div_links, dict) else None
    div_linked = len(dl) if isinstance(dl, list) else len(divs_raw)

    il = infl_links.get("influence_links") if isinstance(infl_links, dict) else None
    infl_count = len(il) if isinstance(il, list) else len(infl_raw)

    arch_ch = (arch.get("book") or {}).get("chapters") or []
    thesis_state = (arch.get("project") or {}).get("status", "unknown")

    ready_now = [
        c
        for c in chapters
        if c.get("status") in ("research_ready", "ready_for_outline", "draft_in_progress", "analysis_complete")
    ]
    blocked = [c for c in chapters if c.get("blocking")]

    pack_dir = WORK_DIR / "evidence-packs"
    expected_ch = {c.get("id") for c in arch_ch if c.get("id")}
    pack_files = list(pack_dir.glob("ch*.md")) if pack_dir.exists() else []
    pack_ids = set()
    for p in pack_files:
        # ch01.md -> ch01
        stem = p.stem
        if stem.startswith("ch"):
            pack_ids.add(stem)

    lines = [
        "# work-jiang — status",
        "",
        "> Operator lane — not Voice knowledge until merged through the gate.",
        "",
        "## Corpus",
        "",
        f"- **Geo-Strategy lectures:** {lecture_count}",
        f"- **Civilization series lectures (curated files):** {civ_lecture_count}",
        f"- **Analysis memos:** {analysis_count}",
        f"- **Missing analysis:** {len(missing_analysis)} ({', '.join(missing_analysis) if missing_analysis else 'none'})",
        "",
        "## Book architecture",
        "",
        f"- **Project status:** {thesis_state}",
        f"- **Chapters defined:** {len(arch_ch)}",
        f"- **Chapters in queue:** {len(chapters)} (from book-architecture.yaml)",
        f"- **Chapters research-ready or ready for outline:** {len(ready_now)}",
        f"- **Chapters with blockers listed:** {len(blocked)}",
        f"- **Evidence packs present:** {len(pack_ids & expected_ch)} / {len(expected_ch)} chapters",
        "",
        "## Registries",
        "",
        f"- **Predictions (raw jsonl):** {len(preds_raw)}",
        f"- **Predictions linked (metadata):** {pred_linked}",
        f"- **Unresolved / pending predictions (heuristic):** {unresolved}",
        f"- **Divergences (raw jsonl):** {len(divs_raw)}",
        f"- **Divergences linked (metadata):** {div_linked}",
        f"- **Influence snapshots:** {infl_count}",
        "",
        "## Next actions",
        "",
    ]
    for i, c in enumerate(chapters[:5], 1):
        lines.append(f"{i}. {c.get('next_action', '')} ({c.get('id', '')})")
    if not chapters:
        lines.append("1. (Define chapters in metadata/book-architecture.yaml)")
    lines.append("")
    lines.append(
        "*Generated by `scripts/work_jiang/render_status_dashboard.py` — run after registry/link updates.*"
    )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
