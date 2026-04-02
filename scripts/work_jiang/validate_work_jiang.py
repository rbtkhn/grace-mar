"""Validate work-jiang metadata consistency."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from arch_chapters import all_chapter_ids, all_chapters_flat, top_level_chapters  # noqa: E402
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_DIR / "lectures"
ANALYSIS = WORK_DIR / "analysis"
QUOTES = WORK_DIR / "metadata" / "quotes.yaml"

GEO_LECTURE = re.compile(r"^geo-strategy-(\d{2})-(.+)\.md$", re.I)
CIV_LECTURE = re.compile(r"^civilization-(\d{2})-(.+)\.md$", re.I)
GAME_LECTURE = re.compile(r"^game-theory-(\d{2})-(.+)\.md$", re.I)
GREAT_BOOKS_LECTURE = re.compile(r"^great-books-(\d{2})-(.+)\.md$", re.I)
INTERVIEWS_LECTURE = re.compile(r"^interviews-(\d{2})-(.+)\.md$", re.I)

VALID_STATUSES = [
    "not_started",
    "analysis_missing",
    "analysis_complete",
    "ready_for_outline",
    "outline_complete",
    "research_ready",
    "drafting",
    "draft_complete",
    "review",
    "done",
]

FORBIDDEN_EXPORT_PREFIXES = [
    "users/grace-mar/self.md",
    "users/grace-mar/self-archive.md",
    "users/grace-mar/self-evidence.md",
    "users/grace-mar/recursion-gate.md",
]


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


def chapter_evidence_pack_exists(cid: str) -> bool:
    return (WORK_DIR / "evidence-packs" / f"{cid}.md").exists()


def chapter_outline_exists(item: dict) -> bool:
    p = item.get("outline_path")
    return bool(p) and (WORK_DIR / p).exists()


def chapter_draft_exists(item: dict) -> bool:
    p = item.get("draft_path")
    return bool(p) and (WORK_DIR / p).exists()


def count_chapter_quotes_by_status(quotes: list[dict], chapter_id: str, statuses: set[str]) -> int:
    total = 0
    for q in quotes:
        if (q.get("status") or "") not in statuses:
            continue
        if chapter_id in (q.get("chapter_ids") or []):
            total += 1
    return total


def assert_safe_output_path(path: Path) -> None:
    """Raise if path would write into Record. Used by membrane validator."""
    p = path.as_posix()
    for prefix in FORBIDDEN_EXPORT_PREFIXES:
        if prefix in p:
            raise ValueError(f"Unsafe export target for work-jiang lane: {p}")


def _scan_rendered_status_drift(
    path: Path,
    path_name: str,
    header_pat: re.Pattern[str],
    expected: dict[str, str],
    status_prefix: str,
    errors: list[str],
) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    current_cid: str | None = None
    for line in lines:
        m = header_pat.match(line)
        if m:
            current_cid = m.group(1)
            continue
        if current_cid and status_prefix in line:
            val = line.split("**Status:**", 1)[-1].strip()
            exp = expected.get(current_cid)
            if exp is not None and val != exp:
                errors.append(
                    f"{path_name} status for {current_cid} is {val!r}, "
                    f"book-architecture.yaml has {exp!r} — re-run renderers"
                )
            current_cid = None


def check_rendered_status_drift(architecture: dict, errors: list[str]) -> None:
    """Verify rendered queue/architecture markdown status matches book-architecture.yaml."""
    expected_v1 = {
        c["id"]: c.get("status", "")
        for c in top_level_chapters(architecture)
    }
    status_line = "- **Status:**"
    _scan_rendered_status_drift(
        WORK_DIR / "CHAPTER-QUEUE.md",
        "CHAPTER-QUEUE.md",
        re.compile(r"^## (ch\d+)"),
        expected_v1,
        status_line,
        errors,
    )
    _scan_rendered_status_drift(
        WORK_DIR / "BOOK-ARCHITECTURE.md",
        "BOOK-ARCHITECTURE.md",
        re.compile(r"^### (ch\d+)"),
        expected_v1,
        status_line,
        errors,
    )

    vol2 = architecture.get("volume_2_civilization") or {}
    ch2 = (vol2.get("book") or {}).get("chapters") or []
    if ch2:
        expected_v2 = {c["id"]: c.get("status", "") for c in ch2}
        _scan_rendered_status_drift(
            WORK_DIR / "CHAPTER-QUEUE-VOLUME-II.md",
            "CHAPTER-QUEUE-VOLUME-II.md",
            re.compile(r"^## (civ-ch\d+)"),
            expected_v2,
            status_line,
            errors,
        )
        _scan_rendered_status_drift(
            WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-II.md",
            "BOOK-ARCHITECTURE-VOLUME-II.md",
            re.compile(r"^### (civ-ch\d+)"),
            expected_v2,
            status_line,
            errors,
        )

    vol3 = architecture.get("volume_3_secret_history") or {}
    ch3 = (vol3.get("book") or {}).get("chapters") or []
    if ch3:
        expected_v3 = {c["id"]: c.get("status", "") for c in ch3}
        _scan_rendered_status_drift(
            WORK_DIR / "CHAPTER-QUEUE-VOLUME-III.md",
            "CHAPTER-QUEUE-VOLUME-III.md",
            re.compile(r"^## (sh-ch\d+)"),
            expected_v3,
            status_line,
            errors,
        )
        _scan_rendered_status_drift(
            WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-III.md",
            "BOOK-ARCHITECTURE-VOLUME-III.md",
            re.compile(r"^### (sh-ch\d+)"),
            expected_v3,
            status_line,
            errors,
        )

    vol4 = architecture.get("volume_4_game_theory") or {}
    ch4 = (vol4.get("book") or {}).get("chapters") or []
    if ch4:
        expected_v4 = {c["id"]: c.get("status", "") for c in ch4}
        _scan_rendered_status_drift(
            WORK_DIR / "CHAPTER-QUEUE-VOLUME-IV.md",
            "CHAPTER-QUEUE-VOLUME-IV.md",
            re.compile(r"^## (gt-ch\d+)"),
            expected_v4,
            status_line,
            errors,
        )
        _scan_rendered_status_drift(
            WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-IV.md",
            "BOOK-ARCHITECTURE-VOLUME-IV.md",
            re.compile(r"^### (gt-ch\d+)"),
            expected_v4,
            status_line,
            errors,
        )


def check_membrane(errors: list[str]) -> None:
    """Scan work_jiang scripts for forbidden Record path writes."""
    scripts_dir = ROOT / "scripts" / "work_jiang"
    if not scripts_dir.exists():
        return
    skip = {"validate_work_jiang.py"}  # defines FORBIDDEN_EXPORT_PREFIXES
    for py_path in scripts_dir.glob("*.py"):
        if py_path.name in skip:
            continue
        try:
            text = py_path.read_text(encoding="utf-8")
        except OSError:
            continue
        for prefix in FORBIDDEN_EXPORT_PREFIXES:
            if prefix in text:
                errors.append(
                    f"scripts/work_jiang/{py_path.name} contains forbidden path "
                    f"prefix {prefix!r} — work-jiang must not write to Record"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-analysis-frontmatter",
        action="store_true",
        help="Fail if any analysis memo lacks parseable YAML front matter.",
    )
    parser.add_argument(
        "--check-drift",
        action="store_true",
        default=True,
        help="Verify rendered markdown status matches book-architecture.yaml (default: True).",
    )
    parser.add_argument(
        "--no-check-drift",
        action="store_false",
        dest="check_drift",
        help="Skip rendered status drift check.",
    )
    args = parser.parse_args()

    errors: list[str] = []

    arch_path = WORK_DIR / "metadata" / "book-architecture.yaml"
    if not arch_path.exists():
        errors.append("Missing metadata/book-architecture.yaml")
    architecture = load(arch_path) if arch_path.exists() else {}
    chapter_ids = all_chapter_ids(architecture)

    if not (architecture.get("project") or {}).get("thesis_one_sentence"):
        errors.append("Missing project.thesis_one_sentence")

    sm = load(WORK_DIR / "metadata" / "source-map.yaml")
    chapter_map = sm.get("chapter_map") or {}
    for ch in chapter_map:
        if ch not in chapter_ids:
            errors.append(f"source-map chapter_map references unknown chapter: {ch}")

    sources = load(WORK_DIR / "metadata" / "sources.yaml").get("sources", [])
    source_ids = {s["source_id"] for s in sources}

    lecture_paths_seen: list[str] = []
    for s in sources:
        lp = s.get("lecture_path")
        if not lp:
            continue
        lecture_paths_seen.append(lp)
        abs_lecture = WORK_DIR / lp
        if not abs_lecture.is_file():
            errors.append(f"Missing lecture file for {s.get('source_id')}: {lp}")
            continue
        name = Path(lp).name
        series = s.get("series")
        ep = s.get("episode")
        if ep is None:
            errors.append(f"{s.get('source_id')}: missing episode for lecture_path")
            continue
        if series == "geo-strategy":
            m = GEO_LECTURE.match(name)
            if not m:
                errors.append(
                    f"{s['source_id']}: lecture filename must match "
                    f"geo-strategy-NN-<slug>.md (NN two digits), got {name!r}"
                )
            elif int(m.group(1)) != int(ep):
                errors.append(
                    f"{s['source_id']}: filename episode {m.group(1)} != episode {ep}"
                )
        elif series == "civilization":
            m = CIV_LECTURE.match(name)
            if not m:
                errors.append(
                    f"{s['source_id']}: lecture filename must match "
                    f"civilization-NN-<slug>.md (NN two digits), got {name!r}"
                )
            elif int(m.group(1)) != int(ep):
                errors.append(
                    f"{s['source_id']}: filename episode {m.group(1)} != episode {ep}"
                )
        elif series == "game-theory":
            m = GAME_LECTURE.match(name)
            if not m:
                errors.append(
                    f"{s['source_id']}: lecture filename must match "
                    f"game-theory-NN-<slug>.md (NN two digits), got {name!r}"
                )
            elif int(m.group(1)) != int(ep):
                errors.append(
                    f"{s['source_id']}: filename episode {m.group(1)} != episode {ep}"
                )
        elif series == "great-books":
            m = GREAT_BOOKS_LECTURE.match(name)
            if not m:
                errors.append(
                    f"{s['source_id']}: lecture filename must match "
                    f"great-books-NN-<slug>.md (NN two digits), got {name!r}"
                )
            elif int(m.group(1)) != int(ep):
                errors.append(
                    f"{s['source_id']}: filename episode {m.group(1)} != episode {ep}"
                )
        elif series == "interviews":
            m = INTERVIEWS_LECTURE.match(name)
            if not m:
                errors.append(
                    f"{s['source_id']}: lecture filename must match "
                    f"interviews-NN-<slug>.md (NN two digits), got {name!r}"
                )
            elif int(m.group(1)) != int(ep):
                errors.append(
                    f"{s['source_id']}: filename episode {m.group(1)} != episode {ep}"
                )
    dup_lp = [p for p in set(lecture_paths_seen) if lecture_paths_seen.count(p) > 1]
    for p in sorted(dup_lp):
        errors.append(f"Duplicate lecture_path in sources: {p}")

    registered_lectures = {s["lecture_path"] for s in sources if s.get("lecture_path")}
    for pattern, label in (
        ("geo-strategy-*.md", "geo-strategy"),
        ("civilization-*.md", "civilization"),
        ("game-theory-*.md", "game-theory"),
        ("great-books-*.md", "great-books"),
        ("interviews-*.md", "interviews"),
    ):
        for path in sorted(LECTURES.glob(pattern)):
            rel = path.relative_to(WORK_DIR).as_posix()
            if rel not in registered_lectures:
                errors.append(
                    f"Lecture on disk not listed in metadata/sources.yaml: {rel} ({label})"
                )

    for ch, data in chapter_map.items():
        for sid in data.get("source_ids") or []:
            if sid not in source_ids:
                errors.append(f"Unknown source_id {sid} in chapter_map.{ch}")

    valid_ch = chapter_ids | set(chapter_map.keys())
    if args.require_analysis_frontmatter:
        for path in ANALYSIS.glob("*.md"):
            if path.name == ".gitkeep":
                continue
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if not fm:
                errors.append(f"Missing or invalid front matter: {path.name}")
                continue
            for cand in fm.get("chapter_candidates") or []:
                if cand not in valid_ch:
                    errors.append(f"{path.name}: invalid chapter_candidates entry {cand}")

    # Chapter validation from book-architecture.yaml (canonical source)
    qdoc = load(QUOTES) if QUOTES.exists() else {}
    quotes = qdoc.get("quotes") or []
    src_by = {s["source_id"]: s for s in sources}
    chapters = all_chapters_flat(architecture)
    for item in chapters:
        cid = item.get("id", "")
        status = (item.get("status") or "").strip()
        sids = item.get("source_ids") or chapter_map.get(cid, {}).get("source_ids") or []

        if status == "research_ready":
            with_analysis = sum(
                1 for s in sources if s["source_id"] in sids and s["status"].get("analysis") == "complete"
            )
            if sids and with_analysis == 0:
                errors.append(
                    f"Chapter {cid} marked research_ready but no mapped source has complete analysis"
                )
            if not chapter_evidence_pack_exists(cid):
                errors.append(f"Chapter {cid} marked research_ready but evidence pack is missing")
            draft_safe_count = count_chapter_quotes_by_status(quotes, cid, {"draft_safe"})
            if draft_safe_count < 3:
                errors.append(
                    f"Chapter {cid} marked research_ready but has fewer than 3 draft_safe quotes"
                )

        if status in {"ready_for_outline", "outline_complete", "research_ready", "drafting", "draft_complete", "review", "done"}:
            trusted_quote_count = count_chapter_quotes_by_status(quotes, cid, {"verified", "draft_safe"})
            if trusted_quote_count == 0:
                errors.append(f"Chapter {cid} status={status} but has no verified/draft_safe quotes")
            if not chapter_outline_exists(item):
                errors.append(
                    f"Chapter {cid} status={status} but outline_path is missing or file does not exist"
                )
        if status in {"drafting", "draft_complete", "review", "done"}:
            if not chapter_draft_exists(item):
                errors.append(
                    f"Chapter {cid} status={status} but draft_path is missing or file does not exist"
                )

    if args.check_drift:
        check_rendered_status_drift(architecture, errors)

    check_membrane(errors)

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
