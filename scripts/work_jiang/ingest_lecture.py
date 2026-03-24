#!/usr/bin/env python3
"""Create or replace a work-jiang curated lecture from transcript text or fetch.

Resolves video_id + YouTube title from CHANNEL-VIDEO-INDEX.md via channel_video_lookup.
Writes ``lectures/<series>-NN-<slug>.md``, then optionally runs refresh_after_ingest.

Examples::

    python3 scripts/work_jiang/ingest_lecture.py civilization 25 --file raw.txt
    cat raw.txt | python3 scripts/work_jiang/ingest_lecture.py civ 25
    python3 scripts/work_jiang/ingest_lecture.py geo 3 --fetch
    python3 scripts/work_jiang/ingest_lecture.py civ 26 --fetch --asr --no-refresh
"""

from __future__ import annotations

import argparse
import glob
import subprocess
import sys
import tempfile
from pathlib import Path

_WJ = Path(__file__).resolve().parent
_SCRIPTS = _WJ.parent
ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts.hashing import strip_transcript_header  # noqa: E402

from channel_video_lookup import (  # noqa: E402
    lookup_series_episode,
    youtube_title_to_heading,
    youtube_title_to_slug,
)

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_JIANG / "lectures"
DEFAULT_TRANSCRIPT_ROOT = (
    ROOT / "research" / "external" / "youtube-channels" / "predictive-history"
)


def _series_prefix(series: str) -> str:
    s = series.lower().replace("_", "-")
    if s in ("civilization", "civ"):
        return "civilization"
    if s in ("secret-history", "secret", "sh"):
        return "secret-history"
    if s in ("geo-strategy", "geo"):
        return "geo-strategy"
    raise ValueError(series)


def _read_transcript_stdin() -> str:
    data = sys.stdin.read()
    if not data.strip():
        print("stdin empty — pass --file or pipe transcript text", file=sys.stderr)
        raise SystemExit(1)
    return data


