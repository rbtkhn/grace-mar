"""Ensure YAML front matter on analysis memos; optional --write.

Skips (never overwrites):
  - ``essay-*-analysis.md`` (Volume VII Substack schema: ``source_kind``, ``es-NN``, etc.)
  - ``interviews-NN-analysis.md`` when the filename has no leading YouTube id (registry uses
    ``{video_id}-interviews-NN-analysis.md`` for wired interviews)
  - ``*-civmem-analysis.md``, ``*-psy-hist-analysis.md`` (lane-specific front matter)
  - Existing front matter with ``source_kind: substack`` or ``series: substack``

Use ``--only-glob '*.md'`` to limit which files are considered (fnmatch on basename).

Examples::

  python3 scripts/work_jiang/normalize_analysis_frontmatter.py
  python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write --only-glob '*-game-theory-*-analysis.md'
"""
from __future__ import annotations

import argparse
import fnmatch
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ANALYSIS = WORK_DIR / "analysis"
SOURCES_PATH = WORK_DIR / "metadata" / "sources.yaml"

VIDEO_PREFIX = re.compile(r"^([A-Za-z0-9_-]{11})-")
CANONICAL_RE = re.compile(r"\*\*canonical_url:\*\*\s*<?(https?://[^\s>]+)>?", re.I)
ESSAY_ANALYSIS = re.compile(r"^essay-.+-analysis\.md$", re.I)
INTERVIEWS_NO_VIDEO_PREFIX = re.compile(r"^interviews-\d+-analysis\.md$", re.I)
CIVMEM_ANALYSIS = re.compile(r".+-civmem-analysis\.md$", re.I)
PSYHIST_ANALYSIS = re.compile(r".+-psy-hist-analysis\.md$", re.I)


def load_sources() -> dict[str, dict]:
    if not SOURCES_PATH.exists():
        return {}
    with SOURCES_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    by_vid = {}
    for s in data.get("sources") or []:
        if s.get("video_id"):
            by_vid[s["video_id"]] = s
    return by_vid


def extract_video_id(path: Path) -> str | None:
    m = VIDEO_PREFIX.match(path.name)
    return m.group(1) if m else None


def extract_canonical_url(body: str) -> str:
    m = CANONICAL_RE.search(body)
    return m.group(1).strip() if m else ""


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def memo_kind_skip_filename(name: str) -> bool:
    """True when this basename uses a non-video analysis schema we must not clobber."""
    if ESSAY_ANALYSIS.match(name):
        return True
    if INTERVIEWS_NO_VIDEO_PREFIX.match(name):
        return True
    if CIVMEM_ANALYSIS.match(name):
        return True
    if PSYHIST_ANALYSIS.match(name):
        return True
    return False


def is_substack_front_matter(fm: dict | None) -> bool:
    if not fm or not isinstance(fm, dict):
        return False
    if str(fm.get("source_kind") or "").strip().lower() == "substack":
        return True
    if str(fm.get("series") or "").strip().lower() == "substack":
        return True
    return False


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        return None, text
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        return yaml.safe_load(raw) or {}, body
    except yaml.YAMLError:
        return None, text


def build_frontmatter(path: Path, by_vid: dict[str, dict], body: str) -> dict:
    vid = extract_video_id(path)
    src = by_vid.get(vid) if vid else None
    source_id = src["source_id"] if src else None
    canon = (src or {}).get("canonical_url") or extract_canonical_url(body)
    episode = (src or {}).get("episode")
    sidecar_json = path.with_suffix(".json")
    rel_json = None
    if sidecar_json.exists():
        try:
            rel_json = str(sidecar_json.relative_to(WORK_DIR))
        except ValueError:
            rel_json = str(sidecar_json)

    return {
        "analysis_id": source_id or path.stem,
        "video_id": vid or "",
        "source_id": source_id,
        "canonical_url": canon,
        "series": "geo-strategy",
        "episode": episode,
        "memo_format_version": 1,
        "analysis_json_path": rel_json,
        "chapter_candidates": [],
        "appendix_candidates": [],
        "themes": [],
        "status": "complete",
        "quality_level": "draft",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--write", action="store_true", help="Write patched files.")
    parser.add_argument(
        "--only-glob",
        default="*.md",
        metavar="PATTERN",
        help="fnmatch pattern against analysis basename (default: *.md)",
    )
    args = parser.parse_args()

    by_vid = load_sources()
    changed = 0
    for path in sorted(ANALYSIS.glob("*.md")):
        if path.name == ".gitkeep":
            continue
        if not fnmatch.fnmatch(path.name, args.only_glob):
            continue
        if memo_kind_skip_filename(path.name):
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if is_substack_front_matter(fm):
            continue
        if fm is not None and isinstance(fm, dict) and fm.get("video_id"):
            continue
        if fm is None and has_frontmatter(text):
            # malformed — skip
            print(f"SKIP (ambiguous front matter): {path.name}")
            continue
        merged = build_frontmatter(path, by_vid, text if fm is None else body)
        block = yaml.safe_dump(merged, sort_keys=False, allow_unicode=True).strip()
        new_text = f"---\n{block}\n---\n\n{(body if fm is not None else text)}"
        if args.write:
            path.write_text(new_text, encoding="utf-8")
            print(f"Patched {path.name}")
            changed += 1
        else:
            print(f"Would patch {path.name} (use --write)")
            changed += 1
    if not args.write and changed:
        print(f"\n{changed} file(s) need --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
