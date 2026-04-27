#!/usr/bin/env python3
"""
Refined page word budget: target ~3000 words per page, ~70–80% verbatim (from transcript).

- **Check** an existing *-page-*.md: total words, `### Verbatim` words, ratio.
- **Condense** lane text from a raw transcript (e.g. from `extract_transcript_speaker_lanes.py`)
  when the lane exceeds the verbatim budget, using head+tail + omission marker (default).

See: docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md

WORK only; not Record.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

# Defaults aligned with refined-page-template.md
DEFAULT_PAGE_TARGET = 3000
DEFAULT_VERBATIM_MIN_RATIO = 0.70
DEFAULT_VERBATIM_MAX_RATIO = 0.80

_VERBATIM = re.compile(
    r"^###\s+Verbatim\s*$(.*?)(?=^###\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)


def count_words(s: str) -> int:
    s = s.strip()
    if not s:
        return 0
    return len(re.findall(r"\S+", s))


def verbatim_budget_words(
    page_target: int = DEFAULT_PAGE_TARGET,
    min_r: float = DEFAULT_VERBATIM_MIN_RATIO,
    max_r: float = DEFAULT_VERBATIM_MAX_RATIO,
) -> tuple[int, int]:
    return (int(page_target * min_r), int(page_target * max_r))


def extract_verbatim_block(page_text: str) -> tuple[str, int, int]:
    """Return verbatim body (no heading), start index, end index, or ('', -1, -1)."""
    m = _VERBATIM.search(page_text)
    if not m:
        return "", -1, -1
    block = m.group(1).strip()
    return block, m.start(1), m.end(1)


def condense_paragraphs(
    text: str,
    max_words: int,
    head_ratio: float = 0.55,
    tail_ratio: float = 0.35,
) -> tuple[str, int]:
    """
    Keep leading and trailing paragraphs by word budget; omit the middle.
    Returns (condensed_markdown, omitted_word_count).
    """
    text = text.strip()
    w_all = count_words(text)
    if w_all <= max_words:
        return text, 0
    parts = re.split(r"\n\s*\n+", text)
    if len(parts) <= 2:
        # long blobs: hard split by words
        toks = text.split()
        n = len(toks)
        hw = int(max_words * head_ratio)
        tw = int(max_words * tail_ratio)
        if hw + tw >= n:
            return " ".join(toks), 0
        head = " ".join(toks[:hw])
        tail = " ".join(toks[n - tw :])
        mid_w = n - hw - tw
        gap = f"\n\n*… {mid_w} words omitted; full continuous text: link under **### Appendix** …*\n\n"
        return f"{head}{gap}{tail}", mid_w
    # paragraph-wise: greedily add from start, then from end
    w_head = 0
    i_hi = 0
    for i, p in enumerate(parts):
        cw = count_words(p)
        if w_head + cw > max_words * head_ratio and i > 0:
            break
        w_head += cw
        i_hi = i + 1
    w_tail = 0
    i_lo = len(parts)
    for j in range(len(parts) - 1, -1, -1):
        cw = count_words(parts[j])
        if w_tail + cw > max_words * tail_ratio and j < len(parts) - 1:
            break
        w_tail += cw
        i_lo = j
    if i_lo <= i_hi:
        i_lo = min(i_hi + 1, len(parts))
    head_parts = parts[:i_hi]
    tail_parts = parts[i_lo:]
    middle = parts[i_hi:i_lo]
    omitted = count_words("\n\n".join(middle))
    head_s = "\n\n".join(head_parts).strip()
    tail_s = "\n\n".join(tail_parts).strip()
    gap = f"\n\n*… {omitted} words omitted (middle of transcript lane); see **Full verbatim (capture):** in **### Appendix** …*\n\n"
    return f"{head_s}{gap}{tail_s}", omitted


def cmd_check(args: argparse.Namespace) -> int:
    path: Path = args.page
    text = path.read_text(encoding="utf-8")
    total = count_words(text)
    vbody, _, _ = extract_verbatim_block(text)
    vw = count_words(vbody) if vbody else 0
    nonv = max(0, total - vw)
    ratio = (vw / total) if total else 0.0
    lo, hi = verbatim_budget_words(
        args.page_target, args.verbatim_min_ratio, args.verbatim_max_ratio
    )
    print(path.as_posix())
    print(f"  total words:     {total}  (target page ~{args.page_target})")
    print(f"  verbatim words: {vw}  (budget {lo}–{hi} for {args.verbatim_min_ratio:.0%}–{args.verbatim_max_ratio:.0%} of {args.page_target})")
    print(f"  verbatim / total: {ratio:.1%}  (target 70%–80%)")
    if total > args.page_target * 1.15:
        print("  ** page over soft target; consider condensing (see --condense) **", file=sys.stderr)
    if (
        total >= args.page_target * 0.5
        and vw > 0
        and not (args.verbatim_min_ratio <= ratio <= args.verbatim_max_ratio + 0.05)
    ):
        print("  ** verbatim share outside 70–80% band (expected when page is short) **", file=sys.stderr)
    return 0


def cmd_condense(args: argparse.Namespace) -> int:
    from extract_transcript_speaker_lanes import extract_lanes  # type: ignore

    raw = Path(args.raw).read_text(encoding="utf-8")
    lanes = extract_lanes(raw)
    if args.lane not in lanes:
        print(f"Lane {args.lane!r} not in {list(lanes)}", file=sys.stderr)
        return 1
    text = lanes[args.lane]
    w = count_words(text)
    lo, hi = verbatim_budget_words(
        args.page_target, args.verbatim_min_ratio, args.verbatim_max_ratio
    )
    # aim middle of band
    target_v = (lo + hi) // 2
    if w <= hi:
        print(text)
        print(
            f"\n<!-- condense: lane {w} words, within verbatim budget {lo}–{hi}; paste as ### Verbatim -->\n",
            file=sys.stderr,
        )
        return 0
    out, omitted = condense_paragraphs(
        text,
        max_words=target_v,
        head_ratio=args.head_ratio,
        tail_ratio=args.tail_ratio,
    )
    print(out)
    print(
        f"\n<!-- condense: {w} words -> ~{count_words(out)} in page; {omitted} words omitted; full: raw file -->\n",
        file=sys.stderr,
    )
    return 0


def _add_budget_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--page-target",
        type=int,
        default=DEFAULT_PAGE_TARGET,
        help=f"Soft target total words (default {DEFAULT_PAGE_TARGET})",
    )
    p.add_argument(
        "--verbatim-min-ratio",
        type=float,
        default=DEFAULT_VERBATIM_MIN_RATIO,
    )
    p.add_argument(
        "--verbatim-max-ratio",
        type=float,
        default=DEFAULT_VERBATIM_MAX_RATIO,
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Refined page word budget (target 3000, 70–80% verbatim)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="Report word counts for a *-page-*.md file")
    c.add_argument("page", type=Path, help="Path to refined page markdown")
    _add_budget_args(c)
    c.set_defaults(func=cmd_check)

    d = sub.add_parser(
        "condense",
        help="Print condense lane text from raw when over verbatim budget (stderr: stats)",
    )
    d.add_argument("raw", type=Path, help="Raw-input transcript .md")
    d.add_argument(
        "--lane", required=True, help="Lane key: glenn, alastair, scott, john (from extract_lanes)"
    )
    d.add_argument("--head-ratio", type=float, default=0.55)
    d.add_argument("--tail-ratio", type=float, default=0.35)
    _add_budget_args(d)
    d.set_defaults(func=cmd_condense)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
