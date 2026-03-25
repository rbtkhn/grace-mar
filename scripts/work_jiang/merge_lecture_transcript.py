#!/usr/bin/env python3
"""Replace only the body under ``## Full transcript`` in a curated lecture .md.

Use when the transcript is too large for a single editor paste: concatenate parts on stdin
or pass multiple ``--file`` arguments (order preserved). No temporary chunk files need to live
in the repo.

Examples::

    cat part1.txt part2.txt | python3 scripts/work_jiang/merge_lecture_transcript.py \\
      research/external/work-jiang/lectures/secret-history-21-roman-anti-civilization.md

    python3 scripts/work_jiang/merge_lecture_transcript.py lectures/secret-history-21-....md \\
      -f part1.txt -f part2.txt

    python3 scripts/work_jiang/merge_lecture_transcript.py lecture.md --normalize --write
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_WJ = Path(__file__).resolve().parent
_ROOT = _WJ.parent.parent
if str(_WJ) not in sys.path:
    sys.path.insert(0, str(_WJ))

from normalize_lecture_transcript_asr import FULL_TRANSCRIPT_HEADING, split_full_transcript  # noqa: E402


def _read_body(args: argparse.Namespace) -> str:
    if args.file:
        chunks: list[str] = []
        for p in args.file:
            chunks.append(p.read_text(encoding="utf-8", errors="replace"))
        return "\n".join(chunks).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    print("Provide transcript text on stdin or use --file", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "lecture",
        type=Path,
        help="Curated lecture .md (must contain ## Full transcript)",
    )
    parser.add_argument(
        "--file",
        "-f",
        action="append",
        type=Path,
        default=None,
        help="Transcript fragment (repeat for multiple files, concatenated in order)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write merged file; default is dry-run (print byte counts only)",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="After merge, run normalize_lecture_transcript_asr.py --write on the lecture",
    )
    args = parser.parse_args()

    lecture = args.lecture.resolve()
    if not lecture.is_file():
        print(f"Not a file: {lecture}", file=sys.stderr)
        return 1

    raw = lecture.read_text(encoding="utf-8")
    head, _old_body, _ = split_full_transcript(raw)
    if _old_body is None:
        print(f"{lecture}: no '{FULL_TRANSCRIPT_HEADING}' section", file=sys.stderr)
        return 1

    new_body = _read_body(args)
    if not new_body:
        print("Transcript body is empty.", file=sys.stderr)
        return 1

    merged = head + new_body + ("\n" if not new_body.endswith("\n") else "")

    if not args.write:
        print(
            f"{lecture}: would replace transcript body ({len(new_body)} chars); "
            f"total file {len(merged)} chars — pass --write to apply",
            file=sys.stderr,
        )
        return 0

    lecture.write_text(merged, encoding="utf-8")
    print(f"{lecture}: wrote transcript body ({len(new_body)} chars)", file=sys.stderr)

    if args.normalize:
        norm = _WJ / "normalize_lecture_transcript_asr.py"
        subprocess.run(
            [sys.executable, str(norm), str(lecture), "--write"],
            cwd=str(_ROOT),
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
