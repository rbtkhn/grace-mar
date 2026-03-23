"""Render CONCEPT-DICTIONARY.md from metadata/concepts.yaml."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
META = WORK_DIR / "metadata" / "concepts.yaml"
OUT = WORK_DIR / "CONCEPT-DICTIONARY.md"


def norm_term(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(concepts: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_terms: set[str] = set()
    for c in concepts:
        cid = c.get("concept_id")
        term = c.get("term")
        if not cid:
            errors.append("concept missing concept_id")
            continue
        if cid in seen_ids:
            errors.append(f"duplicate concept_id: {cid}")
        seen_ids.add(cid)
        if term:
            nt = norm_term(term)
            if nt in seen_terms:
                errors.append(f"duplicate primary term (normalized): {term!r}")
            seen_terms.add(nt)
    return errors


def render(data: dict) -> str:
    concepts = data.get("concepts") or []
    lines = [
        "# Concept dictionary",
        "",
        "Recurring Jiang / Geo-Strategy vocabulary for the book-site lane. "
        "Machine source: `metadata/concepts.yaml`.",
        "",
    ]
    for c in concepts:
        cid = c.get("concept_id", "")
        lines += [
            f"## {cid}",
            "",
            f"- **Term:** {c.get('term', '')}",
        ]
        aliases = c.get("aliases") or []
        if aliases:
            lines.append(f"- **Aliases:** {', '.join(aliases)}")
        wd = (c.get("working_definition") or "").strip()
        if wd:
            lines.append(f"- **Working definition:** {wd}")
        sd = (c.get("stronger_definition") or "").strip()
        if sd:
            lines.append(f"- **Stronger definition:** {sd}")
        tens = c.get("tensions") or []
        if tens:
            lines.append("- **Tensions:**")
            for t in tens:
                lines.append(f"  - {t}")
        rel = c.get("related_concepts") or []
        if rel:
            lines.append(f"- **Related concepts:** {', '.join(rel)}")
        fss = c.get("first_seen_source_id")
        if fss:
            lines.append(f"- **First seen (source):** `{fss}`")
        src = c.get("source_ids") or []
        ana = c.get("analysis_ids") or []
        ch = c.get("chapter_ids") or []
        if src:
            lines.append(f"- **Sources:** {', '.join(f'`{s}`' for s in src)}")
        if ana:
            lines.append(f"- **Analysis (source ids):** {', '.join(f'`{a}`' for a in ana)}")
        if ch:
            lines.append(f"- **Chapter candidates:** {', '.join(f'`{x}`' for x in ch)}")
        lines.append(f"- **Status:** {c.get('status', 'draft')}")
        lines.append("")
    lines.append(
        "*Generated from `metadata/concepts.yaml` — run "
        "`python scripts/work_jiang/render_concept_dictionary.py` after edits.*"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = load(META)
    concepts = data.get("concepts") or []
    errors = validate(concepts)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    OUT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
