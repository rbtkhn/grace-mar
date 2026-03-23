"""Emit metadata/counter-reading-links.yaml from counter-readings.jsonl."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
REG = WORK_DIR / "counter-readings" / "registry" / "counter-readings.jsonl"
OUT = WORK_DIR / "metadata" / "counter-reading-links.yaml"


def main() -> int:
    chapter_links: dict[str, list[str]] = defaultdict(list)
    thesis_links: dict[str, list[str]] = defaultdict(list)
    claim_links: dict[str, list[str]] = defaultdict(list)
    concept_links: dict[str, list[str]] = defaultdict(list)

    with REG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            cid = r.get("counter_id")
            if not cid:
                continue
            tt = r.get("target_type")
            tid = r.get("target_id")
            if not tid:
                continue
            if tt == "chapter":
                chapter_links[tid].append(cid)
            elif tt == "thesis_subclaim":
                thesis_links[tid].append(cid)
            elif tt == "claim":
                claim_links[tid].append(cid)
            elif tt == "concept":
                concept_links[tid].append(cid)

    def sort_map(m: dict[str, list[str]]) -> dict[str, list[str]]:
        return {k: sorted(v) for k, v in sorted(m.items())}

    payload = {
        "chapter_links": sort_map(chapter_links),
        "thesis_links": sort_map(thesis_links),
        "claim_links": sort_map(claim_links),
        "concept_links": sort_map(concept_links),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
