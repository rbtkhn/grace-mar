"""Per-video metadata via yt-dlp full extract; optional YouTube Data API v3."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # type: ignore

from youtube_transcripts.retry import retry_call


def fetch_metadata_ytdlp(video_id: str, *, max_attempts: int = 4) -> dict[str, object]:
    """Full extract_info for one video (not flat)."""
    if yt_dlp is None:
        return {}
    url = f"https://www.youtube.com/watch?v={video_id}"

    def _one() -> dict[str, object]:
        opts: dict = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "ignoreerrors": False,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if not isinstance(info, dict):
            return {}
        return info

    try:
        return retry_call(_one, max_attempts=max_attempts)
    except Exception:
        return {}


def ytdlp_to_record(info: dict[str, object]) -> dict[str, object]:
    """Normalize yt-dlp info dict for manifest."""
    dur = info.get("duration")
    subs = info.get("subtitles") or {}
    auto_s = info.get("automatic_captions") or {}
    manual_langs = list(subs.keys()) if isinstance(subs, dict) else []
    auto_langs = list(auto_s.keys()) if isinstance(auto_s, dict) else []
    return {
        "duration_seconds": int(dur) if dur is not None else None,
        "upload_date": (info.get("upload_date") or "") or None,
        "title": (info.get("title") or "") or None,
        "channel": (info.get("channel") or info.get("uploader") or "") or None,
        "was_live": bool(info.get("was_live") or info.get("is_live")),
        "availability": (info.get("availability") or "") or None,
        "metadata_source": "yt-dlp",
        "caption_manual_langs": manual_langs[:40],
        "caption_auto_langs": auto_langs[:40],
    }


def fetch_metadata_youtube_api(video_id: str) -> dict[str, object] | None:
    """Optional snippet + contentDetails; requires GOOGLE_API_KEY."""
    key = (os.environ.get("GOOGLE_API_KEY") or os.environ.get("YOUTUBE_DATA_API_KEY") or "").strip()
    if not key:
        return None
    q = urllib.parse.urlencode(
        {
            "part": "snippet,contentDetails",
            "id": video_id,
            "key": key,
        }
    )
    url = f"https://www.googleapis.com/youtube/v3/videos?{q}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    items = raw.get("items") or []
    if not items:
        return None
    it = items[0]
    sn = it.get("snippet") or {}
    cd = it.get("contentDetails") or {}
    iso_dur = cd.get("duration") or ""
    return {
        "published_at": sn.get("publishedAt"),
        "title_api": sn.get("title"),
        "duration_iso8601": iso_dur,
        "metadata_source_api": "youtube_data_v3",
    }
