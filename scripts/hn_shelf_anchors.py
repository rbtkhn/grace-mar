#!/usr/bin/env python3
"""Writer ergonomics: inverse map Bookshelf (HNSRC) → `hn-*` chapter ids and lookups.

- Generates research/SHELF-ANCHORS-BY-CHAPTER.md (do not edit by hand).
- CLI: one-card lookup for a shelf id; list shelf anchors for a chapter; paste one-line **stub** for a chapter file.

SSOT: bookshelf-catalog.yaml (`candidate_hn_chapters`); order of chapters: book-architecture.yaml.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
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
HN_ARCH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "book-architecture.yaml"
)
OUT = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "SHELF-ANCHORS-BY-CHAPTER.md"
)

RE_HNSRC = re.compile(r"^HNSRC-\d{4}$")
RE_HN = re.compile(r"^hn-[\w-]+$")

HEADER = """# Shelf anchors by chapter (generated)

**Do not edit by hand.** This file inverts [bookshelf-catalog.yaml](bookshelf-catalog.yaml) `candidate_hn_chapters` into **`hn-*` id → HNSRC list** (planning hints, not draft SSOT).

- Regenerate: `python3 scripts/hn_shelf_anchors.py`
- **Lookup:** `python3 scripts/hn_shelf_anchors.py --hnsrc HNSRC-0001` or `--chapter hn-i-v1-01`
- **Paste line** for a chapter file: `python3 scripts/hn_shelf_anchors.py --stub-line hn-i-v1-01`

[book-architecture.yaml](../book-architecture.yaml) remains chapter SSOT for title and file path.

