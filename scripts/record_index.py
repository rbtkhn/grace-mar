"""
Deterministic indexes for canonical EVIDENCE (self-archive.md) and self-memory (memory.md).

- Evidence: Roman section spans (I–VIII) + entry id → character span for fast slice / lookup.
- Memory: horizon line ranges (short / medium / long) + preamble; same semantics as bot/core.py.

Used by bot/retriever.py (section-tagged chunks, routing hints) and bot/core.py (memory + recency).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Main EVIDENCE sections: ## I. READING LIST … ## VIII. GATED …
_EVIDENCE_SECTION_HDR = re.compile(r"(?m)^##\s+([IVX]+)\.\s+.+$")

# Evidence entry ids (list items and inline id: in YAML)
_EVIDENCE_ENTRY_ID = re.compile(
    r"(?m)(^\s*-\s+id:\s+|^[ \t]*id:\s*)"
    r"(LEARN-\d+|CUR-\d+|PER-\d+|ACT-\d+|READ-\d+|WRITE-\d+|CREATE-\d+|MEDIA-\d+)\b",
    re.IGNORECASE,
)

ROMAN_TO_SECTION_LABEL = {
    "I": "Reading",
    "II": "Writing",
    "III": "Creation",
    "IV": "Media",
    "V": "Activity",
    "VI": "Attestation",
    "VII": "Metrics",
    "VIII": "Gated",
}


@dataclass
class EvidenceIndex:
    """Character offsets into the original EVIDENCE file content."""

    section_spans: dict[str, tuple[int, int]] = field(default_factory=dict)
    entry_spans: dict[str, tuple[int, int]] = field(default_factory=dict)
    content_len: int = 0


def build_evidence_index(content: str) -> EvidenceIndex:
    """Build section map (Roman numeral → [start, end)) and entry id → [start, end))."""
    idx = EvidenceIndex(content_len=len(content))
    if not content:
        return idx

    sec_matches = list(_EVIDENCE_SECTION_HDR.finditer(content))
    for i, m in enumerate(sec_matches):
        roman = m.group(1).upper()
        start = m.start()
        end = sec_matches[i + 1].start() if i + 1 < len(sec_matches) else len(content)
        idx.section_spans[roman] = (start, end)

    matches = list(_EVIDENCE_ENTRY_ID.finditer(content))
    for i, m in enumerate(matches):
        raw = m.group(2).upper()
        if raw in idx.entry_spans:
            continue
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        idx.entry_spans[raw] = (start, end)

    return idx


def evidence_section_for_offset(index: EvidenceIndex, pos: int) -> str | None:
    """Return Roman section key (e.g. 'V') for a character offset, or None."""
    for roman, (a, b) in index.section_spans.items():
        if a <= pos < b:
            return roman
    return None


def slice_evidence_section(content: str, index: EvidenceIndex, roman: str) -> str:
    """Return substring for section Roman numeral, or full content if unknown."""
    span = index.section_spans.get(roman)
    if not span:
        return content
    return content[span[0] : span[1]]


def slice_evidence_entry(content: str, index: EvidenceIndex, entry_id: str) -> str:
    """Return substring for one entry id (uppercase ACT-0001), or empty."""
    key = entry_id.strip().upper()
    span = index.entry_spans.get(key)
    if not span:
        return ""
    return content[span[0] : span[1]]


# --- Memory (aligned with bot/core.py horizon headers) ---

_MEMORY_HEADER_NAMES = {
    "short-term": "short",
    "medium-term": "medium",
    "long-term": "long",
}


def _memory_header_horizon_key(line: str) -> str | None:
    if not line.startswith("## "):
        return None
    title = line[3:].strip()
    if "(" in title:
        title = title.split("(", 1)[0].strip()
    key = title.lower().replace(" ", "-")
    return _MEMORY_HEADER_NAMES.get(key)


@dataclass
class MemoryHorizonIndex:
    """Line-based index into memory.md (0-based line indices, end exclusive)."""

    lines: list[str]
    saw_horizon: bool
    preamble_range: tuple[int, int]  # [start, end) line indices
    horizon_ranges: dict[str, tuple[int, int]]  # short|medium|long -> [start, end)


def build_memory_horizon_index(content: str) -> MemoryHorizonIndex:
    """Line ranges match bot/core.py _parse_memory_horizons (preamble vs short/medium/long bodies)."""
    lines = content.splitlines()
    n = len(lines)
    horizon_ranges: dict[str, tuple[int, int]] = {
        "short": (n, n),
        "medium": (n, n),
        "long": (n, n),
    }
    current: str | None = None
    body_start: dict[str, int] = {}
    saw_horizon = False
    first_horizon_line: int | None = None

    for i, line in enumerate(lines):
        h = _memory_header_horizon_key(line)
        if h:
            saw_horizon = True
            if first_horizon_line is None:
                first_horizon_line = i
            if current is not None:
                horizon_ranges[current] = (body_start[current], i)
            current = h
            body_start[current] = i + 1
            continue

    if current is not None:
        horizon_ranges[current] = (body_start[current], n)

    if not saw_horizon:
        return MemoryHorizonIndex(
            lines=lines,
            saw_horizon=False,
            preamble_range=(0, n),
            horizon_ranges=horizon_ranges,
        )

    assert first_horizon_line is not None
    preamble_range = (0, first_horizon_line)

    return MemoryHorizonIndex(
        lines=lines,
        saw_horizon=True,
        preamble_range=preamble_range,
        horizon_ranges=horizon_ranges,
    )


def memory_buckets_from_index(idx: MemoryHorizonIndex) -> tuple[dict[str, list[str]], list[str]]:
    """
    Build the same bucket structure as legacy _parse_memory_horizons:
    (buckets dict short/medium/long -> lines, preamble lines).
    """
    buckets: dict[str, list[str]] = {"short": [], "medium": [], "long": []}
    ps, pe = idx.preamble_range
    preamble = idx.lines[ps:pe]

    for k in ("short", "medium", "long"):
        a, b = idx.horizon_ranges.get(k, (0, 0))
        if a < b:
            buckets[k] = idx.lines[a:b]
        else:
            buckets[k] = []

    return buckets, preamble
