"""Create chapter scaffold: outline.md, draft.md, notes.md from book-architecture.

Supports --dual-lens mode: uses CHAPTER-SCAFFOLD-DUAL-LENS.md template,
auto-links approved CIV-MEM (structure/seams) and PSY-HIST (prediction/steering) memos,
and pulls claims from claims.jsonl for the Integrated Operator Thesis.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
CHAPTERS_DIR = WORK_DIR / "chapters"
ANALYSIS_DIR = WORK_DIR / "analysis"
TEMPLATE_PATH = Path(__file__).parent / "templates" / "CHAPTER-SCAFFOLD-DUAL-LENS.md"
CLAIMS_PATH = WORK_DIR / "claims" / "registry" / "claims.jsonl"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _approved_memos_for_sources(source_ids: list[str]) -> tuple[list[str], list[str]]:
    """Return (civmem_paths, psyhist_paths) for sources that have approved memos in analysis/."""
    civmem: list[str] = []
    psyhist: list[str] = []
    if not ANALYSIS_DIR.exists():
        return civmem, psyhist
    for p in ANALYSIS_DIR.glob("*.md"):
        if p.name.endswith("-civmem-analysis.md"):
            sid = p.stem.removesuffix("-civmem-analysis")
            if sid in source_ids:
                civmem.append(f"`{p.relative_to(WORK_DIR)}`")
        elif p.name.endswith("-psy-hist-analysis.md"):
            sid = p.stem.removesuffix("-psy-hist-analysis")
            if sid in source_ids:
                psyhist.append(f"`{p.relative_to(WORK_DIR)}`")
    return civmem, psyhist


def _claims_for_chapter(cid: str) -> list[dict]:
    """Return claims where chapter is in chapter_candidates."""
    if not CLAIMS_PATH.exists():
        return []
    out = []
    for line in CLAIMS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
            if cid in (c.get("chapter_candidates") or []):
                out.append(c)
        except json.JSONDecodeError:
            continue
    return out


def _generate_dual_lens_scaffold(cid: str, title: str, sids: list[str], force: bool) -> int:
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: Dual-lens template not found: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    content = content.replace("Chapter X – [Working Title]", f"Chapter {cid.upper()} – {title}")
    content = content.replace("chXX", cid)
    content = content.replace("YYYY-MM-DD", today)

    lecture_list = "\n".join(f"- `{sid}`" for sid in sids) if sids else "- (none linked yet)"
    content = content.replace(
        "- List of linked lectures (e.g., civ-21, geo-strategy-12, etc.)",
        lecture_list,
    )

    civmem_paths, psyhist_paths = _approved_memos_for_sources(sids)
    civmem_block = "\n".join(f"- {p}" for p in civmem_paths) if civmem_paths else "- (no approved CIV-MEM memos yet)"
    psyhist_block = "\n".join(f"- {p}" for p in psyhist_paths) if psyhist_paths else "- (no approved PSY-HIST memos yet)"
    content = content.replace(
        "Linked CIV-MEM memos: `analysis/civ-21-civmem-analysis.md`",
        f"Linked CIV-MEM memos:\n{civmem_block}",
    )
    content = content.replace(
        "Linked PSY-HIST memos: `analysis/civ-21-psy-hist-analysis.md`",
        f"Linked PSY-HIST memos:\n{psyhist_block}",
    )

    claims = _claims_for_chapter(cid)
    if claims:
        claim_lines = []
        for c in claims[:15]:
            claim_id = c.get("claim_id", "")
            claim_text = (c.get("claim") or "")[:80] + ("…" if len(c.get("claim") or "") > 80 else "")
            source = c.get("source_id", "")
            claim_lines.append(f"- [{claim_id}] {claim_text} → {source}")
        if len(claims) > 15:
            claim_lines.append(f"- … and {len(claims) - 15} more (see claims.jsonl)")
        claims_block = "\n".join(claim_lines)
    else:
        claims_block = "- [civ-mem / psy-hist / clio-elite-overproduction / asimov-seldon-crisis / lever] Claim text → source lecture + memo"
    content = content.replace(
        "- [civ-mem / psy-hist / clio-elite-overproduction / asimov-seldon-crisis / lever] Claim text → source lecture + memo\n- [repeat for each major claim]",
        claims_block,
    )

    out_path = CHAPTERS_DIR / cid / "scaffold-dual-lens.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not force:
        print(f"Skip {out_path.relative_to(ROOT)} (exists; use --force to overwrite)", file=sys.stderr)
        return 0

    out_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"  Title: {title}")
    print(f"  Lectures: {len(sids)} ({', '.join(sids[:5])}{'…' if len(sids) > 5 else ''})")
    print(f"  CIV-MEM memos: {len(civmem_paths)} | PSY-HIST memos: {len(psyhist_paths)} | Claims: {len(claims)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-id", "-c", required=True, help="Chapter ID (e.g. ch01)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dual-lens", action="store_true", help="Use dual-lens scaffold (CIV-MEM + PSY-HIST v1.4)")
    args = parser.parse_args()

    cid = args.chapter_id
    arch = load(WORK_DIR / "metadata" / "book-architecture.yaml")
    sm = load(WORK_DIR / "metadata" / "source-map.yaml")
    sources = load(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    quote_links = load(WORK_DIR / "metadata" / "chapter-quote-links.yaml").get("chapter_quote_links") or {}

    by_id = {c["id"]: c for c in (arch.get("book") or {}).get("chapters") or []}
    ch = by_id.get(cid)
    if not ch:
        print(f"ERROR: Unknown chapter_id: {cid}", file=sys.stderr)
        return 1

    title = ch.get("title", cid)
    sids = ch.get("source_ids") or (sm.get("chapter_map") or {}).get(cid, {}).get("source_ids") or []

    if args.dual_lens:
        return _generate_dual_lens_scaffold(cid, title, sids, args.force)

    purpose = ch.get("purpose", "")
    pred_ids = ch.get("prediction_ids") or []
    div_ids = ch.get("divergence_ids") or []

    src_by = {s["source_id"]: s for s in sources}
    lecture_refs = []
    for sid in sids:
        s = src_by.get(sid)
        if s:
            lp = s.get("lecture_path", "")
            lecture_refs.append(f"- `{sid}` → [{lp}]({lp})")

    quote_ids = quote_links.get(cid, [])
    quote_placeholders = [f"- [{q}]" for q in quote_ids[:5]]
    if len(quote_ids) > 5:
        quote_placeholders.append(f"- … and {len(quote_ids) - 5} more (see chapter-quote-links)")
    quote_block = "\n".join(quote_placeholders) if quote_placeholders else "- [Q1]\n- [Q2]\n- [Q3]"

    out_dir = CHAPTERS_DIR / cid
    out_dir.mkdir(parents=True, exist_ok=True)

    outline_path = out_dir / "outline.md"
    draft_path = out_dir / "draft.md"
    notes_path = out_dir / "notes.md"

    for p in (outline_path, draft_path, notes_path):
        if p.exists() and not args.force:
            print(f"Skip {p.relative_to(WORK_DIR)} (exists; use --force to overwrite)")
            continue

    outline_content = f"""# {cid} — {title}