---
"""


def load_items(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get("items")
    if not isinstance(items, list):
        return []
    return [x for x in items if isinstance(x, dict) and x.get("id")]


def item_index(items: list[dict]) -> dict[str, dict]:
    return {str(x["id"]): x for x in items if x.get("id")}


def invert_hn_to_hnsrc(items: list[dict]) -> dict[str, list[str]]:
    m: dict[str, list[str]] = {}
    for it in items:
        sid = str(it.get("id") or "")
        for ch in it.get("candidate_hn_chapters") or []:
            if not isinstance(ch, str):
                continue
            m.setdefault(ch.strip(), []).append(sid)
    for ch in m:
        m[ch] = sorted(m[ch], key=str)
    return m


def load_chapters_ordered(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    chapters = data.get("chapters")
    if not isinstance(chapters, list):
        return []
    out: list[dict] = []
    for c in chapters:
        if not isinstance(c, dict) or "id" not in c:
            continue
        out.append(
            {
                "id": str(c["id"]),
                "title": str(c.get("title") or ""),
                "file": str(c.get("file") or "").strip() or None,
            }
        )
    return out


def rel_link_from_chapter_file_to_research(chapter_file: str) -> str:
    """e.g. chapters/vol-i/v1-01.md -> ../../research/SHELF-ANCHORS-BY-CHAPTER.md"""
    p = Path(chapter_file)
    n = len(p.parent.parts) if p.parent != Path(".") else 0
    return f"{'../' * n}research/SHELF-ANCHORS-BY-CHAPTER.md"


def build_markdown(
    chapter_rows: list[dict],
    hn_to_hnsrc: dict[str, list[str]],
) -> str:
    lines: list[str] = [HEADER, "## `hn-*` → shelf ids", ""]
    for row in chapter_rows:
        hid = row["id"]
        title = row.get("title") or ""
        rel = row.get("file")
        fpath = f" — draft file `{rel}`" if rel else ""
        lines.append(f"### {hid}{fpath}")
        if title:
            lines.append(f"*{title}*")
        anchors = hn_to_hnsrc.get(hid, [])
        if not anchors:
            lines.append("- *(no `candidate_hn_chapters` point here yet — add in catalog or use another chapter id)*")
        else:
            lines.append(
                "- **HNSRC:** " + ", ".join(f"`{a}`" for a in anchors)
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def hnsrc_card(item: dict) -> str:
    sid = item.get("id", "")
    title = (item.get("title") or "").strip()
    author = (item.get("author") or "").strip()
    era = item.get("era", "")
    hv = item.get("hn_volume", "")
    hv_s = str(hv) if hv else "*(none)*"
    chs = item.get("candidate_hn_chapters") or []
    chs_s = ", ".join(str(c) for c in chs) if chs else "*(none)*"
    notes = (item.get("notes") or "").strip()
    if len(notes) > 500:
        notes = notes[:497] + "…"
    return (
        f"**`{sid}`** — {author} — *{title}*\n"
        f"- **Era:** {era!r} · **hn_volume:** {hv_s}\n"
        f"- **Planning (`candidate_hn_chapters`):** {chs_s}\n"
        f"- **Notes:** {notes or '*(none)*'}"
    )


def chapter_brief(
    by_hn: dict[str, list[str]],
    index: dict[str, dict],
    hn_id: str,
) -> str:
    ids = by_hn.get(hn_id, [])
    if not ids:
        return f"**`{hn_id}`:** no HNSRC rows list this chapter in `candidate_hn_chapters`."
    lines = [f"**`{hn_id}`** — {len(ids)} shelf row(s):"]
    for s in ids:
        it = index.get(s, {})
        title = (it.get("title") or "?").strip()
        author = (it.get("author") or "?").strip()
        lines.append(f"- `{s}` — {author} — *{title}*")
    return "\n".join(lines)


def stub_line(
    by_hn: dict[str, list[str]],
    arch_by_id: dict[str, dict],
    hn_id: str,
) -> tuple[str, int]:
    if hn_id not in arch_by_id:
        return (f"ERROR: unknown chapter id {hn_id!r} in book-architecture.yaml", 1)
    rel = (arch_by_id[hn_id].get("file") or "").strip()
    if not rel:
        return (f"ERROR: chapter {hn_id!r} has no `file` in book-architecture.yaml", 1)
    ids = by_hn.get(hn_id, [])
    if not ids:
        inner = "*(no shelf rows tag this chapter yet; add `candidate_hn_chapters` in the catalog or leave this line as a placeholder)*"
    else:
        inner = ", ".join(f"`{x}`" for x in ids)
    mdf = rel_link_from_chapter_file_to_research(rel)
    return (
        (
            f"**Shelf anchors (owned print, planning):** {inner} — *index:* "
            f"[SHELF-ANCHORS-BY-CHAPTER.md]({mdf}#{hn_id}) — *regen:* `python3 scripts/hn_shelf_anchors.py`"
        ),
        0,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        type=Path,
        default=CATALOG,
        help="Path to bookshelf-catalog.yaml",
    )
    ap.add_argument(
        "--architecture",
        type=Path,
        default=HN_ARCH,
        help="Path to book-architecture.yaml",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=OUT,
        help="Output path for SHELF-ANCHORS-BY-CHAPTER.md",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated file differs from disk (use after catalog or architecture edits)",
    )
    ap.add_argument(
        "--hnsrc",
        metavar="HNSRC-NNNN",
        help="Print a one-shelf **card** for this id and exit",
    )
    ap.add_argument(
        "--chapter",
        metavar="hn-*",
        help="List shelf rows that tag this chapter in candidate_hn_chapters and exit",
    )
    ap.add_argument(
        "--stub-line",
        metavar="hn-*",
        help="Print one **Markdown line** to paste under the chapter id line in a draft file, then exit",
    )
    args = ap.parse_args()

    if not args.catalog.is_file():
        print(f"ERROR: missing {args.catalog}", file=sys.stderr)
        return 1
    if not args.architecture.is_file():
        print(f"ERROR: missing {args.architecture}", file=sys.stderr)
        return 1

    items = load_items(args.catalog)
    if not items:
        print("ERROR: no items in catalog", file=sys.stderr)
        return 1
    index = item_index(items)
    by_hn = invert_hn_to_hnsrc(items)
    chapter_rows = load_chapters_ordered(args.architecture)
    arch_by_id = {c["id"]: c for c in chapter_rows}
    if not chapter_rows:
        print("ERROR: no chapters in book-architecture.yaml", file=sys.stderr)
        return 1

    if args.hnsrc:
        sid = args.hnsrc.strip()
        if not RE_HNSRC.match(sid):
            print(f"ERROR: id must look like HNSRC-NNNN, got {sid!r}", file=sys.stderr)
            return 1
        it = index.get(sid)
        if not it:
            print(f"ERROR: unknown {sid}", file=sys.stderr)
            return 1
        print(hnsrc_card(it))
        return 0

    if args.chapter:
        hid = args.chapter.strip()
        if not RE_HN.match(hid):
            print(
                f"ERROR: chapter id should look like hn-..., got {hid!r}",
                file=sys.stderr,
            )
            return 1
        print(chapter_brief(by_hn, index, hid))
        return 0

    if args.stub_line is not None:
        hid = args.stub_line.strip()
        if not RE_HN.match(hid):
            print(
                f"ERROR: chapter id should look like hn-..., got {hid!r}",
                file=sys.stderr,
            )
            return 1
        text, code = stub_line(by_hn, arch_by_id, hid)
        if code:
            print(text, file=sys.stderr)
            return code
        print(text)
        return 0

    content = build_markdown(chapter_rows, by_hn)

    if args.check:
        if not args.out.is_file():
            print(f"CHECK: missing {args.out}", file=sys.stderr)
            print("Run: python3 scripts/hn_shelf_anchors.py", file=sys.stderr)
            return 1
        if args.out.read_text(encoding="utf-8") != content:
            print(f"CHECK: stale {args.out}", file=sys.stderr)
            print("Run: python3 scripts/hn_shelf_anchors.py", file=sys.stderr)
            return 1
        print("ok: shelf anchors by chapter up to date")
        return 0

    args.out.write_text(content, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
