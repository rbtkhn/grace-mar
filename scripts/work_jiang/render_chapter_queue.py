"""Render CHAPTER-QUEUE.md from metadata/chapter-queue.yaml + book-architecture titles."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
QUEUE_PATH = WORK_DIR / "metadata" / "chapter-queue.yaml"
ARCH_PATH = WORK_DIR / "metadata" / "book-architecture.yaml"
OUT = WORK_DIR / "CHAPTER-QUEUE.md"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    q = load(QUEUE_PATH).get("chapter_queue") or []
    arch = load(ARCH_PATH)
    titles = {
        c["id"]: c.get("title", "")
        for c in (arch.get("book") or {}).get("chapters") or []
    }
    lines = [
        "# CHAPTER QUEUE",
        "",
        "Production order and blockers for the Jiang book/site lane.",
        "",
    ]
    for item in q:
        cid = item.get("chapter_id", "")
        title = item.get("title") or titles.get(cid, cid)
        lines += [
            f"## {cid} — {title}",
            "",
            f"- **Status:** {item.get('status', '')}",
            f"- **Owner:** {item.get('owner', '')}",
            f"- **Sprint:** {item.get('sprint', '')}",
            "",
        ]
        bi = item.get("blocking_items") or []
        if bi:
            lines.append("**Blocking:**")
            for b in bi:
                lines.append(f"- {b}")
            lines.append("")
        lines.append(f"**Next action:** {item.get('next_action', '')}")
        lines.append("")
    lines.append(
        "*Generated from `metadata/chapter-queue.yaml` — run "
        "`python scripts/work_jiang/render_chapter_queue.py` after edits.*"
    )
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
