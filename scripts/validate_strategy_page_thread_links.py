#!/usr/bin/env python3
"""Validate bindings between standalone expert pages and expert thread files.

WORK only; not Record.

This is an adoption validator for the page-thread binding contract:

- Pages / Work Product are standalone ``experts/<id>/<id>-page-YYYY-MM-DD*.md``.
- Thread / Continuity is the matching monthly thread file
  ``experts/<id>/<id>-thread-YYYY-MM.md`` or legacy ``experts/<id>/thread.md``.
- Page appendix metadata may declare Thread file / Thread month / Thread role /
  Continuity delta.
- Thread month segments may include a compact ``### Pages / Work Product`` index.

By default, missing adoption metadata is reported as warnings so the script can
be introduced before the tree is migrated. Use ``--require-page-metadata`` and
``--require-thread-index`` to turn those into errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
VALID_ROLES = {
    "new-thesis",
    "update",
    "contradiction",
    "falsifier",
    "synthesis",
    "carry-forward",
}
FIELD_RE = re.compile(
    r"^-\s+\*\*(?P<field>Thread file|Thread month|Thread role|Continuity delta):\*\*\s*(?P<value>.*)$",
    re.MULTILINE,
)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\((?P<href>[^)]+)\)")


@dataclass
class PageInfo:
    expert_id: str
    date: str
    month: str
    path: Path
    title: str
    fields: dict[str, str]


def repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def notebook_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(NOTEBOOK_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def clean_inline(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for m in FIELD_RE.finditer(text):
        fields[m.group("field").lower().replace(" ", "_")] = clean_inline(m.group("value"))
    return fields


def page_title(text: str, fallback: str) -> str:
    m = H1_RE.search(text)
    if not m:
        return fallback
    return m.group(1).strip()


def discover_pages(notebook_dir: Path, expert_filter: str = "", month_filter: str = "") -> list[PageInfo]:
    pages: list[PageInfo] = []
    experts_dir = notebook_dir / "experts"
    for expert_dir in sorted(experts_dir.iterdir() if experts_dir.is_dir() else []):
        if not expert_dir.is_dir() or expert_dir.name.startswith("."):
            continue
        expert_id = expert_dir.name
        if expert_filter and expert_id != expert_filter:
            continue
        for path in sorted(expert_dir.glob(f"{expert_id}-page-*.md")):
            m = re.match(rf"^{re.escape(expert_id)}-page-(\d{{4}}-\d{{2}}-\d{{2}})(?:-.+)?\.md$", path.name)
            if not m:
                continue
            date = m.group(1)
            month = date[:7]
            if month_filter and month != month_filter:
                continue
            text = read_text(path)
            pages.append(
                PageInfo(
                    expert_id=expert_id,
                    date=date,
                    month=month,
                    path=path,
                    title=page_title(text, path.stem),
                    fields=parse_fields(text),
                )
            )
    return pages


def expected_thread_file(page: PageInfo, notebook_dir: Path) -> Path:
    expert_dir = notebook_dir / "experts" / page.expert_id
    monthly = expert_dir / f"{page.expert_id}-thread-{page.month}.md"
    if monthly.is_file():
        return monthly
    return expert_dir / "thread.md"


def resolve_declared_thread(page: PageInfo) -> Path | None:
    raw = page.fields.get("thread_file", "")
    if not raw:
        return None
    m = LINK_RE.search(raw)
    href = m.group("href") if m else raw
    href = href.split("#", 1)[0].strip()
    if not href:
        return None
    p = Path(href)
    if p.is_absolute():
        return p
    # Prefer page-relative links; fall back to repo-relative links.
    page_relative = (page.path.parent / p).resolve()
    if page_relative.exists():
        return page_relative
    return (REPO_ROOT / p).resolve()


def human_layer(text: str) -> str:
    if THREAD_MARKER_START in text:
        return text.split(THREAD_MARKER_START, 1)[0]
    return text


def month_segment(text: str, month: str) -> str:
    human = human_layer(text)
    m = re.search(rf"^##\s+{re.escape(month)}\s*$", human, re.MULTILINE)
    if not m:
        return human
    rest = human[m.end():]
    n = re.search(r"^##\s+\d{4}-\d{2}\s*$", rest, re.MULTILINE)
    return rest[: n.start()] if n else rest


def pages_work_product_section(segment: str) -> str:
    m = re.search(r"^###\s+Pages / Work Product\s*$", segment, re.MULTILINE)
    if not m:
        return ""
    rest = segment[m.end():]
    n = re.search(r"^###\s+", rest, re.MULTILINE)
    return rest[: n.start()] if n else rest


def page_is_indexed(page: PageInfo, thread_path: Path) -> tuple[bool, bool]:
    if not thread_path.is_file():
        return False, False
    segment = month_segment(read_text(thread_path), page.month)
    section = pages_work_product_section(segment)
    if not section:
        return False, False
    needles = {
        page.path.name,
        notebook_rel(page.path),
        repo_rel(page.path),
    }
    return any(n in section for n in needles), True


def validate(args: argparse.Namespace) -> dict[str, Any]:
    notebook = args.notebook_dir.resolve()
    pages = discover_pages(notebook, args.expert_id, args.year_month)
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict[str, Any]] = []
    missing_index_reported: set[tuple[str, str]] = set()

    for page in pages:
        expected_thread = expected_thread_file(page, notebook)
        declared_thread = resolve_declared_thread(page)
        declared_month = clean_inline(page.fields.get("thread_month", ""))
        declared_role = clean_inline(page.fields.get("thread_role", ""))
        declared_delta = clean_inline(page.fields.get("continuity_delta", ""))

        row: dict[str, Any] = {
            "page": repo_rel(page.path),
            "expert_id": page.expert_id,
            "date": page.date,
            "month": page.month,
            "expected_thread": repo_rel(expected_thread),
            "declared_thread": repo_rel(declared_thread) if declared_thread else "",
            "thread_month": declared_month,
            "thread_role": declared_role,
            "has_delta": bool(declared_delta),
        }

        if not expected_thread.is_file():
            errors.append(f"{repo_rel(page.path)}: expected thread file missing: {repo_rel(expected_thread)}")

        missing = [
            name
            for name, value in (
                ("Thread file", declared_thread),
                ("Thread month", declared_month),
                ("Thread role", declared_role),
                ("Continuity delta", declared_delta),
            )
            if not value
        ]
        if missing:
            msg = f"{repo_rel(page.path)}: missing page-thread metadata: {', '.join(missing)}"
            (errors if args.require_page_metadata else warnings).append(msg)

        if declared_thread and not declared_thread.is_file():
            errors.append(f"{repo_rel(page.path)}: declared Thread file does not exist: {repo_rel(declared_thread)}")

        if declared_month and declared_month != page.month:
            errors.append(f"{repo_rel(page.path)}: Thread month {declared_month!r} does not match page month {page.month!r}")

        if declared_role and declared_role not in VALID_ROLES:
            errors.append(
                f"{repo_rel(page.path)}: Thread role {declared_role!r} is not one of {', '.join(sorted(VALID_ROLES))}"
            )

        indexed, has_section = page_is_indexed(page, expected_thread)
        row["thread_index_section"] = has_section
        row["thread_indexed"] = indexed
        if not has_section:
            msg = f"{repo_rel(expected_thread)}: missing `### Pages / Work Product` for {page.month}"
            key = (repo_rel(expected_thread), page.month)
            if key not in missing_index_reported:
                (errors if args.require_thread_index else warnings).append(msg)
                missing_index_reported.add(key)
        elif not indexed:
            msg = f"{repo_rel(expected_thread)}: page not listed in `### Pages / Work Product`: {page.path.name}"
            (errors if args.require_thread_index else warnings).append(msg)
        rows.append(row)

    return {
        "ok": not errors,
        "pages_checked": len(pages),
        "errors": errors,
        "warnings": warnings,
        "rows": rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notebook-dir", type=Path, default=NOTEBOOK_DIR)
    ap.add_argument("--expert-id", default="", help="Limit to one expert id.")
    ap.add_argument("--year-month", default="", help="Limit to YYYY-MM.")
    ap.add_argument("--require-page-metadata", action="store_true")
    ap.add_argument("--require-thread-index", action="store_true")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    if args.year_month and not re.fullmatch(r"\d{4}-\d{2}", args.year_month):
        print("error: --year-month must be YYYY-MM", file=sys.stderr)
        return 2

    result = validate(args)
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        for error in result["errors"]:
            print(f"error: {error}", file=sys.stderr)
        print(
            f"{'ok' if result['ok'] else 'failed'}: checked {result['pages_checked']} standalone expert page(s); "
            f"{len(result['warnings'])} warning(s), {len(result['errors'])} error(s)"
        )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
