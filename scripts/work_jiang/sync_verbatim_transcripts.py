#!/usr/bin/env python3
"""Build lightly-cleaned verbatim markdown from raw YouTube caption files per lecture.

Reads ``research/external/work-jiang/lectures/*.md``, extracts ``watch?v=VIDEO_ID``,
loads ``predictive-history/transcripts/{video_id}_*.txt`` (newest mtime if several),
strips the fetch header, applies the same ASR replacement tier as
``normalize_lecture_transcript_asr.py`` (via ``asr_light_clean``), and writes
``verbatim-transcripts/<same-basename>.md``.

Populate raw captions first (see ``research/external/youtube-channels/predictive-history/README.md``).

Examples::

    python3 scripts/work_jiang/sync_verbatim_transcripts.py
    python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run
    python3 scripts/work_jiang/sync_verbatim_transcripts.py --write
    python3 scripts/work_jiang/sync_verbatim_transcripts.py --write --only-glob 'geo-strategy-01*'
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import re
import sys
from pathlib import Path

import yaml

_WJ_DIR = Path(__file__).resolve().parent
_SCRIPTS = _WJ_DIR.parent
ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts.hashing import strip_transcript_header  # noqa: E402

from asr_light_clean import detect_series_from_basename, normalize_transcript_text  # noqa: E402

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_JIANG / "lectures"
VERBATIM = WORK_JIANG / "verbatim-transcripts"
DEFAULT_TRANSCRIPT_ROOT = (
    ROOT / "research" / "external" / "youtube-channels" / "predictive-history"
)

VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})\b",
)


def parse_transcript_file_header(raw: str) -> dict[str, str]:
    """Parse leading # comment lines from a saved transcript .txt file."""
    out: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.startswith("#"):
            break
        body = line[1:].strip()
        if not body:
            continue
        if ":" in body:
            k, _, v = body.partition(":")
            key = k.strip().lower().replace(" ", "_")
            out[key] = v.strip()
    return out


def extract_video_id(lecture_md: str) -> str | None:
    m = VIDEO_ID_RE.search(lecture_md)
    return m.group(1) if m else None


def lecture_title_line(lecture_md: str, *, fallback: str) -> str:
    first = lecture_md.lstrip().split("\n", 1)[0].strip()
    if first.startswith("#"):
        return first[1:].strip() or fallback
    return fallback


def find_raw_transcript(transcript_root: Path, video_id: str) -> Path | None:
    pattern = str(transcript_root / "transcripts" / f"{video_id}_*.txt")
    matches = sorted(glob.glob(pattern), key=lambda p: Path(p).stat().st_mtime, reverse=True)
    if not matches:
        return None
    return Path(matches[0])


