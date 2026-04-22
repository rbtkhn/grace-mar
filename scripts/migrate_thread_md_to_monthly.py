#!/usr/bin/env python3
"""Split legacy ``experts/<id>/thread.md`` into ``<id>-thread-YYYY-MM.md`` (WORK only).

Copies the **journal layer** (human content above ``<!-- strategy-expert-thread:start``)
by ``## YYYY-MM`` headings into one file per month. Preserves a shared prefix
(lines before the first ``## YYYY-MM``) in each output file. Appends any trailing
content after the last month block (e.g. ``<!-- backfill:``) to the last month file.

The **machine layer** from the source file is **not** copied per month; run
``python3 scripts/strategy_thread.py`` (or corpus ``rebuild_threads``) after migration
to regenerate machine blocks.

Usage::

    python3 scripts/migrate_thread_md_to_monthly.py --dry-run
    python3 scripts/migrate_thread_md_to_monthly.py --apply

"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (  # noqa: E402
    THREAD_MARKER_END,
    THREAD_MARKER_START,
    month_thread_paths_by_month,
)

NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")


def _extract_human_and_machine(text: str) -> tuple[str, str]:
    if THREAD_MARKER_START not in text:
        return text.rstrip(), ""
    human, rest = text.split(THREAD_MARKER_START, 1)
    if THREAD_MARKER_END in rest:
        machine, after = rest.split(THREAD_MARKER_END, 1)
    else:
        machine, after = rest, ""
    return human.rstrip(), after


def _month_segments(human: str) -> tuple[str, list[tuple[str, str]], str]:
    """Prefix before first ``## YYYY-MM``, list of (ym, body), trailing tail."""
    lines = human.splitlines()
    first_month_i: int | None = None
    for i, line in enumerate(lines):
        if RE_MONTH_H2.match(line.strip()):
            first_month_i = i
            break
    if first_month_i is None:
        return human, [], ""

    prefix = "\n".join(lines[:first_month_i]).rstrip()
    segments: list[tuple[str, str]] = []
    i = first_month_i
    while i < len(lines):
        m = RE_MONTH_H2.match(lines[i].strip())
        if not m:
            i += 1
            continue
        ym = m.group(1)
        i += 1
        body_start = i
        while i < len(lines):
            if RE_MONTH_H2.match(lines[i].strip()):
                break
            i += 1
        body = "\n".join(lines[body_start:i]).rstrip()
        segments.append((ym, body))

    tail = "\n".join(lines[i:]).strip()
    return prefix, segments, tail


def _compose_month_file(
    *,
    expert_id: str,
    prefix: str,
    ym: str,
    body: str,
    tail: str,
    include_tail: bool,
) -> str:
    parts = []
    if prefix:
        parts.append(prefix)
        parts.append("")
    parts.append(f"## {ym}")
    parts.append("")
    if body:
        parts.append(body)
    if include_tail and tail:
        parts.append("")
        parts.append(tail)
    parts.append("")
    parts.append(THREAD_MARKER_START)
    parts.append("")
    parts.append(
        "_Machine layer will be filled on next `thread` run._\n"
    )
    parts.append(THREAD_MARKER_END)
    parts.append("")
    return "\n".join(parts)


def migrate_expert_dir(notebook_dir: Path, expert_dir: Path, *, apply: bool) -> list[str]:
    expert_id = expert_dir.name
    src = expert_dir / "thread.md"
    if not src.is_file():
        return []
    if month_thread_paths_by_month(notebook_dir, expert_id):
        return [f"skip (already has monthly threads): {expert_id}"]

    text = src.read_text(encoding="utf-8")
    human, _ = _extract_human_and_machine(text)
    prefix, segments, tail = _month_segments(human)
    if not segments:
        return [f"skip (no ## YYYY-MM in journal): {expert_id}"]

    actions: list[str] = []
    for j, (ym, body) in enumerate(segments):
        dest = expert_dir / f"{expert_id}-thread-{ym}.md"
        include_tail = j == len(segments) - 1
        content = _compose_month_file(
            expert_id=expert_id,
            prefix=prefix,
            ym=ym,
            body=body,
            tail=tail,
            include_tail=include_tail,
        )
        actions.append(f"{'write' if apply else 'would write'} {dest.relative_to(REPO_ROOT)}")
        if apply:
            dest.write_text(content, encoding="utf-8")
    if apply:
        bak = expert_dir / "thread.md.bak"
        src.rename(bak)
        actions.append(f"renamed {src.relative_to(REPO_ROOT)} -> {bak.name}")
    else:
        actions.append(f"would rename {src.relative_to(REPO_ROOT)} -> thread.md.bak")
    return actions


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--notebook",
        type=Path,
        default=NOTEBOOK,
        help="Strategy notebook root",
    )
    ap.add_argument("--apply", action="store_true", help="Write files and rename thread.md")
    args = ap.parse_args()
    apply = args.apply

    all_actions: list[str] = []
    for expert_dir in sorted(args.notebook.glob("experts/*")):
        if not expert_dir.is_dir():
            continue
        all_actions.extend(migrate_expert_dir(args.notebook, expert_dir, apply=apply))

    for line in all_actions:
        print(line)
    if not all_actions:
        print("no migrations", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
