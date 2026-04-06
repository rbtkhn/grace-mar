"""Read-only audit: sources vs analysis memos and front matter shape.

Exits 0 always (report-only). Run from repo root:
  python3 scripts/work_jiang/audit_predictive_history_format.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ANALYSIS_DIR = WORK_DIR / "analysis"
SOURCES_PATH = WORK_DIR / "metadata" / "sources.yaml"
SOURCE_MAP_PATH = WORK_DIR / "metadata" / "source-map.yaml"

EXPECTED_KEYS = (
    "analysis_id",
    "video_id",
    "source_id",
    "canonical_url",
    "series",
    "episode",
    "chapter_candidates",
    "status",
    "quality_level",
)


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    raw = text[4:end]
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return None


def main() -> int:
    sources = load(SOURCES_PATH).get("sources", [])
    sm = load(SOURCE_MAP_PATH).get("chapter_map") or {}

    # source_id -> list of chapters that cite it
    sid_to_chapters: dict[str, list[str]] = defaultdict(list)
    for ch, data in sm.items():
        for sid in data.get("source_ids") or []:
            sid_to_chapters[sid].append(ch)

    by_series: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "analysis_complete": 0, "analysis_missing": 0, "null_path": 0}
    )
    for s in sources:
        ser = s.get("series") or "unknown"
        st = s.get("status") or {}
        by_series[ser]["total"] += 1
        if st.get("analysis") == "complete":
            by_series[ser]["analysis_complete"] += 1
        elif st.get("analysis") == "missing":
            by_series[ser]["analysis_missing"] += 1
        if s.get("analysis_path") is None:
            by_series[ser]["null_path"] += 1

    print("# Predictive History format audit (machine scan)\n")
    print("## Per-series counts (sources.yaml)\n")
    print("| series | total | analysis complete | analysis missing | analysis_path null |")
    print("|--------|-------|-------------------|------------------|-------------------|")
    for ser in sorted(by_series.keys()):
        b = by_series[ser]
        print(
            f"| {ser} | {b['total']} | {b['analysis_complete']} | "
            f"{b['analysis_missing']} | {b['null_path']} |"
        )

    src_by_id = {s["source_id"]: s for s in sources if s.get("source_id")}

    print("\n## Analysis memo files (analysis/*.md)\n")

    missing_fm = 0
    missing_keys: list[tuple[str, str]] = []
    empty_candidates_single_map: list[str] = []
    vid_mismatch: list[str] = []

    for path in sorted(ANALYSIS_DIR.glob("*.md")):
        if path.name == ".gitkeep":
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            missing_fm += 1
            print(f"- **No YAML front matter:** `{path.name}`")
            continue
        sid = fm.get("source_id")
        for key in EXPECTED_KEYS:
            if key not in fm or fm.get(key) is None:
                missing_keys.append((path.name, key))
        if sid and len(sid_to_chapters.get(sid, [])) == 1:
            cc = fm.get("chapter_candidates")
            if cc == [] or cc is None:
                empty_candidates_single_map.append(f"{path.name} ({sid})")

        vid = fm.get("video_id") or ""
        if sid and sid in src_by_id and vid:
            reg_vid = (src_by_id[sid].get("video_id") or "").strip()
            if reg_vid and reg_vid != vid:
                vid_mismatch.append(f"{path.name}: frontmatter video_id={vid!r} registry={reg_vid!r}")

    if missing_keys:
        print("### Missing or null expected front matter keys\n")
        by_file: dict[str, list[str]] = defaultdict(list)
        for fname, key in missing_keys:
            by_file[fname].append(key)
        for fname in sorted(by_file.keys())[:40]:
            print(f"- `{fname}`: {', '.join(by_file[fname])}")
        if len(by_file) > 40:
            print(f"- … plus {len(by_file) - 40} more files")
        print()

    if empty_candidates_single_map:
        print("### Empty `chapter_candidates` but source_map has exactly one chapter\n")
        for line in empty_candidates_single_map[:50]:
            print(f"- {line}")
        if len(empty_candidates_single_map) > 50:
            print(f"- … plus {len(empty_candidates_single_map) - 50} more")
        print()

    if vid_mismatch:
        print("### video_id mismatch vs sources.yaml\n")
        for line in vid_mismatch[:30]:
            print(f"- {line}")
        if len(vid_mismatch) > 30:
            print(f"- … plus {len(vid_mismatch) - 30} more")
        print()

    if not missing_fm and not missing_keys and not empty_candidates_single_map and not vid_mismatch:
        print("_No structural issues in the checks above (or memo set empty)._")

    print(f"\n_Scanned {len(list(ANALYSIS_DIR.glob('*.md')))} files under analysis/._")
    return 0


if __name__ == "__main__":
    sys.exit(main())
