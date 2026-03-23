"""Build metadata/quote-index.yaml from quotes.yaml and chapter-quote-links."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
QUOTES_PATH = WORK_DIR / "metadata" / "quotes.yaml"
LINKS_PATH = WORK_DIR / "metadata" / "chapter-quote-links.yaml"
OUT_PATH = WORK_DIR / "metadata" / "quote-index.yaml"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    quotes_data = load(QUOTES_PATH)
    raw_quotes = quotes_data.get("quotes") or []
    links = load(LINKS_PATH).get("chapter_quote_links") or {}

    index_quotes = []
    for q in raw_quotes:
        qid = q.get("quote_id", "")
        chapter_ids = q.get("chapter_ids") or []
        row = {
            "quote_id": qid,
            "source_id": q.get("source_id", ""),
            "chapter_ids": chapter_ids,
            "status": q.get("status", "candidate"),
            "speaker": q.get("speaker", ""),
            "text_raw": q.get("text", ""),
            "text_clean": q.get("text_clean", q.get("text", "")),
            "timestamp": q.get("timestamp", ""),
            "theme_tags": q.get("themes", []) or q.get("concept_ids", []),
        }
        index_quotes.append(row)

    out = {
        "description": "Derived from metadata/quotes.yaml; status: candidate|cleaned|verified|draft_safe",
        "quotes": index_quotes,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        yaml.safe_dump(out, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(index_quotes)} quotes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
