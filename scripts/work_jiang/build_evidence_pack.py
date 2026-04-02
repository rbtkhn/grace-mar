"""Build one evidence pack markdown for a book chapter."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
PACK_DIR = WORK_DIR / "evidence-packs"

import sys

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from arch_chapters import chapter_by_id  # noqa: E402


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_claims() -> list[dict]:
    p = WORK_DIR / "claims" / "registry" / "claims.jsonl"
    if not p.exists():
        return []
    rows = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


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


def excerpt_quote(lecture_path: Path, max_len: int = 400) -> str:
    if not lecture_path.exists():
        return "(lecture file not found)"
    text = lecture_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"## At a glance\s*\n\n(.+?)(?=\n## |\Z)", text, re.DOTALL)
    chunk = m.group(1).strip() if m else text[:max_len]
    chunk = re.sub(r"\s+", " ", chunk)[:max_len]
    return chunk + ("…" if len(chunk) >= max_len else "")


def build_pack(chapter_id: str) -> str:
    arch = load_yaml(WORK_DIR / "metadata" / "book-architecture.yaml")
    smap = load_yaml(WORK_DIR / "metadata" / "source-map.yaml")
    sources_list = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    concepts_data = load_yaml(WORK_DIR / "metadata" / "concepts.yaml").get("concepts", [])
    pred_yl = load_yaml(WORK_DIR / "metadata" / "prediction-links.yaml")
    div_yl = load_yaml(WORK_DIR / "metadata" / "divergence-links.yaml")

    ch_meta = chapter_by_id(arch, chapter_id)
    if not ch_meta:
        raise SystemExit(f"Unknown chapter_id: {chapter_id}")

    purpose = ch_meta.get("purpose", "")
    title = ch_meta.get("title", chapter_id)

    cmap = (smap.get("chapter_map") or {}).get(chapter_id) or {}
    source_ids = list(cmap.get("source_ids") or [])
    if not source_ids:
        source_ids = list(ch_meta.get("source_ids") or [])

    src_by = {s["source_id"]: s for s in sources_list}
    blockers: list[str] = []
    if not source_ids:
        blockers.append("No sources in source-map chapter_map for this chapter.")

    core_analysis: list[str] = []
    lecture_links: list[str] = []
    quotes: list[str] = []
    for sid in source_ids:
        s = src_by.get(sid)
        if not s:
            blockers.append(f"Unknown source_id in map: {sid}")
            continue
        lp = WORK_DIR / s.get("lecture_path", "")
        lecture_links.append(f"- `{sid}` → [{Path(s['lecture_path']).name}]({s['lecture_path']})")
        quotes.append(f"**{sid} (excerpt):** {excerpt_quote(lp)}")
        ap = s.get("analysis_path")
        if ap:
            core_analysis.append(f"- `{sid}` → [{Path(ap).name}]({ap})")
        else:
            blockers.append(f"Analysis memo missing for {sid} (expected before drafting).")

    key_concepts = [
        c
        for c in concepts_data
        if chapter_id in (c.get("chapter_ids") or [])
        or bool(set(c.get("source_ids") or []) & set(source_ids))
    ]
    concept_lines = [f"- **{c.get('concept_id')}** — {c.get('term', '')}" for c in key_concepts[:15]]

    claims = load_claims()
    key_claims = [
        r
        for r in claims
        if chapter_id in (r.get("chapter_candidates") or [])
    ]
    claim_lines = [f"- `{r.get('claim_id')}` ({r.get('claim_type')}) — {r.get('claim', '')[:120]}…" for r in key_claims[:25]]

    preds = pred_yl.get("prediction_links") if isinstance(pred_yl, dict) else []
    divs = div_yl.get("divergence_links") if isinstance(div_yl, dict) else []
    pred_n = sum(
        1
        for p in preds or []
        if chapter_id in (p.get("chapter_ids") or []) or (p.get("source_id") in source_ids)
    )
    div_n = sum(
        1
        for d in divs or []
        if chapter_id in (d.get("chapter_ids") or []) or (d.get("source_id") in source_ids)
    )

    if chapter_id.startswith("civ-ch"):
        open_q = [
            "Which mainstream historiographic line best counters the lecture's central move?",
            "Where does lecture compression overstate consensus or omit named rivals?",
        ]
        spill = (
            "- Appendix / website: divergence notes and Part II historiography "
            "(Volume II — not a prediction scorecard)."
        )
    elif chapter_id.startswith("sh-ch"):
        open_q = [
            "Which named scholarly or primary-source line best tests the lecture's power / narrative claims?",
            "Where does pedagogical compression risk epistemic overreach (e.g. Kant gloss, finance, history)?",
        ]
        spill = (
            "- Appendix / website: divergence notes and Part II method per "
            "book/VOLUME-III-SECRET-HISTORY.md (not a Geo-style prediction scorecard by default)."
        )
    else:
        open_q = [
            "Does Jiang treat religion instrumentally or ontologically in these sources?",
            "Which competing IR or theological framework deserves the strongest counter-reading?",
        ]
        spill = "- Appendix / website: prediction scorecard rows; divergence notes where claims are contested."

    lines = [
        f"# Evidence pack — {chapter_id}",
        "",
        f"**Chapter title:** {title}",
        "",
        "## Chapter purpose",
        "",
        purpose,
        "",
        "## Core sources",
        "",
    ]
    if lecture_links:
        lines.extend(lecture_links)
    else:
        lines.append("(none mapped)")
    lines += ["", "## Core analysis", ""]
    if core_analysis:
        lines.extend(core_analysis)
    else:
        lines.append("(none — see blockers)")
    lines += ["", "## Key concepts", ""]
    if concept_lines:
        lines.extend(concept_lines)
    else:
        lines.append("(none tagged for this chapter yet — expand `metadata/concepts.yaml`.)")
    lines += ["", "## Key claims", ""]
    if claim_lines:
        lines.extend(claim_lines)
    else:
        lines.append("(none with chapter_candidates including this id — see `claims/registry/claims.jsonl`.)")
    lines += [
        "",
        "## Supporting registries",
        "",
        f"- **Predictions (linked to this chapter / sources):** {pred_n}",
        f"- **Divergences (linked):** {div_n}",
        "",
        "## Quotation candidates (auto excerpt)",
        "",
    ]
    if quotes:
        for q in quotes[:3]:
            lines.append(q)
            lines.append("")
    else:
        lines.append("(Quote bank TBD — add bold pulls manually.)")
        lines.append("")
    lines += ["## Open questions", ""]
    for q in open_q:
        lines.append(f"- {q}")
    lines += ["", "## Appendix / site spillover", "", spill, ""]
    lines += ["## Blockers", ""]
    if blockers:
        for b in blockers:
            lines.append(f"- [ ] {b}")
    else:
        lines.append("- (none detected)")
    lines.append("")
    lines.append(
        f"*Generated by `scripts/work_jiang/build_evidence_pack.py --chapter {chapter_id}` — operator lane.*"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", required=True, help="Chapter id, e.g. ch03")
    args = parser.parse_args()

    text = build_pack(args.chapter)
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    out = PACK_DIR / f"{args.chapter}.md"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