def _fetch_transcript_text(video_id: str, *, out_root: Path, fetch_force: bool) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    fetch_cli = _SCRIPTS / "fetch_youtube_channel_transcripts.py"
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(url + "\n")
        tmp_path = tmp.name
    cmd = [
        sys.executable,
        str(fetch_cli),
        "--input",
        tmp_path,
        "--limit",
        "1",
        "-o",
        str(out_root),
        "--resume",
    ]
    if fetch_force:
        cmd.append("--force")
    try:
        subprocess.run(cmd, cwd=str(ROOT), check=True)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    tx_dir = out_root / "transcripts"
    pattern = str(tx_dir / f"{video_id}_*.txt")
    matches = sorted(glob.glob(pattern), key=lambda p: Path(p).stat().st_mtime, reverse=True)
    if not matches:
        print(
            f"No transcript file matching {pattern!r} after fetch.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    raw = Path(matches[0]).read_text(encoding="utf-8", errors="replace")
    return strip_transcript_header(raw).strip()


def _build_markdown(
    *,
    heading: str,
    series_prefix: str,
    episode: int,
    video_id: str,
    transcript_note: str,
    body: str,
) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    if series_prefix == "civilization":
        series_label = "Civilization"
        series_md = f"**Series:** {series_label} **#{episode}**"
    elif series_prefix == "secret-history":
        series_label = "Secret History"
        series_md = f"**Series:** {series_label} **#{episode}**"
    else:
        series_label = "Geo-Strategy"
        if episode == 12:
            series_md = (
                f"**Series:** {series_label} **#12** **(finale)** — "
                "YouTube title uses “Geo-Strategy END”; numbered **#12** for the book line."
            )
        else:
            series_md = f"**Series:** {series_label} **#{episode}**"

    date_line = "**Date (YouTube upload):** TBD (fill from YouTube / metadata)"
    if series_prefix == "geo-strategy" and episode != 12:
        date_line = (
            "**Date (stated in session):** TBD  \n"
            "**Date (YouTube upload):** TBD (fill from YouTube / metadata)"
        )

    return f"""# {heading}

**Speaker:** Jiang Xueqin  
**Audience:** Chinese high school students  
{series_md}  
{date_line}  
**Topic:** TBD — one-paragraph summary after listen.

**Source (canonical recording):** [Predictive History — {heading}]({url}) (`@PredictiveHistory`).  
**Transcript:** {transcript_note}

---

## At a glance

- TBD after listen.

---

## Concepts named in lecture (tags)

`tbd`

---

## Full transcript

{body}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "series",
        help="civilization|civ|secret-history|secret|sh|geo-strategy|geo",
    )
    parser.add_argument("episode", type=int, help="Episode number (1–99+)")
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=None,
        help="Read transcript from file (otherwise stdin unless --fetch)",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Run fetch_youtube_channel_transcripts.py for this watch URL, then read transcripts/",
    )
    parser.add_argument(
        "--fetch-force",
        action="store_true",
        help="Pass --force to the fetch script (refetch even if manifest matches)",
    )
    parser.add_argument(
        "--transcript-root",
        type=Path,
        default=DEFAULT_TRANSCRIPT_ROOT,
        help="predictive-history output dir for --fetch",
    )
    parser.add_argument(
        "--asr",
        action="store_true",
        help="After write, run normalize_lecture_transcript_asr.py --write on the lecture",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing lecture file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print path and heading; do not write or refresh",
    )
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Skip refresh_after_ingest.py",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=None,
        help="Override CHANNEL-VIDEO-INDEX.md path",
    )
    args = parser.parse_args()

    if args.episode < 1:
        parser.error("episode must be >= 1")
    if args.file and args.fetch:
        parser.error("Use either --file or --fetch, not both")
    if not args.file and not args.fetch and sys.stdin.isatty():
        parser.error("Provide --file, --fetch, or pipe transcript on stdin")

    sprefix = _series_prefix(args.series)
    if sprefix == "civilization":
        lookup_series = "civilization"
    elif sprefix == "secret-history":
        lookup_series = "secret-history"
    else:
        lookup_series = "geo-strategy"
    row = lookup_series_episode(lookup_series, args.episode, index_path=args.index)
    if not row:
        print(
            f"No index row for {lookup_series!r} episode {args.episode}. "
            "Refresh CHANNEL-VIDEO-INDEX.md or pass --index.",
            file=sys.stderr,
        )
        return 1

    video_id, yt_title = row
    heading = youtube_title_to_heading(yt_title, lookup_series, args.episode)
    slug = youtube_title_to_slug(yt_title, lookup_series, args.episode)
    nn = f"{args.episode:02d}"
    out_name = f"{sprefix}-{nn}-{slug}.md"
    out_path = LECTURES / out_name

    if args.fetch:
        body = _fetch_transcript_text(
            video_id, out_root=args.transcript_root.resolve(), fetch_force=args.fetch_force
        )
        transcript_note = (
            "Pulled via `scripts/fetch_youtube_channel_transcripts.py` (caption tiers as configured); "
            "provenance header stripped; wording preserved for traceability."
        )
    elif args.file:
        body = args.file.read_text(encoding="utf-8", errors="replace").strip()
        transcript_note = (
            "Operator-supplied text (file); wording preserved for traceability; "
            "run `normalize_lecture_transcript_asr.py` after editorial pass if needed."
        )
    else:
        body = _read_transcript_stdin().strip()
        transcript_note = (
            "Operator-supplied text (stdin); wording preserved for traceability; "
            "run `normalize_lecture_transcript_asr.py` after editorial pass if needed."
        )

    if not body:
        print("Transcript body is empty after read/fetch.", file=sys.stderr)
        return 1

    md = _build_markdown(
        heading=heading,
        series_prefix=sprefix,
        episode=args.episode,
        video_id=video_id,
        transcript_note=transcript_note,
        body=body,
    )

    print(f"{out_path}  (# {heading})", file=sys.stderr)
    if args.dry_run:
        return 0

    if out_path.exists() and not args.force:
        print(f"Refusing to overwrite {out_path} (use --force)", file=sys.stderr)
        return 1

    LECTURES.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    if args.asr:
        norm = _WJ / "normalize_lecture_transcript_asr.py"
        subprocess.run(
            [sys.executable, str(norm), str(out_path), "--write"],
            cwd=str(ROOT),
            check=True,
        )

    if not args.no_refresh:
        refresh = _WJ / "refresh_after_ingest.py"
        subprocess.run([sys.executable, str(refresh)], cwd=str(ROOT), check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
