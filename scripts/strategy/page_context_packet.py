#!/usr/bin/env python3
"""Build a bounded thread-context packet for expert-page composition.

WORK only; not Record.

The packet is a drafting aid, not canonical notebook state. It distills the
previous thread months for an expert into a small, page-shaping brief:

- month briefs
- settled background
- unresolved claims
- contradictions / tensions
- newly changed items
- recurring themes

The helper is intentionally simple and deterministic. It does not try to read
the raw source as an oracle; it only compresses the thread history into a
bounded context packet that can sit beside a page scaffold.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from collections import Counter
from pathlib import Path
from typing import Sequence

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
MONTH_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2})\s*$", re.MULTILINE)

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'\-]+")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_CODE_RE = re.compile(r"`([^`]+)`")

_CONTRADICTION_KEYS = (
    "contradict",
    "contradiction",
    "tension",
    "diverge",
    "mismatch",
    "however",
    "but",
    "yet",
    "instead",
    "versus",
    "v.",
    "roadblock",
    "barrier",
)
_UNRESOLVED_KEYS = (
    "open",
    "unresolved",
    "unclear",
    "uncertain",
    "question",
    "pending",
    "verify",
    "not yet",
    "don't know",
    "do not know",
    "maybe",
    "perhaps",
    "who knows",
    "hard to see",
    "can't see",
    "cannot see",
)
_NEW_KEYS = (
    "new",
    "update",
    "changed",
    "shift",
    "pivot",
    "turn",
    "breakout",
    "now",
    "as of",
    "fresh",
    "latest",
    "bombshell",
)
_SETTLED_KEYS = (
    "settled",
    "remains",
    "remain",
    "still",
    "continues",
    "continue",
    "anchor",
    "stable",
    "stays",
    "time is on the side",
    "will continue",
    "is not going to",
    "not about to",
)
_STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "because",
    "being",
    "but",
    "can",
    "could",
    "does",
    "doing",
    "for",
    "from",
    "have",
    "having",
    "into",
    "just",
    "like",
    "more",
    "most",
    "not",
    "now",
    "onto",
    "our",
    "out",
    "over",
    "such",
    "that",
    "the",
    "their",
    "there",
    "these",
    "this",
    "those",
    "through",
    "very",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "will",
    "thread",
    "page",
    "pages",
    "expert",
    "month",
    "months",
    "crooke",
    "diesen",
    "davis",
    "threads",
    "refined",
    "context",
}


@dataclass(frozen=True)
class MonthContext:
    month: str
    source_path: str
    brief: str
    settled: list[str]
    unresolved: list[str]
    contradicted: list[str]
    newly_changed: list[str]


@dataclass(frozen=True)
class ThreadContextPacket:
    expert_id: str
    page_date: str
    page_title: str
    selection_note: str
    source_months: list[str]
    source_paths: list[str]
    month_contexts: list[MonthContext]
    settled: list[str]
    unresolved: list[str]
    contradicted: list[str]
    newly_changed: list[str]
    recurring_themes: list[str]
    drafting_guidance: list[str]


def _strip_markdown_noise(text: str) -> str:
    out = text.strip()
    out = _BOLD_RE.sub(r"\1", out)
    out = _LINK_RE.sub(r"\1", out)
    out = _CODE_RE.sub(r"\1", out)
    out = out.replace("\u2019", "'").replace("\u2018", "'")
    out = out.replace("\u201c", '"').replace("\u201d", '"')
    out = re.sub(r"\s+", " ", out)
    return out.strip()


def _truncate_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    if max_words <= 1:
        return "..."
    return " ".join(words[: max_words - 1]).rstrip(",;:") + " ..."


def _human_layer(text: str) -> str:
    if THREAD_MARKER_START in text:
        return text.split(THREAD_MARKER_START, 1)[0].rstrip()
    return text.rstrip()


def _month_segments_from_text(text: str) -> dict[str, str]:
    matches = list(MONTH_HEADING_RE.finditer(text))
    segments: dict[str, str] = {}
    for i, match in enumerate(matches):
        month = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        segments[month] = text[start:end].strip()
    return segments


def _paragraph_blocks(segment: str) -> list[str]:
    out: list[str] = []
    for block in re.split(r"\n\s*\n+", segment.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## ") or block.startswith("### "):
            continue
        if block.startswith("<!--"):
            continue
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        if all(line.startswith("- ") for line in lines):
            out.extend(_strip_markdown_noise(line[2:]) for line in lines if line[2:].strip())
            continue
        joined = _strip_markdown_noise(" ".join(lines))
        if joined:
            out.append(joined)
    return out


def _classify_snippet(snippet: str, *, is_newest_source: bool) -> str:
    low = snippet.lower()
    if any(key in low for key in _CONTRADICTION_KEYS):
        return "contradicted"
    if any(key in low for key in _UNRESOLVED_KEYS):
        return "unresolved"
    if any(key in low for key in _NEW_KEYS):
        return "newly_changed"
    if any(key in low for key in _SETTLED_KEYS):
        return "settled"
    return "newly_changed" if is_newest_source else "settled"


def _unique_extend(dest: list[str], items: Sequence[str], *, limit: int) -> None:
    seen = {item.lower() for item in dest}
    for item in items:
        cleaned = _strip_markdown_noise(item)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        dest.append(cleaned)
        seen.add(key)
        if len(dest) >= limit:
            break


def _extract_theme_terms(snippets: Sequence[str], *, limit: int = 5) -> list[str]:
    counts: Counter[str] = Counter()
    for snippet in snippets:
        for token in _WORD_RE.findall(snippet.lower()):
            token = token.strip("-'")
            if len(token) < 4 or token in _STOPWORDS:
                continue
            if token.isdigit():
                continue
            counts[token] += 1
    if not counts:
        return []
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [f"{term} ({count})" for term, count in ordered[:limit] if count > 1]


def _month_sort_key(month: str) -> tuple[int, int]:
    y, m = month.split("-")
    return int(y), int(m)


def _selection_months(available_months: Sequence[str], page_month: str, lookback_months: int) -> tuple[list[str], str]:
    ordered = sorted(set(available_months), key=_month_sort_key)
    prior = [m for m in ordered if m < page_month]
    if prior:
        selected = prior[-lookback_months:]
        return selected, f"selected the last {len(selected)} prior month segment(s) before {page_month}"
    fallback = [m for m in ordered if m <= page_month]
    if fallback:
        selected = fallback[-lookback_months:]
        return selected, f"no earlier month segments found; fell back to the nearest available month segment(s) through {page_month}"
    selected = ordered[-lookback_months:]
    if selected:
        return selected, "no month segment at or before the page date was found; used the nearest available month segment(s)"
    return [], "no month segments were found in the provided thread file(s)"


def _month_brief(snippets: Sequence[str], *, max_words: int = 42) -> str:
    if not snippets:
        return ""
    joined = " ".join(snippets[:2])
    return _truncate_words(joined, max_words=max_words)


def build_thread_context_packet(
    *,
    expert_id: str,
    page_date: str,
    thread_paths: Sequence[Path],
    page_title: str = "",
    lookback_months: int = 3,
) -> ThreadContextPacket:
    """Build a bounded context packet from prior thread months.

    The helper reads all supplied thread files, extracts human-layer month
    segments, and selects the last ``lookback_months`` months *before* the page
    date. If no earlier months exist, it falls back to the nearest available
    month segment(s) so early pages still get a usable frame.
    """

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", page_date):
        raise ValueError(f"page_date must be YYYY-MM-DD, got {page_date!r}")

    page_month = page_date[:7]
    month_segments: dict[str, tuple[str, str]] = {}
    source_paths: list[str] = []

    for path in thread_paths:
        if not path.is_file():
            continue
        source_paths.append(path.as_posix())
        human = _human_layer(path.read_text(encoding="utf-8", errors="replace"))
        for month, segment in _month_segments_from_text(human).items():
            if month not in month_segments:
                month_segments[month] = (path.as_posix(), segment)

    selected_months, selection_note = _selection_months(
        list(month_segments.keys()), page_month, lookback_months
    )

    month_contexts: list[MonthContext] = []
    settled: list[str] = []
    unresolved: list[str] = []
    contradicted: list[str] = []
    newly_changed: list[str] = []
    all_snippets: list[str] = []

    for idx, month in enumerate(selected_months):
        source_path, segment = month_segments[month]
        candidate_blocks = _paragraph_blocks(segment)
        brief = _month_brief(candidate_blocks)

        month_settled: list[str] = []
        month_unresolved: list[str] = []
        month_contradicted: list[str] = []
        month_newly_changed: list[str] = []

        for block in candidate_blocks:
            is_newest = idx == len(selected_months) - 1
            bucket = _classify_snippet(block, is_newest_source=is_newest)
            snippet = f"{month}: {block}"
            all_snippets.append(block)
            if bucket == "contradicted":
                month_contradicted.append(snippet)
            elif bucket == "unresolved":
                month_unresolved.append(snippet)
            elif bucket == "newly_changed":
                month_newly_changed.append(snippet)
            else:
                month_settled.append(snippet)

        _unique_extend(settled, month_settled, limit=6)
        _unique_extend(unresolved, month_unresolved, limit=6)
        _unique_extend(contradicted, month_contradicted, limit=6)
        _unique_extend(newly_changed, month_newly_changed, limit=6)
        month_contexts.append(
            MonthContext(
                month=month,
                source_path=source_path,
                brief=brief or "(no prose snippets found in this month segment)",
                settled=month_settled[:2],
                unresolved=month_unresolved[:2],
                contradicted=month_contradicted[:2],
                newly_changed=month_newly_changed[:2],
            )
        )

    recurring_themes = _extract_theme_terms(all_snippets, limit=5)

    drafting_guidance = [
        "Lead the page with the newest delta or the freshest reporting, not a recap of the whole arc.",
        "Use quotes to preserve the best factual or citable lines; keep synthesis focused on what changed in the thread.",
        "If a prior month already settled a point, quote only enough to anchor the page and spend the rest on the new turn or tension.",
    ]

    return ThreadContextPacket(
        expert_id=expert_id,
        page_date=page_date,
        page_title=page_title,
        selection_note=selection_note,
        source_months=selected_months,
        source_paths=source_paths,
        month_contexts=month_contexts,
        settled=settled,
        unresolved=unresolved,
        contradicted=contradicted,
        newly_changed=newly_changed,
        recurring_themes=recurring_themes,
        drafting_guidance=drafting_guidance,
    )


def context_packet_path(expert_dir: Path, page_filename: str) -> Path:
    """Return the generated sidecar path for a page scaffold."""
    stem = Path(page_filename).stem
    return expert_dir / "page-context" / f"{stem}.context.md"


def render_thread_context_packet(packet: ThreadContextPacket) -> str:
    """Render the packet as markdown for a draft sidecar file."""
    lines: list[str] = []
    title = f"# Thread context packet â€” `{packet.expert_id}`"
    if packet.page_title:
        title += f" â€” {packet.page_title}"
    lines.append(title)
    lines.append("")
    lines.append("WORK only; draft aid, not canonical notebook state.")
    lines.append(f"Page date: `{packet.page_date}`")
    lines.append(f"Selection: {packet.selection_note}.")
    if packet.source_months:
        lines.append(f"Source months: {', '.join(packet.source_months)}")
    if packet.source_paths:
        lines.append("Source files:")
        for src in packet.source_paths:
            lines.append(f"- `{src}`")
    lines.append("")

    lines.append("## Month briefs")
    lines.append("")
    if packet.month_contexts:
        for mc in packet.month_contexts:
            lines.append(f"- **{mc.month}:** {mc.brief}")
    else:
        lines.append("- No month briefs available from the provided thread files.")
    lines.append("")

    def section(title: str, items: Sequence[str], *, fallback: str) -> None:
        lines.append(f"## {title}")
        lines.append("")
        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append(f"- {fallback}")
        lines.append("")

    section(
        "Settled background",
        packet.settled,
        fallback="No settled background lines were selected from the thread months.",
    )
    section(
        "Unresolved claims",
        packet.unresolved,
        fallback="No explicit unresolved claims were selected from the thread months.",
    )
    section(
        "Contradictions / tensions",
        packet.contradicted,
        fallback="No explicit contradictions or tensions were selected from the thread months.",
    )
    section(
        "Newly changed",
        packet.newly_changed,
        fallback="No newly changed lines were selected from the thread months.",
    )

    lines.append("## Recurring themes")
    lines.append("")
    if packet.recurring_themes:
        for theme in packet.recurring_themes:
            lines.append(f"- {theme}")
    else:
        lines.append("- No recurring themes were detected from the selected months.")
    lines.append("")

    lines.append("## Drafting guidance")
    lines.append("")
    for tip in packet.drafting_guidance:
        lines.append(f"- {tip}")
    lines.append("")

    if packet.month_contexts:
        lines.append("## Source month notes")
        lines.append("")
        for mc in packet.month_contexts:
            lines.append(f"### {mc.month}")
            lines.append("")
            lines.append(f"- Source: `{mc.source_path}`")
            if mc.settled:
                lines.append(f"- Settled: {mc.settled[0]}")
            if mc.unresolved:
                lines.append(f"- Unresolved: {mc.unresolved[0]}")
            if mc.contradicted:
                lines.append(f"- Tension: {mc.contradicted[0]}")
            if mc.newly_changed:
                lines.append(f"- Changed: {mc.newly_changed[0]}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"
