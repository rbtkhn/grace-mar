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

from strategy_page_reader import discover_pages

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
    "armstrong",
    "baud",
    "barnes",
    "berletic",
    "bigserge",
    "blumenthal",
    "crooke",
    "davis",
    "diesen",
    "freeman",
    "greenwald",
    "jermy",
    "jiang",
    "johnson",
    "macgregor",
    "marandi",
    "mate",
    "mearsheimer",
    "mercouris",
    "pape",
    "parsi",
    "ritter",
    "sachs",
    "simplicius",
)

_EXPERT_IDS_SET = frozenset(CANONICAL_EXPERT_IDS)

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
THREAD_MARKER_END = "<!-- strategy-expert-thread:end -->"

# Monthly thread chapters: ``experts/<id>/<id>-thread-YYYY-MM.md`` (and optional flat
# ``strategy-expert-<id>-thread-YYYY-MM.md``). Journal: that month only; optional ``## YYYY-MM``
# heading matching the filename for validators / grep.
RE_IN_FOLDER_MONTH_THREAD = re.compile(r"^(.+)-thread-(\d{4}-\d{2})\.md$")
RE_FLAT_MONTH_THREAD = re.compile(r"^strategy-expert-(.+)-thread-(\d{4}-\d{2})\.md$")
RE_TRANSCRIPT_DATE_SECTION = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")


def expert_paths(expert_id: str, notebook_dir: Path) -> dict[str, Path]:
    """Resolve per-expert file paths under ``experts/<id>/``."""
    base = notebook_dir / "experts" / expert_id
    return {
        "profile": base / "profile.md",
        "transcript": base / "transcript.md",
        "thread": base / "thread.md",
        "mind": base / "mind.md",
    }


def expert_id_from_thread_path(path: Path) -> str | None:
    """Resolve ``expert_id`` from a thread file path (folder, flat, or monthly)."""
    if path.name == "thread.md" and path.parent.parent.name in ("experts", "voices"):
        return path.parent.name
    m = re.match(r"^strategy-expert-(.+)-thread\.md$", path.name)
    if m:
        return m.group(1)
    m = RE_FLAT_MONTH_THREAD.match(path.name)
    if m:
        return m.group(1)
    m = RE_IN_FOLDER_MONTH_THREAD.match(path.name)
    if m and path.parent.name == m.group(1):
        return m.group(1)
    return None


def month_thread_paths_by_month(notebook_dir: Path, expert_id: str) -> dict[str, Path]:
    """Map ``YYYY-MM`` → thread path; prefer ``experts/<id>/`` over flat root."""
    by_m: dict[str, Path] = {}
    expert_dir = notebook_dir / "experts" / expert_id
    if expert_dir.is_dir():
        for p in expert_dir.glob(f"{expert_id}-thread-*.md"):
            m = RE_IN_FOLDER_MONTH_THREAD.match(p.name)
            if m and m.group(1) == expert_id:
                by_m[m.group(2)] = p
    for p in notebook_dir.glob(f"strategy-expert-{expert_id}-thread-*.md"):
        m = RE_FLAT_MONTH_THREAD.match(p.name)
        if m:
            ym = m.group(2)
            if ym not in by_m:
                by_m[ym] = p
    return {k: by_m[k] for k in sorted(by_m.keys())}


def uses_monthly_thread_layout(notebook_dir: Path, expert_id: str) -> bool:
    return bool(month_thread_paths_by_month(notebook_dir, expert_id))


def expert_thread_paths_for_discovery(notebook_dir: Path, expert_id: str) -> list[Path]:
    """Ordered thread paths for page discovery / validation (monthly or legacy)."""
    mmap = month_thread_paths_by_month(notebook_dir, expert_id)
    if mmap:
        return [mmap[k] for k in sorted(mmap.keys())]
    legacy = notebook_dir / "experts" / expert_id / "thread.md"
    if legacy.is_file():
        return [legacy]
    flat = notebook_dir / f"strategy-expert-{expert_id}-thread.md"
    if flat.is_file():
        return [flat]
    return [legacy]


