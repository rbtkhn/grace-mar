"""Emit metadata/thesis-claim-links.yaml from thesis-map.yaml linked_claim_ids + validate claims exist."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
THESIS = WORK_DIR / "metadata" / "thesis-map.yaml"
CLAIMS = WORK_DIR / "claims" / "registry" / "claims.jsonl"
OUT = WORK_DIR / "metadata" / "thesis-claim-links.yaml"


def load_claim_ids() -> set[str]:
    ids: set[str] = set()
    if not CLAIMS.exists():
        return ids
    with CLAIMS.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            ids.add(row.get("claim_id", ""))
    return ids


def main() -> int:
    thesis = yaml.safe_load(THESIS.read_text(encoding="utf-8")) or {}
    sub = (thesis.get("thesis") or {}).get("subclaims") or []
    valid_ids = load_claim_ids()
    links: dict[str, list[str]] = {}
    errors: list[str] = []

    for sc in sub:
        sid = sc.get("id")
        lc = sc.get("linked_claim_ids") or []
        if not sid:
            continue
        links[sid] = list(lc)
        if not lc:
            errors.append(f"Subclaim {sid} has empty linked_claim_ids")
        for cid in lc:
            if cid not in valid_ids:
                errors.append(f"Unknown claim_id {cid} referenced by {sid}")

    doc = {"thesis_claim_links": links, "weak_support": []}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {OUT}")

    for e in errors:
        print(f"WARNING: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
