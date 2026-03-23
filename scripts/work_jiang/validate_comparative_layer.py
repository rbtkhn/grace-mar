"""Validate quotation bank links, counter-readings links, and intellectual chronology."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_claim_ids() -> set[str]:
    p = WORK_DIR / "claims" / "registry" / "claims.jsonl"
    ids: set[str] = set()
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                if r.get("claim_id"):
                    ids.add(r["claim_id"])
    return ids


def high_priority_analysis_chapters(arch: dict) -> list[str]:
    out = []
    for ch in (arch.get("book") or {}).get("chapters") or []:
        if ch.get("kind") == "analysis" and ch.get("priority") == "high":
            cid = ch.get("id")
            if cid:
                out.append(cid)
    return out


def main() -> int:
    errors: list[str] = []

    arch = load_yaml(WORK_DIR / "metadata" / "book-architecture.yaml")
    chapter_ids = {c.get("id") for c in (arch.get("book") or {}).get("chapters") or [] if c.get("id")}
    hp = high_priority_analysis_chapters(arch)

    concepts = load_yaml(WORK_DIR / "metadata" / "concepts.yaml")
    concept_ids = {c.get("concept_id") for c in (concepts.get("concepts") or []) if c.get("concept_id")}
    claim_ids = load_claim_ids()

    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources") or []
    geo_ids = {s["source_id"] for s in sources if (s.get("source_id") or "").startswith("geo-")}

    # Quotes + chapter links
    quotes_path = WORK_DIR / "metadata" / "quotes.yaml"
    if not quotes_path.exists():
        errors.append("Missing metadata/quotes.yaml")
    else:
        qdoc = load_yaml(quotes_path)
        quotes = qdoc.get("quotes") or []
        if len(quotes) < 50:
            errors.append(f"Expected at least 50 quotes, found {len(quotes)}")

        ql_path = WORK_DIR / "metadata" / "chapter-quote-links.yaml"
        if ql_path.exists():
            ql = load_yaml(ql_path).get("chapter_quote_links") or {}
            for ch in ql:
                if ch not in chapter_ids:
                    errors.append(f"chapter-quote-links.yaml unknown chapter {ch}")
            for ch in hp:
                n = len(ql.get(ch) or [])
                if n < 5:
                    errors.append(
                        f"High-priority analysis chapter {ch} has {n} linked quotes (need >= 5)"
                    )
        else:
            errors.append("Missing metadata/chapter-quote-links.yaml (run link_quotes_to_chapters.py)")

    # Counter-reading links
    cr_path = WORK_DIR / "metadata" / "counter-reading-links.yaml"
    if cr_path.exists():
        cr = load_yaml(cr_path)
        ch_links = cr.get("chapter_links") or {}
        for ch in ch_links:
            if ch not in chapter_ids:
                errors.append(f"counter-reading-links.yaml unknown chapter {ch}")
        for ch in hp:
            if len(ch_links.get(ch) or []) < 1:
                errors.append(
                    f"High-priority analysis chapter {ch} needs >=1 counter-reading in chapter_links"
                )
    else:
        errors.append("Missing metadata/counter-reading-links.yaml")

    # Chronology
    chrono_path = WORK_DIR / "metadata" / "chronology.yaml"
    if not chrono_path.exists():
        errors.append("Missing metadata/chronology.yaml")
    else:
        cdoc = load_yaml(chrono_path)
        periods = cdoc.get("periods") or []
        seen_geo: set[str] = set()
        union_geo: set[str] = set()
        any_concept_in_period = False
        for p in periods:
            pid = p.get("period_id") or "?"
            shifts = p.get("shifts") or []
            conts = p.get("continuities") or []
            if not shifts and not conts:
                errors.append(f"Period {pid} has empty shifts and continuities")
            for s in shifts + conts:
                if not (s or "").strip():
                    errors.append(f"Period {pid} contains an empty shift/continuity string")

            for cid in p.get("dominant_concepts") or []:
                any_concept_in_period = True
                if cid not in concept_ids:
                    errors.append(f"Period {pid} unknown dominant_concept {cid}")
            for cl in p.get("dominant_claims") or []:
                if cl not in claim_ids:
                    errors.append(f"Period {pid} unknown dominant_claim {cl}")

            for gid in p.get("source_ids") or []:
                if gid in seen_geo:
                    errors.append(f"Duplicate source_id {gid} across periods")
                seen_geo.add(gid)
                union_geo.add(gid)
                if gid not in geo_ids:
                    errors.append(f"Period {pid} unknown source_id {gid}")

        missing = geo_ids - union_geo
        extra = union_geo - geo_ids
        if missing:
            errors.append(f"Chronology missing geo sources: {sorted(missing)}")
        if extra:
            errors.append(f"Chronology has unknown geo ids: {sorted(extra)}")
        if not any_concept_in_period:
            errors.append("Chronology: no period lists a non-empty dominant_concepts")

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
