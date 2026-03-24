from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1].parent

# Allow `python scripts/fetch_youtube_channel_transcripts.py` without install
_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _parse_langs(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def run(argv: list[str] | None = None) -> int:
    from youtube_transcripts.discovery import list_videos, load_inputs_from_file
    from youtube_transcripts.manifest_io import load_manifest, manifest_path, save_manifest
    from youtube_transcripts.pipeline import fetch_one_video, result_to_index_row

    parser = argparse.ArgumentParser(description="Download YouTube channel/playlist transcripts.")
    parser.add_argument(
        "--channel",
        default="https://www.youtube.com/@PredictiveHistory/videos",
        help="Channel URL (default Predictive History)",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Optional file: one channel/playlist/watch URL per line (overrides --channel if set)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=str(REPO_ROOT / "research/external/youtube-channels/predictive-history"),
        help="Directory for transcripts/, index.json, transcript_manifest.json",
    )
    parser.add_argument("--limit", type=int, default=0, help="Max videos per input URL (0 = all)")
    parser.add_argument(
        "--languages",
        default="en,en-US,zh-Hans,zh-CN",
        help="Comma-separated caption languages (tier 1)",
    )
    parser.add_argument(
        "--languages-tier2",
        default="",
        help="Comma-separated langs for yt-dlp subs (default: same as --languages)",
    )
    parser.add_argument("--sleep", type=float, default=0.4, help="Seconds between video fetches")
    parser.add_argument("--dry-run", action="store_true", help="Only list video IDs and titles")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Write index.json from listing only (no transcript downloads)",
    )
    parser.add_argument("--resume", action="store_true", help="Skip videos with existing .txt (size>50)")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Refetch even if manifest hash matches (no incremental skip)",
    )
    parser.add_argument(
        "--enable-whisper",
        action="store_true",
        help="Tier 3: local whisper.cpp (WHISPER_CPP_BIN, WHISPER_CPP_MODEL); downloads audio",
    )
    parser.add_argument(
        "--keep-low-quality",
        action="store_true",
        help="Write transcripts below min quality as needs_review instead of rejecting",
    )
    parser.add_argument(
        "--max-attempts-listing",
        type=int,
        default=4,
        help="Retries for yt-dlp channel/playlist listing",
    )
    args = parser.parse_args(argv)

    out_root = Path(args.output_dir)
    tx_dir = out_root / "transcripts"
    tx_dir.mkdir(parents=True, exist_ok=True)

    limit = args.limit if args.limit > 0 else None
    langs = _parse_langs(args.languages)
    langs2 = _parse_langs(args.languages_tier2) if args.languages_tier2.strip() else langs

    min_q = float(os.environ.get("TRANSCRIPT_MIN_QUALITY", "0.35").strip() or "0.35")

    inputs: list[str] = []
    if args.input and args.input.exists():
        inputs = load_inputs_from_file(args.input)
    if not inputs:
        inputs = [args.channel]

    all_videos: list[dict[str, str]] = []
    for inp in inputs:
        print(f"Listing videos: {inp}", file=sys.stderr)
        part = list_videos(inp, limit=limit, max_attempts=args.max_attempts_listing)
        all_videos.extend(part)
    # Dedupe by id preserving order
    seen: set[str] = set()
    videos: list[dict[str, str]] = []
    for v in all_videos:
        if v["id"] in seen:
            continue
        seen.add(v["id"])
        videos.append(v)

    print(f"Found {len(videos)} video(s).", file=sys.stderr)

    if args.dry_run:
        for v in videos:
            print(f"{v['id']}\t{v['title']}")
        return 0

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.index_only:
        index_rows: list[dict[str, object]] = []
        for v in videos:
            index_rows.append(
                {
                    "video_id": v["id"],
                    "title": v["title"],
                    "upload_date": v.get("upload_date") or "",
                    "duration_seconds": v.get("duration") or "",
                    "url": v["url"],
                    "transcript_file": None,
                    "status": "listed_only",
                    "language": None,
                    "error": None,
                }
            )
        index_path = out_root / "index.json"
        payload = {
            "channel_url": inputs[0] if inputs else args.channel,
            "input_urls": inputs,
            "pipeline_version": __import__(
                "youtube_transcripts.constants", fromlist=["PIPELINE_VERSION"]
            ).PIPELINE_VERSION,
            "generated_at_utc": ts,
            "video_count": len(videos),
            "transcripts_attempted": 0,
            "index_mode": "listing_only",
            "videos": index_rows,
        }
        index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        md_path = out_root / "CHANNEL-VIDEO-INDEX.md"
        md_lines = [
            "# Predictive History (@PredictiveHistory) — full video index",
            "",
            f"- **channel:** {inputs[0] if inputs else args.channel}",
            f"- **video_count:** {len(videos)}",
            f"- **generated_at_utc:** {ts}",
            "- **method:** index-only (no transcripts downloaded)",
            "",
            "| # | video_id | title | duration_s | url |",
            "|---:|---|-----|---:|-----|",
        ]
        for i, v in enumerate(videos, start=1):
            title = (v["title"] or "").replace("|", "\\|")
            dur = v.get("duration") or ""
            md_lines.append(f"| {i} | `{v['id']}` | {title} | {dur} | {v['url']} |")
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        print(
            f"Wrote {index_path} and {md_path} ({len(videos)} videos, no transcripts fetched)",
            file=sys.stderr,
        )
        return 0

    mpath = manifest_path(out_root)
    manifest = load_manifest(mpath)
    index_rows: list[dict[str, object]] = []

    for i, v in enumerate(videos):
        res, manifest = fetch_one_video(
            v,
            out_root=out_root,
            languages=langs,
            langs_tier2=langs2,
            fetched_at_utc=ts,
            min_quality=min_q,
            keep_low_quality=args.keep_low_quality,
            enable_whisper=args.enable_whisper,
            force=args.force,
            manifest=manifest,
            sleep_s=args.sleep,
            resume=args.resume,
        )
        index_rows.append(result_to_index_row(res))
        if args.sleep > 0 and i + 1 < len(videos):
            time.sleep(args.sleep)

    save_manifest(mpath, manifest)

    index_path = out_root / "index.json"
    payload = {
        "channel_url": inputs[0] if inputs else args.channel,
        "input_urls": inputs,
        "pipeline_version": __import__(
            "youtube_transcripts.constants", fromlist=["PIPELINE_VERSION"]
        ).PIPELINE_VERSION,
        "generated_at_utc": ts,
        "video_count": len(videos),
        "transcripts_attempted": len(index_rows),
        "videos": index_rows,
    }
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {index_path} and {mpath}", file=sys.stderr)
    print(f"Transcripts in {tx_dir}", file=sys.stderr)
    ok_n = sum(1 for x in index_rows if x.get("status") == "ok")
    err_n = sum(1 for x in index_rows if x.get("status") == "error")
    sk_n = sum(1 for x in index_rows if str(x.get("status") or "").startswith("skipped"))
    print(f"Summary: ok={ok_n} error={err_n} skipped/unchanged={sk_n}", file=sys.stderr)
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
