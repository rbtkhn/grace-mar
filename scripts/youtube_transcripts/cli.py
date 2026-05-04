from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1].parent

# Allow `python scripts/fetch_youtube_channel_transcripts.py` without install
_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _parse_langs(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def _format_upload_date(raw: str) -> str:
    """yt-dlp often returns YYYYMMDD; normalize to YYYY-MM-DD for tables."""
    s = (raw or "").strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s


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
        "--playlist-items",
        type=str,
        default="",
        help="yt-dlp playlist item selector (for example '21-40').",
    )
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
    parser.add_argument(
        "--enrich-metadata",
        action="store_true",
        help="With --index-only: one yt-dlp metadata fetch per video so upload_date is filled (flat lists often omit it). Slower; uses --sleep between videos.",
    )
    parser.add_argument(
        "--enrich-concurrency",
        type=int,
        default=8,
        help="Parallel metadata fetches for --index-only --enrich-metadata (default: 8).",
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
    parser.add_argument(
        "--stop-before-date",
        type=str,
        default="",
        help="Optional earliest upload date to keep (YYYY-MM-DD). When set, flat listings stop once entries get older than this.",
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

    stop_before_date = None
    if args.stop_before_date.strip():
        stop_before_date = date.fromisoformat(args.stop_before_date.strip())

    all_videos: list[dict[str, str]] = []
    for inp in inputs:
        print(f"Listing videos: {inp}", file=sys.stderr)
        part = list_videos(
            inp,
            limit=limit,
            playlist_items=args.playlist_items.strip() or None,
            stop_before_date=stop_before_date,
            max_attempts=args.max_attempts_listing,
        )
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
        if args.enrich_metadata:
            from youtube_transcripts.metadata import fetch_metadata_ytdlp

            max_workers = max(1, int(args.enrich_concurrency or 1))

            def _fetch(v: dict[str, str]) -> tuple[str, dict[str, object]]:
                return v["id"], fetch_metadata_ytdlp(v["id"], max_attempts=args.max_attempts_listing)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(_fetch, v) for v in videos]
                for future in as_completed(futures):
                    vid, info = future.result()
                    if not isinstance(info, dict) or not info:
                        continue
                    for v in videos:
                        if v["id"] != vid:
                            continue
                        ud = (info.get("upload_date") or "").strip()
                        if ud:
                            v["upload_date"] = ud
                        t = (info.get("title") or "").strip()
                        if t:
                            v["title"] = t
                        dur = info.get("duration")
                        if dur is not None:
                            v["duration"] = str(dur)
                        break
            if args.sleep > 0 and len(videos) > 1:
                time.sleep(min(args.sleep, 0.01))

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
        ch = inputs[0] if inputs else args.channel
        if args.enrich_metadata:
            date_note = (
                "- **upload_date:** per-video yt-dlp metadata (`--enrich-metadata`); shown as YYYY-MM-DD when parseable."
            )
        else:
            date_note = (
                "- **upload_date:** often **empty** under flat channel listing; re-run with "
                "`--index-only --enrich-metadata` to fill dates (one metadata fetch per video, slower)."
            )
        md_lines = [
            "# Channel video index",
            "",
            f"- **channel:** {ch}",
            f"- **video_count:** {len(videos)}",
            f"- **generated_at_utc:** {ts}",
            "- **method:** index-only (no transcripts downloaded)",
            date_note,
            "",
            "| # | video_id | title | upload_date | duration_s | url |",
            "|---:|---|-----|-----|---:|-----|",
        ]
        for i, v in enumerate(videos, start=1):
            title = (v["title"] or "").replace("|", "\\|")
            dur = v.get("duration") or ""
            udate = _format_upload_date(str(v.get("upload_date") or ""))
            md_lines.append(f"| {i} | `{v['id']}` | {title} | {udate} | {dur} | {v['url']} |")
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
