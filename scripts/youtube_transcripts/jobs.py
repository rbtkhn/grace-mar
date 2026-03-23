"""RQ job payloads for parallel transcript fetching."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def run_fetch_video_job(serialized: str) -> dict[str, Any]:
    """
    RQ entry: JSON string with keys:
      output_dir, video (dict), languages, langs_tier2, min_quality,
      keep_low_quality, enable_whisper, force, resume, fetched_at_utc
    """
    import filelock

    from youtube_transcripts.manifest_io import load_manifest, manifest_path, save_manifest
    from youtube_transcripts.pipeline import fetch_one_video, result_to_index_row

    cfg = json.loads(serialized)
    out_root = Path(cfg["output_dir"])
    video = cfg["video"]
    langs = cfg["languages"]
    langs2 = cfg.get("langs_tier2") or langs
    mpath = manifest_path(out_root)
    lock = filelock.FileLock(str(mpath) + ".lock")
    with lock:
        manifest = load_manifest(mpath)
        res, manifest = fetch_one_video(
            video,
            out_root=out_root,
            languages=langs,
            langs_tier2=langs2,
            fetched_at_utc=cfg["fetched_at_utc"],
            min_quality=float(cfg.get("min_quality", os.environ.get("TRANSCRIPT_MIN_QUALITY", "0.35"))),
            keep_low_quality=bool(cfg.get("keep_low_quality", False)),
            enable_whisper=bool(cfg.get("enable_whisper", False)),
            force=bool(cfg.get("force", False)),
            manifest=manifest,
            resume=bool(cfg.get("resume", False)),
        )
        save_manifest(mpath, manifest)
    return result_to_index_row(res)
