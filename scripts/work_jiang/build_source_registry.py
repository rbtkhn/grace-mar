"""Scan geo-strategy lectures + analysis; write metadata/sources.yaml."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_DIR / "lectures"
ANALYSIS = WORK_DIR / "analysis"
OUT = WORK_DIR / "metadata" / "sources.yaml"
SOURCE_MAP = WORK_DIR / "metadata" / "source-map.yaml"

GEO_NAME = re.compile(r"^geo-strategy-(\d+)-", re.I)
WATCH_RE = re.compile(r"watch\?v=([A-Za-z0-9_-]{11})")
VIDEO_IN_NAME = re.compile(r"^([A-Za-z0-9_-]{11})-")


def extract_video_id_from_lecture(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = WATCH_RE.search(text)
    return m.group(1) if m else None


def title_from_lecture(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def analysis_for_video(analysis_by_vid: dict[str, Path], video_id: str | None) -> Path | None:
    if not video_id:
        return None
    return analysis_by_vid.get(video_id)


def main() -> int:
    analysis_by_vid: dict[str, Path] = {}
    for p in ANALYSIS.glob("*.md"):
        if p.name == ".gitkeep":
            continue
        m = VIDEO_IN_NAME.match(p.name)
        if m:
            analysis_by_vid[m.group(1)] = p

    lecture_paths = sorted(
        LECTURES.glob("geo-strategy-*.md"),
        key=lambda p: int(GEO_NAME.match(p.name).group(1)) if GEO_NAME.match(p.name) else 0,
    )
    sources: list[dict] = []
    for lecture in lecture_paths:
        m = GEO_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"geo-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched = analysis_for_video(analysis_by_vid, vid)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        analysis_status = "complete" if matched else "missing"
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid,
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "geo-strategy",
                "episode": ep,
                "themes": [],
                "status": {
                    "transcript": "complete",
                    "curated_lecture": "complete",
                    "analysis": analysis_status,
                    "chapter_mapping": "missing",
                },
            }
        )

    mapped_ids: set[str] = set()
    sm = {}
    if SOURCE_MAP.exists():
        sm = yaml.safe_load(SOURCE_MAP.read_text(encoding="utf-8")) or {}
    for _ch, data in (sm.get("chapter_map") or {}).items():
        mapped_ids.update(data.get("source_ids") or [])
    for _k, data in (sm.get("appendix_map") or {}).items():
        mapped_ids.update(data.get("source_ids") or [])

    for s in sources:
        s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "missing"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        yaml.safe_dump({"sources": sources}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(sources)} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
