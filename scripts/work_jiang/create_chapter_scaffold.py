"""Create chapter scaffold: outline.md, draft.md, notes.md from book-architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
CHAPTERS_DIR = WORK_DIR / "chapters"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-id", "-c", required=True, help="Chapter ID (e.g. ch01)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
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
    purpose = ch.get("purpose", "")
    pred_ids = ch.get("prediction_ids") or []
    div_ids = ch.get("divergence_ids") or []
    sids = ch.get("source_ids") or (sm.get("chapter_map") or {}).get(cid, {}).get("source_ids") or []

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
