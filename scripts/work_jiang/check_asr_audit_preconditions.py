#!/usr/bin/env python3
"""Report work-jiang lecture ↔ raw YouTube caption coverage for ASR audit preconditions.

For each ``lectures/*.md`` with a ``watch?v=`` / ``youtu.be/`` URL, checks whether
``predictive-history/transcripts/{video_id}_*.txt`` exists (newest path printed).

Examples::

    python3 scripts/work_jiang/check_asr_audit_preconditions.py
    python3 scripts/work_jiang/check_asr_audit_preconditions.py --only-glob 'geo-strategy-*'
    python3 scripts/work_jiang/check_asr_audit_preconditions.py --strict
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import re
import sys
from pathlib import Path

_WJ_DIR = Path(__file__).resolve().parent
_SCRIPTS = _WJ_DIR.parent
ROOT = _SCRIPTS.parent

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_JIANG / "lectures"
DEFAULT_TRANSCRIPT_ROOT = (
    ROOT / "research" / "external" / "youtube-channels" / "predictive-history"
)

VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})\b",
)


def extract_video_id(md: str) -> str | None:
    m = VIDEO_ID_RE.search(md)
    return m.group(1) if m else None


def find_raw_transcript(transcript_root: Path, video_id: str) -> Path | None:
    pattern = str(transcript_root / "transcripts" / f"{video_id}_*.txt")
    matches = sorted(glob.glob(pattern), key=lambda p: Path(p).stat().st_mtime, reverse=True)
    if not matches:
        return None
    return Path(matches[0])


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
    ap.add_argument(
        "--only-glob",
        default=None,
        help="fnmatch pattern against lecture basename (e.g. geo-strategy-*)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit with code 1 if any lecture with a video_id lacks a raw transcript file",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print one line per lecture (ok or missing)",
    )
    args = ap.parse_args()

    lect_dir = args.work_dir.resolve() / "lectures"
    tx_root = args.transcript_root.resolve()

    if not lect_dir.is_dir():
        print(f"Missing lectures dir: {lect_dir}", file=sys.stderr)
        return 1

    lectures = sorted(lect_dir.glob("*.md"))
    if args.only_glob:
        pat = args.only_glob.lower()
        lectures = [p for p in lectures if fnmatch.fnmatch(p.name.lower(), pat)]

    with_url = 0
    missing_raw: list[tuple[str, str]] = []

    for path in lectures:
        text = path.read_text(encoding="utf-8", errors="replace")
        vid = extract_video_id(text)
        if not vid:
            if args.verbose:
                print(f"no_url\t{path.name}")
            continue
        with_url += 1
        raw = find_raw_transcript(tx_root, vid)
        if raw is None:
            missing_raw.append((path.name, vid))
            if args.verbose:
                print(f"missing_raw\t{path.name}\t{vid}")
        elif args.verbose:
            rel = raw.relative_to(ROOT)
            print(f"ok\t{path.name}\t{vid}\t{rel}")

    n_ok = with_url - len(missing_raw)
    print(
        f"Lectures scanned: {len(lectures)} | with YouTube URL: {with_url} | "
        f"raw transcript found: {n_ok} | missing raw: {len(missing_raw)}",
    )
    if missing_raw and not args.verbose:
        print("Missing (lecture, video_id):", file=sys.stderr)
        for name, vid in missing_raw[:40]:
            print(f"  {name}  {vid}", file=sys.stderr)
        if len(missing_raw) > 40:
            print(f"  ... and {len(missing_raw) - 40} more", file=sys.stderr)

    if args.strict and missing_raw:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
