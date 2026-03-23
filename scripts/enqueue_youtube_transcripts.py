#!/usr/bin/env python3
"""
Enqueue per-video transcript jobs on Redis (RQ). Requires:

  pip install -e ".[transcript-pipeline]"
  export REDIS_URL=redis://localhost:6379/0

Run workers (separate terminals):

  python3 scripts/run_transcript_rq_worker.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts.discovery import list_videos, load_inputs_from_file
from youtube_transcripts.jobs import run_fetch_video_job


def main() -> int:
    try:
        import redis
        from rq import Queue
    except ImportError:
        print("Install: pip install -e '.[transcript-pipeline]'", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="Enqueue YouTube transcript jobs (RQ).")
    parser.add_argument("--channel", default="https://www.youtube.com/@PredictiveHistory/videos")
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument(
        "-o",
        "--output-dir",
        default=str(
            Path(__file__).resolve().parents[1]
            / "research/external/youtube-channels/predictive-history"
        ),
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--languages", default="en,en-US,zh-Hans,zh-CN")
    parser.add_argument("--languages-tier2", default="")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--enable-whisper", action="store_true")
    parser.add_argument("--keep-low-quality", action="store_true")
    args = parser.parse_args()

    out_root = Path(args.output_dir)
    limit = args.limit if args.limit > 0 else None
    langs = [x.strip() for x in args.languages.split(",") if x.strip()]
    langs2 = [x.strip() for x in args.languages_tier2.split(",") if x.strip()] if args.languages_tier2.strip() else langs

    inputs: list[str] = []
    if args.input and args.input.exists():
        inputs = load_inputs_from_file(args.input)
    if not inputs:
        inputs = [args.channel]

    all_videos: list[dict[str, str]] = []
    for inp in inputs:
        all_videos.extend(list_videos(inp, limit=limit))
    seen: set[str] = set()
    videos: list[dict[str, str]] = []
    for v in all_videos:
        if v["id"] in seen:
            continue
        seen.add(v["id"])
        videos.append(v)

    print(f"Enqueueing {len(videos)} job(s).", file=sys.stderr)
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    conn = redis.from_url(url)
    q = Queue("transcript_fetch", connection=conn)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    min_q = float(os.environ.get("TRANSCRIPT_MIN_QUALITY", "0.35").strip() or "0.35")

    job_ids: list[str] = []
    for v in videos:
        payload = json.dumps(
            {
                "output_dir": str(out_root.resolve()),
                "video": v,
                "languages": langs,
                "langs_tier2": langs2,
                "min_quality": min_q,
                "keep_low_quality": args.keep_low_quality,
                "enable_whisper": args.enable_whisper,
                "force": args.force,
                "resume": args.resume,
                "fetched_at_utc": ts,
            }
        )
        job = q.enqueue(run_fetch_video_job, payload, job_timeout="1h")
        job_ids.append(job.id)

    print("job_ids:", ",".join(job_ids), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
