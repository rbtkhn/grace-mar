from __future__ import annotations

import re
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # type: ignore

from youtube_transcripts.retry import retry_call


def _normalize_url_line(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    return line


def load_inputs_from_file(path: Path) -> list[str]:
    """Load channel URLs, playlist URLs, or watch URLs (one per line)."""
    out: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        u = _normalize_url_line(raw)
        if u:
            out.append(u)
    return out


def extract_video_id(text: str) -> str | None:
    """Best-effort 11-char video id from URL or raw id."""
    t = text.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", t):
        return t
    m = re.search(r"(?:v=|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})", t)
    return m.group(1) if m else None


def list_videos(
    url_or_id: str,
    *,
    limit: int | None,
    max_attempts: int = 4,
) -> list[dict[str, str]]:
    """
    List videos using yt-dlp flat extraction (channel, playlist, or single video URL).
    Returns dicts: id, title, upload_date, duration (string), url.
    """
    if yt_dlp is None:
        raise RuntimeError("Missing dependency: pip install yt-dlp")

    url = url_or_id.strip()
    vid = extract_video_id(url)
    if vid and "youtube.com" not in url and "youtu.be" not in url and "playlist" not in url:
        # Bare 11-char id — treat as watch URL
        url = f"https://www.youtube.com/watch?v={vid}"

    def _extract() -> list[dict[str, str]]:
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
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries")
        if entries is None:
            entries = []
        # Single video (not a playlist)
        if not entries and isinstance(info, dict) and info.get("id"):
            entries = [info]
        out: list[dict[str, str]] = []
        for e in entries:
            if not e:
                continue
            eid = e.get("id") or ""
            if not eid:
                continue
            dur = e.get("duration")
            out.append(
                {
                    "id": eid,
                    "title": (e.get("title") or "").strip() or eid,
                    "upload_date": (e.get("upload_date") or "").strip(),
                    "duration": str(dur) if dur is not None else "",
                    "url": f"https://www.youtube.com/watch?v={eid}",
                }
            )
        return out

    return retry_call(_extract, max_attempts=max_attempts)
