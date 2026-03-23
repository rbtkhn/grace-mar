#!/usr/bin/env python3
"""
List all videos on a YouTube channel and save captions/transcripts to disk.

Uses **yt-dlp** (flat playlist extract) + **youtube-transcript-api** (timedtext).
Respect YouTube Terms of Service; use for research / operator analysis only — not part of the Record.

Install (optional extra):

  pip install -e ".[youtube-research]"

Or:

  pip install yt-dlp youtube-transcript-api

Examples:

  python3 scripts/fetch_youtube_channel_transcripts.py \\
    --channel "https://www.youtube.com/@PredictiveHistory/videos" \\
    --output-dir research/external/youtube-channels/predictive-history

  python3 scripts/fetch_youtube_channel_transcripts.py --limit 5 --dry-run

  # Full channel episode list in index.json only (no transcript downloads):
  python3 scripts/fetch_youtube_channel_transcripts.py --index-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # type: ignore

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None  # type: ignore


def _safe_filename(title: str, max_len: int = 100) -> str:
    t = re.sub(r"[^\w\s\-_.]", "", title, flags=re.UNICODE)
    t = re.sub(r"[\s_]+", "-", t).strip("-_.")[:max_len]
    return t or "untitled"


def _list_videos(channel_url: str, *, limit: int | None) -> list[dict[str, str]]:
    if yt_dlp is None:
        raise SystemExit("Missing dependency: pip install yt-dlp")
    opts: dict = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "ignoreerrors": True,
    }
    if limit is not None and limit > 0:
        opts["playlistend"] = limit
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    entries = info.get("entries") or []
    out: list[dict[str, str]] = []
    for e in entries:
        if not e:
            continue
        vid = e.get("id") or ""
        if not vid:
            continue
        dur = e.get("duration")
        out.append(
            {
                "id": vid,
                "title": (e.get("title") or "").strip() or vid,
                "upload_date": (e.get("upload_date") or "").strip(),
                "duration": str(dur) if dur is not None else "",
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return out


def _fetch_transcript(
    video_id: str,
    languages: list[str],
) -> tuple[str | None, str | None, str | None]:
    """Returns (plain_text, language_label, error_message)."""
    if YouTubeTranscriptApi is None:
        return None, None, "youtube-transcript-api not installed"
    last_err = ""

    def _parts_to_text(parts: object) -> str:
        if not isinstance(parts, list):
            return ""
        lines = [p.get("text", "").strip() for p in parts if isinstance(p, dict)]
        return "\n".join(x for x in lines if x)

    def _text_from_fetched(ft: object) -> str:
        """youtube-transcript-api 1.x returns FetchedTranscript with .snippets."""
        snippets = getattr(ft, "snippets", None)
        if not snippets:
            return ""
        lines = [getattr(s, "text", "").strip() for s in snippets]
        return "\n".join(x for x in lines if x)

    # Legacy 0.6.x: class methods get_transcript / list_transcripts
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        if languages:
            try:
                parts = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                text = _parts_to_text(parts)
                if text:
                    return text, ",".join(languages[:3]), None
            except Exception as e:
                last_err = str(e)
        try:
            parts = YouTubeTranscriptApi.get_transcript(video_id)
            text = _parts_to_text(parts)
            if text:
                return text, "default", None
        except Exception as e:
            last_err = str(e)
        try:
            tlist = YouTubeTranscriptApi.list_transcripts(video_id)
            for tr in tlist:
                parts = tr.fetch()
                text = _parts_to_text(parts)
                if text:
                    code = getattr(tr, "language_code", None) or "unknown"
                    return text, code, None
        except Exception as e:
            last_err = str(e)
        return None, None, last_err or "no transcript"

    # 1.x: instance API — fetch() / list()
    api = YouTubeTranscriptApi()
    if languages:
        try:
            ft = api.fetch(video_id, languages=languages)
            text = _text_from_fetched(ft)
            if text:
                code = getattr(ft, "language_code", None) or ",".join(languages[:3])
                return text, code, None
        except Exception as e:
            last_err = str(e)
    try:
        ft = api.fetch(video_id)
        text = _text_from_fetched(ft)
        if text:
            code = getattr(ft, "language_code", None) or "default"
            return text, code, None
    except Exception as e:
        last_err = str(e)

    try:
        tlist = api.list(video_id)
        for tr in tlist:
            ft = tr.fetch()
            text = _text_from_fetched(ft)
            if text:
                code = getattr(tr, "language_code", None) or "unknown"
                return text, code, None
    except Exception as e:
        last_err = str(e)

    return None, None, last_err or "no transcript"


def main() -> int:
    parser = argparse.ArgumentParser(description="Download YouTube channel video transcripts.")
    parser.add_argument(
        "--channel",
        default="https://www.youtube.com/@PredictiveHistory/videos",
        help="Channel uploads URL or @handle /videos page",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=str(REPO_ROOT / "research/external/youtube-channels/predictive-history"),
        help="Directory for transcripts/ and index.json",
    )
    parser.add_argument("--limit", type=int, default=0, help="Max videos (0 = all)")
    parser.add_argument(
        "--languages",
        default="en,en-US,zh-Hans,zh-CN",
        help="Comma-separated caption languages to prefer (fallback: any available)",
    )
    parser.add_argument("--sleep", type=float, default=0.4, help="Seconds between transcript requests")
    parser.add_argument("--dry-run", action="store_true", help="Only list video IDs and titles")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Write index.json from channel listing only (no transcript downloads)",
    )
    parser.add_argument("--resume", action="store_true", help="Skip videos that already have a .txt file")
    args = parser.parse_args()

    out_root = Path(args.output_dir)
    tx_dir = out_root / "transcripts"
    tx_dir.mkdir(parents=True, exist_ok=True)

    limit = args.limit if args.limit > 0 else None
    langs = [x.strip() for x in args.languages.split(",") if x.strip()]

    print(f"Listing videos: {args.channel}", file=sys.stderr)
    videos = _list_videos(args.channel, limit=limit)
    print(f"Found {len(videos)} video(s).", file=sys.stderr)

    if args.dry_run:
        for v in videos:
            print(f"{v['id']}\t{v['title']}")
        return 0

    if args.index_only:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
            "channel_url": args.channel,
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
            f"- **channel:** {args.channel}",
            f"- **video_count:** {len(videos)}",
            f"- **generated_at_utc:** {ts}",
            "- **method:** `python3 scripts/fetch_youtube_channel_transcripts.py --index-only` (playlist walk; no transcripts downloaded)",
            "",
            "| # | video_id | title | duration_s | url |",
            "|---:|---|-----|---:|-----|",
        ]
        for i, v in enumerate(videos, start=1):
            title = (v["title"] or "").replace("|", "\\|")
            dur = v.get("duration") or ""
            md_lines.append(
                f"| {i} | `{v['id']}` | {title} | {dur} | {v['url']} |"
            )
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        print(
            f"Wrote {index_path} and {md_path} ({len(videos)} videos, no transcripts fetched)",
            file=sys.stderr,
        )
        return 0

    index: list[dict[str, object]] = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for i, v in enumerate(videos):
        vid = v["id"]
        title = v["title"]
        stem = f"{vid}_{_safe_filename(title)}"
        path = tx_dir / f"{stem}.txt"

        if args.resume and path.exists() and path.stat().st_size > 50:
            index.append(
                {
                    "video_id": vid,
                    "title": title,
                    "upload_date": v.get("upload_date"),
                    "url": v["url"],
                    "transcript_file": str(path.relative_to(out_root)),
                    "status": "skipped_existing",
                    "language": None,
                    "error": None,
                }
            )
            continue

        text, lang, err = _fetch_transcript(vid, langs)
        if text:
            header = (
                f"# YouTube transcript (auto/creator captions)\n"
                f"# video_id: {vid}\n"
                f"# title: {title}\n"
                f"# url: {v['url']}\n"
                f"# language: {lang or 'unknown'}\n"
                f"# fetched_at_utc: {ts}\n"
                f"#\n\n"
            )
            path.write_text(header + text + "\n", encoding="utf-8")
            status = "ok"
        else:
            status = "error"
            path.write_text(
                f"# video_id: {vid}\n# title: {title}\n# url: {v['url']}\n"
                f"# status: ERROR\n# error: {err}\n",
                encoding="utf-8",
            )

        index.append(
            {
                "video_id": vid,
                "title": title,
                "upload_date": v.get("upload_date"),
                "url": v["url"],
                "transcript_file": str(path.relative_to(out_root)),
                "status": status,
                "language": lang,
                "error": err if status == "error" else None,
            }
        )
        if i + 1 < len(videos):
            time.sleep(max(0.0, args.sleep))

    index_path = out_root / "index.json"
    payload = {
        "channel_url": args.channel,
        "generated_at_utc": ts,
        "video_count": len(videos),
        "transcripts_attempted": len(index),
        "videos": index,
    }
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {index_path}", file=sys.stderr)
    print(f"Transcripts in {tx_dir}", file=sys.stderr)
    ok_n = sum(1 for x in index if x.get("status") == "ok")
    err_n = sum(1 for x in index if x.get("status") == "error")
    sk_n = sum(1 for x in index if x.get("status") == "skipped_existing")
    print(f"Summary: ok={ok_n} error={err_n} skipped={sk_n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
