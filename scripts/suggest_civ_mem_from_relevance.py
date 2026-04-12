#!/usr/bin/env python3
"""
Read-only helper: suggest primary MEMs from upstream MEM–RELEVANCE–X.md,
grouped by a lightweight tri-frame heuristic (Barnes / Mearsheimer / Mercouris).

Does not modify the Record. Requires a local civilization_memory checkout:
  research/repos/civilization_memory/content/civilizations/<ENTITY>/MEM–RELEVANCE–<ENTITY>.md

Usage:
  python3 scripts/suggest_civ_mem_from_relevance.py
  python3 scripts/suggest_civ_mem_from_relevance.py RUSSIA
  python3 scripts/suggest_civ_mem_from_relevance.py PERSIA --max-per-section 3
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CIV_BASE = REPO_ROOT / "research" / "repos" / "civilization_memory" / "content" / "civilizations"

# Heuristic keywords → tri-frame column (see CIV-MEM-TRI-FRAME-ROUTING.md).
MEARSHEIMER_KEYS = (
    "attrition",
    "endurance",
    "geo",
    "nuclear",
    "alliance",
    "steppe",
    "sea",
    "balance",
    "border",
    "black sea",
    "war",
    "operational",
)
BARNES_KEYS = (
    "fiscal",
    "law",
    "morale",
    "defection",
    "serfdom",
    "liability",
    "mechanism",
    "economic",
    "emancipation",
    "sanction",
    "collapse",
)
MERCOURIS_KEYS = (
    "narrative",
    "diplomacy",
    "civilizational",
    "orthodox",
    "information",
    "culture",
    "legitimacy",
    "identity",
)

SECTION_TITLE = re.compile(r"^([IVXLCDM]+)\.\s+(.+)$")
MEM_TOKEN = re.compile(r"^[\u2022\-\*]\s*(MEM[–-][A-Za-z0-9–\-]+)")


def _score_title(title: str) -> tuple[str, int]:
    t = title.lower()
    scores: dict[str, int] = {"mearsheimer": 0, "barnes": 0, "mercouris": 0}
    for k in MEARSHEIMER_KEYS:
        if k in t:
            scores["mearsheimer"] += 1
    for k in BARNES_KEYS:
        if k in t:
            scores["barnes"] += 1
    for k in MERCOURIS_KEYS:
        if k in t:
            scores["mercouris"] += 1
    best = max(scores, key=lambda x: scores[x])
    if scores[best] == 0:
        return "mearsheimer", 0
    return best, scores[best]


def _parse_relevance(path: Path, max_per_section: int) -> tuple[list[tuple[str, str, list[str]]], list[str]]:
    """
    Returns (sections as (roman, title, primary_mem_ids)), and parse warnings.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    warnings: list[str] = []
    sections: list[tuple[str, str, list[str]]] = []
    i = 0
    while i < len(lines):
        m = SECTION_TITLE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        roman, title = m.group(1), m.group(2).strip()
        primaries: list[str] = []
        in_primary = False
        i += 1
        while i < len(lines):
            if SECTION_TITLE.match(lines[i].strip()):
                break
            low = lines[i].strip().lower()
            if low.startswith("primary mems:"):
                in_primary = True
                i += 1
                continue
            if low.startswith("secondary mems:") or low.startswith("secondary mems"):
                in_primary = False
                i += 1
                continue
            if in_primary:
                mm = MEM_TOKEN.match(lines[i].strip())
                if mm:
                    tok = mm.group(1).replace("-", "–")
                    if tok not in primaries:
                        primaries.append(tok)
            i += 1
        if primaries:
            sections.append((roman, title, primaries[:max_per_section]))
        continue
    if not sections:
        warnings.append("No sections with Primary MEMs parsed — file layout may differ from expected.")
    return sections, warnings


def _emit_markdown(entity: str, path: Path, max_per_section: int) -> str:
    sections, warnings = _parse_relevance(path, max_per_section)
    by_mind: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for roman, title, mems in sections:
        mind, _ = _score_title(title)
        for mem in mems:
            by_mind[mind].append((roman, title, mem))

    out: list[str] = [
        f"# MEM suggestions from MEM–RELEVANCE–{entity}",
        "",
        f"_Source: `{path.relative_to(REPO_ROOT)}`_",
        "",
        "Heuristic mapping only — confirm against [CIV-MEM-TRI-FRAME-ROUTING.md]"
        "(docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md).",
        "",
    ]
    for w in warnings:
        out.append(f"_{w}_")
        out.append("")
    labels = {
        "mearsheimer": "Mearsheimer (geo / incentives / attrition)",
        "barnes": "Barnes (mechanism / liability / defection)",
        "mercouris": "Mercouris (narrative / diplomacy / civilizational story)",
    }
    for key in ("mearsheimer", "barnes", "mercouris"):
        out.append(f"## {labels[key]}")
        out.append("")
        rows = by_mind.get(key, [])
        if not rows:
            out.append(f"_No primary MEMs bucketed here (heuristic)._")
        else:
            seen: set[str] = set()
            for roman, title, mem in rows:
                if mem in seen:
                    continue
                seen.add(mem)
                out.append(f"- **{mem}** — §{roman} {title}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Suggest MEMs from MEM–RELEVANCE index (read-only).")
    ap.add_argument("entity", nargs="?", default="RUSSIA", help="Civilization folder name (default RUSSIA)")
    ap.add_argument(
        "--max-per-section",
        type=int,
        default=2,
        metavar="N",
        help="Max primary MEM lines to take per section (default 2)",
    )
    args = ap.parse_args()
    entity = str(args.entity).strip().upper()
    path = CIV_BASE / entity / f"MEM–RELEVANCE–{entity}.md"
    if not path.is_file():
        print(f"error: file not found: {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        print("Clone upstream civilization_memory (see docs/ci/README.md).", file=sys.stderr)
        return 1
    sys.stdout.write(_emit_markdown(entity, path, max(1, args.max_per_section)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
