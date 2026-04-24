#!/usr/bin/env python3
"""Generate Chicago-style (author–date, simplified) bibliography Markdown from bookshelf-catalog.yaml.

Source of truth: docs/skill-work/work-strategy/history-notebook/research/bookshelf-catalog.yaml
Outputs: research/bibliography/REFERENCES-shelf-by-era.md, REFERENCES-shelf-by-hnsrc-id.md

Author strings are emitted as stored in the catalog (usually First Last). For formal publication,
invert names manually or enrich `cite_as` / optional `editor` / `translator` / imprint fields in YAML.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
CATALOG = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
BIB_DIR = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bibliography"
)

ERA_ORDER = ["ancient", "medieval", "colonial", "industrial", "modern"]
ERA_LABELS = {
    "ancient": "Ancient",
    "medieval": "Medieval",
    "colonial": "Colonial (Vol III–style bucket)",
    "industrial": "Industrial (Vol IV–style bucket)",
    "modern": "Modern (Vol V–style bucket)",
}

GENERATED_HEADER = """# Working shelf bibliography (generated)

**Do not edit by hand.** Source: [../bookshelf-catalog.yaml](../bookshelf-catalog.yaml).

**Style:** Chicago *author–date* (simplified, machine-generated). The catalog `author` field is printed
as given (not inverted to *Last, First*). For publication-grade lines, set optional YAML fields
(`cite_as`, `place`, `publisher`, `edition`, `series`, `editor`, `translator`) or fix rows by hand
in a **cited-ids** export.

Regenerate: `python3 scripts/build_hn_bookshelf_bibliography.py`

---
"""


def _one_line(s: str) -> str:
    return " ".join((s or "").split())


def year_str(item: dict) -> str:
    """Publication year (no trailing period; sentence punctuation adds the dot)."""
    y = item.get("year")
    if y is None or y == "":
        return "n.d"
    return str(y).strip()


def format_entry(item: dict, *, include_id: bool = True) -> str:
    author = _one_line(str(item.get("cite_as") or item.get("author") or "Unknown author"))
    ys = year_str(item)
    title = _one_line(str(item.get("title") or "Untitled"))
    sid = (item.get("id") or "").strip()

    title_md = f"*{title}*"
    if item.get("series"):
        title_md = f"{title_md} ({_one_line(str(item['series']))})"

    parts: list[str] = [f"{author}. {ys}. {title_md}."]

    if item.get("editor"):
        parts.append(f"Edited by {_one_line(str(item['editor']))}.")
    if item.get("translator"):
        parts.append(f"Trans. {_one_line(str(item['translator']))}.")

    imprint: list[str] = []
    if item.get("edition"):
        imprint.append(_one_line(str(item["edition"])))
    if item.get("place") and item.get("publisher"):
        imprint.append(f"{_one_line(str(item['place']))}: {_one_line(str(item['publisher']))}")
    elif item.get("publisher"):
        imprint.append(_one_line(str(item["publisher"])))
    if imprint:
        parts.append(" ".join(imprint) + ".")

    if item.get("isbn"):
        parts.append(f"ISBN {_one_line(str(item['isbn']))}.")

    line = " ".join(p for p in parts if p)
    if include_id and sid:
        line = f"{line} `{sid}`"
    return line


def load_items(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get("items")
    if not isinstance(items, list):
        return []
    return [x for x in items if isinstance(x, dict) and x.get("id")]


def build_by_era(items: list[dict]) -> str:
    lines: list[str] = [GENERATED_HEADER, "## By era (Bookshelf `era`)", ""]
    by_era: dict[str, list[dict]] = {}
    for it in items:
        e = str(it.get("era") or "unknown")
        by_era.setdefault(e, []).append(it)

    order = [e for e in ERA_ORDER if e in by_era] + sorted(
        e for e in by_era if e not in ERA_ORDER
    )

    for era in order:
        bucket = by_era[era]
        if not bucket:
            continue
        label = ERA_LABELS.get(era, era.replace("_", " ").title())
        lines.append(f"### {label} (`{era}`)")
        lines.append("")
        bucket.sort(
            key=lambda x: (
                (x.get("author") or "").lower(),
                (x.get("title") or "").lower(),
                x.get("id") or "",
            )
        )
        for it in bucket:
            lines.append(f"- {format_entry(it)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_by_id(items: list[dict]) -> str:
    lines: list[str] = [GENERATED_HEADER, "## By HNSRC id (stable order)", ""]
    sorted_items = sorted(items, key=lambda x: x.get("id") or "")
    for it in sorted_items:
        lines.append(f"- {format_entry(it)}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        type=Path,
        default=CATALOG,
        help="Path to bookshelf-catalog.yaml",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=BIB_DIR,
        help="Output directory (default: history-notebook/research/bibliography)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if on-disk files differ from generated content (CI freshness)",
    )
    args = ap.parse_args()

    if not args.catalog.is_file():
        print(f"ERROR: missing {args.catalog}", file=sys.stderr)
        return 1

    items = load_items(args.catalog)
    if not items:
        print("ERROR: no items in catalog", file=sys.stderr)
        return 1

    out_dir = args.out_dir
    f_era = out_dir / "REFERENCES-shelf-by-era.md"
    f_id = out_dir / "REFERENCES-shelf-by-hnsrc-id.md"
    content_era = build_by_era(items)
    content_id = build_by_id(items)

    if args.check:
        ok = True
        for path, new in ((f_era, content_era), (f_id, content_id)):
            if not path.is_file():
                print(f"CHECK: missing {path}", file=sys.stderr)
                ok = False
                continue
            old = path.read_text(encoding="utf-8")
            if old != new:
                print(f"CHECK: stale {path}", file=sys.stderr)
                ok = False
        if not ok:
            print(
                "Run: python3 scripts/build_hn_bookshelf_bibliography.py",
                file=sys.stderr,
            )
            return 1
        print("ok: hn bookshelf bibliography up to date")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    f_era.write_text(content_era, encoding="utf-8")
    f_id.write_text(content_id, encoding="utf-8")
    print(f"wrote {f_era}")
    print(f"wrote {f_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