def collect_strategy_thread_paths(notebook_dir: Path) -> list[Path]:
    """All thread files: legacy, monthly in-folder, monthly flat (for validate / sync)."""
    out: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        resolved = p.resolve()
        if resolved not in seen:
            seen.add(resolved)
            out.append(p)

    for p in sorted(notebook_dir.glob("experts/*/thread.md")):
        add(p)
    for p in sorted(notebook_dir.glob("voices/*/thread.md")):
        add(p)
    for d in sorted(notebook_dir.glob("experts/*")):
        if d.is_dir():
            eid = d.name
            for p in sorted(d.glob(f"{eid}-thread-*.md")):
                if RE_IN_FOLDER_MONTH_THREAD.match(p.name):
                    add(p)
    for d in sorted(notebook_dir.glob("voices/*")):
        if d.is_dir():
            eid = d.name
            for p in sorted(d.glob(f"{eid}-thread-*.md")):
                if RE_IN_FOLDER_MONTH_THREAD.match(p.name):
                    add(p)
    for p in sorted(notebook_dir.glob("strategy-expert-*-thread.md")):
        add(p)
    for p in sorted(notebook_dir.glob("strategy-expert-*-thread-*.md")):
        if RE_FLAT_MONTH_THREAD.match(p.name):
            add(p)
    return out


def thread_path_for_page_month(notebook_dir: Path, expert_id: str, page_month_yyyy_mm: str) -> Path:
    """Target thread file for a ``strategy-page`` dated in ``page_month_yyyy_mm``."""
    mmap = month_thread_paths_by_month(notebook_dir, expert_id)
    if mmap:
        if page_month_yyyy_mm in mmap:
            return mmap[page_month_yyyy_mm]
        return notebook_dir / "experts" / expert_id / (
            f"{expert_id}-thread-{page_month_yyyy_mm}.md"
        )
    return expert_paths(expert_id, notebook_dir)["thread"]


def transcript_body_lines(transcript_path: Path) -> list[str]:
    """Lines below the transcript triage marker (including blanks)."""
    if not transcript_path.is_file():
        return []
    text = transcript_path.read_text(encoding="utf-8")
    marker = "<!-- Triage appends new date sections below. Do not add content above this line. -->"
    idx = text.find(marker)
    body = text[idx + len(marker):] if idx != -1 else text
    return body.splitlines()


def parse_transcript_by_month(transcript_path: Path) -> dict[str, list[str]]:
    """Group transcript lines under ``## YYYY-MM-DD`` by calendar month ``YYYY-MM``."""
    by_month: dict[str, list[str]] = defaultdict(list)
    current_month: str | None = None
    for line in transcript_body_lines(transcript_path):
        m = RE_TRANSCRIPT_DATE_SECTION.match(line.strip())
        if m:
            day = m.group(1)
            current_month = day[:7]
            by_month[current_month].append(line.rstrip())
            continue
        if current_month is None:
            continue
        if line.strip():
            by_month[current_month].append(line.rstrip())
    return dict(by_month)


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
# Verify-tail expert tag (see daily-strategy-inbox.md): ``| thread:<id> |`` — not hook prose ``**`thread:davis`**``.
_RE_THREAD_PIPE = re.compile(
    r"\|\s*thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)\s*\|"
)
_RE_PUBLISHED = re.compile(r"published:(\d{4}-\d{2}-\d{2})")
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


