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
from collections import defaultdict
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


def _split_simple_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse leading YAML-style ``key: value`` block after first ``---``."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---\n", 1)
    if end == -1:
        return {}, text
    fm_raw = text[4:end].strip()
    body = text[end + 5 :]
    fm: dict[str, str] = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def _extract_markdown_h1_title(body: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            return s[2:].strip()
    return "RSS item"


def _iter_raw_input_md_paths(raw_root: Path, cutoff: date) -> list[Path]:
    """Markdown files under ``raw-input/YYYY-MM-DD/`` with folder date strictly after ``cutoff``."""
    if not raw_root.is_dir():
        return []
    out: list[Path] = []
    for child in sorted(raw_root.iterdir()):
        if not child.is_dir():
            continue
        try:
            d = date.fromisoformat(child.name)
        except ValueError:
            continue
        if d <= cutoff:
            continue
        out.extend(sorted(child.glob("*.md")))
    return out


def _rss_row_air_date(fm: dict[str, str], path: Path) -> date | None:
    for key in ("aired_date", "ingest_date"):
        raw = (fm.get(key) or "").strip()
        if raw and len(raw) >= 10:
            try:
                return _parse_date(raw[:10])
            except ValueError:
                pass
    try:
        return date.fromisoformat(path.parent.name)
    except ValueError:
        return None


def collect_rss_thread_ingests(
    raw_root: Path,
    *,
    cutoff: date,
    expert_ids_set: frozenset[str],
) -> dict[str, dict[date, list[str]]]:
    """Build ``expert_id -> date -> verbatim`` from ``raw-input`` RSS markdown with ``thread:``."""
    nested: dict[str, dict[date, list[str]]] = defaultdict(lambda: defaultdict(list))
    for path in _iter_raw_input_md_paths(raw_root, cutoff):
        text = path.read_text(encoding="utf-8")
        fm, body = _split_simple_frontmatter(text)
        if fm.get("kind") != "rss-item":
            continue
        tid = (fm.get("thread") or "").strip()
        if not tid or tid not in expert_ids_set:
            continue
        d = _rss_row_air_date(fm, path)
        if d is None or d <= cutoff:
            continue
        title = _extract_markdown_h1_title(body)
        url = (fm.get("source_url") or "").strip()
        verbatim = (
            f"- RSS | cold: **{title}** // raw-input `{path.name}`"
            f" | {url} | verify:rss-fetch | thread:{tid}"
        )
        nested[tid][d].append(verbatim)
    return {e: dict(dm) for e, dm in nested.items()}


def _merge_date_ingest_maps(
    inbox_map: dict[date, list[str]],
    rss_map: dict[date, list[str]],
) -> dict[date, list[str]]:
    dates = set(inbox_map) | set(rss_map)
    return {d: inbox_map.get(d, []) + rss_map.get(d, []) for d in dates}


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
    raw_input_root: Path | None = None,
) -> list[Path]:
    """Route inbox thread lines to transcript files, append-only + prune.

    Also merges ``raw-input/**/*.md`` files with ``kind: rss-item`` and a
    ``thread:`` line in YAML front matter (from :func:`collect_rss_thread_ingests`),
    after inbox lines for the same date.

    Args:
        expert_ids: If provided, only process these experts. Otherwise imports
                    CANONICAL_EXPERT_IDS from strategy_expert_corpus.
        raw_input_root: Defaults to ``out_dir / "raw-input"``. Set to a nonexistent
                    path to skip RSS merge.
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

    raw_root = raw_input_root if raw_input_root is not None else (out_dir / "raw-input")
    rss_by_expert = (
        collect_rss_thread_ingests(raw_root, cutoff=cutoff, expert_ids_set=expert_ids_set)
        if raw_root.is_dir()
        else {}
    )

    written: list[Path] = []
    warn_ingest: list[str] = []

    for expert_id in all_ids:
        transcript_path = expert_paths(expert_id, out_dir)["transcript"]

        new_by_date = _merge_date_ingest_maps(
            extracted.get(expert_id, {}),
            rss_by_expert.get(expert_id, {}),
        )

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
            transcript_path.parent.mkdir(parents=True, exist_ok=True)
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
