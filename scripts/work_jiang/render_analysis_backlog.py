"""Render ANALYSIS-BACKLOG.md from sources, source-map, and book-architecture."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ANALYSIS_DIR = WORK_DIR / "analysis"
PENDING_DIR = WORK_DIR / "analysis" / "pending"
OUT = WORK_DIR / "ANALYSIS-BACKLOG.md"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def priority_for_source(
    source: dict,
    mapped_chapters: list[str],
    chapters: list[dict],
    next_in_queue_statuses: set[str],
) -> int:
    """Score 0+; higher = more urgent. Blocks next chapter +100, sprint +50, geo +20, missing +10."""
    score = 0
    sid = source.get("source_id", "")
    analysis_complete = (source.get("status") or {}).get("analysis") == "complete"

    for ch in chapters:
        if ch.get("status") in next_in_queue_statuses:
            sids = ch.get("source_ids") or []
            if sid in sids:
                score += 100
                break

    if mapped_chapters:
        score += 50
    if source.get("series") == "geo-strategy":
        score += 20
    if not analysis_complete:
        score += 10

    return score


def scan_lens_coverage() -> tuple[dict[str, str], dict[str, str], set[str], set[str]]:
    """Return (civmem_by_sid, psyhist_by_sid, civmem_pending, psyhist_pending)."""
    civmem_complete: dict[str, str] = {}
    psyhist_complete: dict[str, str] = {}
    civmem_pending: set[str] = set()
    psyhist_pending: set[str] = set()

    for d in (ANALYSIS_DIR, PENDING_DIR):
        if not d.exists():
            continue
        is_pending = d == PENDING_DIR
        for p in d.glob("*.md"):
            if p.name.endswith("-civmem-analysis.md"):
                sid = p.stem.removesuffix("-civmem-analysis")
                if is_pending:
                    civmem_pending.add(sid)
                else:
                    civmem_complete[sid] = "complete"
            elif p.name.endswith("-psy-hist-analysis.md"):
                sid = p.stem.removesuffix("-psy-hist-analysis")
                if is_pending:
                    psyhist_pending.add(sid)
                else:
                    psyhist_complete[sid] = "complete"

    return civmem_complete, psyhist_complete, civmem_pending, psyhist_pending


def main() -> int:
    sources = load(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    sm = load(WORK_DIR / "metadata" / "source-map.yaml")
    arch = load(WORK_DIR / "metadata" / "book-architecture.yaml")
    chapter_map = sm.get("chapter_map") or {}
    chapters = (arch.get("book") or {}).get("chapters") or []

    civmem_ok, psyhist_ok, civmem_pending, psyhist_pending = scan_lens_coverage()

    next_in_queue = {"ready_for_outline", "analysis_complete"}

    rows = []
    for s in sources:
        sid = s.get("source_id", "")
        mapped = [
            cid
            for cid, data in chapter_map.items()
            if sid in (data.get("source_ids") or [])
        ]
        score = priority_for_source(s, mapped, chapters, next_in_queue)
        analysis_status = (s.get("status") or {}).get("analysis", "missing")
        civmem_status = civmem_ok.get(sid) or ("pending" if sid in civmem_pending else "missing")
        psyhist_status = psyhist_ok.get(sid) or ("pending" if sid in psyhist_pending else "missing")
        reason_parts = []
        if score >= 100:
            reason_parts.append("blocks next chapter in queue")
        if mapped:
            reason_parts.append(f"mapped to {', '.join(mapped)}")
        if s.get("series") == "geo-strategy":
            reason_parts.append("geo-series")
        if analysis_status != "complete":
            reason_parts.append("analysis missing")
        reason = "; ".join(reason_parts) if reason_parts else "—"
        rows.append(
            {
                "source_id": sid,
                "series": s.get("series", ""),
                "lecture_title": s.get("title", ""),
                "analysis_status": analysis_status,
                "civmem": civmem_status,
                "psy_hist": psyhist_status,
                "mapped_chapters": ", ".join(mapped) if mapped else "—",
                "priority_score": score,
                "reason": reason,
            }
        )

    rows.sort(key=lambda r: -r["priority_score"])

    lines = [
        "# ANALYSIS BACKLOG",
        "",
        "Sources missing or needing analysis, ordered by priority.",
        "",
        "| source_id | series | lecture_title | analysis | civmem | psy-hist | mapped_chapters | priority_score | reason |",
        "|-----------|--------|---------------|----------|--------|----------|-----------------|----------------|--------|",
    ]
    for r in rows:
        title = (r["lecture_title"] or "")[:40] + ("…" if len(r["lecture_title"] or "") > 40 else "")
        lines.append(
            f"| {r['source_id']} | {r['series']} | {title} | {r['analysis_status']} | "
            f"{r['civmem']} | {r['psy_hist']} | {r['mapped_chapters']} | {r['priority_score']} | {r['reason']} |"
        )

    pending_civmem = sorted(civmem_pending)
    pending_psyhist = sorted(psyhist_pending)
    if pending_civmem or pending_psyhist:
        lines.append("")
        lines.append("## Pending lens drafts")
        if pending_civmem:
            lines.append(f"- **CIV-MEM:** {len(pending_civmem)} — `{'`, `'.join(pending_civmem[:10])}{'…' if len(pending_civmem) > 10 else ''}`")
            lines.append("  Review and run: `python3 scripts/work_jiang/promote_reviewed_memo.py --id <id> --lens civ-mem`")
        if pending_psyhist:
            lines.append(f"- **PSY-HIST:** {len(pending_psyhist)} — `{'`, `'.join(pending_psyhist[:10])}{'…' if len(pending_psyhist) > 10 else ''}`")
            lines.append("  Review and run: `python3 scripts/work_jiang/promote_reviewed_memo.py --id <id> --lens psy-hist`")

    lines.append("")
    lines.append(
        "*Generated by `scripts/work_jiang/render_analysis_backlog.py` — run after registry/source updates.*"
    )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
