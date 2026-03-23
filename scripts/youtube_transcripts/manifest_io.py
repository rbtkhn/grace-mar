from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from youtube_transcripts.constants import MANIFEST_VERSION, PIPELINE_VERSION


def manifest_path(output_dir: Path) -> Path:
    return output_dir / "transcript_manifest.json"


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "manifest_version": MANIFEST_VERSION,
            "pipeline_version": PIPELINE_VERSION,
            "last_run_utc": None,
            "videos": {},
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {
            "manifest_version": MANIFEST_VERSION,
            "pipeline_version": PIPELINE_VERSION,
            "last_run_utc": None,
            "videos": {},
        }
    if "videos" not in data:
        data["videos"] = {}
    return data


def save_manifest(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["manifest_version"] = MANIFEST_VERSION
    data["pipeline_version"] = PIPELINE_VERSION
    data["last_run_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def update_video_entry(
    manifest: dict[str, Any],
    video_id: str,
    *,
    content_hash: str | None,
    source_tier: str,
    quality: float,
    status: str,
    error: str | None = None,
) -> None:
    vids = manifest.setdefault("videos", {})
    row = vids.get(video_id, {})
    row.update(
        {
            "content_hash": content_hash,
            "source_tier": source_tier,
            "quality": round(quality, 4),
            "status": status,
            "error": error,
            "last_updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    if status == "ok" and content_hash:
        row["last_successful_fetch_at_utc"] = row["last_updated_utc"]
    vids[video_id] = row
