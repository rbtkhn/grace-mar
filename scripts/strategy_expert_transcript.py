#!/usr/bin/env python3
"""Triage inbox thread lines to per-expert transcript files (append + prune).

For each indexed expert, extracts ``thread:<expert_id>`` lines from
``daily-strategy-inbox.md``, appends new date/line pairs to the expert's
``strategy-expert-<expert_id>-transcript.md`` (preserving any operator edits),
and prunes date sections older than ``--days`` (default 7).

This module is **not** an operator-facing command. It is called automatically
by ``strategy_thread.py`` before the thread distillation step.

WORK-only; not Record.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from strategy_expert_corpus import (
    MAX_VERBATIM_WORDS_PER_INGEST,
    SOFT_MAX_TRANSCRIPT_FILE_WORDS,
    _word_count,
    expert_paths,
    extract_thread_ingests,
    verbatim_to_transcript_lines,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)

TRIAGE_MARKER = "<!-- Triage appends new date sections below. Do not add content above this line. -->"


def canonical_transcript_header(expert_id: str) -> str:
    """Top-of-file header for `strategy-expert-<expert_id>-transcript.md` (through triage marker)."""
    return (
        f"# Expert transcript \u2014 `{expert_id}`\n"
        f"\n"
        f"WORK only; not Record.\n"
        f"\n"
        f"**Source:** Verbatim blocks from [`daily-strategy-inbox.md`](daily-strategy-inbox.md) "
        f"that include `thread:{expert_id}` (first line + optional continuation paragraphs), routed on ingest.\n"
        f"**Length:** Target **≤ {MAX_VERBATIM_WORDS_PER_INGEST} words** per ingest block; whole file soft "
        f"**≤ {SOFT_MAX_TRANSCRIPT_FILE_WORDS} words** after prune (7-day window makes overrun unlikely).\n"
        f"**Retention:** 7-day rolling window; date sections older than 7 days are pruned automatically.\n"
        f"**Editing:** Operator may lightly edit for clarity after triage. Edits are preserved across triage runs "
        f"(append-only, not overwrite).\n"
        f"**Companion files:** [`strategy-expert-{expert_id}.md`](strategy-expert-{expert_id}.md) (profile) "
        f"and [`strategy-expert-{expert_id}-thread.md`](strategy-expert-{expert_id}-thread.md) (distilled thread).\n"
        f"\n"
        f"---\n"
        f"\n"
        f"{TRIAGE_MARKER}\n"
    )


_RE_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def parse_transcript_file(path: Path) -> tuple[str, dict[str, list[str]]]:
    """Parse a transcript file into header and date-keyed sections.

    Returns (header, sections) where header is everything up to and including
    the triage marker, and sections is {date_str: [lines including the heading]}.
    """
    text = path.read_text(encoding="utf-8")

    marker_idx = text.find(TRIAGE_MARKER)
    if marker_idx != -1:
        header_end = marker_idx + len(TRIAGE_MARKER)
        header = text[:header_end].rstrip() + "\n"
        body = text[header_end:]
    else:
        header = text.rstrip() + "\n"
        body = ""

    sections: dict[str, list[str]] = {}
    current_date: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        m = _RE_DATE_HEADING.match(line)
        if m:
            if current_date is not None:
                sections[current_date] = current_lines
            current_date = m.group(1)
            current_lines = [line]
        elif current_date is not None:
            current_lines.append(line)

    if current_date is not None:
        sections[current_date] = current_lines

    return header, sections


def triage_to_transcripts(
    *,
    inbox_path: Path,
    out_dir: Path,
    keep_days: int,
    today: date | None = None,
    dry_run: bool = False,
    expert_ids: frozenset[str] | None = None,
) -> list[Path]:
    """Route inbox thread lines to transcript files, append-only + prune.

    Args:
        expert_ids: If provided, only process these experts. Otherwise imports
                    CANONICAL_EXPERT_IDS from strategy_expert_corpus.
    """
    today = today or datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=keep_days)

    if expert_ids is None:
        from strategy_expert_corpus import CANONICAL_EXPERT_IDS, _EXPERT_IDS_SET
        expert_ids_set = _EXPERT_IDS_SET
        all_ids = CANONICAL_EXPERT_IDS
    else:
        expert_ids_set = expert_ids
        all_ids = tuple(sorted(expert_ids))

    inbox_text = inbox_path.read_text(encoding="utf-8")
    extracted = extract_thread_ingests(inbox_text, today=today)

    written: list[Path] = []
    warn_ingest: list[str] = []

    for expert_id in all_ids:
        transcript_path = expert_paths(expert_id, out_dir)["transcript"]

        new_by_date = extracted.get(expert_id, {})

        if transcript_path.is_file():
            header, existing_sections = parse_transcript_file(transcript_path)
        else:
            header = canonical_transcript_header(expert_id)
            existing_sections = {}

        for d, lines in new_by_date.items():
            date_str = d.isoformat()
            if date_str in existing_sections:
                existing_lines_text = "\n".join(existing_sections[date_str])
                for verbatim in lines:
                    rendered = "\n".join(verbatim_to_transcript_lines(verbatim))
                    if rendered.rstrip() not in existing_lines_text:
                        msg = _warn_verbatim_size(verbatim, expert_id, date_str)
                        if msg:
                            warn_ingest.append(msg)
                        new_lines = verbatim_to_transcript_lines(verbatim)
                        existing_sections[date_str].extend(new_lines)
                        existing_lines_text = "\n".join(existing_sections[date_str])
            else:
                section_lines = [f"## {date_str}"]
                for verbatim in lines:
                    msg = _warn_verbatim_size(verbatim, expert_id, date_str)
                    if msg:
                        warn_ingest.append(msg)
                    section_lines.extend(verbatim_to_transcript_lines(verbatim))
                existing_sections[date_str] = section_lines

        pruned: dict[str, list[str]] = {}
        for date_str, lines in existing_sections.items():
            try:
                d = _parse_date(date_str)
                if d > cutoff:
                    pruned[date_str] = lines
            except (ValueError, TypeError):
                pruned[date_str] = lines

        body_parts: list[str] = []
        for date_str in sorted(pruned.keys(), reverse=True):
            body_parts.append("\n".join(pruned[date_str]))

        final = header + "\n" + "\n\n".join(body_parts) + "\n" if body_parts else header

        if body_parts and not dry_run:
            file_words = _word_count("\n".join("\n".join(pruned[ds]) for ds in sorted(pruned.keys(), reverse=True)))
            if file_words > SOFT_MAX_TRANSCRIPT_FILE_WORDS:
                warn_ingest.append(
                    f"{transcript_path.name}: total ~{file_words} words in file after prune "
                    f"(soft cap {SOFT_MAX_TRANSCRIPT_FILE_WORDS}); consider shorter captures or rely on 7d prune."
                )

        if not dry_run:
            transcript_path.write_text(final, encoding="utf-8")

        written.append(transcript_path)

    for msg in warn_ingest:
        print(f"strategy_expert_transcript: {msg}", flush=True)

    return written


def _warn_verbatim_size(verbatim: str, expert_id: str, date_str: str) -> str | None:
    wc = _word_count(verbatim)
    if wc > MAX_VERBATIM_WORDS_PER_INGEST:
        return (
            f"{expert_id} @ {date_str}: verbatim ingest ~{wc} words "
            f"(policy max {MAX_VERBATIM_WORDS_PER_INGEST}); split or trim if unintended."
        )
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--today", help="Override today (YYYY-MM-DD)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    today = _parse_date(args.today) if args.today else None
    paths = triage_to_transcripts(
        inbox_path=args.inbox,
        out_dir=args.out,
        keep_days=max(1, args.days),
        today=today,
        dry_run=args.dry_run,
    )
    for path in paths:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
