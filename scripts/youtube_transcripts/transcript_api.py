"""Tier 1: youtube-transcript-api (timedtext)."""

from __future__ import annotations

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None  # type: ignore


def fetch_transcript_tier1(
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
        snippets = getattr(ft, "snippets", None)
        if not snippets:
            return ""
        lines = [getattr(s, "text", "").strip() for s in snippets]
        return "\n".join(x for x in lines if x)

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


def fetch_transcript_tier1_with_meta(
    video_id: str,
    languages: list[str],
) -> tuple[str | None, str | None, str | None, float | None]:
    """Returns (text, lang, err, coverage_seconds)."""
    if YouTubeTranscriptApi is None:
        return None, None, "youtube-transcript-api not installed", None

    def _cov(parts: list) -> float | None:
        if not parts:
            return None
        last = parts[-1]
        if isinstance(last, dict):
            return float(last.get("start", 0)) + float(last.get("duration", 0))
        return None

    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        if languages:
            try:
                parts = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                if isinstance(parts, list) and parts:
                    lines = [p.get("text", "").strip() for p in parts if isinstance(p, dict)]
                    text = "\n".join(x for x in lines if x)
                    if text:
                        return text, ",".join(languages[:3]), None, _cov(parts)
            except Exception:
                pass
        try:
            parts = YouTubeTranscriptApi.get_transcript(video_id)
            if isinstance(parts, list) and parts:
                lines = [p.get("text", "").strip() for p in parts if isinstance(p, dict)]
                text = "\n".join(x for x in lines if x)
                if text:
                    return text, "default", None, _cov(parts)
        except Exception:
            pass

    t, lang, err = fetch_transcript_tier1(video_id, languages)
    return t, lang, err, None
