#!/usr/bin/env python3
"""Validate strategy-expert-*-thread.md Segment 1 month blocks (WORK only).

Segment 1 is a **narrative journal** (see ``strategy-expert-template.md``): default
expectation is **readable prose**, with optional ``## YYYY-MM`` sections. Month-scale
**bullet ledgers** (strength-tagged hooks) are allowed as *compressed* material, but
they must not be treated as a substitute for prose without operator intent.

This script **warns** (stderr) when:

- a ``## YYYY-MM`` block has **three or more** list lines and **no** detected prose
  lines (bullets-only months), **or**
- a ``## YYYY-MM`` block has **fewer than 500 words** of detected prose (words on
  ``is_prose_line`` lines only; list lines do not count).

**Opt-out (whole file):** place anywhere in the human layer (above
``<!-- strategy-expert-thread:start -->``)::

    <!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->

Exit 0 by default (warnings do not fail). Use ``--strict`` to exit 1 if any warning.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"

RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")
RE_BACKFILL_START = re.compile(r"^<!--\s*backfill:")
RE_LIST = re.compile(r"^\s*[-*]\s+\S")
RE_NUM_LIST = re.compile(r"^\s*\d+\.\s+\S")

OPT_OUT_BULLETS_LEDGER = "<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->"

MIN_PROSE_WORDS = 500


def expert_id_from_thread_name(name: str) -> str | None:
    m = re.match(r"^strategy-expert-(.+)-thread\.md$", name)
    return m.group(1) if m else None


def extract_human_layer(thread_text: str) -> str:
    if THREAD_MARKER_START in thread_text:
        return thread_text.split(THREAD_MARKER_START, 1)[0].rstrip()
    return thread_text.rstrip()


def strip_backfill_block(text: str, expert_id: str) -> str:
    start = f"<!-- backfill:{expert_id}:start -->"
    end = f"<!-- backfill:{expert_id}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    out = pattern.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def is_prose_line(line: str) -> bool:
    s = line.strip()
    if len(s) < 12:
        return False
    if s.startswith("#"):
        return False
    if s == "---":
        return False
    if RE_LIST.match(line):
        return False
    if RE_NUM_LIST.match(line):
        return False
    if s.startswith(">"):
        return False
    return True


def iter_month_h2_bodies(human: str) -> list[tuple[str, str]]:
    """Split human layer on ``## YYYY-MM`` headings; return (id, body) pairs."""
    lines = human.splitlines()
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        m = RE_MONTH_H2.match(lines[i])
        if not m:
            i += 1
            continue
        month_id = m.group(1)
        i += 1
        body_lines: list[str] = []
        while i < len(lines):
            if RE_MONTH_H2.match(lines[i]):
                break
            if RE_BACKFILL_START.match(lines[i].strip()):
                break
            body_lines.append(lines[i])
            i += 1
        blocks.append((month_id, "\n".join(body_lines)))
    return blocks


def analyze_month_body(body: str) -> tuple[int, int]:
    """Return (bullet_line_count, prose_line_count) for non-empty substantive lines."""
    bullet = 0
    prose = 0
    for line in body.splitlines():
        if not line.strip():
            continue
        if RE_LIST.match(line) or RE_NUM_LIST.match(line):
            bullet += 1
        elif is_prose_line(line):
            prose += 1
    return bullet, prose


def prose_word_count(body: str) -> int:
    """Word count on prose lines only (same rule as ``is_prose_line``)."""
    n = 0
    for line in body.splitlines():
        if is_prose_line(line):
            n += len(line.split())
    return n


def validate_thread_file(path: Path) -> list[str]:
    """Return warning strings for one thread file."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    eid = expert_id_from_thread_name(path.name)
    if not eid:
        return [f"unexpected filename (expected strategy-expert-<id>-thread.md): {path.name}"]

    human = extract_human_layer(text)
    if OPT_OUT_BULLETS_LEDGER in human:
        return []

    human = strip_backfill_block(human, eid)

    for month_id, body in iter_month_h2_bodies(human):
        bullets, prose_lines = analyze_month_body(body)
        words = prose_word_count(body)
        if bullets >= 3 and prose_lines == 0:
            warnings.append(
                f"{path.name}: ## {month_id} — bullet-led month with no prose lines "
                f"({bullets} list lines). Add a short prose lede or "
                f"{OPT_OUT_BULLETS_LEDGER} if ledger-only is intentional "
                f"(see strategy-expert-template.md — Segment 1 narrative journal)."
            )
        elif words < MIN_PROSE_WORDS:
            warnings.append(
                f"{path.name}: ## {month_id} — prose word count {words} < {MIN_PROSE_WORDS} "
                f"(prose lines only; expand narrative or run "
                f"`python3 scripts/expand_strategy_expert_segment_prose.py --apply`)."
            )
    return warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir",
        type=Path,
        default=NOTEBOOK_DIR,
        help="Directory containing strategy-expert-*-thread.md files",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 if any warning is emitted.",
    )
    args = ap.parse_args()

    paths = sorted(args.dir.glob("strategy-expert-*-thread.md"))
    if not paths:
        print("error: no strategy-expert-*-thread.md files found", file=sys.stderr)
        return 1

    all_warnings: list[str] = []
    for path in paths:
        all_warnings.extend(validate_thread_file(path))

    for w in all_warnings:
        print(f"warning: {w}", file=sys.stderr)

    if all_warnings:
        print(
            f"strategy expert threads: {len(all_warnings)} Segment 1 month warning(s) "
            f"in {len(paths)} file(s) — see stderr",
            file=sys.stderr,
        )
        if args.strict:
            return 1
    else:
        print(f"ok: {len(paths)} strategy expert thread file(s) — no Segment 1 month warnings")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