def ingest_thread_slugs(line: str) -> list[str]:
    """Resolve expert ids for an inbox ingest line.

    Prefer pipe-delimited verify-tail tags (``| thread:id |``) so hook prose like
    ``**`thread:davis`**`` does not route the row to the wrong transcript.
    Fallback: ``| thread:id`` at end of line, then legacy ``thread:`` scan.
    """
    pipe_hits = [
        m.group(1)
        for m in _RE_THREAD_PIPE.finditer(line)
        if m.group(1) in _EXPERT_IDS_SET
    ]
    if pipe_hits:
        return [pipe_hits[-1]]
    m_end = re.search(
        r"\|\s*thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)\s*$",
        line.rstrip(),
    )
    if m_end and m_end.group(1) in _EXPERT_IDS_SET:
        return [m_end.group(1)]
    # Backtick synthetic rows (e.g. ``batch-analysis``) often contain ``thread:`` in prose;
    # do not fall back to naive findall — avoids false routes.
    if line.lstrip().startswith("`"):
        return []
    return [s for s in _RE_THREAD.findall(line) if s in _EXPERT_IDS_SET]


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

    **Date key:** Uses scratch context / accumulator unless the first line contains
    ``published:YYYY-MM-DD`` in the verify tail (Substack / article byline date), which
    overrides the section date for that block only.

    **Expert routing:** Prefer verify-tail ``| thread:<id> |`` via :func:`ingest_thread_slugs`;
    hook prose like ``**`thread:davis`**`` must not route the row to the wrong transcript.
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

        slugs = ingest_thread_slugs(line)
        if not slugs:
            i += 1
            continue

        use_date = context_date
        if use_date is None and accum:
            use_date = _parse_date_yyyy_mm_dd(accum)
        if use_date is None:
            i += 1
            continue

        pub_m = _RE_PUBLISHED.search(line)
        if pub_m:
            use_date = _parse_date_yyyy_mm_dd(pub_m.group(1))

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
    page_blocks: list | None = None,
) -> str:
    """Render machine-layer content between -thread.md markers (overwrite each run).

    Human narrative belongs *above* THREAD_MARKER_START in the file; see
    STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread (two layers).
    """
    page_blocks = page_blocks or []
    parts: list[str] = []
    parts.append("## Machine layer — Extraction (script-maintained)\n")
    parts.append(
        "_Auto-generated from `-transcript.md` + `strategy-page` blocks in this thread "
        "+ optional knot-index rows (legacy). "
        "**Journal layer** (narrative) lives **above** the **strategy-expert-thread** "
        "start HTML comment. The machine-layer HTML block is replaced on each `thread` run._\n"
    )

    if transcript_lines:
        parts.append("### Recent transcript material\n")
        for line in transcript_lines:
            parts.append(line)
        parts.append("")

    if page_blocks:
        parts.append("### Page references\n")
        for pb in page_blocks:
            w = f" watch=`{pb.watch}`" if pb.watch else ""
            parts.append(f"- **{pb.id}** — {pb.date}{w}")
        parts.append("")

    if knot_refs:
        parts.append("### Legacy knot references (deprecated)\n")
        parts.append(
            "_Standalone `chapters/…/knots/` files; prefer **Page references** above._\n"
        )
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

    if not transcript_lines and not knot_refs and not page_blocks:
        parts.append(
            "_(No transcript, page, or knot material for extraction.)_\n"
        )

    return "\n".join(parts).rstrip() + "\n"


def write_thread_file(
    dest: Path,
    inner: str,
) -> None:
    """Write extraction content between thread markers in a -thread.md file."""
    dest.parent.mkdir(parents=True, exist_ok=True)
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
    """Extract transcript + knot material → thread files for all experts.

    When any ``<expert_id>-thread-YYYY-MM.md`` exists for an expert (in-folder or flat),
    machine layers are written **per month**; legacy knot references attach to the
    **current UTC calendar month** file only. Otherwise behavior is unchanged (single
    ``thread.md``).
    """
    written: list[Path] = []
    today_ym = datetime.now(timezone.utc).date().strftime("%Y-%m")

    for expert_id in CANONICAL_EXPERT_IDS:
        paths = expert_paths(expert_id, out_dir)
        transcript_path = paths["transcript"]
        legacy_thread = paths["thread"]
        mmap = month_thread_paths_by_month(out_dir, expert_id)

        if not mmap:
            transcript_lines = read_transcript_content(transcript_path)
            knot_refs = find_knot_references(expert_id, knot_index_path=knot_index_path)
            page_blocks = discover_pages(legacy_thread, expert_id=expert_id)
            inner = render_thread_extraction(
                expert_id,
                transcript_lines=transcript_lines,
                knot_refs=knot_refs,
                page_blocks=page_blocks,
            )
            if not dry_run:
                write_thread_file(legacy_thread, inner)
            written.append(legacy_thread)
            continue

        by_m_transcript = parse_transcript_by_month(transcript_path)
        months = sorted(set(mmap.keys()) | set(by_m_transcript.keys()))
        knot_refs_all = find_knot_references(expert_id, knot_index_path=knot_index_path)

        for ym in months:
            dest = mmap.get(ym)
            if dest is None:
                dest = out_dir / "experts" / expert_id / f"{expert_id}-thread-{ym}.md"
            tlines = by_m_transcript.get(ym, [])
            pages = discover_pages(dest, expert_id=expert_id) if dest.is_file() else []
            knots = knot_refs_all if ym == today_ym else []
            inner = render_thread_extraction(
                expert_id,
                transcript_lines=tlines,
                knot_refs=knots,
                page_blocks=pages,
            )
            if not dry_run:
                write_thread_file(dest, inner)
            written.append(dest)

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
