#!/usr/bin/env python3
"""Generate counterfactual red-team findings for history-notebook chapters.

Output:
- research/REDTEAM-FINDINGS.md

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
    / "REDTEAM-FINDINGS.md"
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


def extract_claims(chapter_file: Path, title: str) -> list[str]:
    if not chapter_file.is_file():
        return [f"{title}: principal claim still unexpressed in draft prose."]
    raw = chapter_file.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("*("):
            continue
        lines.append(s)
    text = " ".join(lines)
    sents = [s.strip() for s in SENTENCE_SPLIT.split(text) if len(s.strip()) > 20]
    if not sents:
        return [f"{title}: principal claim still unexpressed in draft prose."]
    return sents[:1]


def classify_claim(claim: str, anchors: list[str], status: str, cfg: dict) -> tuple[str, str]:
    heur = (cfg.get("redteam") or {}).get("heuristics") or {}
    supported_cfg = heur.get("supported") or {}
    disputed_cfg = heur.get("disputed") or {}
    weak_cfg = heur.get("weakly_supported") or {}
    trigger_terms = [str(t).lower() for t in (disputed_cfg.get("trigger_terms") or [])]
    claim_l = claim.lower()

    if len(anchors) >= int(supported_cfg.get("min_hnsrc", 2)) and status in {"drafted", "in-progress"}:
        return ("supported", "Anchoring depth and chapter maturity are acceptable for MVP.")
    if any(t in claim_l for t in trigger_terms):
        return ("disputed", "Absolute language detected; requires narrower scope and counter-evidence.")
    if len(anchors) <= int(weak_cfg.get("max_hnsrc", 1)):
        return ("weakly-supported", "Insufficient shelf anchoring for strong confidence.")
    return ("disputed", "Competing interpretations likely; add explicit rival thesis test.")


def counterclaims_for(claim: str, n: int) -> list[str]:
    seeds = [
        "Alternative explanation: the observed outcome is better explained by institutional inertia than by elite intent.",
        "Alternative explanation: external systems pressure (trade, war, ecology) drives the result more than civilizational design.",
        "Alternative explanation: chronology may be over-compressed; sequence effects could reverse causal priority.",
    ]
    if n <= len(seeds):
        return seeds[:n]
    return seeds + [seeds[-1]] * (n - len(seeds))


def build_markdown(rows: list[dict], findings: list[dict]) -> str:
    lines = [
        "# Counterfactual red-team findings (generated)",
        "",
        "**Do not edit by hand.**",
        "Regenerate: `python3 scripts/build_hn_redteam_findings.py`",
        "",
        "Labels: `supported | disputed | weakly-supported`.",
        "",
        "## Coverage summary",
        "",
        f"- Chapters covered: `{len(rows)}`",
        f"- Findings generated: `{len(findings)}`",
        "",
    ]
    counts = {"supported": 0, "disputed": 0, "weakly-supported": 0}
    for f in findings:
        counts[f["classification"]] += 1
    lines.append(
        f"- Classification split: supported `{counts['supported']}`, disputed `{counts['disputed']}`, weakly-supported `{counts['weakly-supported']}`"
    )
    lines.append("")
    lines.append("## Findings by chapter")
    lines.append("")
    for f in findings:
        lines.extend(
            [
                f"### {f['finding_id']}",
                f"- `chapter_id`: `{f['chapter_id']}`",
                f"- `classification`: `{f['classification']}`",
                f"- `claim`: {f['claim']}",
                f"- `counterclaims`:",
            ]
        )
        for cc in f["counterclaims"]:
            lines.append(f"  - {cc}")
        lines.append(f"- `remediation`: {f['remediation']}")
        lines.append(
            f"- `supporting_hnsrc`: {', '.join(f'`{x}`' for x in f['supporting_hnsrc']) if f['supporting_hnsrc'] else '*(none)*'}"
        )
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

    cfg = load_yaml(args.config)
    per_claim = int((cfg.get("redteam") or {}).get("per_chapter_counterclaims", 2))
    rows = chapter_rows(load_yaml(args.architecture))
    anchors = anchor_map(load_yaml(args.catalog))

    findings: list[dict] = []
    for row in rows:
        hid = row["id"]
        chapter_path = (
            REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / row["file"]
            if row["file"]
            else Path("/dev/null")
        )
        claims = extract_claims(chapter_path, row["title"])
        # MVP requirement: at least one challenge per chapter.
        claim = claims[0]
        ch_anchors = anchors.get(hid, [])
        label, rationale = classify_claim(claim, ch_anchors, row["status"], cfg)
        findings.append(
            {
                "finding_id": f"{hid}-r01",
                "chapter_id": hid,
                "classification": label,
                "claim": claim,
                "counterclaims": counterclaims_for(claim, per_claim),
                "remediation": rationale,
                "supporting_hnsrc": ch_anchors[:5],
            }
        )

    findings.sort(key=lambda x: x["chapter_id"])
    content = build_markdown(rows, findings)

    if args.check:
        if not args.out.is_file():
            print(f"CHECK: missing {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_redteam_findings.py", file=sys.stderr)
            return 1
        if args.out.read_text(encoding="utf-8") != content:
            print(f"CHECK: stale {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_redteam_findings.py", file=sys.stderr)
            return 1
        print("ok: hn red-team findings up to date")
        return 0

    args.out.write_text(content, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
