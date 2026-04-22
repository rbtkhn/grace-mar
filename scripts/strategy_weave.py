#!/usr/bin/env python3
"""Integrated cross-expert analysis (Think lane, read-only).

Replaces ``strategy_weave_inbox_stub.py``. Accepts a mix of expert IDs,
watch tags, and topic keywords. Gathers relevant material from thread files,
transcripts, inbox, and existing pages, then produces an integrated analysis
to stdout.

Also refreshes the batch-analysis snapshot (moved from ``strategy_thread.py``).

Usage::

    python3 scripts/strategy_weave.py davis barnes hormuz
    python3 scripts/strategy_weave.py --watch hormuz
    python3 scripts/strategy_weave.py escalation blockade
    python3 scripts/strategy_weave.py pape ritter --json

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    THREAD_MARKER_END,
    THREAD_MARKER_START,
    _EXPERT_IDS_SET,
    expert_paths,
    expert_thread_paths_for_discovery,
    read_transcript_content,
)
from strategy_page_reader import (
    PageBlock,
    all_watch_ids,
    discover_all_pages,
    discover_pages,
    pages_for_watch,
)

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_NOTEBOOK = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)


# ---------------------------------------------------------------------------
# Argument classification
# ---------------------------------------------------------------------------

def classify_args(
    positional: list[str],
    notebook_dir: Path,
) -> tuple[list[str], list[str], list[str]]:
    """Split positional arguments into expert IDs, watch tags, and keywords."""
    experts: list[str] = []
    watches: list[str] = []
    keywords: list[str] = []

    known_watches = set(all_watch_ids(notebook_dir))

    for arg in positional:
        a = arg.lower().strip()
        if a in _EXPERT_IDS_SET:
            experts.append(a)
        elif a in known_watches:
            watches.append(a)
        else:
            keywords.append(a)

    return experts, watches, keywords


# ---------------------------------------------------------------------------
# Material gathering
# ---------------------------------------------------------------------------

def _gather_pages(
    experts: list[str],
    watches: list[str],
    notebook_dir: Path,
) -> list[PageBlock]:
    """Collect pages matching named experts or watches."""
    seen_ids: set[tuple[str, str]] = set()
    pages: list[PageBlock] = []

    if watches:
        for w in watches:
            for expert_id, expert_pages in pages_for_watch(notebook_dir, w).items():
                for p in expert_pages:
                    key = (p.expert_id, p.id)
                    if key not in seen_ids:
                        seen_ids.add(key)
                        pages.append(p)

    if experts:
        all_pages = discover_all_pages(notebook_dir)
        for eid in experts:
            for p in all_pages.get(eid, []):
                key = (p.expert_id, p.id)
                if key not in seen_ids:
                    seen_ids.add(key)
                    pages.append(p)

    return pages


def _gather_transcript_lines(experts: list[str], notebook_dir: Path) -> dict[str, list[str]]:
    """Read transcript content for named experts."""
    result: dict[str, list[str]] = {}
    for eid in experts:
        tp = expert_paths(eid, notebook_dir)["transcript"]
        lines = read_transcript_content(tp)
        if lines:
            result[eid] = lines
    return result


def _gather_inbox_lines(
    experts: list[str],
    keywords: list[str],
    inbox_path: Path,
) -> list[str]:
    """Extract relevant inbox lines (thread:<expert> and keyword matches)."""
    if not inbox_path.is_file():
        return []
    text = inbox_path.read_text(encoding="utf-8")
    relevant: list[str] = []
    for line in text.splitlines():
        lower = line.lower()
        for eid in experts:
            if f"thread:{eid}" in lower:
                relevant.append(line)
                break
        else:
            for kw in keywords:
                if kw.lower() in lower:
                    relevant.append(line)
                    break
    return relevant


def _extract_machine_layer(experts: list[str], notebook_dir: Path) -> dict[str, str]:
    """Read the machine layer extraction from expert thread files."""
    result: dict[str, str] = {}
    for eid in experts:
        chunks: list[str] = []
        for tp in expert_thread_paths_for_discovery(notebook_dir, eid):
            if not tp.is_file():
                continue
            text = tp.read_text(encoding="utf-8")
            if THREAD_MARKER_START in text and THREAD_MARKER_END in text:
                _, after = text.split(THREAD_MARKER_START, 1)
                inner, _ = after.split(THREAD_MARKER_END, 1)
                stripped = inner.strip()
                if stripped:
                    chunks.append(stripped)
        if chunks:
            result[eid] = "\n\n".join(chunks)
    return result


# ---------------------------------------------------------------------------
# Batch-analysis snapshot (moved from strategy_thread.py)
# ---------------------------------------------------------------------------

def _refresh_batch_snapshot(inbox_path: Path) -> int:
    """Parse batch-analysis lines and write snapshot JSON. Returns count."""
    from parse_batch_analysis import build_snapshot, parse_inbox

    batch_refs = parse_inbox(inbox_path)
    snapshot = build_snapshot(batch_refs)
    out = REPO_ROOT / "artifacts/skill-work/work-strategy/batch-analysis-snapshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(batch_refs)


# ---------------------------------------------------------------------------
# Analysis output
# ---------------------------------------------------------------------------

def _build_analysis(
    experts: list[str],
    watches: list[str],
    keywords: list[str],
    pages: list[PageBlock],
    transcripts: dict[str, list[str]],
    inbox_lines: list[str],
    machine_layers: dict[str, str],
) -> dict:
    """Structure the gathered material into an analysis dict."""
    expert_positions: dict[str, list[str]] = {}
    for p in pages:
        bucket = expert_positions.setdefault(p.expert_id, [])
        summary = f"[{p.date}] {p.id}"
        if p.watch:
            summary += f" (watch: {p.watch})"
        bucket.append(summary)

    for eid, ml in machine_layers.items():
        bucket = expert_positions.setdefault(eid, [])
        first_line = ml.splitlines()[0] if ml else "(machine layer)"
        bucket.append(f"[machine] {first_line[:120]}")

    shared_watches: list[str] = []
    page_watches = {p.watch for p in pages if p.watch}
    shared_watches = sorted(page_watches)

    shared_page_ids: dict[str, list[str]] = {}
    for p in pages:
        shared_page_ids.setdefault(p.id, []).append(p.expert_id)
    shared_ground = [
        f"{pid}: {', '.join(eids)}"
        for pid, eids in shared_page_ids.items()
        if len(eids) > 1
    ]

    page_candidate = None
    if len(experts) >= 2 and pages:
        page_candidate = (
            f"page {' '.join(experts)}"
            + (f" --watch {watches[0]}" if watches else "")
        )

    return {
        "query": {
            "experts": experts,
            "watches": watches,
            "keywords": keywords,
        },
        "material": {
            "pages_found": len(pages),
            "transcript_experts": list(transcripts.keys()),
            "inbox_lines": len(inbox_lines),
            "machine_layer_experts": list(machine_layers.keys()),
        },
        "shared_ground": shared_ground,
        "expert_positions": expert_positions,
        "shared_watches": shared_watches,
        "open_threads": keywords if keywords else [],
        "page_candidate": page_candidate,
    }


def _format_markdown(analysis: dict) -> str:
    """Render analysis as readable markdown to stdout."""
    parts: list[str] = []
    q = analysis["query"]
    parts.append("# Weave analysis\n")

    if q["experts"]:
        parts.append(f"**Experts:** {', '.join(q['experts'])}")
    if q["watches"]:
        parts.append(f"**Watches:** {', '.join(q['watches'])}")
    if q["keywords"]:
        parts.append(f"**Keywords:** {', '.join(q['keywords'])}")
    parts.append("")

    mat = analysis["material"]
    parts.append(
        f"**Material:** {mat['pages_found']} pages, "
        f"{len(mat['transcript_experts'])} transcripts, "
        f"{mat['inbox_lines']} inbox lines, "
        f"{len(mat['machine_layer_experts'])} machine layers"
    )
    parts.append("")

    if analysis["shared_ground"]:
        parts.append("## Shared ground\n")
        for sg in analysis["shared_ground"]:
            parts.append(f"- {sg}")
        parts.append("")

    if analysis["expert_positions"]:
        parts.append("## Expert positions\n")
        for eid, positions in sorted(analysis["expert_positions"].items()):
            parts.append(f"### {eid}\n")
            for pos in positions:
                parts.append(f"- {pos}")
            parts.append("")

    if analysis["shared_watches"]:
        parts.append("## Shared watches\n")
        for w in analysis["shared_watches"]:
            parts.append(f"- {w}")
        parts.append("")

    if analysis["open_threads"]:
        parts.append("## Open threads\n")
        for ot in analysis["open_threads"]:
            parts.append(f"- {ot}")
        parts.append("")

    if analysis["page_candidate"]:
        parts.append("## Page candidate\n")
        parts.append(f"`{analysis['page_candidate']}`")
        parts.append("")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "items",
        nargs="*",
        help="Expert IDs, watch tags, or topic keywords (auto-classified)",
    )
    ap.add_argument("--watch", help="Explicit watch tag to analyze")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    ap.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK)
    ap.add_argument(
        "--no-batch-snapshot",
        action="store_true",
        help="Skip batch-analysis snapshot refresh",
    )
    args = ap.parse_args()

    experts, watches, keywords = classify_args(args.items or [], args.notebook)
    if args.watch:
        watches.append(args.watch)

    if not experts and not watches and not keywords:
        print("error: provide at least one expert ID, watch tag, or keyword", file=sys.stderr)
        return 1

    if not args.no_batch_snapshot:
        count = _refresh_batch_snapshot(args.inbox)
        print(f"batch-analysis snapshot: {count} refs", file=sys.stderr)

    pages = _gather_pages(experts, watches, args.notebook)
    transcripts = _gather_transcript_lines(experts, args.notebook)
    inbox_lines = _gather_inbox_lines(experts, keywords, args.inbox)
    machine_layers = _extract_machine_layer(experts, args.notebook)

    analysis = _build_analysis(
        experts, watches, keywords,
        pages, transcripts, inbox_lines, machine_layers,
    )

    if args.json:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print(_format_markdown(analysis))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