def build_verbatim_markdown(
    *,
    lecture_rel: str,
    raw_rel: str,
    title: str,
    header_meta: dict[str, str],
    body_clean: str,
) -> str:
    fm: dict[str, object] = {
        "video_id": header_meta.get("video_id", ""),
        "source_lecture": lecture_rel.replace("\\", "/"),
        "raw_transcript_path": raw_rel.replace("\\", "/"),
    }
    for key in ("title", "url", "language", "source_tier", "quality", "fetched_at_utc", "status"):
        if key in header_meta:
            fm[key] = header_meta[key]
    head = yaml.safe_dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False).rstrip()
    md = f"---\n{head}\n---\n\n# {title}\n\n## Verbatim transcript (lightly cleaned)\n\n{body_clean}\n"
    return md


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--transcript-root",
        type=Path,
        default=DEFAULT_TRANSCRIPT_ROOT,
        help="predictive-history channel root (contains transcripts/)",
    )
    ap.add_argument(
        "--work-dir",
        type=Path,
        default=WORK_JIANG,
        help="work-jiang root",
    )
    ap.add_argument("--only-glob", default=None, help="fnmatch pattern against lecture basename")
    ap.add_argument("--limit", type=int, default=0, help="max lectures to process (0 = all)")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="plan only; do not write (default when --write is omitted; explicit for audits)",
    )
    ap.add_argument("--write", action="store_true", help="write verbatim files")
    ap.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing verbatim files (default: skip if target exists)",
    )
    ap.add_argument(
        "--fail-on-missing-raw",
        action="store_true",
        help="exit with code 2 if any lecture has no matching raw transcript file",
    )
    args = ap.parse_args()
    if args.write and args.dry_run:
        ap.error("Cannot use --write and --dry-run together")

    work = args.work_dir.resolve()
    lect_dir = work / "lectures"
    out_dir = work / "verbatim-transcripts"
    tx_root = args.transcript_root.resolve()

    if not lect_dir.is_dir():
        print(f"Missing lectures dir: {lect_dir}", file=sys.stderr)
        return 1

    lectures = sorted(lect_dir.glob("*.md"))
    if args.only_glob:
        pat = args.only_glob.lower()
        lectures = [p for p in lectures if fnmatch.fnmatch(p.name.lower(), pat)]

    written = 0
    skipped_exists = 0
    missing_raw: list[str] = []
    missing_vid: list[str] = []
    processed = 0

    for path in lectures:
        if args.limit and processed >= args.limit:
            break
        raw_text = path.read_text(encoding="utf-8", errors="replace")
        vid = extract_video_id(raw_text)
        if not vid:
            missing_vid.append(path.name)
            continue

        raw_path = find_raw_transcript(tx_root, vid)
        if raw_path is None:
            missing_raw.append(f"{path.name} (video_id={vid})")
            continue

        out_path = out_dir / path.name
        if out_path.exists() and not args.force:
            print(f"{path.name} -> skip (exists: {out_path.relative_to(ROOT)})")
            skipped_exists += 1
            processed += 1
            continue

        raw_file = raw_path.read_text(encoding="utf-8", errors="replace")
        header_meta = parse_transcript_file_header(raw_file)
        header_meta.setdefault("video_id", vid)
        body = strip_transcript_header(raw_file).strip()
        series = detect_series_from_basename(path.name)
        body_clean, n_sub = normalize_transcript_text(body, series=series)

        title = lecture_title_line(
            raw_text,
            fallback=header_meta.get("title") or path.stem.replace("-", " "),
        )
        lecture_rel = path.relative_to(ROOT).as_posix()
        raw_rel = raw_path.relative_to(ROOT).as_posix()

        md = build_verbatim_markdown(
            lecture_rel=lecture_rel,
            raw_rel=raw_rel,
            title=title,
            header_meta=header_meta,
            body_clean=body_clean,
        )

        rel_out = out_path.relative_to(ROOT)
        print(f"{path.name} -> {rel_out} (replacements={n_sub}, series={series!r})")
        if args.write:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            written += 1
        processed += 1

    if missing_vid:
        print(f"\n{len(missing_vid)} lecture(s) with no youtube watch URL in body:", file=sys.stderr)
        for n in missing_vid[:30]:
            print(f"  {n}", file=sys.stderr)
        if len(missing_vid) > 30:
            print(f"  ... and {len(missing_vid) - 30} more", file=sys.stderr)

    if missing_raw:
        print(f"\n{len(missing_raw)} lecture(s) with no raw transcript file:", file=sys.stderr)
        for n in missing_raw[:30]:
            print(f"  {n}", file=sys.stderr)
        if len(missing_raw) > 30:
            print(f"  ... and {len(missing_raw) - 30} more", file=sys.stderr)

    if skipped_exists:
        print(f"\nSkipped {skipped_exists} existing verbatim file(s) (use --force to overwrite)")

    mode = "wrote" if args.write else "dry-run"
    print(f"\nSummary ({mode}): processed={processed}, written={written}, missing_raw={len(missing_raw)}")

    if args.fail_on_missing_raw and missing_raw:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
