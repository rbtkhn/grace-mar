#!/usr/bin/env python3
"""Validate ``strategy-page`` fenced blocks in expert ``thread.md`` files (WORK only).

Checks:

- Every ``<!-- strategy-page:start`` has a matching ``<!-- strategy-page:end -->``.
- Optional ``--strict-prose``: for each page body, text above ``### Technical appendix``
  (or entire body if no appendix heading) should be **≥90%** of words in that page
  (excludes appendix from denominator when present).

Exit 0 on success; 1 if errors (or strict-prose failures with ``--strict-prose``).
Warnings go to stderr.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import CANONICAL_EXPERT_IDS, expert_thread_paths_for_discovery
from strategy_page_reader import PAGE_END_RE, PAGE_MARKER_RE, discover_pages

NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"


def _human_layer(text: str) -> str:
    if THREAD_MARKER_START in text:
        return text.split(THREAD_MARKER_START, 1)[0]
    return text


def find_unclosed_page_markers(text: str) -> list[str]:
    """Return error strings for orphan strategy-page fences."""
    errs: list[str] = []
    pos = 0
    while True:
        m = PAGE_MARKER_RE.search(text, pos)
        if not m:
            break
        end_m = PAGE_END_RE.search(text, m.end())
        if not end_m:
            errs.append(
                f"unclosed strategy-page fence starting at offset {m.start()} "
                f"(missing <!-- strategy-page:end -->)"
            )
            break
        pos = end_m.end()
    return errs


def prose_ratio_before_appendix(page_inner: str) -> tuple[float, int, int]:
    """Return (ratio 0–1, prose_words, total_words) for one page inner (between HTML markers)."""
    low = page_inner.lower()
    idx = low.find("### technical appendix")
    prose_part = page_inner[:idx] if idx != -1 else page_inner
    total_w = len(page_inner.split())
    prose_w = len(prose_part.split())
    if total_w == 0:
        return (1.0, 0, 0)
    return (prose_w / total_w, prose_w, total_w)


def validate_notebook(
    notebook_dir: Path,
    *,
    strict_prose: bool,
    warn_prose: bool,
    min_prose_ratio: float,
) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    for expert_id in CANONICAL_EXPERT_IDS:
        for thread_path in expert_thread_paths_for_discovery(notebook_dir, expert_id):
            if not thread_path.is_file():
                continue
            text = thread_path.read_text(encoding="utf-8")
            human = _human_layer(text)
            for msg in find_unclosed_page_markers(human):
                errors.append(f"{thread_path.relative_to(REPO_ROOT)}: {msg}")

            pages = discover_pages(thread_path, expert_id=expert_id)
            for pb in pages:
                ratio, pw, tw = prose_ratio_before_appendix(pb.content)
                if tw > 0 and ratio < min_prose_ratio:
                    msg = (
                        f"{thread_path.relative_to(REPO_ROOT)}: page `{pb.id}` — "
                        f"prose ratio {ratio:.2f} < {min_prose_ratio:.2f} "
                        f"(words before `### Technical appendix` = {pw} / all = {tw})"
                    )
                    if strict_prose:
                        errors.append(msg)
                    elif warn_prose:
                        warnings.append(msg + " (optional)")

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--notebook-dir",
        type=Path,
        default=NOTEBOOK_DIR,
        help="Strategy notebook root",
    )
    ap.add_argument(
        "--strict-prose",
        action="store_true",
        help="Fail if any page is below --min-prose-ratio (default 0.90).",
    )
    ap.add_argument(
        "--warn-prose",
        action="store_true",
        help="Print stderr warnings for low prose-vs-appendix ratio (not default).",
    )
    ap.add_argument(
        "--min-prose-ratio",
        type=float,
        default=0.90,
        help="Minimum share of words before ### Technical appendix (default 0.90).",
    )
    args = ap.parse_args()

    errs = validate_notebook(
        args.notebook_dir.resolve(),
        strict_prose=args.strict_prose,
        warn_prose=args.warn_prose,
        min_prose_ratio=args.min_prose_ratio,
    )
    for e in errs:
        print(f"error: {e}", file=sys.stderr)

    if errs:
        print(
            f"validate_strategy_pages: {len(errs)} error(s)",
            file=sys.stderr,
        )
        return 1

    print(
        f"ok: strategy-page fences validated under {args.notebook_dir.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
