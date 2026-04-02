"""Scan work-jiang lectures + analysis; write metadata/sources.yaml."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_DIR / "lectures"
ESSAYS_DIR = WORK_DIR / "substack" / "essays"
ANALYSIS = WORK_DIR / "analysis"
OUT = WORK_DIR / "metadata" / "sources.yaml"
SOURCE_MAP = WORK_DIR / "metadata" / "source-map.yaml"

GEO_NAME = re.compile(r"^geo-strategy-(\d+)-", re.I)
CIV_NAME = re.compile(r"^civilization-(\d+)-", re.I)
SH_NAME = re.compile(r"^secret-history-(\d+)-", re.I)
GT_NAME = re.compile(r"^game-theory-(\d+)-", re.I)
GB_NAME = re.compile(r"^great-books-(\d+)-", re.I)
INTERVIEWS_NAME = re.compile(r"^interviews-(\d+)-", re.I)
# Analysis memo without leading YouTube id (operator transcript only)
INTERVIEWS_ANALYSIS_NOVID = re.compile(r"^interviews-(\d+)-analysis\.md$", re.I)
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


def essay_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---\n", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def analysis_for_video(analysis_by_vid: dict[str, Path], video_id: str | None) -> Path | None:
    if not video_id:
        return None
    return analysis_by_vid.get(video_id)


_SOURCE_KEY_ORDER = (
    "source_id",
    "video_id",
    "title",
    "canonical_url",
    "publication_date",
    "lecture_path",
    "analysis_path",
    "series",
    "episode",
    "themes",
    "status",
)


def reorder_source_dict(s: dict) -> None:
    """Stable YAML key order for sources.yaml (human-friendly diffs)."""
    rest = {k: v for k, v in s.items() if k not in _SOURCE_KEY_ORDER}
    new = {k: s[k] for k in _SOURCE_KEY_ORDER if k in s}
    new.update(rest)
    s.clear()
    s.update(new)


def merge_preserved_fields_from_previous_yaml(sources: list[dict], previous_path: Path) -> None:
    """Keep hand-maintained fields (e.g. publication_date, themes) across registry rebuilds."""
    if not previous_path.is_file():
        return
    try:
        prev_doc = yaml.safe_load(previous_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return
    by_id = {
        s["source_id"]: s
        for s in (prev_doc.get("sources") or [])
        if isinstance(s, dict) and s.get("source_id")
    }
    for s in sources:
        p = by_id.get(s["source_id"])
        if not p:
            continue
        pd = p.get("publication_date")
        if pd is not None:
            s["publication_date"] = pd
        th = p.get("themes")
        if th:
            s["themes"] = list(th)
    for s in sources:
        reorder_source_dict(s)


def main() -> int:
    analysis_by_vid: dict[str, Path] = {}
    civmem_by_source: dict[str, Path] = {}
    psyhist_by_source: dict[str, Path] = {}
    interviews_analysis_by_ep: dict[int, Path] = {}
    for p in ANALYSIS.glob("*.md"):
        if p.name == ".gitkeep":
            continue
        m = VIDEO_IN_NAME.match(p.name)
        if m:
            analysis_by_vid[m.group(1)] = p
            continue
        if p.name.endswith("-civmem-analysis.md"):
            sid = p.stem.removesuffix("-civmem-analysis")
            civmem_by_source[sid] = p
            continue
        if p.name.endswith("-psy-hist-analysis.md"):
            sid = p.stem.removesuffix("-psy-hist-analysis")
            psyhist_by_source[sid] = p
            continue
        m_iv = INTERVIEWS_ANALYSIS_NOVID.match(p.name)
        if m_iv:
            interviews_analysis_by_ep[int(m_iv.group(1))] = p

    def analysis_for_source(
        vid: str | None,
        sid: str,
    ) -> tuple[Path | None, str]:
        """Return (path, analysis_status). Prefer video_id match, then civmem, then psy-hist."""
        matched = analysis_for_video(analysis_by_vid, vid)
        if matched:
            return matched, "complete"
        if sid.startswith("vi-"):
            ep = int(sid.split("-", 1)[1])
            p_iv = interviews_analysis_by_ep.get(ep)
            if p_iv:
                return p_iv, "complete"
        if sid in civmem_by_source:
            return civmem_by_source[sid], "complete"
        if sid in psyhist_by_source:
            return psyhist_by_source[sid], "complete"
        return None, "missing"

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
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
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

    civ_paths = sorted(
        LECTURES.glob("civilization-*.md"),
        key=lambda p: int(CIV_NAME.match(p.name).group(1)) if CIV_NAME.match(p.name) else 0,
    )
    for lecture in civ_paths:
        m = CIV_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"civ-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid,
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "civilization",
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

    sh_paths = sorted(
        LECTURES.glob("secret-history-*.md"),
        key=lambda p: int(SH_NAME.match(p.name).group(1)) if SH_NAME.match(p.name) else 0,
    )
    for lecture in sh_paths:
        m = SH_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"sh-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid,
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "secret-history",
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

    gt_paths = sorted(
        LECTURES.glob("game-theory-*.md"),
        key=lambda p: int(GT_NAME.match(p.name).group(1)) if GT_NAME.match(p.name) else 0,
    )
    for lecture in gt_paths:
        m = GT_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"gt-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid,
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "game-theory",
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

    gb_paths = sorted(
        LECTURES.glob("great-books-*.md"),
        key=lambda p: int(GB_NAME.match(p.name).group(1)) if GB_NAME.match(p.name) else 0,
    )
    for lecture in gb_paths:
        m = GB_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"gb-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid,
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "great-books",
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

    interview_paths = sorted(
        LECTURES.glob("interviews-*.md"),
        key=lambda p: int(INTERVIEWS_NAME.match(p.name).group(1)) if INTERVIEWS_NAME.match(p.name) else 0,
    )
    for lecture in interview_paths:
        m = INTERVIEWS_NAME.match(lecture.name)
        if not m:
            continue
        ep = int(m.group(1))
        source_id = f"vi-{ep:02d}"
        vid = extract_video_id_from_lecture(lecture)
        matched, analysis_status = analysis_for_source(vid, source_id)
        analysis_path = str(matched.relative_to(WORK_DIR)) if matched else None
        sources.append(
            {
                "source_id": source_id,
                "video_id": vid or "",
                "title": title_from_lecture(lecture),
                "canonical_url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
                "lecture_path": str(lecture.relative_to(WORK_DIR)),
                "analysis_path": analysis_path,
                "series": "interviews",
                "episode": ep,
                "themes": [],
                "status": {
                    "transcript": "complete" if vid else "pending",
                    "curated_lecture": "complete" if vid else "stub",
                    "analysis": analysis_status,
                    "chapter_mapping": "missing",
                },
            }
        )

    essay_analysis_by_slug: dict[str, Path] = {}
    for p in ANALYSIS.glob("essay-*-analysis.md"):
        if p.name == ".gitkeep":
            continue
        stem = p.stem
        if not stem.startswith("essay-") or not stem.endswith("-analysis"):
            continue
        slug = stem[len("essay-") : -len("-analysis")]
        essay_analysis_by_slug[slug] = p

    essay_rows: list[dict] = []
    if ESSAYS_DIR.is_dir():
        for essay_path in ESSAYS_DIR.glob("*.md"):
            if essay_path.name == "README.md":
                continue
            fm = essay_frontmatter(essay_path)
            slug = str(fm.get("substack_slug") or essay_path.stem).strip()
            title = str(fm.get("title") or essay_path.stem).strip()
            canonical_url = str(fm.get("canonical_url") or "").strip()
            publication_date = fm.get("publication_date")
            essay_rows.append(
                {
                    "path": essay_path,
                    "slug": slug,
                    "title": title,
                    "canonical_url": canonical_url,
                    "publication_date": publication_date,
                }
            )
    essay_rows.sort(key=lambda r: (str(r.get("publication_date") or ""), r["slug"]))
    for ep, row in enumerate(essay_rows, start=1):
        source_id = f"es-{ep:02d}"
        slug = row["slug"]
        apath = essay_analysis_by_slug.get(slug)
        analysis_status = "complete" if apath else "missing"
        analysis_path = str(apath.relative_to(WORK_DIR)) if apath else None
        lecture_path = str(row["path"].relative_to(WORK_DIR))
        sources.append(
            {
                "source_id": source_id,
                "video_id": "",
                "title": row["title"],
                "canonical_url": row["canonical_url"],
                "publication_date": row.get("publication_date"),
                "lecture_path": lecture_path,
                "analysis_path": analysis_path,
                "series": "essays",
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

    for s in sources:
        if s["source_id"].startswith("civ-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"
        if s["source_id"].startswith("sh-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"
        if s["source_id"].startswith("gt-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"
        if s["source_id"].startswith("gb-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"
        if s["source_id"].startswith("vi-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"
        if s["source_id"].startswith("es-"):
            s["status"]["chapter_mapping"] = "complete" if s["source_id"] in mapped_ids else "not_started"

    merge_preserved_fields_from_previous_yaml(sources, OUT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        yaml.safe_dump({"sources": sources}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(sources)} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
