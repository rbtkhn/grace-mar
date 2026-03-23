"""Validate concept dictionary, claims ledger, thesis links, and evidence packs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"


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


def main() -> int:
    errors: list[str] = []

    thesis = load_yaml(WORK_DIR / "metadata" / "thesis-map.yaml").get("thesis") or {}
    subclaims = thesis.get("subclaims") or []
    claim_rows = load_claims()
    claim_by_id = {r["claim_id"]: r for r in claim_rows if r.get("claim_id")}

    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources") or []
    src_by = {s["source_id"]: s for s in sources}

    for sc in subclaims:
        sid = sc.get("id")
        lc = sc.get("linked_claim_ids") or []
        if not lc:
            errors.append(f"Thesis subclaim {sid} has no linked_claim_ids")
        for cid in lc:
            if cid not in claim_by_id:
                errors.append(f"Thesis {sid} references unknown claim_id {cid}")

    for r in claim_rows:
        cid = r.get("claim_id")
        src = r.get("source_id")
        if not src:
            errors.append(f"Claim {cid} missing source_id")
            continue
        if src not in src_by:
            errors.append(f"Claim {cid} unknown source_id {src}")
        st = r.get("status") or ""
        ana = r.get("analysis_id")
        reg = src_by.get(src) if src in src_by else {}
        analysis_complete = (reg.get("status") or {}).get("analysis") == "complete"
        if st == "supported" and analysis_complete and not ana:
            errors.append(f"Claim {cid} marked supported but analysis_id empty while source has analysis")

    arch = load_yaml(WORK_DIR / "metadata" / "book-architecture.yaml")
    chapters = (arch.get("book") or {}).get("chapters") or []
    for ch in chapters:
        cid = ch.get("id")
        if not cid:
            continue
        pack = WORK_DIR / "evidence-packs" / f"{cid}.md"
        if not pack.exists():
            errors.append(f"Missing evidence pack for {cid}: {pack.relative_to(WORK_DIR)}")
        text = pack.read_text(encoding="utf-8") if pack.exists() else ""
        for m in re.findall(r"`(geo-\d\d)`", text):
            if m not in src_by:
                errors.append(f"Evidence pack {cid} references unknown source {m}")
        for m in re.findall(r"`(clm-\d+)`", text):
            if m not in claim_by_id:
                errors.append(f"Evidence pack {cid} references unknown claim {m}")
        if text:
            if len(re.findall(r"`geo-\d\d`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no source ids (expected at least one)")
            if len(re.findall(r"`clm-\d+`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no claim ids (expected at least one)")

    claim_chapter_gaps = [r for r in claim_rows if not r.get("chapter_candidates")]
    for r in claim_chapter_gaps:
        errors.append(f"Claim {r.get('claim_id')} missing chapter_candidates")

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
