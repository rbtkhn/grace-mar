"""Create chapter and site stub files from book-architecture.yaml."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"


def slugify(text: str) -> str:
    s = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return "-".join(s.split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing stub files.",
    )
    args = parser.parse_args()

    data = yaml.safe_load(
        (WORK_DIR / "metadata" / "book-architecture.yaml").read_text(encoding="utf-8")
    )
    chapters = (data.get("book") or {}).get("chapters") or []
    website = (data.get("website") or {}).get("sections") or []

    chapters_dir = WORK_DIR / "chapters"
    site_dir = WORK_DIR / "site"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)

    for ch in chapters:
        path = chapters_dir / f"{ch['id']}-{slugify(ch['title'])}.md"
        if path.exists() and not args.force:
            print(f"SKIP (exists): {path.name}")
            continue
        title_json = json.dumps(ch["title"], ensure_ascii=False)
        body = "\n".join(
            [
                "---",
                f"chapter_id: {ch['id']}",
                f"title: {title_json}",
                f"status: {ch['status']}",
                "source_ids: []",
                "analysis_ids: []",
                "---",
                "",
                f"# {ch['title']}",
                "",
                "## Purpose",
                "",
                ch["purpose"],
                "",
                "## Argument spine",
                "",
                "## Evidence",
                "",
                "## Draft",
                "",
            ]
        )
        path.write_text(body + "\n", encoding="utf-8")
        print(f"Wrote {path.name}")

    for sec in website:
        sid = sec.get("id", "section")
        title = sec.get("title", sid)
        path = site_dir / f"{slugify(sid)}.md"
        if path.exists() and not args.force:
            print(f"SKIP (exists): {path.name}")
            continue
        body = "\n".join(
            [
                "---",
                f"section_id: {json.dumps(sid, ensure_ascii=False)}",
                f"title: {json.dumps(title, ensure_ascii=False)}",
                "chapter_id: null",
                "source_ids: []",
                "---",
                "",
                f"# {title}",
                "",
                "(Stub — expand from book architecture and site IA.)",
                "",
            ]
        )
        path.write_text(body + "\n", encoding="utf-8")
        print(f"Wrote site/{path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
