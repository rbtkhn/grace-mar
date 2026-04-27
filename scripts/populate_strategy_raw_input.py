#!/usr/bin/env python3
"""Backfill strategy-notebook/raw-input from on-disk artifacts (rolling window).

Copies:
  - Standalone *verbatim*.md under the strategy-notebook root (date from filename)
  - Per-expert experts/<id>/transcript.md sections (## YYYY-MM-DD) in window
  - X screenshot index markdown (links to assets/**/x-*.png grouped by date in filename)

Date window matches scripts/strategy_expert_transcript.py and prune_strategy_raw_input.py:
  include dates d where d > (today - days).

Destination folders ``raw-input/YYYY-MM-DD/`` use the **air / publication** day
(``pub_date``), aligned with ``raw-input/README.md`` § Layout — not “ingest day.”

WORK-only; not Record.

Usage:
  python3 scripts/populate_strategy_raw_input.py --dry-run
  python3 scripts/populate_strategy_raw_input.py --apply
  python3 scripts/populate_strategy_raw_input.py --apply --append-inbox
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from strategy_expert_transcript import parse_transcript_file

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_NOTEBOOK = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_RAW_ROOT = DEFAULT_NOTEBOOK / "raw-input"

_RE_DATE_IN_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")
_RE_X_PNG_DATE = re.compile(r"x-(\d{4}-\d{2}-\d{2})")


def _word_count(text: str) -> int:
    return len(text.split())


def _in_window(d: date, *, today: date, days: int) -> bool:
    cutoff = today - timedelta(days=days)
    return d > cutoff


def _rel_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _find_verbatim_files(notebook_root: Path) -> list[Path]:
    return sorted(notebook_root.glob("*verbatim*.md"))


def _verbatim_air_date(path: Path) -> date | None:
    m = _RE_DATE_IN_NAME.search(path.name)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d").date()


def _discover_x_pngs(notebook_root: Path) -> list[tuple[date, Path]]:
    assets = notebook_root / "assets"
    if not assets.is_dir():
        return []
    out: list[tuple[date, Path]] = []
    for p in sorted(assets.rglob("x-*.png")):
        m = _RE_X_PNG_DATE.search(p.name)
        if not m:
            continue
        d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        out.append((d, p))
    return out


def _x_index_markdown(*, day: date, pngs: list[Path], notebook_root: Path) -> str:
    lines = [
        "---",
        f"ingest_date: {day.isoformat()}",
        f"pub_date: {day.isoformat()}",
        "kind: x-screenshots-index",
        "source: assets/**/*.png",
        "---",
        "",
        f"# X screenshot index — {day.isoformat()}",
        "",
        "Embedded from strategy-notebook `assets/` (single SSOT; no PNG duplication).",
        "",
    ]
    for p in sorted(pngs, key=lambda x: x.as_posix()):
        rel_from_notebook = p.resolve().relative_to(notebook_root.resolve())
        # Index file lives at raw-input/YYYY-MM-DD/x-screenshots-index.md → ../../ + path under notebook
        href = Path("../../") / rel_from_notebook
        alt = p.stem.replace("-", " ")
        lines.append(f"## `{p.name}`")
        lines.append("")
        lines.append(f"![{alt}]({href.as_posix()})")
        lines.append("")
    return "\n".join(lines) + "\n"


def _transcript_frontmatter(
    *,
    expert_id: str,
    section_date: str,
    source_path: str,
) -> str:
    return (
        "---\n"
        f"ingest_date: {section_date}\n"
        f"pub_date: {section_date}\n"
        f"thread: {expert_id}\n"
        "kind: transcript\n"
        f"source_path: {source_path}\n"
        "---\n\n"
    )


def _verbatim_frontmatter(*, air_date: str, source_path: str, kind: str = "verbatim-sidecar") -> str:
    return (
        "---\n"
        f"ingest_date: {air_date}\n"
        f"pub_date: {air_date}\n"
        "kind: " + kind + "\n"
        f"source_path: {source_path}\n"
        "---\n\n"
    )


def _file_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _append_populate_inbox_block(
    notebook_root: Path,
    run_key: str,
    stubs: list[tuple[str, Path]],
    *,
    dry_run: bool,
) -> int:
    """Replace ``<!-- strategy-populate:KEY -->`` … block in **daily-strategy-inbox** (idempotent by day)."""
    if not stubs:
        return 0
    from fetch_strategy_raw_input import INBOX_APPEND_LINE  # noqa: PLC0415

    inbox = notebook_root / "daily-strategy-inbox.md"
    if not inbox.is_file():
        print(f"populate: skip --append-inbox (missing {inbox})", file=sys.stderr)
        return 0
    nbase = notebook_root.resolve()
    seen: set[str] = set()
    new_lines: list[str] = []
    for expert_id, abs_p in stubs:
        ap = abs_p.resolve()
        try:
            rel = ap.relative_to(nbase)
        except ValueError:
            try:
                rel = ap.relative_to(REPO_ROOT)
            except ValueError:
                rel = ap
        rel_s = str(rel).replace("\\", "/")
        if rel_s in seen:
            continue
        seen.add(rel_s)
        fn = ap.name
        title = re.sub(r"[-_]+", " ", ap.stem).strip()[:80] or fn
        new_lines.append(
            f"- populate | cold: **{title}** // hook: backfill to raw-input | "
            f"[{fn}]({rel_s}) | verify:populate+strategy_raw_input | thread:{expert_id}\n"
        )
    if not new_lines:
        return 0
    if dry_run:
        for ln in new_lines:
            print(f"would append-inbox: {ln.strip()}", flush=True)
        return len(new_lines)
    text = inbox.read_text(encoding="utf-8")
    start = f"<!-- strategy-populate:{run_key} -->"
    end = f"<!-- /strategy-populate:{run_key} -->"
    new_block = start + "\n" + "".join(new_lines) + end + "\n"
    if start in text and end in text:
        p0 = text.index(start)
        p1 = text.index(end) + len(end)
        while p1 < len(text) and text[p1] in "\n":
            p1 += 1
        text = text[:p0] + new_block + text[p1:]
    elif INBOX_APPEND_LINE in text:
        i = text.index(INBOX_APPEND_LINE) + len(INBOX_APPEND_LINE)
        text = text[:i] + "\n\n" + new_block + text[i:]
    else:
        text = text.rstrip() + "\n\n" + new_block
    inbox.write_text(text, encoding="utf-8")
    print(
        f"populate: inbox block strategy-populate:{run_key} ({len(new_lines)} stub(s)) → {inbox.relative_to(REPO_ROOT)}",
        flush=True,
    )
    return len(new_lines)


def run(
    *,
    notebook_root: Path,
    raw_root: Path,
    days: int,
    today: date,
    apply: bool,
    force: bool,
    append_inbox: bool = False,
) -> int:
    raw_root = raw_root.resolve()
    notebook_root = notebook_root.resolve()

    planned: list[tuple[Path, str, int]] = []  # path, content, words
    inbox_mirrors: list[tuple[str, Path]] = []  # transcript → raw-input mirror rows (for --append-inbox)

    # --- Verbatim sidecars ---
    for vf in _find_verbatim_files(notebook_root):
        air = _verbatim_air_date(vf)
        if air is None or not _in_window(air, today=today, days=days):
            continue
        body = vf.read_text(encoding="utf-8")
        if body.lstrip().startswith("---"):
            out_body = body
        else:
            out_body = _verbatim_frontmatter(
                air_date=air.isoformat(),
                source_path=_rel_to_repo(vf),
            ) + body
        dest = raw_root / air.isoformat() / vf.name
        planned.append((dest, out_body, _word_count(out_body)))

    # --- Expert transcript sections ---
    experts_dir = notebook_root / "experts"
    if experts_dir.is_dir():
        for transcript_path in sorted(experts_dir.glob("*/transcript.md")):
            expert_id = transcript_path.parent.name
            _header, sections = parse_transcript_file(transcript_path)
            src_rel = _rel_to_repo(transcript_path)
            for date_str, lines in sections.items():
                try:
                    d = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if not _in_window(d, today=today, days=days):
                    continue
                section_text = "\n".join(lines) + "\n"
                out_text = _transcript_frontmatter(
                    expert_id=expert_id,
                    section_date=date_str,
                    source_path=src_rel,
                ) + section_text
                dest = raw_root / date_str / f"{date_str}-{expert_id}.md"
                planned.append((dest, out_text, _word_count(out_text)))
                inbox_mirrors.append((expert_id, dest))

    # --- X PNG index (one file per day in window that has PNGs) ---
    by_day: dict[date, list[Path]] = {}
    for d, p in _discover_x_pngs(notebook_root):
        if not _in_window(d, today=today, days=days):
            continue
        by_day.setdefault(d, []).append(p)

    for d, pngs in sorted(by_day.items()):
        dest = raw_root / d.isoformat() / "x-screenshots-index.md"
        content = _x_index_markdown(day=d, pngs=pngs, notebook_root=notebook_root)
        planned.append((dest, content, _word_count(content)))

    mirror_eid: dict[Path, str] = {d.resolve(): eid for eid, d in inbox_mirrors}
    inbox_todo: list[tuple[str, Path]] = []

    # --- Write or print ---
    for dest, content, words in sorted(planned, key=lambda x: str(x[0])):
        rel = dest.relative_to(REPO_ROOT) if dest.is_relative_to(REPO_ROOT) else dest
        exists = dest.is_file()
        same = (
            exists
            and hashlib.sha256(dest.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            == _file_sha256(content)
        )
        if exists and same:
            print(f"skip (unchanged): {rel}  ({words} words)")
            continue

        if not apply:
            action = "would update" if exists else "would write"
            extra = " [exists]" if exists else ""
            print(f"{action}: {rel}  ({words} words){extra}")
            dr = dest.resolve()
            if append_inbox and dr in mirror_eid:
                inbox_todo.append((mirror_eid[dr], dest))
            continue

        if exists and not force:
            print(f"skip (exists, use --force): {rel}")
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print(f"wrote: {rel}  ({words} words)")
        dr = dest.resolve()
        if append_inbox and dr in mirror_eid:
            inbox_todo.append((mirror_eid[dr], dest))

    if not planned:
        print("No artifacts in window; nothing to do.")
        return 0

    if not apply:
        print(f"\nDry-run complete ({len(planned)} file(s)). Pass --apply to write.")

    if append_inbox and inbox_todo:
        _append_populate_inbox_block(
            notebook_root,
            run_key=today.isoformat(),
            stubs=inbox_todo,
            dry_run=not apply,
        )
    return 0


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--notebook-root",
        type=Path,
        default=DEFAULT_NOTEBOOK,
        help="strategy-notebook directory",
    )
    p.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_RAW_ROOT,
        help="raw-input root directory",
    )
    p.add_argument("--days", type=int, default=7, help="Rolling window (default: 7)")
    p.add_argument(
        "--today",
        type=str,
        default=None,
        help="Override local today as YYYY-MM-DD (testing)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print planned writes only")
    p.add_argument("--apply", action="store_true", help="Write files")
    p.add_argument("--force", action="store_true", help="Overwrite when content differs")
    p.add_argument(
        "--append-inbox",
        action="store_true",
        help="After writes (or dry-run), append idempotent daily-strategy-inbox block for "
        "transcript→raw-input mirrors (same run replaces <!-- strategy-populate:YYYY-MM-DD --> block)",
    )
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("Use only one of --dry-run or --apply")
    if not args.apply and not args.dry_run:
        args.dry_run = True

    today = (
        datetime.strptime(args.today, "%Y-%m-%d").date()
        if args.today
        else date.today()
    )

    return run(
        notebook_root=args.notebook_root,
        raw_root=args.root,
        days=args.days,
        today=today,
        apply=args.apply,
        force=args.force,
        append_inbox=args.append_inbox,
    )


if __name__ == "__main__":
    raise SystemExit(main())
