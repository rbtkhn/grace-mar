#!/usr/bin/env python3
"""Parse `batch-analysis` lines from strategy inbox text → batch_analysis_refs JSON.

Contract: docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md
§ *Batch-analysis — machine parse & visual snapshot*.

Usage:
  python3 scripts/parse_batch_analysis.py [path/to/daily-strategy-inbox.md]
  python3 scripts/parse_batch_analysis.py --stdin < inbox.md

Stdin or file; defaults to repo daily-strategy-inbox.md when no args.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from strategy_expert_corpus import CANONICAL_EXPERT_IDS, _RE_THREAD  # noqa: E402

ALLOWLIST = frozenset(CANONICAL_EXPERT_IDS)

_RE_MINI_START = re.compile(
    r"^---\s*batch-analysis\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*---\s*$"
)
_RE_MINI_END = re.compile(r"^---\s*end batch-analysis\s*---\s*$", re.IGNORECASE)
_RE_CROSSES = re.compile(
    r"crosses:([a-z0-9+-]+)(?:\s|$|,|\||\*\*)", re.IGNORECASE
)


def _norm_label(label: str) -> str:
    return " ".join(label.lower().split())


def _valid_expert(slug: str) -> bool:
    return slug in ALLOWLIST


def _parse_crosses(body: str) -> list[str]:
    """Return allowlist-validated ids from crosses:id+id (+ optional repeats)."""
    m = _RE_CROSSES.search(body)
    if not m:
        return []
    raw = m.group(1).lower()
    parts = [p.strip() for p in raw.split("+") if p.strip()]
    out: list[str] = []
    for p in parts:
        if _valid_expert(p):
            out.append(p)
    return out


def _parse_threads(text: str) -> list[str]:
    out: list[str] = []
    for m in _RE_THREAD.finditer(text):
        slug = m.group(1)
        if _valid_expert(slug):
            out.append(slug)
    return list(dict.fromkeys(out))


def _split_batch_pipe_line(line: str) -> tuple[str, str, str] | None:
    s = line.strip().strip("`")
    if not s.startswith("batch-analysis |"):
        return None
    parts = s.split(" | ", 3)
    if len(parts) < 4:
        return None
    if parts[0].strip() != "batch-analysis":
        return None
    date_s, label, body = parts[1].strip(), parts[2].strip(), parts[3]
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_s):
        return None
    return date_s, label, body


def _extract_single_line_records(lines: list[str]) -> list[tuple[int, str, str, str, str]]:
    """List of (line_index, date, label, body, raw_line)."""
    out: list[tuple[int, str, str, str, str]] = []
    for i, line in enumerate(lines):
        sp = _split_batch_pipe_line(line)
        if sp:
            d, label, body = sp
            out.append((i, d, label, body, line.rstrip()))
    return out


def _extract_mini_blocks(lines: list[str]) -> list[tuple[int, str, str, str]]:
    """List of (start_line_index, date, label, combined_raw)."""
    out: list[tuple[int, str, str, str]] = []
    i = 0
    n = len(lines)
    while i < n:
        m = _RE_MINI_START.match(lines[i].strip())
        if not m:
            i += 1
            continue
        d, label = m.group(1), m.group(2).strip()
        start = i
        i += 1
        while i < n and not _RE_MINI_END.match(lines[i].strip()):
            i += 1
        if i >= n:
            break
        raw = "\n".join(lines[start : i + 1])
        i += 1
        out.append((start, d, label, raw))
    return out


def _upstream_threads(lines: list[str], batch_line_idx: int) -> list[str]:
    """thread: slugs from ingest lines strictly above batch line until break."""
    collected: list[str] = []
    j = batch_line_idx - 1
    while j >= 0:
        line = lines[j]
        stripped = line.strip()
        if not stripped:
            break
        if stripped.startswith("<!--"):
            j -= 1
            continue
        if stripped.startswith("#"):
            break
        if stripped.startswith("batch-analysis |") or stripped.startswith("`batch-analysis |"):
            break
        if stripped.startswith("---") and "batch-analysis" in stripped:
            break
        for m in _RE_THREAD.finditer(line):
            slug = m.group(1)
            if _valid_expert(slug):
                collected.append(slug)
        j -= 1
    return list(dict.fromkeys(reversed(collected)))


def _confidence_and_ids(
    crosses: list[str],
    thread_line: list[str],
    upstream: list[str],
) -> tuple[list[str], str, dict[str, list[str]]]:
    sources: dict[str, list[str]] = {
        "crosses": list(dict.fromkeys(crosses)),
        "thread_in_line": list(dict.fromkeys(thread_line)),
        "upstream_verify": list(dict.fromkeys(upstream)),
        "label_alias": [],
    }
    high_ids = set(sources["crosses"]) | set(sources["thread_in_line"])
    mid_ids = set(sources["upstream_verify"])
    all_ids = list(dict.fromkeys(sources["crosses"] + sources["thread_in_line"] + sources["upstream_verify"]))

    if high_ids:
        conf = "high"
    elif mid_ids:
        conf = "medium"
    else:
        conf = "none"
    return all_ids, conf, sources


def parse_inbox_text(text: str) -> dict:
    """Return a document matching the batch_analysis_refs snapshot shape."""
    lines = text.splitlines()
    records: list[dict] = []

    # Single-line batch-analysis rows
    single_line_indices: set[int] = set()
    for i, d, label, body, raw in _extract_single_line_records(lines):
        single_line_indices.add(i)
        crosses = _parse_crosses(body)
        upstream = _upstream_threads(lines, i)
        thread_in_line = _parse_threads(lines[i])
        expert_ids, confidence, sources = _confidence_and_ids(
            crosses, thread_in_line, upstream
        )
        records.append(
            {
                "date": d,
                "label": label,
                "raw": raw,
                "expert_ids": expert_ids,
                "confidence": confidence,
                "sources": sources,
            }
        )

    for start, d, label, raw in _extract_mini_blocks(lines):
        if start in single_line_indices:
            continue
        crosses = _parse_crosses(raw)
        thread_in_line = _parse_threads(raw)
        upstream = _upstream_threads(lines, start)
        expert_ids, confidence, sources = _confidence_and_ids(
            crosses, thread_in_line, upstream
        )
        records.append(
            {
                "date": d,
                "label": label,
                "raw": raw,
                "expert_ids": expert_ids,
                "confidence": confidence,
                "sources": sources,
            }
        )

    merged = _merge_records(records)
    return {
        "schemaVersion": "1.0.0-strategy-notebook-view",
        "lane": "work-strategy",
        "batch_analysis_refs": merged,
    }


def _merge_records(records: list[dict]) -> list[dict]:
    """Union expert_ids for same (date, normalized label); prefer high-signal ids."""
    buckets: dict[tuple[str, str], dict] = {}
    order: list[tuple[str, str]] = []

    for r in records:
        key = (r["date"], _norm_label(r["label"]))
        if key not in buckets:
            buckets[key] = dict(r)
            order.append(key)
            continue
        cur = buckets[key]
        ids = list(dict.fromkeys(cur["expert_ids"] + r["expert_ids"]))
        cur["expert_ids"] = ids
        # Merge sources
        for k in ("crosses", "thread_in_line", "upstream_verify", "label_alias"):
            cur["sources"][k] = list(
                dict.fromkeys(cur["sources"].get(k, []) + r["sources"].get(k, []))
            )
        # Longer raw wins for display (usually the prose-heavy line)
        if len(r["raw"]) > len(cur["raw"]):
            cur["raw"] = r["raw"]
        _recompute_confidence(cur)

    for k in order:
        _recompute_confidence(buckets[k])
    return [buckets[k] for k in order]


def _recompute_confidence(rec: dict) -> None:
    s = rec["sources"]
    crosses = s["crosses"]
    til = s["thread_in_line"]
    up = s["upstream_verify"]
    la = s["label_alias"]
    rec["expert_ids"] = list(dict.fromkeys(crosses + til + up + la))
    if set(crosses) | set(til):
        rec["confidence"] = "high"
    elif up:
        rec["confidence"] = "medium"
    elif la:
        rec["confidence"] = "low"
    else:
        rec["confidence"] = "none"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "inbox",
        nargs="?",
        type=Path,
        default=REPO_ROOT
        / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md",
    )
    ap.add_argument("--stdin", action="store_true", help="Read inbox from stdin")
    args = ap.parse_args()
    if args.stdin:
        text = sys.stdin.read()
    else:
        p = args.inbox
        if not p.is_file():
            print(f"error: not a file: {p}", file=sys.stderr)
            return 1
        text = p.read_text(encoding="utf-8", errors="replace")
    doc = parse_inbox_text(text)
    json.dump(doc, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
