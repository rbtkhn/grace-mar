#!/usr/bin/env python3
"""Rebuild per-expert rolling ingest corpus files from daily-strategy-inbox.md.

Each indexed expert gets a markdown file under strategy-notebook/expert-ingest-corpus/
containing verbatim strategy inbox lines that carry ``thread:<expert_id>``, grouped by
calendar date. Only the last ``--days`` calendar days are kept (older ## sections are
not written). WORK-only; not Record.

See docs/skill-work/work-strategy/strategy-notebook/expert-ingest-corpus/README.md
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Sync with strategy-commentator-threads.md expert_id column.
CANONICAL_EXPERT_IDS: tuple[str, ...] = (
    "seyed-marandi",
    "scott-ritter",
    "trita-parsi",
    "robert-barnes",
    "douglas-macgregor",
    "robert-pape",
    "daniel-davis",
    "john-mearsheimer",
    "alexander-mercouris",
    "larry-johnson",
    "charles-freeman",
    "alastair-crooke",
    "glenn-diesen",
)

_EXPERT_IDS_SET = frozenset(CANONICAL_EXPERT_IDS)

_RE_ACCUM = re.compile(r"\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})")
_RE_BUNDLE = re.compile(r"<!--\s*brief-handoff-bundle:\s*(\d{4}-\d{2}-\d{2})")
_RE_PRIOR = re.compile(r"\*\*Prior scratch —\s*(\d{4}-\d{2}-\d{2})")
_RE_FOLDED = re.compile(r"\*\*Folded\s*\((\d{4}-\d{2}-\d{2})\)")
_RE_PREP = re.compile(r"### Prep —\s*(\d{4}-\d{2}-\d{2})")
_RE_RETAINED = re.compile(
    r"### Retained reference \((\d{4}-\d{2}-\d{2})(?:\s+fold)?\)"
)
_RE_THREAD = re.compile(r"thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)")


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


def render_expert_file(
    expert_id: str,
    by_date: dict[date, list[str]],
    *,
    keep_days: int,
    today: date,
    anchor_name: str | None = None,
) -> str:
    """Render one expert markdown file; only dates within the rolling window."""
    cutoff = today - timedelta(days=keep_days - 1)
    lines: list[str] = [
        f"# Expert ingest corpus — `{expert_id}`",
        "",
        f"**Anchor:** {anchor_name or '(see strategy-commentator-threads.md)'}  ",
        "**Source:** Verbatim lines from [`daily-strategy-inbox.md`](../daily-strategy-inbox.md) that include `thread:{0}`.".format(
            expert_id
        ),
        "**Retention:** Rolling **{0}** calendar days (older daily sections are omitted on rebuild).".format(
            keep_days
        ),
        "**Not Record.** Rebuilt by `scripts/strategy_expert_corpus.py` — not a merge surface.",
        "",
        "<!-- generated: do not hand-edit; script overwrites -->",
        "",
    ]

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


def rebuild_corpus(
    *,
    inbox_path: Path,
    out_dir: Path,
    keep_days: int,
    today: date | None = None,
    dry_run: bool = False,
) -> list[Path]:
    today = today or datetime.now(timezone.utc).date()
    text = inbox_path.read_text(encoding="utf-8")
    extracted = extract_thread_ingests(text, today=today)

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for expert_id in CANONICAL_EXPERT_IDS:
        by_date = extracted.get(expert_id, {})
        body = render_expert_file(
            expert_id,
            by_date,
            keep_days=keep_days,
            today=today,
        )
        dest = out_dir / f"{expert_id}.md"
        if not dry_run:
            dest.write_text(body, encoding="utf-8")
        written.append(dest)

    return written


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--inbox",
        type=Path,
        default=REPO_ROOT
        / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md",
        help="Path to daily-strategy-inbox.md",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT
        / "docs/skill-work/work-strategy/strategy-notebook/expert-ingest-corpus",
        help="Output directory for per-expert .md files",
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
