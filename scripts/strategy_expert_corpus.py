#!/usr/bin/env python3
"""Extract raw material for per-expert thread distillation.

Reads from ``strategy-expert-<id>-transcript.md`` (recent verbatim) and
relevant knot files (where expert material was used), writes structured
extraction to ``strategy-expert-<id>-thread.md`` between script markers.

The output is **raw material** for assistant refinement — the assistant
distills it into a curated analytical thread (convergences, tensions,
drift, knot impact).

**Two-step ``thread`` flow:**

1. ``strategy_expert_transcript.py`` triages inbox → transcripts (automatic)
2. This script extracts transcript + knot material → thread files
3. Assistant refines the extraction into curated thread prose

Imported by ``strategy_expert_transcript.py`` for shared constants and
``extract_thread_ingests()``.

WORK-only; not Record.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

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
DEFAULT_KNOT_INDEX = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml"
)

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
    "jacques-baud",
    "brian-berletic",
)

_EXPERT_IDS_SET = frozenset(CANONICAL_EXPERT_IDS)

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
THREAD_MARKER_END = "<!-- strategy-expert-thread:end -->"

# Legacy markers kept for backward compat (extract_thread_ingests)
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
# Dated `## YYYY-MM-DD` scratch subsection (inbox) — same pattern as transcript date headings.
_RE_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")

# Policy: long-form captures per ingest; 7-day prune keeps whole files near this band.
MAX_VERBATIM_WORDS_PER_INGEST = 2000
SOFT_MAX_TRANSCRIPT_FILE_WORDS = 20000


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


def _word_count(s: str) -> int:
    return len(s.split())


def _top_level_list_item(line: str) -> bool:
    """True if this line starts a new top-level `- ` list item (column 0 only)."""
    return line.startswith("- ")


def verbatim_to_transcript_lines(verbatim: str) -> list[str]:
    """Turn one ingest block (possibly multi-line) into markdown lines for `-transcript.md`."""
    parts = verbatim.splitlines()
    if not parts:
        return []
    out: list[str] = []
    first = parts[0].rstrip()
    if first.lstrip().startswith("- "):
        out.append(first)
    else:
        out.append(f"- {first}")
    for pl in parts[1:]:
        out.append(f"    {pl.rstrip()}")
    return out


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


# ---------------------------------------------------------------------------
# Inbox extraction — kept for strategy_expert_transcript.py import
# ---------------------------------------------------------------------------

def _continuation_stops_thread_block(line: str) -> bool:
    """True if this line ends a multi-line verbatim block opened by a thread ingest."""
    if not line.strip():
        return False
    if line.startswith("## "):
        return True
    if _date_markers(line):
        return True
    if _top_level_list_item(line):
        return True
    return False


def extract_thread_ingests(
    text: str,
    *,
    today: date | None = None,
) -> dict[str, dict[date, list[str]]]:
    """Return nested dict expert_id -> date -> list of verbatim blocks (strings, possibly multi-line).

    Each block is the first ingest line (with ``thread:``) plus continuation lines until
    a new top-level ``- `` list item (column 0), a ``## `` heading, a scratch ``## YYYY-MM-DD``,
    a brief-handoff / fold date marker line, or end of file. Blank lines **inside** the block
    are kept (multi-paragraph quotes).
    """
    today = today or datetime.now(timezone.utc).date()
    accum: str | None = None
    m = _RE_ACCUM.search(text)
    if m:
        accum = m.group(1)

    context_date: date | None = None
    if accum:
        context_date = _parse_date_yyyy_mm_dd(accum)

    out: dict[str, dict[date, list[str]]] = defaultdict(lambda: defaultdict(list))
    lines = text.splitlines()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        dm = _date_markers(line)
        if dm:
            context_date = _parse_date_yyyy_mm_dd(dm)
            i += 1
            continue

        mh = _RE_DATE_HEADING.match(line.strip())
        if mh:
            context_date = _parse_date_yyyy_mm_dd(mh.group(1))
            i += 1
            continue

        if not _is_ingest_line(line) or "thread:" not in line:
            i += 1
            continue

        slugs = [s for s in _RE_THREAD.findall(line) if s in _EXPERT_IDS_SET]
        if not slugs:
            i += 1
            continue

        use_date = context_date
        if use_date is None and accum:
            use_date = _parse_date_yyyy_mm_dd(accum)
        if use_date is None:
            i += 1
            continue

        block_lines = [line.rstrip()]
        j = i + 1
        while j < n:
            nxt = lines[j]
            if not nxt.strip():
                block_lines.append("")
                j += 1
                continue
            if _continuation_stops_thread_block(nxt):
                break
            block_lines.append(nxt.rstrip())
            j += 1

        verbatim = "\n".join(block_lines).rstrip()
        for slug in slugs:
            if verbatim not in out[slug][use_date]:
                out[slug][use_date].append(verbatim)
        i = j

    return {k: dict(v) for k, v in out.items()}


# ---------------------------------------------------------------------------
# Transcript reading
# ---------------------------------------------------------------------------

def read_transcript_content(transcript_path: Path) -> list[str]:
    """Read all content lines from a transcript file (below the triage marker)."""
    if not transcript_path.is_file():
        return []
    text = transcript_path.read_text(encoding="utf-8")
    marker = "<!-- Triage appends new date sections below. Do not add content above this line. -->"
    idx = text.find(marker)
    if idx != -1:
        body = text[idx + len(marker):]
    else:
        body = text
    return [ln for ln in body.strip().splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
# Knot scanning
# ---------------------------------------------------------------------------

def find_knot_references(
    expert_id: str,
    *,
    knot_index_path: Path,
) -> list[dict]:
    """Find knots that reference this expert (via clusters or file content)."""
    if not knot_index_path.is_file():
        return []

    try:
        data = yaml.safe_load(knot_index_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    if not data or "knots" not in data:
        return []

    refs: list[dict] = []
    for knot in data["knots"]:
        clusters = knot.get("clusters", []) or []
        if expert_id in clusters:
            refs.append(knot)
            continue
        knot_path = REPO_ROOT / knot.get("path", "")
        if knot_path.is_file():
            content = knot_path.read_text(encoding="utf-8")
            if f"thread:{expert_id}" in content or f"`{expert_id}`" in content:
                refs.append(knot)

    return refs


# ---------------------------------------------------------------------------
# Thread extraction (writes raw material to -thread.md)
# ---------------------------------------------------------------------------

def render_thread_extraction(
    expert_id: str,
    *,
    transcript_lines: list[str],
    knot_refs: list[dict],
) -> str:
    """Render machine-layer content between -thread.md markers (overwrite each run).

    Human narrative belongs *above* THREAD_MARKER_START in the file; see
    STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread (two layers).
    """
    parts: list[str] = []
    parts.append("## Machine layer — Extraction (script-maintained)\n")
    parts.append(
        "_Auto-generated from `-transcript.md` + knot index. "
        "**Journal layer** (narrative) lives **above** the **strategy-expert-thread** "
        "start HTML comment. The machine-layer HTML block is replaced on each `thread` run._\n"
    )

    if transcript_lines:
        parts.append("### Recent transcript material\n")
        for line in transcript_lines:
            parts.append(line)
        parts.append("")

    if knot_refs:
        parts.append("### Knot references\n")
        for knot in knot_refs:
            knot_path = knot.get("path", "?")
            knot_date = knot.get("date", "?")
            knot_label = knot.get("knot_label", "")
            note = knot.get("note", "")
            label_str = f" ({knot_label})" if knot_label else ""
            note_str = f" — {note}" if note else ""
            basename = Path(knot_path).name
            parts.append(f"- [{basename}]({basename}) {knot_date}{label_str}{note_str}")
        parts.append("")

    if not transcript_lines and not knot_refs:
        parts.append("_(No transcript or knot material for extraction.)_\n")

    return "\n".join(parts).rstrip() + "\n"


def write_thread_file(
    dest: Path,
    inner: str,
) -> None:
    """Write extraction content between thread markers in a -thread.md file."""
    if not dest.exists():
        dest.write_text(
            THREAD_MARKER_START + "\n" + inner.rstrip() + "\n" + THREAD_MARKER_END + "\n",
            encoding="utf-8",
        )
        return

    text = dest.read_text(encoding="utf-8")
    if THREAD_MARKER_START in text and THREAD_MARKER_END in text:
        before, _, rest = text.partition(THREAD_MARKER_START)
        _, _, after = rest.partition(THREAD_MARKER_END)
        new_text = (
            before.rstrip()
            + "\n"
            + THREAD_MARKER_START
            + "\n"
            + inner.rstrip()
            + "\n"
            + THREAD_MARKER_END
            + "\n"
            + after.lstrip()
        )
        dest.write_text(new_text, encoding="utf-8")
        return

    dest.write_text(
        text.rstrip() + "\n\n"
        + THREAD_MARKER_START + "\n" + inner.rstrip() + "\n" + THREAD_MARKER_END + "\n",
        encoding="utf-8",
    )


def rebuild_threads(
    *,
    out_dir: Path,
    knot_index_path: Path,
    dry_run: bool = False,
) -> list[Path]:
    """Extract transcript + knot material → thread files for all experts."""
    written: list[Path] = []

    for expert_id in CANONICAL_EXPERT_IDS:
        transcript_path = out_dir / f"strategy-expert-{expert_id}-transcript.md"
        thread_path = out_dir / f"strategy-expert-{expert_id}-thread.md"

        transcript_lines = read_transcript_content(transcript_path)
        knot_refs = find_knot_references(expert_id, knot_index_path=knot_index_path)

        inner = render_thread_extraction(
            expert_id,
            transcript_lines=transcript_lines,
            knot_refs=knot_refs,
        )

        if not dry_run:
            write_thread_file(thread_path, inner)

        written.append(thread_path)

    return written


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Directory containing expert files",
    )
    p.add_argument(
        "--knot-index",
        type=Path,
        default=DEFAULT_KNOT_INDEX,
        help="Path to knot-index.yaml",
    )
    p.add_argument("--dry-run", action="store_true", help="Parse only; do not write files")
    args = p.parse_args()

    paths = rebuild_threads(
        out_dir=args.out,
        knot_index_path=args.knot_index,
        dry_run=args.dry_run,
    )
    for path in paths:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
