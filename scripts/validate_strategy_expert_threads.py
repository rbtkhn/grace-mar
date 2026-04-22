#!/usr/bin/env python3
"""Validate strategy-expert-*-thread.md journal-layer month blocks (WORK only).

The **journal layer** (above ``<!-- strategy-expert-thread:start -->``) is a **narrative journal** (see ``strategy-expert-template.md``): default
expectation is **readable prose**, with optional ``## YYYY-MM`` sections. Month-scale
**bullet ledgers** (strength-tagged hooks) are allowed as *compressed* material, but
they must not be treated as a substitute for prose without operator intent.

This script **warns** (stderr) when:

- a ``## YYYY-MM`` block has **three or more** list lines and **no** detected prose
  lines (bullets-only months), **or**
- a ``## YYYY-MM`` block has **fewer than 500 words** of substantive text: **prose lines**
  (``is_prose_line``) **plus** words in **markdown blockquote** lines (``>`` …), matching
  **verbatim-forward** journal policy; list lines still do not count toward the threshold.

**Opt-out (whole file):** place anywhere in the human layer (above
``<!-- strategy-expert-thread:start -->``)::

    <!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->

**Opt-out (verbatim-forward / alternate journal discipline):** suppress month word-count
warnings for the whole file::

    <!-- strategy-expert-thread:verbatim-forward-journal-ok -->

Exit 0 by default (warnings do not fail). Use ``--strict`` to exit 1 if any warning.

**Month filter:** ``--month MM`` (``01``–``12``) checks only ``## YYYY-MM`` blocks whose month
matches **MM** (any year). Omit ``--month`` to validate **all** month segments (default).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

from strategy_expert_corpus import (  # noqa: E402
    collect_strategy_thread_paths,
    expert_id_from_thread_path,
)

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"

RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")
RE_BACKFILL_START = re.compile(r"^<!--\s*backfill:")
RE_LIST = re.compile(r"^\s*[-*]\s+\S")
RE_NUM_LIST = re.compile(r"^\s*\d+\.\s+\S")

OPT_OUT_BULLETS_LEDGER = "<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->"
OPT_OUT_VERBATIM_FORWARD = "<!-- strategy-expert-thread:verbatim-forward-journal-ok -->"

MIN_PROSE_WORDS = 500


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


def blockquote_word_count(body: str) -> int:
    """Word count on markdown blockquote lines (verbatim-forward months)."""
    n = 0
    for line in body.splitlines():
        if line.strip().startswith(">"):
            # strip leading '>' and optional space for counting
            stripped = line.lstrip()
            if stripped.startswith(">"):
                content = stripped[1:].lstrip()
                if content:
                    n += len(content.split())
    return n


def substantive_word_count(body: str) -> int:
    """Prose lines + blockquote words (architecture verbatim-forward policy)."""
    return prose_word_count(body) + blockquote_word_count(body)


def strategy_page_fence_word_count(body: str) -> int:
    """Words inside ``<!-- strategy-page:start`` … ``end`` --> blocks (thread-embedded pages)."""
    n = 0
    pos = 0
    while True:
        start = body.find("<!-- strategy-page:start", pos)
        if start == -1:
            break
        end = body.find("<!-- strategy-page:end", start)
        if end == -1:
            break
        chunk = body[start:end]
        n += len(chunk.split())
        pos = end + 1
    return n


def validate_thread_file(path: Path, month_mm: str | None = None) -> list[str]:
    """Return warning strings for one thread file.

    If ``month_mm`` is set (``01``–``12``), only ``## YYYY-MM`` blocks with that month are checked.
    """
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    eid = expert_id_from_thread_path(path)
    if not eid:
        return [
            "unexpected filename (expected experts/<id>/thread.md, "
            "experts/<id>/<id>-thread-YYYY-MM.md, or strategy-expert-<id>-thread*.md): "
            f"{path}"
        ]

    human = extract_human_layer(text)
    if OPT_OUT_BULLETS_LEDGER in human:
        return []

    skip_word_warnings = OPT_OUT_VERBATIM_FORWARD in human

    human = strip_backfill_block(human, eid)

    for month_id, body in iter_month_h2_bodies(human):
        if month_mm is not None:
            parts = month_id.split("-", 2)
            if len(parts) < 2 or parts[1] != month_mm:
                continue
        bullets, prose_lines = analyze_month_body(body)
        bq_words = blockquote_word_count(body)
        sp_words = strategy_page_fence_word_count(body)
        words = substantive_word_count(body) + sp_words
        if bullets >= 3 and prose_lines == 0 and bq_words < 50:
            warnings.append(
                f"{path.name}: ## {month_id} — bullet-led month with no prose lines "
                f"({bullets} list lines). Add a short prose lede, blockquoted expert text, or "
                f"{OPT_OUT_BULLETS_LEDGER} if ledger-only is intentional "
                f"(see strategy-expert-template.md — journal layer narrative)."
            )
        elif not skip_word_warnings and words < MIN_PROSE_WORDS:
            pw = prose_word_count(body)
            warnings.append(
                f"{path.name}: ## {month_id} — substantive word count {words} < {MIN_PROSE_WORDS} "
                f"(prose={pw}, blockquotes={bq_words}, strategy-page={sp_words}; expand narrative/quotes or run "
                f"`python3 scripts/expand_strategy_expert_segment_prose.py --apply`; "
                f"or {OPT_OUT_VERBATIM_FORWARD} to skip word-count warnings for this file)."
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
    ap.add_argument(
        "--month",
        metavar="MM",
        default=None,
        help="Only validate ## YYYY-MM segments for this month (01–12), any year.",
    )
    args = ap.parse_args()

    month_mm: str | None = args.month
    if month_mm is not None:
        if not re.fullmatch(r"(0[1-9]|1[0-2])", month_mm):
            print(
                "error: --month must be two digits 01–12 (e.g. --month 04)",
                file=sys.stderr,
            )
            return 1

    paths = collect_strategy_thread_paths(args.dir)
    if not paths:
        print(
            "error: no thread files found (experts|voices/*/thread.md, "
            "*/*-thread-YYYY-MM.md, strategy-expert-*-thread.md)",
            file=sys.stderr,
        )
        return 1

    all_warnings: list[str] = []
    for path in paths:
        all_warnings.extend(validate_thread_file(path, month_mm=month_mm))

    for w in all_warnings:
        print(f"warning: {w}", file=sys.stderr)

    if all_warnings:
        scope = f"month {month_mm}" if month_mm else "all months"
        print(
            f"strategy expert threads: {len(all_warnings)} journal-layer month warning(s) "
            f"({scope}) in {len(paths)} file(s) — see stderr",
            file=sys.stderr,
        )
        if args.strict:
            return 1
    else:
        scope = f" (month {month_mm} only)" if month_mm else ""
        print(
            f"ok: {len(paths)} strategy expert thread file(s) — "
            f"no journal-layer month warnings{scope}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
