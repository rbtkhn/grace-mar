"""Render BOOK-ARCHITECTURE.md from metadata/book-architecture.yaml."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
META = WORK_DIR / "metadata" / "book-architecture.yaml"
OUT = WORK_DIR / "BOOK-ARCHITECTURE.md"
OUT_VOL2 = WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-II.md"
OUT_VOL3 = WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-III.md"
OUT_VOL4 = WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-IV.md"
OUT_VOL5 = WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-V.md"
OUT_VOL6 = WORK_DIR / "BOOK-ARCHITECTURE-VOLUME-VI.md"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    proj = data.get("project") or {}
    if not proj.get("thesis_one_sentence"):
        errors.append("project.thesis_one_sentence is required")
    chapters = (data.get("book") or {}).get("chapters")
    if not chapters:
        errors.append("book.chapters must contain at least one chapter")
    return errors


def render(data: dict) -> str:
    project = data["project"]
    chapters = data["book"]["chapters"]
    appendix = data.get("appendix") or {}
    website = data.get("website") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE",
        "",
        f"**Project:** {project['title']}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — multivolume work; **one volume per lecture series**.",
            "",
            f"{vol_line} (this book’s primary lecture corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        project["thesis_one_sentence"],
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    cep = data.get("chapter_end_predictions") or {}
    if cep:
        lines += [
            "",
            "## End-of-chapter predictions (Part I)",
            "",
            f"- **Minimum per chapter:** {cep.get('min_per_chapter', 3)}",
            f"- **Registry:** `{cep.get('registry_path', '')}`",
            "",
            str(cep.get("instruction") or "").strip(),
            "",
        ]
    part2 = data.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "ch12"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs (chapter-end box):** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    items = appendix.get("items") or []
    if items:
        lines += ["## Appendix", ""]
        for it in items:
            lines.append(f"- **{it.get('id')}** — {it.get('title')} (source: {it.get('source')})")
        lines.append("")
    wsec = website.get("sections") or []
    if wsec:
        lines += ["## Website sections", ""]
        for ws in wsec:
            lines.append(f"- **{ws.get('id')}** — {ws.get('title')}")
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` — run "
        "`python scripts/work_jiang/render_book_architecture.py` after edits.*"
    )
    lines.append("")
    return "\n".join(lines)


def render_volume_ii(data: dict) -> str | None:
    """Render BOOK-ARCHITECTURE-VOLUME-II.md from `volume_2_civilization`."""
    vol = data.get("volume_2_civilization") or {}
    chapters = (vol.get("book") or {}).get("chapters") or []
    if not chapters:
        return None
    project = vol.get("project") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE — Volume II (Civilization)",
        "",
        f"**Project:** {project.get('title', '')}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — nested block `volume_2_civilization` in `book-architecture.yaml`.",
            "",
            f"{vol_line} (this volume’s lecture corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        str(project.get("thesis_one_sentence") or "").strip(),
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    ced = vol.get("chapter_end_divergence") or {}
    if ced:
        lines += [
            "",
            "## End-of-chapter divergence (Part I)",
            "",
            f"- **Registry:** `{ced.get('registry_path', '')}`",
            "",
            str(ced.get("instruction") or "").strip(),
            "",
        ]
    part2 = vol.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "civ-ch60"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs:** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` (`volume_2_civilization`) — "
        "`python scripts/work_jiang/render_book_architecture.py`.*"
    )
    lines.append("")
    return "\n".join(lines)


def render_volume_iii(data: dict) -> str | None:
    """Render BOOK-ARCHITECTURE-VOLUME-III.md from `volume_3_secret_history`."""
    vol = data.get("volume_3_secret_history") or {}
    chapters = (vol.get("book") or {}).get("chapters") or []
    if not chapters:
        return None
    project = vol.get("project") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE — Volume III (Secret History)",
        "",
        f"**Project:** {project.get('title', '')}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — nested block `volume_3_secret_history` in `book-architecture.yaml`.",
            "",
            f"{vol_line} (this volume’s lecture corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        str(project.get("thesis_one_sentence") or "").strip(),
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    ced = vol.get("chapter_end_divergence") or {}
    if ced:
        lines += [
            "",
            "## End-of-chapter divergence (Part I)",
            "",
            f"- **Registry:** `{ced.get('registry_path', '')}`",
            "",
            str(ced.get("instruction") or "").strip(),
            "",
        ]
    part2 = vol.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "sh-ch28"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs:** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` (`volume_3_secret_history`) — "
        "`python scripts/work_jiang/render_book_architecture.py`.*"
    )
    lines.append("")
    return "\n".join(lines)


def render_volume_iv(data: dict) -> str | None:
    """Render BOOK-ARCHITECTURE-VOLUME-IV.md from `volume_4_game_theory`."""
    vol = data.get("volume_4_game_theory") or {}
    chapters = (vol.get("book") or {}).get("chapters") or []
    if not chapters:
        return None
    project = vol.get("project") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE — Volume IV (Game Theory)",
        "",
        f"**Project:** {project.get('title', '')}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — nested block `volume_4_game_theory` in `book-architecture.yaml`.",
            "",
            f"{vol_line} (this volume’s lecture corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        str(project.get("thesis_one_sentence") or "").strip(),
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    ced = vol.get("chapter_end_divergence") or {}
    if ced:
        lines += [
            "",
            "## End-of-chapter divergence (Part I)",
            "",
            f"- **Registry:** `{ced.get('registry_path', '')}`",
            "",
            str(ced.get("instruction") or "").strip(),
            "",
        ]
    part2 = vol.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "gt-ch17"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs:** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` (`volume_4_game_theory`) — "
        "`python scripts/work_jiang/render_book_architecture.py`.*"
    )
    lines.append("")
    return "\n".join(lines)


def render_volume_v(data: dict) -> str | None:
    """Render BOOK-ARCHITECTURE-VOLUME-V.md from `volume_5_great_books`."""
    vol = data.get("volume_5_great_books") or {}
    chapters = (vol.get("book") or {}).get("chapters") or []
    if not chapters:
        return None
    project = vol.get("project") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE — Volume V (Great Books)",
        "",
        f"**Project:** {project.get('title', '')}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — nested block `volume_5_great_books` in `book-architecture.yaml`.",
            "",
            f"{vol_line} (this volume’s lecture corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        str(project.get("thesis_one_sentence") or "").strip(),
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    ced = vol.get("chapter_end_divergence") or {}
    if ced:
        lines += [
            "",
            "## End-of-chapter divergence (Part I)",
            "",
            f"- **Registry:** `{ced.get('registry_path', '')}`",
            "",
            str(ced.get("instruction") or "").strip(),
            "",
        ]
    part2 = vol.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "gb-ch08"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs:** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` (`volume_5_great_books`) — "
        "`python scripts/work_jiang/render_book_architecture.py`.*"
    )
    lines.append("")
    return "\n".join(lines)


def render_volume_vi(data: dict) -> str | None:
    """Render BOOK-ARCHITECTURE-VOLUME-VI.md from `volume_6_interviews`."""
    vol = data.get("volume_6_interviews") or {}
    chapters = (vol.get("book") or {}).get("chapters") or []
    if not chapters:
        return None
    project = vol.get("project") or {}
    series_title = project.get("series_title")
    volume = project.get("volume") or {}
    lines = [
        "# BOOK ARCHITECTURE — Volume VI (Interviews)",
        "",
        f"**Project:** {project.get('title', '')}",
    ]
    if series_title and isinstance(volume, dict) and volume.get("lecture_series"):
        vol_n = volume.get("number")
        ls = volume.get("lecture_series")
        vol_line = f"**Volume {vol_n}:** {ls}" if vol_n is not None else f"**Volume:** {ls}"
        lines += [
            "",
            "## Series and volume",
            "",
            f"**Series:** {series_title} — nested block `volume_6_interviews` in `book-architecture.yaml`.",
            "",
            f"{vol_line} (this volume’s interview corpus).",
        ]
    lines += [
        "",
        "## Thesis",
        "",
        str(project.get("thesis_one_sentence") or "").strip(),
        "",
        "## Book promise",
        "",
        str(project.get("promise_paragraph") or "").strip(),
        "",
        "## Audience",
        "",
        f"- **Primary:** {project.get('audience', {}).get('primary', '')}",
    ]
    sec = project.get("audience", {}).get("secondary") or []
    for s in sec:
        lines.append(f"- **Secondary:** {s}")
    ced = vol.get("chapter_end_divergence") or {}
    if ced:
        lines += [
            "",
            "## End-of-chapter divergence (Part I)",
            "",
            f"- **Registry:** `{ced.get('registry_path', '')}`",
            "",
            str(ced.get("instruction") or "").strip(),
            "",
        ]
    part2 = vol.get("part_2") or {}
    if part2:
        after = part2.get("after_chapter") or "vi-ch11"
        lines += [
            "",
            "## Part II (after Part I)",
            "",
            f"### {part2.get('title', 'Part II')}",
            "",
            f"**Begins after:** `{after}`",
            "",
            str(part2.get("description") or "").strip(),
            "",
        ]
    lines += ["", "## Chapters (Part I)", ""]
    for ch in chapters:
        pred_ids = ch.get("prediction_ids") or []
        pred_line = ""
        if pred_ids:
            pred_line = f"- **Prediction IDs:** `{', '.join(pred_ids)}`"
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append(f"- **Blocking:** {', '.join(blocking)}")
        outline_path = ch.get("outline_path")
        draft_path = ch.get("draft_path")
        if outline_path:
            lines.append(f"- **Outline:** `{outline_path}`")
        if draft_path:
            lines.append(f"- **Draft:** `{draft_path}`")
        if pred_line:
            lines.append(pred_line)
        lines.append("")
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` (`volume_6_interviews`) — "
        "`python scripts/work_jiang/render_book_architecture.py`.*"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json-summary",
        type=Path,
        default=None,
        help="Optional path to write a small JSON summary for dashboards.",
    )
    args = parser.parse_args()

    data = load_yaml(META)
    errors = validate(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    OUT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUT}")
    vol2_md = render_volume_ii(data)
    if vol2_md:
        OUT_VOL2.write_text(vol2_md, encoding="utf-8")
        print(f"Wrote {OUT_VOL2}")
    vol3_md = render_volume_iii(data)
    if vol3_md:
        OUT_VOL3.write_text(vol3_md, encoding="utf-8")
        print(f"Wrote {OUT_VOL3}")
    vol4_md = render_volume_iv(data)
    if vol4_md:
        OUT_VOL4.write_text(vol4_md, encoding="utf-8")
        print(f"Wrote {OUT_VOL4}")
    vol5_md = render_volume_v(data)
    if vol5_md:
        OUT_VOL5.write_text(vol5_md, encoding="utf-8")
        print(f"Wrote {OUT_VOL5}")
    vol6_md = render_volume_vi(data)
    if vol6_md:
        OUT_VOL6.write_text(vol6_md, encoding="utf-8")
        print(f"Wrote {OUT_VOL6}")
    if args.json_summary:
        summary = {
            "project_id": (data.get("project") or {}).get("id"),
            "chapter_count": len((data.get("book") or {}).get("chapters") or []),
            "status": (data.get("project") or {}).get("status"),
        }
        args.json_summary.parent.mkdir(parents=True, exist_ok=True)
        args.json_summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.json_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
