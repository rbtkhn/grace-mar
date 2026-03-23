"""Render CHAPTER-QUEUE.md from metadata/book-architecture.yaml (canonical source)."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
ARCH_PATH = WORK_DIR / "metadata" / "book-architecture.yaml"
OUT = WORK_DIR / "CHAPTER-QUEUE.md"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    arch = load(ARCH_PATH)
    chapters = (arch.get("book") or {}).get("chapters") or []
    lines = [
        "# CHAPTER QUEUE",
        "",
        "Production order and blockers for the Jiang book/site lane.",
        "",
    ]
    for ch in chapters:
        cid = ch.get("id", "")
        title = ch.get("title", cid)
        lines += [
            f"## {cid} — {title}",
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
    lines.append(
        "*Generated from `metadata/book-architecture.yaml` — run "
        "`python scripts/work_jiang/render_chapter_queue.py` after edits.*"
    )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
