#!/usr/bin/env python3
"""
PSY-HIST Memo Generator for work-jiang.
Generates structured analysis memos using the PSY-HIST-LENS.md lattice.
PSY-HIST = prediction/steering: macro variables, cycle phase, Seldon crisis, levers.
Paired with CIV-MEM (structure/seams); use generate_dual_lenses.py for both.
Drafts land in analysis/pending/.

Requires OPENAI_API_KEY (and optionally OPENAI_MODEL) in env.

Usage:
    python3 scripts/work_jiang/generate_psy_hist_memo.py --lecture geo-12
    python3 scripts/work_jiang/generate_psy_hist_memo.py --batch civ-21 civ-22 --delay 3
    python3 scripts/work_jiang/generate_psy_hist_memo.py --lecture civ-60 --dry-run
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

_WJ = Path(__file__).resolve().parent
ROOT = _WJ.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
SOURCES_YAML = WORK_JIANG / "metadata" / "sources.yaml"
PSYHIST_LENS = WORK_JIANG / "PSY-HIST-LENS.md"
PENDING_DIR = WORK_JIANG / "analysis" / "pending"
MAX_CONTENT_CHARS = 14000

PROMPT_TEMPLATE = """You are a precise operator applying the strict PSY-HIST-LENS to a Jiang Xueqin lecture.

Lecture content:
{lecture_content}

Apply the PSY-HIST-LENS.md lattice rigorously. Use the exact examples and style from the lens file as guidance.
{lattice_content}

Output ONLY a valid Markdown file with this exact frontmatter and structure (no extra text, no explanations):

---
title: PSY-HIST Analysis - {lecture_id}
lecture_id: {lecture_id}
video_id: {video_id}
date: {today}
review_status: draft
tags: [psy-hist, analysis, predictive-history]
---

## Thesis / Aim (one sentence from the lecture)

## PSY-HIST Lattice

### Macro Variables (Turchin-style)

### Psychological Inertia / Collective Memory Effects

### Cycle Phase Detection

### Seldon Crisis Identification

### Predictability Horizon vs Chaos Boundaries

### Steering Levers (Intervention Points)

### Validation Protocol

## Key PSY-HIST Claims (tagged)
- [macro-var / inertia / cycle-phase / seldon-crisis / lever] ...

## Tensions & Open Questions

## Prediction Seeds & Divergence Flags
- Explicit forecasts with horizon and confidence (0–100)

## Placement in Predictive History

## Integrated Operator Thesis (with CIV-MEM)
One-paragraph synthesis (leave empty if CIV-MEM memo not yet available).

Human review required before promotion to the main analysis/ folder.
"""


def load_sources() -> list[dict]:
    if not SOURCES_YAML.exists():
        return []
    with SOURCES_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return (data or {}).get("sources", [])


def resolve_source(source_id: str) -> dict | None:
    sources = load_sources()
    for s in sources:
        if s.get("source_id") == source_id:
            return s
    return None


def truncate_at_word_boundary(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(maxsplit=1)[0]
    return cut + "\n\n[Truncated for context window]"


def generate_memo(source_id: str, *, dry_run: bool = False) -> bool:
    source = resolve_source(source_id)
    if not source:
        print(f"❌ Source not found: {source_id} (check sources.yaml)", file=sys.stderr)
        return False

    lecture_path = WORK_JIANG / source["lecture_path"]
    if not lecture_path.exists():
        print(f"❌ Lecture file not found: {lecture_path}", file=sys.stderr)
        return False

    video_id = source.get("video_id") or ""
    output_path = PENDING_DIR / f"{source_id}-psy-hist-analysis.md"

    if dry_run:
        content_len = len(lecture_path.read_text(encoding="utf-8"))
        trunc_len = min(content_len, MAX_CONTENT_CHARS)
        print(f"dry-run: would generate {output_path}")
        print(f"  lecture: {lecture_path} ({content_len} chars, truncate to {trunc_len})")
        print(f"  video_id: {video_id}")
        return True

    # Load lens from disk
    if not PSYHIST_LENS.exists():
        print(f"❌ PSY-HIST-LENS.md not found: {PSYHIST_LENS}", file=sys.stderr)
        return False
    lattice_content = PSYHIST_LENS.read_text(encoding="utf-8")

    content = lecture_path.read_text(encoding="utf-8")
    content = truncate_at_word_boundary(content, MAX_CONTENT_CHARS)

    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
        load_dotenv(ROOT / "bot" / ".env")
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except ImportError as e:
        print(f"❌ Missing dependency: {e}", file=sys.stderr)
        return False

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    prompt = PROMPT_TEMPLATE.format(
        lecture_content=content,
        lattice_content=lattice_content,
        lecture_id=source_id,
        video_id=video_id,
        today=datetime.now().strftime("%Y-%m-%d"),
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0.25,
        max_tokens=2500,
        messages=[
            {"role": "system", "content": "You are a rigorous analytic operator inside the Grace-Mar work-jiang membrane."},
            {"role": "user", "content": prompt},
        ],
    )
    memo_text = (response.choices[0].message.content or "").strip()

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(memo_text, encoding="utf-8")

    print(f"✅ PSY-HIST draft memo generated → {output_path}")
    print(f"   Next: Review the file, set `review_status: approved`, then run:")
    print(f"   python3 scripts/work_jiang/promote_reviewed_memo.py --id {source_id} --lens psy-hist")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PSY-HIST analysis memo")
    parser.add_argument("--lecture", type=str, help="Source ID, e.g. civ-21, geo-12")
    parser.add_argument("--batch", nargs="*", help="Multiple source IDs")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; no LLM call")
    parser.add_argument("--delay", type=float, default=2.5, help="Seconds between batch items (default 2.5)")
    args = parser.parse_args()

    ids = []
    if args.batch:
        ids = args.batch
    elif args.lecture:
        ids = [args.lecture]
    else:
        print("Error: Provide --lecture or --batch", file=sys.stderr)
        return 1

    ok = 0
    for i, sid in enumerate(ids):
        if i > 0 and not args.dry_run:
            time.sleep(args.delay)
        if generate_memo(sid, dry_run=args.dry_run):
            ok += 1

    return 0 if ok == len(ids) else 1


if __name__ == "__main__":
    raise SystemExit(main())
