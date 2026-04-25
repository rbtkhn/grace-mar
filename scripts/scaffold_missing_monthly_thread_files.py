#!/usr/bin/env python3
"""Create ``<id>-thread-YYYY-MM.md`` files for months in ``thread.md`` that are not on disk yet.

For experts who **already** use a monthly layout (at least one ``*-thread-YYYY-MM`` file),
the full :file:`migrate_thread_md_to_monthly.py` run is skipped. This script fills in
**gaps** by copying the human journal (``## YYYY-MM`` segments) from
``experts/<id>/thread.md`` and appending a placeholder machine block. It does **not**
rename ``thread.md``.

Body segments are cut at ``<!-- backfill:<expert_id>:start -->`` if present (so
backfill stays in the legacy file until you move it deliberately).

Run ``python3 scripts/strategy_thread.py`` after scaffolding to fill machine layers.

WORK only; not Record.

Usage::

    python3 scripts/scaffold_missing_monthly_thread_files.py --expert ritter
    python3 scripts/scaffold_missing_monthly_thread_files.py --expert ritter --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from migrate_thread_md_to_monthly import (  # noqa: E402
    _compose_month_file,
    _extract_human_and_machine,
    _month_segments,
)
from strategy_expert_corpus import month_thread_paths_by_month  # noqa: E402

NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"


def _action_path(dest: Path) -> str:
    try:
        return str(dest.relative_to(REPO_ROOT))
    except ValueError:
        return str(dest)


_RE_BACKFILL = re.compile(
    r"\n*<!--\s*backfill:[a-z][a-z0-9-]*:start\s*-->", re.IGNORECASE
)


def _strip_backfill_from_segment(body: str) -> str:
    """If a backfill fence appears mid-segment, keep only the journal part above it."""
    m = _RE_BACKFILL.search(body)
    if m:
        return body[: m.start()].rstrip()
    return body.rstrip()


def scaffold_missing(
    notebook_dir: Path,
    expert_id: str,
    *,
    apply: bool,
) -> list[str]:
    if not month_thread_paths_by_month(notebook_dir, expert_id):
        return [f"skip (no monthly layout yet for {expert_id})"]

    expert_dir = notebook_dir / "experts" / expert_id
    src = expert_dir / "thread.md"
    if not src.is_file():
        return [f"skip (no {src.relative_to(REPO_ROOT)})"]

    text = src.read_text(encoding="utf-8")
    human, _ = _extract_human_and_machine(text)
    prefix, segments, _tail = _month_segments(human)
    if not segments:
        return [f"skip (no ## YYYY-MM in journal for {expert_id})"]

    actions: list[str] = []
    for _j, (ym, body) in enumerate(segments):
        dest = expert_dir / f"{expert_id}-thread-{ym}.md"
        if dest.is_file():
            continue
        body_use = _strip_backfill_from_segment(body)
        content = _compose_month_file(
            expert_id=expert_id,
            prefix=prefix,
            ym=ym,
            body=body_use,
            tail="",
            include_tail=False,
        )
        actions.append(f"{'write' if apply else 'would write'} {_action_path(dest)}")
        if apply:
            dest.write_text(content, encoding="utf-8")

    if not actions:
        return [f"nothing to scaffold (all segment months have files for {expert_id})"]
    return actions


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--notebook",
        type=Path,
        default=NOTEBOOK,
        help="Strategy notebook root",
    )
    ap.add_argument(
        "--expert",
        required=True,
        help="Expert id (e.g. ritter)",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Write files; default is dry-run",
    )
    args = ap.parse_args()
    for line in scaffold_missing(
        args.notebook,
        args.expert.lower().strip(),
        apply=bool(args.apply),
    ):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