## One-sentence thesis

(placeholder)

## What Jiang argues (exposition)

(placeholder)

## How the argument is structured

(placeholder)

## Key quotations

{quote_block}

## Analysis

### CIV-MEM Reading

(placeholder)

### PSY-HIST Reading

(placeholder)

### Integrated Operator Thesis

(placeholder)

### Strengths

### Tensions

### Dependencies

### Forecast implications

## Chapter-end prediction box

{chr(10).join(f"- `{pid}`" for pid in pred_ids) if pred_ids else "(see book-architecture prediction_ids)"}

## Open questions

"""

    draft_content = f"""# {cid} — {title}

## Mapped lectures

{"\n".join(lecture_refs) if lecture_refs else "(none)"}

## Chapter purpose

{purpose}

## Draft

(placeholder — see outline.md)

"""

    notes_content = f"""# {cid} — notes

Scratch space for drafting.

"""

    if not outline_path.exists() or args.force:
        outline_path.write_text(outline_content.strip() + "\n", encoding="utf-8")
        print(f"Wrote {outline_path.relative_to(ROOT)}")
    if not draft_path.exists() or args.force:
        draft_path.write_text(draft_content.strip() + "\n", encoding="utf-8")
        print(f"Wrote {draft_path.relative_to(ROOT)}")
    if not notes_path.exists() or args.force:
        notes_path.write_text(notes_content.strip() + "\n", encoding="utf-8")
        print(f"Wrote {notes_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
