#!/usr/bin/env python3
"""Parse ``batch-analysis`` lines from the strategy inbox and emit a
WORK-only JSON snapshot for visual overlays.

Spec: STRATEGY-NOTEBOOK-ARCHITECTURE.md § *Batch-analysis — machine parse
& visual snapshot* — each element of ``batch_analysis_refs[]`` includes:
``date``, ``label``, ``raw``, ``expert_ids``, ``confidence``, ``sources``.

Usage::

    python3 scripts/parse_batch_analysis.py
    python3 scripts/parse_batch_analysis.py --pretty
    python3 scripts/parse_batch_analysis.py --dry-run
    python3 scripts/parse_batch_analysis.py --inbox path/to/inbox.md --out path/to/out.json

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import CANONICAL_EXPERT_IDS, _EXPERT_IDS_SET

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_OUT = (
    REPO_ROOT / "artifacts/skill-work/work-strategy/batch-analysis-snapshot.json"
)

SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

_RE_BATCH_TOKEN = re.compile(r"\bbatch-analysis\b", re.IGNORECASE)

# Canonical pipe format: `batch-analysis | YYYY-MM-DD | <label> | <body>`
# Lines may be wrapped in backticks or start with a bullet.
_RE_PIPE = re.compile(
    r"batch-analysis\s*\|\s*"
    r"(\d{4}-\d{2}-\d{2})\s*\|\s*"
    r"([^|]+?)\s*\|\s*"
    r"(.+)",
    re.IGNORECASE,
)

_RE_CROSSES = re.compile(r"crosses:([a-z][a-z0-9-]*(?:\+[a-z][a-z0-9-]*)+)")
_RE_THREAD = re.compile(r"thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)")
_RE_SEAM = re.compile(r"seam:([a-z][a-z0-9-]*(?:\+[a-z][a-z0-9-]*)*)")

# Date context markers reused from inbox structure
_RE_ACCUM = re.compile(r"\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})")
_RE_PRIOR = re.compile(r"\*\*Prior scratch\s*[-—–]\s*(\d{4}-\d{2}-\d{2})")
_RE_DATE_HEADING = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})")

# Build alias lookup: last name segment of each canonical slug → full slug.
# e.g. "scott-ritter" → alias "ritter" → "scott-ritter"
_ALIAS_TO_ID: dict[str, str] = {}
for _cid in CANONICAL_EXPERT_IDS:
    parts = _cid.split("-")
    _ALIAS_TO_ID[_cid] = _cid
    if len(parts) > 1:
        _ALIAS_TO_ID[parts[-1]] = _cid
        _ALIAS_TO_ID[parts[0]] = _cid
_ALIAS_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in sorted(_ALIAS_TO_ID, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class BatchRef:
    date: str
    label: str
    raw: str
    expert_ids: list[str] = field(default_factory=list)
    confidence: str = "none"
    sources: dict[str, list[str]] = field(default_factory=dict)
    seams: list[str] = field(default_factory=list)
    line_number: int = 0

    def to_dict(self) -> dict:
        d: dict = {
            "date": self.date,
            "label": self.label,
            "raw": self.raw,
            "expert_ids": self.expert_ids,
            "confidence": self.confidence,
            "sources": self.sources,
        }
        if self.seams:
            d["seams"] = self.seams
        return d


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _extract_crosses(text: str) -> list[str]:
    """Extract canonical expert IDs from crosses:id+id markers."""
    ids: list[str] = []
    for m in _RE_CROSSES.finditer(text):
        for slug in m.group(1).split("+"):
            slug = slug.strip()
            if slug in _EXPERT_IDS_SET and slug not in ids:
                ids.append(slug)
    return ids


def _extract_threads(text: str) -> list[str]:
    """Extract canonical expert IDs from thread:<id> markers."""
    ids: list[str] = []
    for m in _RE_THREAD.finditer(text):
        slug = m.group(1)
        if slug in _EXPERT_IDS_SET and slug not in ids:
            ids.append(slug)
    return ids


def _extract_seams(text: str) -> list[str]:
    """Extract seam slugs (topology, not necessarily expert IDs)."""
    seams: list[str] = []
    for m in _RE_SEAM.finditer(text):
        seams.append(m.group(1))
    return seams


def _extract_aliases(text: str, already: set[str]) -> list[str]:
    """Extract expert IDs by alias/name matching in body text."""
    ids: list[str] = []
    for m in _ALIAS_PATTERN.finditer(text):
        canonical = _ALIAS_TO_ID.get(m.group(1).lower())
        if canonical and canonical not in already and canonical not in ids:
            ids.append(canonical)
    return ids


def _assign_confidence(
    crosses: list[str],
    threads: list[str],
    aliases: list[str],
) -> str:
    if len(crosses) >= 2:
        return "high"
    if crosses or threads:
        return "medium"
    if len(aliases) >= 2:
        return "medium"
    if aliases:
        return "low"
    return "none"


def _context_date(line: str) -> str | None:
    """Try to extract a date context marker from a non-batch line."""
    for rx in (_RE_ACCUM, _RE_PRIOR, _RE_DATE_HEADING):
        m = rx.search(line)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_inbox(inbox_path: Path) -> list[BatchRef]:
    """Parse all batch-analysis lines from the inbox file."""
    if not inbox_path.is_file():
        print(f"warning: inbox not found: {inbox_path}", file=sys.stderr)
        return []

    text = inbox_path.read_text(encoding="utf-8")
    refs: list[BatchRef] = []
    current_date: str | None = None

    for line_num, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()

        ctx = _context_date(stripped)
        if ctx:
            current_date = ctx
            continue

        if not _RE_BATCH_TOKEN.search(stripped):
            continue

        # Strip surrounding backticks and bullets
        raw = stripped
        clean = stripped.lstrip("- ").strip("`").strip()

        pipe_m = _RE_PIPE.search(clean)
        if pipe_m:
            batch_date = pipe_m.group(1)
            label = pipe_m.group(2).strip()
            body = pipe_m.group(3).strip()
        elif clean.lower().startswith("batch-analysis"):
            if "YYYY-MM-DD" in clean:
                continue
            batch_date = current_date or "unknown"
            label = clean[:80]
            body = clean
        else:
            # Prose mention of "batch-analysis" — not an entry line
            continue

        crosses = _extract_crosses(body)
        threads = _extract_threads(body)
        seams = _extract_seams(body)

        already = set(crosses) | set(threads)
        aliases = _extract_aliases(body, already)

        all_ids = list(dict.fromkeys(crosses + threads + aliases))
        confidence = _assign_confidence(crosses, threads, aliases)

        sources: dict[str, list[str]] = {}
        if crosses:
            sources["crosses"] = crosses
        if threads:
            sources["thread_in_line"] = threads
        if aliases:
            sources["alias_match"] = aliases

        refs.append(BatchRef(
            date=batch_date,
            label=label,
            raw=raw,
            expert_ids=all_ids,
            confidence=confidence,
            sources=sources,
            seams=seams,
            line_number=line_num,
        ))

    return refs


def build_snapshot(refs: list[BatchRef]) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(refs),
        "batch_analysis_refs": [r.to_dict() for r in refs],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--pretty", action="store_true", help="Indent JSON output")
    p.add_argument("--dry-run", action="store_true", help="Print to stdout, don't write")
    args = p.parse_args()

    refs = parse_inbox(args.inbox)
    snapshot = build_snapshot(refs)

    indent = 2 if args.pretty else None
    output = json.dumps(snapshot, indent=indent, ensure_ascii=False)

    if args.dry_run:
        print(output)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output + "\n", encoding="utf-8")
        print(f"ok: {len(refs)} batch-analysis refs → {args.out.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
