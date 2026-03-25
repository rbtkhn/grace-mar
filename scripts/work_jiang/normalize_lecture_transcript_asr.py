#!/usr/bin/env python3
"""Apply systematic ASR spelling fixes to work-jiang curated lecture transcripts.

By default only edits the markdown section below ``## Full transcript`` so headers
and topic lines stay untouched unless you pass ``--whole-file``.

Civilization lectures get an extra replacement tier (ancient Greek names/places).
Geo-Strategy lectures use the common tier only.
Secret History (``secret-history-*.md``) uses common + Roman / Volume III phrase tier.
Game Theory (``game-theory-*.md``) uses common + Volume IV phrase tier (may be empty until ingests).

Examples::

    python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \\
      research/external/work-jiang/lectures/civilization-11-....md

    python3 scripts/work_jiang/normalize_lecture_transcript_asr.py \\
      research/external/work-jiang/lectures/civilization-11-....md --write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_WJ_DIR = Path(__file__).resolve().parent
if str(_WJ_DIR) not in sys.path:
    sys.path.insert(0, str(_WJ_DIR))

from asr_light_clean import detect_series, normalize_transcript_text

FULL_TRANSCRIPT_HEADING = "## Full transcript"


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
    series: str | None,
    dry_run: bool,
) -> int:
    raw = path.read_text(encoding="utf-8")

    if whole_file:
        new_body, n = normalize_transcript_text(raw, series=series)
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

    new_body, n = normalize_transcript_text(body, series=series)
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
        choices=("auto", "civilization", "geo-strategy", "secret-history", "game-theory", "none"),
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

    if args.series == "auto":
        series_resolved: str | None = detect_series(path)
    elif args.series == "none":
        series_resolved = None
    else:
        series_resolved = args.series

    dry_run = not args.write
    return run_file(path, whole_file=args.whole_file, series=series_resolved, dry_run=dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
