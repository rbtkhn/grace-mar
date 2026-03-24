#!/usr/bin/env python3
"""
CIV-MEM Memo Generator for work-jiang.
Generates structured analysis memos using the CIV-MEM-LENS.md lattice.
CIV-MEM = structure/seams: conditions, institutions, continuity, decline.
Paired with PSY-HIST (prediction/steering); use generate_dual_lenses.py for both.
Drafts land in analysis/pending/; review and run promote_reviewed_memo.py to promote.

Requires OPENAI_API_KEY (and optionally OPENAI_MODEL) in env.

Usage:
    python3 scripts/work_jiang/generate_civmem_memo.py --lecture civ-21
    python3 scripts/work_jiang/generate_civmem_memo.py --batch civ-22 civ-23 --delay 3
    python3 scripts/work_jiang/generate_civmem_memo.py --lecture geo-12 --dry-run
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
CIVMEM_LENS = WORK_JIANG / "CIV-MEM-LENS.md"
PENDING_DIR = WORK_JIANG / "analysis" / "pending"
MAX_CONTENT_CHARS = 12000

PROMPT_TEMPLATE = """You are an operator applying the strict CIV-MEM lens to a Jiang lecture.

Lecture content:
{lecture_content}

CIV-MEM Lattice (apply rigorously to every slot):
{lattice_content}

Output ONLY a valid Markdown file with this exact frontmatter + structure:

---
title: CIV-MEM Analysis - {lecture_id}
lecture_id: {lecture_id}
video_id: {video_id}
date: {today}
review_status: draft
tags: [civ-mem, analysis]
---

## Thesis / Aim (one sentence)
...

## CIV-MEM Lattice
### Conditions
...

### Institutions
...

### Seams / Friction
...

### Continuity / Memory
...

### Time Structure
...

### Decline / Stress Vectors
...

## Key Claims (tagged)
- [observation/interpretation/forecast] ...

## Tensions & Open Questions
...

## Prediction Seeds & Divergence Flags
...

## Placement in Predictive History Volume II
...

Human review required before promotion.
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
    output_path = PENDING_DIR / f"{source_id}-civmem-analysis.md"

    if dry_run:
        content_len = len(lecture_path.read_text(encoding="utf-8"))
        trunc_len = min(content_len, MAX_CONTENT_CHARS)
        print(f"dry-run: would generate {output_path}")
        print(f"  lecture: {lecture_path} ({content_len} chars, truncate to {trunc_len})")
        print(f"  video_id: {video_id}")
        return True

    # Load lens from disk
    if not CIVMEM_LENS.exists():
        print(f"❌ CIV-MEM-LENS.md not found: {CIVMEM_LENS}", file=sys.stderr)
        return False
    lattice_content = CIVMEM_LENS.read_text(encoding="utf-8")

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
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a precise analytic operator."},
            {"role": "user", "content": prompt},
        ],
    )
    memo_text = (response.choices[0].message.content or "").strip()

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(memo_text, encoding="utf-8")

    print(f"✅ Generated draft memo → {output_path}")
    print(f"   Review it, then run: python3 scripts/work_jiang/promote_reviewed_memo.py --id {source_id} --lens civ-mem")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CIV-MEM analysis memo")
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
