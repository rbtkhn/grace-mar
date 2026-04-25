#!/usr/bin/env python3
"""List thread-embedded ``strategy-page`` blocks in a calendar month (WORK only).

Reads expert thread file(s) via ``discover_all_pages`` (same dedupe rules as
validators: monthly file preferred over legacy ``thread.md`` for the same
``id=``). Filters by ``date=`` prefix ``YYYY-MM``.

Optional ``--chronicle-snippets`` extracts **advisory** candidates from each
page body: first non-empty paragraph under ``### Chronicle`` (dumb parse) and
lines that look like markdown blockquotes (``>``). **Never** auto-inserts into
the thread; selection still follows the rubric in ``strategy-expert-template.md``
(Thread).

Usage (repo root)::

    python3 scripts/list_strategy_pages_by_month.py --year-month 2026-04
    python3 scripts/list_strategy_pages_by_month.py --year-month 2026-04 --expert-id mercouris
    python3 scripts/list_strategy_pages_by_month.py --year-month 2026-04 --chronicle-snippets
    python3 scripts/list_strategy_pages_by_month.py --year-month 2026-04 --json
    python3 scripts/list_strategy_pages_by_month.py --year-month 2026-04 --json --chronicle-snippets
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import CANONICAL_EXPERT_IDS  # noqa: E402
from strategy_page_reader import PageBlock, discover_all_pages  # noqa: E402

NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

YM_RE = re.compile(r"^\d{4}-\d{2}$")
# Chronicle body: from ### Chronicle through the next ### heading or EOF
RE_CHRONICLE = re.compile(
    r"^###\s+Chronicle\s*$(.*?)(?=^###\s+|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
MAX_PARA_CHARS = 500
MAX_BQ = 20


def _chronicle_section(content: str) -> str:
    m = RE_CHRONICLE.search(content)
    if not m:
        return ""
    return m.group(1).strip()


def _first_paragraph(chronicle: str) -> str:
    if not chronicle:
        return ""
    parts = re.split(r"\n\s*\n", chronicle)
    for p in parts:
        t = p.strip()
        if not t:
            continue
        t = re.sub(r"\s+", " ", t)
        if len(t) > MAX_PARA_CHARS:
            t = t[: MAX_PARA_CHARS - 1] + "…"
        return t
    return ""


def _blockquote_lines(chronicle: str) -> list[str]:
    out: list[str] = []
    for line in chronicle.splitlines():
        s = line.strip()
        if s.startswith(">"):
            inner = s[1:].strip() if len(s) > 1 else ""
            if inner and len(out) < MAX_BQ:
                out.append(inner)
    return out


def chronicle_snippets_from_page_content(content: str) -> dict[str, Any]:
    ch = _chronicle_section(content)
    if not ch:
        return {
            "chronicle_found": False,
            "first_paragraph": "",
            "blockquotes": [],
        }
    return {
        "chronicle_found": True,
        "first_paragraph": _first_paragraph(ch),
        "blockquotes": _blockquote_lines(ch),
    }


def _rel_path(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="List strategy-page blocks in expert threads for a YYYY-MM window.",
    )
    ap.add_argument(
        "--year-month",
        required=True,
        metavar="YYYY-MM",
        help="Calendar month (e.g. 2026-04).",
    )
    ap.add_argument(
        "--expert-id",
        metavar="ID",
        default="",
        help="Limit to one expert (slug, e.g. mercouris). Omit for all experts.",
    )
    ap.add_argument(
        "--notebook-dir",
        type=Path,
        default=NOTEBOOK_DIR,
        help=f"Strategy notebook root (default: {NOTEBOOK_DIR}).",
    )
    ap.add_argument(
        "--chronicle-snippets",
        action="store_true",
        help="Advisory: first Chronicle paragraph + blockquote lines per page (dumb parse).",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit JSON array (one object per page).",
    )
    args = ap.parse_args()
    ym = args.year_month.strip()
    if not YM_RE.match(ym):
        print(
            "error: --year-month must look like YYYY-MM (e.g. 2026-04)",
            file=sys.stderr,
        )
        return 1

    expert_filter = args.expert_id.strip()
    if expert_filter and expert_filter not in CANONICAL_EXPERT_IDS:
        print(
            f"warning: {expert_filter!r} is not in CANONICAL_EXPERT_IDS — "
            "listing anyway if pages exist on disk.",
            file=sys.stderr,
        )

    by_expert = discover_all_pages(args.notebook_dir.resolve())
    page_rows: list[tuple[str, PageBlock]] = []
    for eid, pages in sorted(by_expert.items()):
        if expert_filter and eid != expert_filter:
            continue
        for pb in pages:
            d = (pb.date or "").strip()
            if len(d) < 7 or d[:7] != ym:
                continue
            page_rows.append((eid, pb))

    page_rows.sort(key=lambda r: (r[0], r[1].date, r[1].id))

    if not page_rows:
        if args.as_json:
            print("[]")
        else:
            print(f"(no strategy-page blocks with date in {ym})")
        return 0

    if args.as_json:
        items: list[dict[str, Any]] = []
        for eid, pb in page_rows:
            w = pb.watch if pb.watch is not None else ""
            obj: dict[str, Any] = {
                "expert_id": eid,
                "id": pb.id,
                "date": pb.date,
                "watch": w,
                "source_path": _rel_path(pb.source_path),
            }
            if args.chronicle_snippets:
                obj["snippets"] = chronicle_snippets_from_page_content(pb.content)
            items.append(obj)
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    for eid, pb in page_rows:
        w = pb.watch if pb.watch is not None else ""
        print(f"{eid}\t{pb.id}\t{pb.date}\t{w}\t{_rel_path(pb.source_path)}")

    if args.chronicle_snippets:
        print()
        print("--- chronicle-snippets (advisory; not auto-insert) ---")
        for eid, pb in page_rows:
            sn = chronicle_snippets_from_page_content(pb.content)
            print()
            print(f"### {eid} / {pb.id} / {pb.date}")
            if not sn.get("chronicle_found"):
                print("(no `### Chronicle` section parsed in fence body — check heading spelling.)")
                continue
            fp = sn.get("first_paragraph") or ""
            if fp:
                print("first_paragraph:", fp)
            bqs: list[str] = sn.get("blockquotes") or []
            if bqs:
                print("blockquotes:")
                for b in bqs:
                    print(f"  - {b}")
            if not fp and not bqs:
                print("(Chronicle section empty or only whitespace after parse.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
