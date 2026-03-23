from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from youtube_transcripts.constants import PIPELINE_VERSION
from youtube_transcripts.hashing import compute_content_hash
from youtube_transcripts.manifest_io import load_manifest, manifest_path, save_manifest, update_video_entry
from youtube_transcripts.metadata import fetch_metadata_ytdlp, fetch_metadata_youtube_api, ytdlp_to_record
from youtube_transcripts.quality import compute_quality, tier_from_parts
from youtube_transcripts.subtitles_ytdlp import fetch_subtitles_ytdlp
from youtube_transcripts.transcript_api import fetch_transcript_tier1_with_meta
from youtube_transcripts import whisper_local


def _safe_filename(title: str, max_len: int = 100) -> str:
    t = re.sub(r"[^\w\s\-_.]", "", title, flags=re.UNICODE)
    t = re.sub(r"[\s_]+", "-", t).strip("-_.")[:max_len]
    return t or "untitled"


@dataclass
class FetchResult:
    video_id: str
    title: str
    url: str
    transcript_file: str
    status: str
    language: str | None
    error: str | None
    upload_date: str | None
    duration_seconds: float | None
    metadata_source: str | None
    content_hash: str | None
    pipeline_version: str
    source_tier: str
    quality: float
    caption_kinds_available: dict[str, Any]
    youtube_api_meta: dict[str, Any] | None
    fetched_at_utc: str
    last_listing_seen_at: str


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, "").strip() or default)
    except ValueError:
        return default


