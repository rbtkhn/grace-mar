"""Render QUOTE-BANK.md from metadata/quotes.yaml."""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
QUOTES = WORK_DIR / "metadata" / "quotes.yaml"
CONCEPTS = WORK_DIR / "metadata" / "concepts.yaml"
OUT = WORK_DIR / "QUOTE-BANK.md"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    errors: list[str] = []
    qdoc = load_yaml(QUOTES)
    quotes = qdoc.get("quotes") or []
    cdoc = load_yaml(CONCEPTS)
    valid_concepts = {c.get("concept_id") for c in (cdoc.get("concepts") or []) if c.get("concept_id")}

    by_ch: dict[str, list[dict]] = defaultdict(list)
    incomplete: list[dict] = []
    for row in quotes:
        text = (row.get("text") or "").strip()
        if not text:
            incomplete.append(row)
            continue
        for ch in row.get("chapter_ids") or ["ch01"]:
            by_ch[ch].append(row)
        for cid in row.get("concept_ids") or []:
            if cid and cid not in valid_concepts:
                errors.append(f"Quote {row.get('quote_id')} unknown concept_id {cid}")

    lines = [
        "# Quotation bank — work-jiang (Geo-Strategy)",
        "",
        "Curated lines from transcript-backed lectures and analysis memos. Wording may follow ASR; check notes before final citation.",
        "",
        f"**Total quotes:** {len(quotes)}",
        "",
    ]

    order = sorted(by_ch.keys(), key=lambda x: (x[2:], x))
    for ch in order:
        lines.append(f"## {ch}")
        lines.append("")
        for row in sorted(by_ch[ch], key=lambda r: r.get("quote_id") or ""):
            qid = row.get("quote_id") or "?"
            src = row.get("source_id") or "?"
            body = (row.get("text") or "").strip()
            lines.append(f"- **`{qid}`** (`{src}`) — {body}")
            note = (row.get("notes") or "").strip()
            if note:
                lines.append(f"  - *Notes:* {note}")
        lines.append("")

    if incomplete:
        lines.append("## Incomplete")
        lines.append("")
        for row in incomplete:
            lines.append(f"- `{row.get('quote_id')}` — (empty text)")
        lines.append("")

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
