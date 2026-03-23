"""Emit metadata/chapter-quote-links.yaml from metadata/quotes.yaml."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
QUOTES = WORK_DIR / "metadata" / "quotes.yaml"
OUT = WORK_DIR / "metadata" / "chapter-quote-links.yaml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    qdoc = load_yaml(QUOTES)
    quotes = qdoc.get("quotes") or []
    links: dict[str, list[str]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)

    for row in quotes:
        qid = row.get("quote_id")
        if not qid:
            continue
        for ch in row.get("chapter_ids") or ["ch01"]:
            if qid not in seen[ch]:
                seen[ch].add(qid)
                links[ch].append(qid)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"chapter_quote_links": dict(sorted(links.items()))},
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
