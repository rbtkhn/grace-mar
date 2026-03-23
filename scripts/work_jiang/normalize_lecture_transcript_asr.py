#!/usr/bin/env python3
"""Apply systematic ASR spelling fixes to work-jiang curated lecture transcripts.

By default only edits the markdown section below ``## Full transcript`` so headers
and topic lines stay untouched unless you pass ``--whole-file``.

Civilization lectures get an extra replacement tier (ancient Greek names/places).
Geo-Strategy lectures use the common tier only.

Examples::

    python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \\
      research/external/work-jiang/lectures/civilization-11-....md

    python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \\
      research/external/work-jiang/lectures/civilization-11-....md --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_WJ_DIR = Path(__file__).resolve().parent
if str(_WJ_DIR) not in sys.path:
    sys.path.insert(0, str(_WJ_DIR))

from asr_transcript_replacements import CIVILIZATION_REPLACEMENTS, COMMON_REPLACEMENTS

FULL_TRANSCRIPT_HEADING = "## Full transcript"


def detect_series(path: Path) -> str | None:
    name = path.name.lower()
    if name.startswith("civilization-"):
        return "civilization"
    if name.startswith("geo-strategy-"):
        return "geo-strategy"
    return None


def _sort_by_length(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return sorted(pairs, key=lambda x: len(x[0]), reverse=True)


def apply_ordered_replacements(text: str, pairs: list[tuple[str, str]]) -> tuple[str, int]:
    """Return (new_text, number of non-overlapping substring replacements)."""
    count = 0
    ordered = _sort_by_length(pairs)
    for old, new in ordered:
        if not old:
            continue
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n
    return text, count


def fix_civilization_thieves(text: str) -> tuple[str, int]:
    """Map ASR 'thieves' → Thebes without leaving 'the Thebes'."""
    count = 0
    for pat, repl in (
        (r"(?i)\bthe thieves\b", "Thebes"),
        (r"(?i)\bthieves\b", "Thebes"),
    ):
        n = len(re.findall(pat, text))
        if n:
            text = re.sub(pat, repl, text)
            count += n
    return text, count


def normalize_section(
    text: str,
    *,
    series: str | None,
) -> tuple[str, int]:
    total = 0
    text, n = apply_ordered_replacements(text, COMMON_REPLACEMENTS)
    total += n
    if series == "civilization":
        text, n = apply_ordered_replacements(text, CIVILIZATION_REPLACEMENTS)
        total += n
        text, n = fix_civilization_thieves(text)
        total += n
    return text, total


def split_full_transcript(md: str) -> tuple[str, str | None, str]:
    """Return (before_heading, transcript_body_or_None, after_if_whole)."""
    idx = md.find(FULL_TRANSCRIPT_HEADING)
    if idx == -1:
        return md, None, ""
    # Include heading line in "before" so we only transform body after \n\n following heading
    rest = md[idx:]
    nl = rest.find("\n")
    if nl == -1:
        return md[: idx + len(FULL_TRANSCRIPT_HEADING)], "", ""
    heading_block = md[: idx + nl + 1]
    body = rest[nl + 1 :]
    return heading_block, body, ""


def run_file(
    path: Path,
    *,
    whole_file: bool,
    series_override: str | None,
    dry_run: bool,
) -> int:
    raw = path.read_text(encoding="utf-8")
    series = series_override or detect_series(path)

    if whole_file:
        new_body, n = normalize_section(raw, series=series)
        if n == 0:
            print(f"{path}: no substitutions (series={series!r})", file=sys.stderr)
            return 0
        print(f"{path}: {n} substitution(s) (series={series!r}, whole file)")
        if not dry_run:
            path.write_text(new_body, encoding="utf-8")
        return 0

    head, body, _ = split_full_transcript(raw)
    if body is None:
        print(f"{path}: no '{FULL_TRANSCRIPT_HEADING}' — use --whole-file or add heading", file=sys.stderr)
        return 1

    new_body, n = normalize_section(body, series=series)
    if n == 0:
        print(f"{path}: no substitutions in transcript section (series={series!r})", file=sys.stderr)
        return 0
    print(f"{path}: {n} substitution(s) in transcript section (series={series!r})")
    if not dry_run:
        path.write_text(head + new_body, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Curated lecture .md under work-jiang/lectures/")
    parser.add_argument(
        "--series",
        choices=("auto", "civilization", "geo-strategy", "none"),
        default="auto",
        help="Replacement tier: auto from filename, or force one series; none = common only.",
    )
    parser.add_argument(
        "--whole-file",
        action="store_true",
        help="Apply fixes to entire file (not only below ## Full transcript).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes; default is dry-run (report counts only).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicit dry-run (default unless --write).",
    )
    args = parser.parse_args()
    if args.dry_run and args.write:
        parser.error("Use --write or --dry-run, not both")

    path = args.path.resolve()
    if not path.is_file():
        print(f"Not a file: {path}", file=sys.stderr)
        return 1

    series_map = {
        "auto": detect_series(path),
        "civilization": "civilization",
        "geo-strategy": "geo-strategy",
        "none": None,
    }
    series = series_map[args.series]

    dry_run = not args.write
    return run_file(path, whole_file=args.whole_file, series_override=series, dry_run=dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
