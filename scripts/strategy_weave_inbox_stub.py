#!/usr/bin/env python3
"""Print a grep-friendly weave registry block for daily-strategy-inbox.md.

Emits the same shape as the optional **Weave registry — YYYY-MM-DD (grep anchor)**
section: a ``notebook-weave`` one-liner and a ``batch-analysis`` line. Operator
fills cold/batch prose or passes flags. WORK only; not Record.

Example::

    python3 scripts/strategy_weave_inbox_stub.py \\
      --date 2026-04-14 \\
      --page-id armstrong-cash-hormuz-digital-dollar-arc \\
      --cold 'Martin Armstrong (@ArmstrongEcon) X — …' \\
      --batch-theme 'Armstrong cash × Gulf fertilizer × U.S. digital-dollar law' \\
      --batch-body '**Tension-first:** …'

Pipe or paste below **Accumulator for:** in daily-strategy-inbox.md.
"""

from __future__ import annotations

import argparse
import sys


def _build_basename(date: str, page_id: str) -> str:
    return f"strategy-notebook-knot-{date}-{page_id}.md"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", required=True, help="Calendar day YYYY-MM-DD")
    ap.add_argument(
        "--page-id",
        "--knot-label",
        required=True,
        dest="page_id",
        metavar="ID",
        help="Page id / basename slug (kebab-case; legacy index filename on disk is unchanged).",
    )
    ap.add_argument(
        "--cold",
        default="",
        help="Cold clause (source facts; before // hook). Empty = placeholder.",
    )
    ap.add_argument(
        "--hook",
        default="",
        help="Hook clause after //. Empty = auto from basename and --weave-tag.",
    )
    ap.add_argument(
        "--weave-tag",
        default="",
        help='Optional tag shown as "(weave TAG)" in auto hook, e.g. D',
    )
    ap.add_argument(
        "--minds",
        default="Barnes, Mercouris, Mearsheimer",
        help="Comma-separated mind names for default hook tail",
    )
    ap.add_argument(
        "--batch-theme",
        default="",
        help="Short theme between pipes in batch-analysis (empty = placeholder).",
    )
    ap.add_argument(
        "--batch-body",
        default="",
        help="Body after batch-theme (Tension-first prose). Empty = placeholder.",
    )
    ap.add_argument(
        "--no-section-header",
        action="store_true",
        help="Omit ### Weave registry header (lines only).",
    )
    args = ap.parse_args()

    date = args.date.strip()
    page_id = args.page_id.strip()
    if not date or len(date) != 10:
        print("error: --date must be YYYY-MM-DD", file=sys.stderr)
        return 1
    if not page_id:
        print("error: --page-id required", file=sys.stderr)
        return 1

    basename = _build_basename(date, page_id)
    cold = args.cold.strip()
    if not cold:
        cold = "(operator: paste cold — who / what / URL)"

    if args.hook.strip():
        hook = args.hook.strip()
    else:
        weave_part = f" (weave {args.weave_tag.strip()})" if args.weave_tag.strip() else ""
        hook = (
            f"landed page basename {basename}{weave_part}; "
            f"lenses from CIV-MIND {args.minds} — not a thread: expert row"
        )

    verify_tail = (
        "verify:basename-on-disk | membrane:single | "
        f"grep:{page_id}"
    )
    weave_line = (
        f"`notebook-weave | cold: {cold} // hook: {hook} | {verify_tail}`"
    )

    theme = args.batch_theme.strip() or "(operator: short batch theme)"
    body = args.batch_body.strip() or (
        "(operator: **Tension-first:** … **Orthogonal** … **Weak bridge:** …)"
    )
    batch_line = f"`batch-analysis | {date} | {theme} | {body}`"

    out_lines: list[str] = []
    if not args.no_section_header:
        out_lines.append(f"### Weave registry — {date} (grep anchor)")
        out_lines.append("")
    out_lines.append(weave_line)
    out_lines.append("")
    out_lines.append(batch_line)
    print("\n".join(out_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
