"""Render CHAPTER-QUEUE.md from metadata/book-architecture.yaml (canonical source)."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ARCH_PATH = WORK_DIR / "metadata" / "book-architecture.yaml"
OUT = WORK_DIR / "CHAPTER-QUEUE.md"
OUT_VOL2 = WORK_DIR / "CHAPTER-QUEUE-VOLUME-II.md"
OUT_VOL3 = WORK_DIR / "CHAPTER-QUEUE-VOLUME-III.md"
OUT_VOL4 = WORK_DIR / "CHAPTER-QUEUE-VOLUME-IV.md"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _render_queue_lines(title: str, blurb: str, chapters: list) -> list[str]:
    lines = [f"# {title}", "", blurb, ""]
    for ch in chapters:
        cid = ch.get("id", "")
        title_ch = ch.get("title", cid)
        lines += [
            f"## {cid} — {title_ch}",
            "",
            f"- **Status:** {ch.get('status', '')}",
            f"- **Owner:** {ch.get('owner', '')}",
            f"- **Sprint:** {ch.get('sprint', '')}",
            "",
        ]
        blocking = ch.get("blocking") or []
        if blocking:
            lines.append("**Blocking:**")
            for b in blocking:
                lines.append(f"- {b}")
            lines.append("")
        lines.append(f"**Next action:** {ch.get('next_action', '')}")
        lines.append("")
    return lines


def main() -> int:
    arch = load(ARCH_PATH)
    chapters = (arch.get("book") or {}).get("chapters") or []
    lines = _render_queue_lines(
        "CHAPTER QUEUE",
        "Production order and blockers for the Jiang book/site lane (Volume I — Geo-Strategy, top-level `book`).",
        chapters,
    )
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` — run "
        "`python scripts/work_jiang/render_chapter_queue.py` after edits.*"
    )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")

    vol2 = arch.get("volume_2_civilization") or {}
    ch2 = (vol2.get("book") or {}).get("chapters") or []
    if ch2:
        lines2 = _render_queue_lines(
            "CHAPTER QUEUE — Volume II (Civilization)",
            "Nested `volume_2_civilization.book.chapters` — see "
            "`docs/skill-work/work-jiang/volume-ii-book-track-conventions.md`.",
            ch2,
        )
        lines2.append(
            "*Generated from `metadata/book-architecture.yaml` (`volume_2_civilization`) — "
            "same command as Volume I queue.*"
        )
        lines2.append("")
        OUT_VOL2.write_text("\n".join(lines2), encoding="utf-8")
        print(f"Wrote {OUT_VOL2}")

    vol3 = arch.get("volume_3_secret_history") or {}
    ch3 = (vol3.get("book") or {}).get("chapters") or []
    if ch3:
        lines3 = _render_queue_lines(
            "CHAPTER QUEUE — Volume III (Secret History)",
            "Nested `volume_3_secret_history.book.chapters` — see "
            "`docs/skill-work/work-jiang/volume-iii-book-track-conventions.md`.",
            ch3,
        )
        lines3.append(
            "*Generated from `metadata/book-architecture.yaml` (`volume_3_secret_history`) — "
            "same command as Volume I queue.*"
        )
        lines3.append("")
        OUT_VOL3.write_text("\n".join(lines3), encoding="utf-8")
        print(f"Wrote {OUT_VOL3}")

    vol4 = arch.get("volume_4_game_theory") or {}
    ch4 = (vol4.get("book") or {}).get("chapters") or []
    if ch4:
        lines4 = _render_queue_lines(
            "CHAPTER QUEUE — Volume IV (Game Theory)",
            "Nested `volume_4_game_theory.book.chapters` — see "
            "`docs/skill-work/work-jiang/volume-iv-book-track-conventions.md`.",
            ch4,
        )
        lines4.append(
            "*Generated from `metadata/book-architecture.yaml` (`volume_4_game_theory`) — "
            "same command as Volume I queue.*"
        )
        lines4.append("")
        OUT_VOL4.write_text("\n".join(lines4), encoding="utf-8")
        print(f"Wrote {OUT_VOL4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
