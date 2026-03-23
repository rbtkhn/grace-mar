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
    lines = [
        "# BOOK ARCHITECTURE",
        "",
        f"**Project:** {project['title']}",
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
    lines += ["", "## Chapters", ""]
    for ch in chapters:
        lines += [
            f"### {ch['id']} — {ch['title']}",
            "",
            f"- **Purpose:** {ch['purpose']}",
            f"- **Kind:** {ch['kind']}",
            f"- **Priority:** {ch['priority']}",
            f"- **Target words:** {ch.get('target_words', '')}",
            f"- **Status:** {ch['status']}",
            "",
        ]
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
