#!/usr/bin/env python3
"""Generate provenance claim packets for all history-notebook chapters.

Output:
- research/PROVENANCE-PACKETS.md

Rules:
- No high confidence without >=1 HNSRC anchor and non-empty evidence note.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
ARCH_PATH = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "book-architecture.yaml"
CATALOG_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
CONFIG_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "AGENTIC-MVP-CONFIG.yaml"
)
OUT_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "PROVENANCE-PACKETS.md"
)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def chapter_rows(arch: dict) -> list[dict]:
    rows = []
    for c in arch.get("chapters") or []:
        if isinstance(c, dict) and c.get("id"):
            rows.append(
                {
                    "id": str(c["id"]),
                    "title": str(c.get("title") or ""),
                    "status": str(c.get("status") or "unknown"),
                    "file": str(c.get("file") or "").strip(),
                }
            )
    return rows


def anchor_map(catalog: dict) -> dict[str, list[str]]:
    by_hn: dict[str, list[str]] = {}
    for item in catalog.get("items") or []:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("id") or "").strip()
        for ch in item.get("candidate_hn_chapters") or []:
            if isinstance(ch, str):
                by_hn.setdefault(ch, []).append(sid)
    for ch in by_hn:
        by_hn[ch] = sorted(set(by_hn[ch]))
    return by_hn


def chapter_claim_texts(chapter_file: Path, title: str, max_claims: int) -> list[str]:
    if not chapter_file.is_file():
        return [f"{title}: draft is not yet written; claim extraction pending authored prose."]
    raw = chapter_file.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("*("):
            continue
        lines.append(s)
    text = " ".join(lines)
    if not text:
        return [f"{title}: prose remains skeletal; add source-backed claims before publication."]
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(text) if len(s.strip()) > 20]
    if not sentences:
        return [f"{title}: prose remains skeletal; add source-backed claims before publication."]
    return sentences[:max_claims]


def classify_confidence(anchor_count: int, evidence_note: str, open_tasks: int, rules: dict) -> str:
    high = rules.get("high") or {}
    med = rules.get("medium") or {}
    if (
        anchor_count >= int(high.get("min_hnsrc", 1))
        and bool(evidence_note.strip()) == bool(high.get("requires_nonempty_evidence_note", True))
        and open_tasks <= int(high.get("max_open_tasks", 1))
    ):
        return "high"
    if anchor_count >= int(med.get("min_hnsrc", 1)) and open_tasks <= int(med.get("max_open_tasks", 3)):
        return "medium"
    return "low"


def build_markdown(rows: list[dict], packets: list[dict]) -> str:
    lines = [
        "# Provenance packets (generated)",
        "",
        "**Do not edit by hand.**",
        "Regenerate: `python3 scripts/build_hn_provenance_packets.py`",
        "",
        "Schema: `claim_id`, `chapter_id`, `claim_text`, `supporting_hnsrc[]`, `evidence_note`, `confidence`, `open_verification_tasks[]`.",
        "",
        "## Coverage summary",
        "",
        f"- Chapters covered: `{len(rows)}`",
        f"- Claim packets generated: `{len(packets)}`",
        "",
    ]
    conf_counts = {"high": 0, "medium": 0, "low": 0}
    for p in packets:
        conf_counts[p["confidence"]] += 1
    lines.append(
        f"- Confidence split: high `{conf_counts['high']}`, medium `{conf_counts['medium']}`, low `{conf_counts['low']}`"
    )
    lines.append("")
    lines.append("## Packets")
    lines.append("")
    for p in packets:
        lines.extend(
            [
                f"### {p['claim_id']}",
                f"- `chapter_id`: `{p['chapter_id']}`",
                f"- `claim_text`: {p['claim_text']}",
                f"- `supporting_hnsrc`: {', '.join(f'`{x}`' for x in p['supporting_hnsrc']) if p['supporting_hnsrc'] else '*(none)*'}",
                f"- `evidence_note`: {p['evidence_note']}",
                f"- `confidence`: `{p['confidence']}`",
                "- `open_verification_tasks`:",
            ]
        )
        for t in p["open_verification_tasks"]:
            lines.append(f"  - {t}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--architecture", type=Path, default=ARCH_PATH)
    ap.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    ap.add_argument("--config", type=Path, default=CONFIG_PATH)
    ap.add_argument("--out", type=Path, default=OUT_PATH)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    for p in (args.architecture, args.catalog, args.config):
        if not p.is_file():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 1

    arch = load_yaml(args.architecture)
    rows = chapter_rows(arch)
    if not rows:
        print("ERROR: no chapters found in book-architecture", file=sys.stderr)
        return 1
    anchors = anchor_map(load_yaml(args.catalog))
    cfg = load_yaml(args.config)
    prov_cfg = (cfg.get("provenance") or {})
    conf_rules = prov_cfg.get("confidence_rules") or {}
    defaults = prov_cfg.get("default_open_verification_tasks") or []
    max_claims = int(prov_cfg.get("max_claims_per_chapter", 3))

    packets: list[dict] = []
    for r in rows:
        hid = r["id"]
        chapter_path = (
            REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / r["file"]
            if r["file"]
            else Path("/dev/null")
        )
        claims = chapter_claim_texts(chapter_path, r["title"], max_claims)
        supporting = anchors.get(hid, [])
        evidence_note = (
            f"Anchored to {len(supporting)} shelf source(s); verify one direct quote before publication."
            if supporting
            else "No direct HNSRC anchor mapped yet; packet is provisional."
        )
        for i, claim in enumerate(claims, start=1):
            open_tasks = list(defaults)
            if not supporting:
                open_tasks = [
                    "Map at least one `HNSRC-*` source to this chapter claim.",
                    "Add one primary-source or specialist secondary reference.",
                ] + open_tasks
            confidence = classify_confidence(len(supporting), evidence_note, len(open_tasks), conf_rules)
            packets.append(
                {
                    "claim_id": f"{hid}-c{i:02d}",
                    "chapter_id": hid,
                    "claim_text": claim,
                    "supporting_hnsrc": supporting[:5],
                    "evidence_note": evidence_note,
                    "confidence": confidence,
                    "open_verification_tasks": open_tasks,
                }
            )

    content = build_markdown(rows, packets)
    if args.check:
        if not args.out.is_file():
            print(f"CHECK: missing {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_provenance_packets.py", file=sys.stderr)
            return 1
        if args.out.read_text(encoding="utf-8") != content:
            print(f"CHECK: stale {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_provenance_packets.py", file=sys.stderr)
            return 1
        print("ok: hn provenance packets up to date")
        return 0

    args.out.write_text(content, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
