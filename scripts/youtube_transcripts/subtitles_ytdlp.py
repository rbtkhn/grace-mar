"""Tier 2: yt-dlp subtitle files (manual / automatic)."""

from __future__ import annotations

import re
from pathlib import Path
from tempfile import TemporaryDirectory

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # type: ignore


def _vtt_to_plain(vtt: str) -> str:
    lines_out: list[str] = []
    for line in vtt.splitlines():
        s = line.strip()
        if not s or s.startswith("WEBVTT") or s.startswith("NOTE") or "-->" in s:
            continue
        if re.match(r"^\d+$", s):
            continue
        # strip tags like <c> or <v Speaker>
        s = re.sub(r"<[^>]+>", "", s)
        if s:
            lines_out.append(s)
    return "\n".join(lines_out).strip()


def fetch_subtitles_ytdlp(
    video_id: str,
    languages: list[str],
    *,
    prefer_manual: bool = True,
) -> tuple[str | None, str | None, str | None, str | None]:
    """
    Download subtitles via yt-dlp (skip video).
    Returns (plain_text, kind_manual_or_auto, language, error).
    """
    if yt_dlp is None:
        return None, None, None, "yt-dlp not installed"
    url = f"https://www.youtube.com/watch?v={video_id}"
    langs = languages[:8] if languages else ["en", "en-US", "zh-Hans", "zh-CN"]

    with TemporaryDirectory(prefix="ytsub_") as tmp:
        tmp_path = Path(tmp)
        outtmpl = str(tmp_path / "%(id)s")
        opts: dict = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": langs,
            "outtmpl": outtmpl,
            "ignoreerrors": False,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            return None, None, None, str(e)

        all_vtt = sorted(tmp_path.glob("*.vtt"))
        if not all_vtt:
            return None, None, None, "no vtt subtitle file produced"
        manual_files = [
            p
            for p in all_vtt
            if ".auto." not in p.name and "auto-generated" not in p.name.lower()
        ]
        auto_files = [p for p in all_vtt if p not in manual_files]
        chosen: Path | None = None
        kind: str | None = None
        if prefer_manual and manual_files:
            chosen = manual_files[0]
            kind = "manual"
        elif auto_files:
            chosen = auto_files[0]
            kind = "auto"
        else:
            chosen = all_vtt[0]
            kind = "manual"

        text = _vtt_to_plain(chosen.read_text(encoding="utf-8", errors="replace"))
        if not text:
            return None, kind, None, "empty vtt after parse"
        lang_guess = chosen.stem.replace(video_id, "").strip(".-_") or "unknown"
        return text, kind, lang_guess, None