def fetch_one_video(
    video: dict[str, str],
    *,
    out_root: Path,
    languages: list[str],
    langs_tier2: list[str],
    fetched_at_utc: str,
    min_quality: float,
    keep_low_quality: bool,
    enable_whisper: bool,
    force: bool,
    manifest: dict[str, Any],
    sleep_s: float,
    resume: bool,
) -> tuple[FetchResult, dict[str, Any]]:
    """Returns (result, updated_manifest fragment)."""
    vid = video["id"]
    title = video["title"]
    url = video["url"]
    tx_dir = out_root / "transcripts"
    tx_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{vid}_{_safe_filename(title)}"
    path = tx_dir / f"{stem}.txt"

    meta_full = fetch_metadata_ytdlp(vid)
    yrec = ytdlp_to_record(meta_full) if meta_full else {}
    duration_seconds: float | None = None
    if yrec.get("duration_seconds") is not None:
        try:
            duration_seconds = float(yrec["duration_seconds"])
        except (TypeError, ValueError):
            duration_seconds = None
    if duration_seconds is None and video.get("duration"):
        try:
            duration_seconds = float(video["duration"])
        except (TypeError, ValueError):
            duration_seconds = None

    api_extra = fetch_metadata_youtube_api(vid)
    caption_kinds = {
        "manual_langs": yrec.get("caption_manual_langs") or [],
        "auto_langs": yrec.get("caption_auto_langs") or [],
    }

    prev = (manifest.get("videos") or {}).get(vid, {})
    prev_hash = prev.get("content_hash")

    # --resume: skip if transcript file already exists (legacy behavior)
    if resume and not force and path.exists() and path.stat().st_size > 50:
        raw_existing = path.read_text(encoding="utf-8", errors="replace")
        chash_existing = compute_content_hash(vid, raw_existing, PIPELINE_VERSION)
        q = float(prev.get("quality") or 0.5)
        stier = str(prev.get("source_tier") or "tier1_api")
        result = FetchResult(
            video_id=vid,
            title=title,
            url=url,
            transcript_file=str(path.relative_to(out_root)),
            status="skipped_existing",
            language=prev.get("language"),
            error=None,
            upload_date=(video.get("upload_date") or yrec.get("upload_date")),
            duration_seconds=duration_seconds,
            metadata_source=str(yrec.get("metadata_source") or "yt-dlp"),
            content_hash=chash_existing,
            pipeline_version=PIPELINE_VERSION,
            source_tier=stier,
            quality=q,
            caption_kinds_available=caption_kinds,
            youtube_api_meta=api_extra,
            fetched_at_utc=fetched_at_utc,
            last_listing_seen_at=fetched_at_utc,
        )
        update_video_entry(
            manifest,
            vid,
            content_hash=chash_existing,
            source_tier=stier,
            quality=q,
            status="skipped_existing",
        )
        return result, manifest

    prev_hash = prev.get("content_hash")

    # Tier 1
    text: str | None = None
    lang: str | None = None
    err: str | None = None
    coverage: float | None = None
    tier_key = "tier1_api"

    text, lang, err, coverage = fetch_transcript_tier1_with_meta(vid, languages)

    # Tier 2
    if not text:
        t2, kind, slang, e2 = fetch_subtitles_ytdlp(vid, langs_tier2 or languages)
        if t2:
            text = t2
            lang = slang or lang
            tier_key = tier_from_parts("ytdlp", kind)
            err = None
        else:
            err = e2 or err

    # Tier 3
    if not text and enable_whisper:
        tw, ew = whisper_local.transcribe_video_whisper(vid)
        if tw:
            text = tw
            lang = lang or "whisper"
            tier_key = "tier3_whisper"
            err = None
        else:
            err = ew or err

    quality = compute_quality(text or "", duration_seconds, tier_key, coverage)
    chash: str | None = None
    if text:
        chash = compute_content_hash(vid, text, PIPELINE_VERSION)

    if (
        not force
        and chash
        and prev_hash == chash
        and prev.get("status") == "ok"
        and quality >= min_quality
    ):
        status = "skipped_unchanged"
        result = FetchResult(
            video_id=vid,
            title=title,
            url=url,
            transcript_file=str(path.relative_to(out_root)) if path.exists() else "",
            status=status,
            language=prev.get("language"),
            error=None,
            upload_date=(video.get("upload_date") or yrec.get("upload_date")),
            duration_seconds=duration_seconds,
            metadata_source=str(yrec.get("metadata_source") or "yt-dlp"),
            content_hash=chash,
            pipeline_version=PIPELINE_VERSION,
            source_tier=tier_key,
            quality=quality,
            caption_kinds_available=caption_kinds,
            youtube_api_meta=api_extra,
            fetched_at_utc=fetched_at_utc,
            last_listing_seen_at=fetched_at_utc,
        )
        update_video_entry(
            manifest,
            vid,
            content_hash=chash,
            source_tier=tier_key,
            quality=quality,
            status=status,
        )
        return result, manifest

    if not text:
        status = "error"
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# video_id: {vid}\n# title: {title}\n# url: {url}\n"
            f"# status: ERROR\n# error: {err}\n",
            encoding="utf-8",
        )
        update_video_entry(
            manifest,
            vid,
            content_hash=None,
            source_tier=tier_key,
            quality=0.0,
            status=status,
            error=str(err),
        )
        return (
            FetchResult(
                video_id=vid,
                title=title,
                url=url,
                transcript_file=str(path.relative_to(out_root)),
                status=status,
                language=None,
                error=str(err),
                upload_date=(video.get("upload_date") or yrec.get("upload_date")),
                duration_seconds=duration_seconds,
                metadata_source=str(yrec.get("metadata_source") or "yt-dlp"),
                content_hash=None,
                pipeline_version=PIPELINE_VERSION,
                source_tier=tier_key,
                quality=0.0,
                caption_kinds_available=caption_kinds,
                youtube_api_meta=api_extra,
                fetched_at_utc=fetched_at_utc,
                last_listing_seen_at=fetched_at_utc,
            ),
            manifest,
        )

    assert text is not None
    low_q = quality < min_quality
    if low_q and not keep_low_quality:
        status = "rejected_low_quality"
        path.write_text(
            f"# video_id: {vid}\n# title: {title}\n# url: {url}\n"
            f"# status: REJECTED_LOW_QUALITY quality={quality:.3f}\n# error: below TRANSCRIPT_MIN_QUALITY\n",
            encoding="utf-8",
        )
        update_video_entry(
            manifest,
            vid,
            content_hash=chash,
            source_tier=tier_key,
            quality=quality,
            status=status,
            error="below min quality",
        )
    elif low_q and keep_low_quality:
        status = "needs_review"
        header = (
            f"# YouTube transcript (quality flag: needs_review)\n"
            f"# video_id: {vid}\n"
            f"# title: {title}\n"
            f"# url: {url}\n"
            f"# language: {lang or 'unknown'}\n"
            f"# source_tier: {tier_key}\n"
            f"# quality: {quality:.4f}\n"
            f"# fetched_at_utc: {fetched_at_utc}\n"
            f"#\n\n"
        )
        path.write_text(header + text + "\n", encoding="utf-8")
        update_video_entry(
            manifest,
            vid,
            content_hash=chash,
            source_tier=tier_key,
            quality=quality,
            status=status,
        )
    else:
        status = "ok"
        header = (
            f"# YouTube transcript (auto/creator captions)\n"
            f"# video_id: {vid}\n"
            f"# title: {title}\n"
            f"# url: {url}\n"
            f"# language: {lang or 'unknown'}\n"
            f"# source_tier: {tier_key}\n"
            f"# quality: {quality:.4f}\n"
            f"# fetched_at_utc: {fetched_at_utc}\n"
            f"#\n\n"
        )
        path.write_text(header + text + "\n", encoding="utf-8")
        update_video_entry(
            manifest,
            vid,
            content_hash=chash,
            source_tier=tier_key,
            quality=quality,
            status=status,
        )

    result = FetchResult(
        video_id=vid,
        title=title,
        url=url,
        transcript_file=str(path.relative_to(out_root)),
        status=status,
        language=lang,
        error=None if status == "ok" else (None if status == "needs_review" else "low_quality"),
        upload_date=(video.get("upload_date") or yrec.get("upload_date")),
        duration_seconds=duration_seconds,
        metadata_source=str(yrec.get("metadata_source") or "yt-dlp"),
        content_hash=chash,
        pipeline_version=PIPELINE_VERSION,
        source_tier=tier_key,
        quality=quality,
        caption_kinds_available=caption_kinds,
        youtube_api_meta=api_extra,
        fetched_at_utc=fetched_at_utc,
        last_listing_seen_at=fetched_at_utc,
    )
    return result, manifest


def result_to_index_row(r: FetchResult) -> dict[str, Any]:
    row: dict[str, Any] = {
        "video_id": r.video_id,
        "title": r.title,
        "upload_date": r.upload_date,
        "duration_seconds": r.duration_seconds,
        "url": r.url,
        "transcript_file": r.transcript_file,
        "status": r.status,
        "language": r.language,
        "error": r.error,
        "metadata_source": r.metadata_source,
        "caption_kinds_available": r.caption_kinds_available,
        "content_hash": r.content_hash,
        "pipeline_version": r.pipeline_version,
        "source_tier": r.source_tier,
        "quality": round(r.quality, 4),
        "fetched_at_utc": r.fetched_at_utc,
        "last_listing_seen_at": r.last_listing_seen_at,
    }
    if r.youtube_api_meta:
        row["youtube_api"] = r.youtube_api_meta
    return row
