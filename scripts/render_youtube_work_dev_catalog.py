#!/usr/bin/env python3
"""
Merge youtube-indexes/index.json + operator-maintained ingestion.json into:

  - CHANNEL-CATALOG.md — table with ingested? + artifact paths
  - episode-catalog.json — merged rows for scripts / ML (ingested flag per video)

Does not modify index.json or ingestion.json. Run after refreshing index or editing ingestion.

  python3 scripts/render_youtube_work_dev_catalog.py \\
    research/external/work-dev/youtube-indexes/nate-b-jones
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _esc_cell(s: str) -> str:
    return (s or "").replace("|", "\\|")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render CHANNEL-CATALOG.md + episode-catalog.json from index + ingestion."
    )
    parser.add_argument(
        "channel_dir",
        type=Path,
        help="Path to e.g. research/external/work-dev/youtube-indexes/nate-b-jones",
    )
    args = parser.parse_args()
    ch_dir = args.channel_dir.resolve()
    if not ch_dir.is_dir():
        print(f"Not a directory: {ch_dir}", file=sys.stderr)
        return 2

    index_path = ch_dir / "index.json"
    ingest_path = ch_dir / "ingestion.json"
    if not index_path.is_file():
        print(f"Missing {index_path}", file=sys.stderr)
        return 2

    index_data = json.loads(index_path.read_text(encoding="utf-8"))
    videos_raw = index_data.get("videos")
    if not isinstance(videos_raw, list):
        print("index.json: expected top-level 'videos' array", file=sys.stderr)
        return 2

    ingest_map: dict = {}
    if ingest_path.is_file():
        ing = json.loads(ingest_path.read_text(encoding="utf-8"))
        raw = ing.get("by_video_id")
        if isinstance(raw, dict):
            ingest_map = raw

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    merged_rows: list[dict] = []

    md_lines = [
        "# Channel catalog (listing + manual ingestion)",
        "",
        f"- **channel_dir:** `{ch_dir.relative_to(REPO_ROOT)}`",
        f"- **source_index_generated_at_utc:** `{index_data.get('generated_at_utc', '')}`",
        f"- **catalog_rendered_at_utc:** `{now}`",
        "- **ingested:** operator-curated material exists in-repo (see [ingestion.json](ingestion.json)); not automatic from YouTube.",
        "",
        "| # | video_id | ingested | artifact(s) | title | url |",
        "|---:|:---|:---:|:---|-----|-----|",
    ]

    for i, v in enumerate(videos_raw, start=1):
        if not isinstance(v, dict):
            continue
        vid = str(v.get("video_id") or "").strip()
        title = str(v.get("title") or "")
        url = str(v.get("url") or "")
        entry = ingest_map.get(vid) if vid else None
        ingested = False
        artifacts: list[str] = []
        ingested_at = ""
        if isinstance(entry, dict):
            ingested = bool(entry.get("ingested"))
            arts = entry.get("artifacts")
            if isinstance(arts, list):
                artifacts = [str(a) for a in arts if str(a).strip()]
            ingested_at = str(entry.get("ingested_at_utc") or "").strip()

        art_display = "; ".join(artifacts) if artifacts else ""
        md_lines.append(
            f"| {i} | `{_esc_cell(vid)}` | {'yes' if ingested else 'no'} | {_esc_cell(art_display)} | {_esc_cell(title)} | {url} |"
        )

        row = {
            "video_id": vid,
            "title": title,
            "url": url,
            "upload_date": v.get("upload_date") or "",
            "duration_seconds": v.get("duration_seconds"),
            "ingested": ingested,
            "ingestion_artifacts": artifacts,
            "ingested_at_utc": ingested_at or None,
        }
        merged_rows.append(row)

    md_path = ch_dir / "CHANNEL-CATALOG.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    slug = ch_dir.name
    merged_payload = {
        "schema_version": 1,
        "channel_slug": slug,
        "channel_url": index_data.get("channel_url"),
        "source_index_generated_at_utc": index_data.get("generated_at_utc"),
        "catalog_rendered_at_utc": now,
        "video_count": len(merged_rows),
        "videos": merged_rows,
    }
    json_path = ch_dir / "episode-catalog.json"
    json_path.write_text(json.dumps(merged_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(f"Wrote {md_path.relative_to(REPO_ROOT)} and {json_path.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
