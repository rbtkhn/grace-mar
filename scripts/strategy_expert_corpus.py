#!/usr/bin/env python3
"""Rebuild per-expert rolling ingest blocks from daily-strategy-inbox.md.

Each indexed expert gets ``strategy-expert-<expert_id>.md`` under
``docs/skill-work/work-strategy/strategy-notebook/``. Verbatim inbox lines that
carry ``thread:<expert_id>`` are grouped by calendar date inside a
script-delimited block; the **Seed** section above the markers is preserved on
rebuild. Only the last ``--days`` calendar days are kept inside the block.

**Operator entry:** run ``python3 scripts/strategy_thread.py`` (same flags) —
canonical name for this rebuild is **``thread``** in notebook docs.

WORK-only; not Record.

See ``docs/skill-work/work-strategy/strategy-notebook/README.md`` (expert files).
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_THREADS = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md"
)
DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)

# Sync with strategy-commentator-threads.md expert_id column (table order).
CANONICAL_EXPERT_IDS: tuple[str, ...] = (
    "seyed-marandi",
    "scott-ritter",
    "trita-parsi",
    "robert-barnes",
    "douglas-macgregor",
    "robert-pape",
    "daniel-davis",
    "steve-jermy",
    "john-mearsheimer",
    "alexander-mercouris",
    "max-blumenthal",
    "aaron-mate",
    "larry-johnson",
    "charles-freeman",
    "alastair-crooke",
    "glenn-diesen",
    "jeffrey-sachs",
    "jiang-xueqin",
    "martin-armstrong",
)

_EXPERT_IDS_SET = frozenset(CANONICAL_EXPERT_IDS)

CORPUS_MARKER_START = "<!-- strategy-expert-corpus:start -->"
CORPUS_MARKER_END = "<!-- strategy-expert-corpus:end -->"

_RE_ACCUM = re.compile(r"\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})")
_RE_BUNDLE = re.compile(r"<!--\s*brief-handoff-bundle:\s*(\d{4}-\d{2}-\d{2})")
_RE_PRIOR = re.compile(r"\*\*Prior scratch —\s*(\d{4}-\d{2}-\d{2})")
_RE_FOLDED = re.compile(r"\*\*Folded\s*\((\d{4}-\d{2}-\d{2})\)")
_RE_PREP = re.compile(r"### Prep —\s*(\d{4}-\d{2}-\d{2})")
_RE_RETAINED = re.compile(
    r"### Retained reference \((\d{4}-\d{2}-\d{2})(?:\s+fold)?\)"
)
_RE_THREAD = re.compile(r"thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)")


@dataclass(frozen=True)
class CommentatorRow:
    expert_id: str
    anchor: str
    role: str
    grep_tag: str
    pairings: str


@dataclass(frozen=True)
class MetricsRow:
    expert_id: str
    sci: str
    ad: str
    ctc: str
    note: str


def _parse_date_yyyy_mm_dd(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _date_markers(line: str) -> str | None:
    for rx in (
        _RE_BUNDLE,
        _RE_PRIOR,
        _RE_FOLDED,
        _RE_PREP,
        _RE_RETAINED,
    ):
        m = rx.search(line)
        if m:
            return m.group(1)
    return None


def _is_ingest_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s.startswith("- "):
        return True
    if s.startswith("`") and "|" in s:
        return True
    return False


def _split_table_row(line: str) -> list[str]:
    if not line.startswith("|"):
        return []
    parts = line.split("|")
    return [p.strip() for p in parts[1:-1]]


def parse_commentator_index(threads_path: Path) -> tuple[list[str], dict[str, CommentatorRow], dict[str, MetricsRow]]:
    """Parse main commentator table + quantitative metrics from threads index."""
    text = threads_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    main_header = "| expert_id | Anchor | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |"
    metrics_header = (
        "| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |"
    )

    main_rows: dict[str, CommentatorRow] = {}
    order: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == main_header:
            i += 2
            while i < len(lines):
                line = lines[i]
                if line.strip().startswith("###"):
                    break
                cells = _split_table_row(line)
                if len(cells) >= 5 and cells[0].startswith("`") and cells[0].endswith("`"):
                    slug = cells[0].strip("`").strip()
                    if slug in _EXPERT_IDS_SET:
                        main_rows[slug] = CommentatorRow(
                            expert_id=slug,
                            anchor=cells[1],
                            role=cells[2],
                            grep_tag=cells[3],
                            pairings=cells[4],
                        )
                        order.append(slug)
                i += 1
            break
        i += 1

    metrics_rows: dict[str, MetricsRow] = {}
    i = 0
    while i < len(lines):
        if lines[i].strip() == metrics_header:
            i += 2
            while i < len(lines):
                line = lines[i]
                if line.strip() == "---":
                    break
                cells = _split_table_row(line)
                if len(cells) >= 5 and cells[0].startswith("`") and cells[0].endswith("`"):
                    slug = cells[0].strip("`").strip()
                    if slug in _EXPERT_IDS_SET:
                        metrics_rows[slug] = MetricsRow(
                            expert_id=slug,
                            sci=cells[1],
                            ad=cells[2],
                            ctc=cells[3],
                            note=cells[4],
                        )
                i += 1
            break
        i += 1

    return order, main_rows, metrics_rows


def verify_index_alignment(
    order: list[str],
    *,
    main_rows: dict[str, CommentatorRow],
) -> None:
    parsed_set = frozenset(order)
    expected = frozenset(CANONICAL_EXPERT_IDS)
    if parsed_set != expected:
        missing = sorted(expected - parsed_set)
        extra = sorted(parsed_set - expected)
        raise SystemExit(
            "strategy-commentator-threads.md table does not match CANONICAL_EXPERT_IDS: "
            f"missing={missing!r} extra={extra!r}"
        )
    if set(main_rows.keys()) != expected:
        raise SystemExit(
            "Parsed commentator rows do not cover all CANONICAL_EXPERT_IDS — "
            f"got {sorted(main_rows.keys())!r}"
        )
    if tuple(order) != CANONICAL_EXPERT_IDS:
        raise SystemExit(
            "Commentator table row order differs from CANONICAL_EXPERT_IDS tuple — "
            f"parsed order: {order!r}"
        )


def build_seed_preamble(
    expert_id: str,
    *,
    main_rows: dict[str, CommentatorRow],
    metrics_rows: dict[str, MetricsRow],
) -> str:
    row = main_rows[expert_id]
    mrow = metrics_rows.get(expert_id)
    lines: list[str] = [
        f"# Strategy expert — `{expert_id}`",
        "",
        "**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) — **`"
        + expert_id
        + "`** lane.",
        "",
        "## Seed (index mirror — operator may extend)",
        "",
        "The block below **Rolling ingest** is replaced on each `strategy_thread.py` / `strategy_expert_corpus.py` run; "
        "edit this **Seed** section freely.",
        "",
        "### Commentator row (from index)",
        "",
        "| expert_id | Anchor | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |",
        "|-----------|--------|-----------------|------------------|-----------------------------------|",
        "| `{0}` | {1} | {2} | {3} | {4} |".format(
            row.expert_id,
            row.anchor,
            row.role,
            row.grep_tag,
            row.pairings,
        ),
        "",
    ]
    if mrow:
        lines += [
            "### Quantitative metrics (illustrative — from index)",
            "",
            "| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |",
            "|-----------|-----|----|-----|--------------------------------------------------|",
            "| `{0}` | {1} | {2} | {3} | {4} |".format(
                mrow.expert_id,
                mrow.sci,
                mrow.ad,
                mrow.ctc,
                mrow.note,
            ),
            "",
        ]

    lines += [
        "## Rolling ingest",
        "",
        "**Source:** Verbatim lines from [`daily-strategy-inbox.md`](daily-strategy-inbox.md) "
        f"that include `thread:{expert_id}`.",
        "**Retention:** Rolling window (see script `--days`); older `## YYYY-MM-DD` sections "
        "inside the generated block are omitted on rebuild.",
        "**Not Record.**",
        "",
        CORPUS_MARKER_START,
    ]
    return "\n".join(lines)


def extract_thread_ingests(
    text: str,
    *,
    today: date | None = None,
) -> dict[str, dict[date, list[str]]]:
    """Return nested dict expert_id -> date -> list of verbatim lines."""
    today = today or datetime.now(timezone.utc).date()
    accum: str | None = None
    m = _RE_ACCUM.search(text)
    if m:
        accum = m.group(1)

    context_date: date | None = None
    if accum:
        context_date = _parse_date_yyyy_mm_dd(accum)

    out: dict[str, dict[date, list[str]]] = defaultdict(lambda: defaultdict(list))

    for line in text.splitlines():
        dm = _date_markers(line)
        if dm:
            context_date = _parse_date_yyyy_mm_dd(dm)
            continue

        if not _is_ingest_line(line) or "thread:" not in line:
            continue

        slugs = [s for s in _RE_THREAD.findall(line) if s in _EXPERT_IDS_SET]
        if not slugs:
            continue

        use_date = context_date
        if use_date is None and accum:
            use_date = _parse_date_yyyy_mm_dd(accum)
        if use_date is None:
            continue

        verbatim = line.rstrip()
        for slug in slugs:
            if verbatim not in out[slug][use_date]:
                out[slug][use_date].append(verbatim)

    return {k: dict(v) for k, v in out.items()}


def render_corpus_inner(
    expert_id: str,
    by_date: dict[date, list[str]],
    *,
    keep_days: int,
    today: date,
) -> str:
    """Content placed between corpus markers (no markers)."""
    cutoff = today - timedelta(days=keep_days - 1)
    lines: list[str] = []

    dates_sorted = sorted(
        (d for d in by_date if d >= cutoff and d <= today),
        reverse=True,
    )
    if not dates_sorted:
        lines.append("_(No `thread:` ingests in the current rolling window.)_")
        lines.append("")
        return "\n".join(lines)

    for d in dates_sorted:
        lines.append(f"## {d.isoformat()}")
        for vl in by_date[d]:
            if vl.lstrip().startswith("- "):
                lines.append(vl)
            else:
                lines.append(f"- {vl}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_strategy_expert_file(
    dest: Path,
    expert_id: str,
    inner: str,
    *,
    main_rows: dict[str, CommentatorRow],
    metrics_rows: dict[str, MetricsRow],
) -> None:
    if not dest.exists():
        preamble = build_seed_preamble(
            expert_id,
            main_rows=main_rows,
            metrics_rows=metrics_rows,
        )
        dest.write_text(preamble + "\n" + inner.rstrip() + "\n" + CORPUS_MARKER_END + "\n", encoding="utf-8")
        return

    text = dest.read_text(encoding="utf-8")
    if CORPUS_MARKER_START in text and CORPUS_MARKER_END in text:
        before, _, rest = text.partition(CORPUS_MARKER_START)
        _, _, after = rest.partition(CORPUS_MARKER_END)
        new_text = (
            before.rstrip()
            + "\n"
            + CORPUS_MARKER_START
            + "\n"
            + inner.rstrip()
            + "\n"
            + CORPUS_MARKER_END
            + "\n"
            + after.lstrip()
        )
        dest.write_text(new_text, encoding="utf-8")
        return

    # Existing file without corpus markers: replace with fresh index seed + corpus.
    preamble = build_seed_preamble(
        expert_id,
        main_rows=main_rows,
        metrics_rows=metrics_rows,
    )
    dest.write_text(preamble + "\n" + inner.rstrip() + "\n" + CORPUS_MARKER_END + "\n", encoding="utf-8")


def rebuild_corpus(
    *,
    inbox_path: Path,
    threads_path: Path,
    out_dir: Path,
    keep_days: int,
    today: date | None = None,
    dry_run: bool = False,
) -> list[Path]:
    today = today or datetime.now(timezone.utc).date()
    order, main_rows, metrics_rows = parse_commentator_index(threads_path)
    verify_index_alignment(order, main_rows=main_rows)

    text = inbox_path.read_text(encoding="utf-8")
    extracted = extract_thread_ingests(text, today=today)

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for expert_id in CANONICAL_EXPERT_IDS:
        by_date = extracted.get(expert_id, {})
        inner = render_corpus_inner(
            expert_id,
            by_date,
            keep_days=keep_days,
            today=today,
        )
        dest = out_dir / f"strategy-expert-{expert_id}.md"
        if not dry_run:
            write_strategy_expert_file(
                dest,
                expert_id,
                inner,
                main_rows=main_rows,
                metrics_rows=metrics_rows,
            )
        written.append(dest)

    return written


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--inbox",
        type=Path,
        default=DEFAULT_INBOX,
        help="Path to daily-strategy-inbox.md",
    )
    p.add_argument(
        "--threads",
        type=Path,
        default=DEFAULT_THREADS,
        help="Path to strategy-commentator-threads.md (for seed tables)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for strategy-expert-<id>.md files",
    )
    p.add_argument("--days", type=int, default=7, help="Rolling window length (default 7)")
    p.add_argument(
        "--today",
        help="Override today's date (YYYY-MM-DD) for testing",
    )
    p.add_argument("--dry-run", action="store_true", help="Parse only; do not write files")
    args = p.parse_args()

    today = _parse_date_yyyy_mm_dd(args.today) if args.today else None
    paths = rebuild_corpus(
        inbox_path=args.inbox,
        threads_path=args.threads,
        out_dir=args.out,
        keep_days=max(1, args.days),
        today=today,
        dry_run=args.dry_run,
    )
    for path in paths:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
