#!/usr/bin/env python3
"""
Build prompt-ready batch-analysis context with optional historical expert context.

WORK-only; additive. Does not modify thread, transcript, days.md, or knot files.

Reads: artifacts/skill-work/work-strategy/batch-analysis-snapshot.json (batch_analysis_refs).

Optional: historical-expert-context/<expert_id>-<start>-to-<end>.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts/skill-work/work-strategy"
SNAPSHOT_PATH = ARTIFACTS_DIR / "batch-analysis-snapshot.json"
HISTORY_DIR = ARTIFACTS_DIR / "historical-expert-context"
OUT_DIR = ARTIFACTS_DIR / "batch-analysis-with-history"

PAIR_RE = re.compile(r"^\s*([a-z0-9\-]+)\s*,\s*([a-z0-9\-]+)\s*$", re.IGNORECASE)
COMPACT_BLOCK_RE = re.compile(
    r"```text\s*\n(historical-expert-context\s*\|.*?)\n```",
    re.DOTALL | re.IGNORECASE,
)


@dataclass
class HistoricalContext:
    expert_id: str
    path: str
    compact_block: Optional[str]
    preview_lines: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def parse_pair(raw: str) -> tuple[str, str]:
    m = PAIR_RE.match(raw)
    if not m:
        raise SystemExit("--pair must look like: scott-ritter,daniel-davis")
    return m.group(1).strip().lower(), m.group(2).strip().lower()


def find_snapshot_rows(snapshot: Any, expert_a: str, expert_b: str) -> list[dict]:
    if isinstance(snapshot, dict) and isinstance(snapshot.get("batch_analysis_refs"), list):
        rows = snapshot["batch_analysis_refs"]
    elif isinstance(snapshot, dict) and isinstance(snapshot.get("rows"), list):
        rows = snapshot["rows"]
    elif isinstance(snapshot, list):
        rows = snapshot
    else:
        rows = []

    a, b = expert_a.lower(), expert_b.lower()
    want = {a, b}
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ids_raw = row.get("expert_ids")
        if isinstance(ids_raw, list):
            ids = {str(x).lower() for x in ids_raw if isinstance(x, str)}
            if want.issubset(ids):
                out.append(row)
                continue
        hay = json.dumps(row, ensure_ascii=False).lower()
        if a in hay and b in hay:
            out.append(row)
    return out


def history_path(expert_id: str, start_seg: str, end_seg: str) -> Path:
    return HISTORY_DIR / f"{expert_id}-{start_seg}-to-{end_seg}.md"


def load_historical_context(expert_id: str, start_seg: str, end_seg: str) -> HistoricalContext:
    path = history_path(expert_id, start_seg, end_seg)
    if not path.exists():
        return HistoricalContext(
            expert_id=expert_id,
            path=path.relative_to(REPO_ROOT).as_posix(),
            compact_block=None,
            preview_lines=["No historical context artifact found."],
        )

    text = read_text(path)
    compact_match = COMPACT_BLOCK_RE.search(text)
    compact_block = compact_match.group(1).strip() if compact_match else None

    preview_lines: list[str] = []
    capture = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip() == "## Historical stance summary":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.startswith("- "):
            preview_lines.append(line[2:].strip())
        if len(preview_lines) >= 4:
            break

    if not preview_lines:
        preview_lines = ["No stance-summary bullets found."]

    return HistoricalContext(
        expert_id=expert_id,
        path=path.relative_to(REPO_ROOT).as_posix(),
        compact_block=compact_block,
        preview_lines=preview_lines,
    )


def compact_row_preview(row: dict) -> str:
    preferred_keys = ["date", "label", "raw", "expert_ids", "confidence"]
    parts = []
    for key in preferred_keys:
        if key in row and row[key] not in (None, "", []):
            parts.append(f"{key}={str(row[key]).strip()}")
    if not parts:
        parts.append(json.dumps(row, ensure_ascii=False))
    text = " | ".join(parts)
    return " ".join(text.split())


def render_output(
    pair: tuple[str, str],
    rows: list[dict],
    hist_a: HistoricalContext,
    hist_b: HistoricalContext,
    start_seg: str,
    end_seg: str,
) -> str:
    a, b = pair
    lines: list[str] = []
    lines.append(f"# Batch-analysis with history — `{a}` × `{b}`")
    lines.append("")
    lines.append("WORK only; additive prompt bundle.")
    lines.append(f"History window: {start_seg} → {end_seg}")
    lines.append("")

    lines.append("## Historical expert context")
    lines.append("")
    for hist in (hist_a, hist_b):
        lines.append(f"### {hist.expert_id}")
        lines.append(f"Source: `{hist.path}`")
        if hist.compact_block:
            lines.append("")
            lines.append("```text")
            lines.append(hist.compact_block)
            lines.append("```")
            lines.append("")
        else:
            lines.append("- No compact block available.")
            lines.append("")
        for item in hist.preview_lines:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Matching batch-analysis snapshot rows")
    lines.append("")
    if rows:
        for row in rows[:8]:
            lines.append(f"- {compact_row_preview(row)}")
    else:
        lines.append("- No matching rows found in batch-analysis-snapshot.json")
    lines.append("")

    lines.append("## Prompt-ready synthesis block")
    lines.append("")
    lines.append("```text")
    lines.append(
        f"Use the following as background for batch-analysis on {a} × {b}. "
        "Treat historical context as comparative memory, not verbatim proof."
    )
    if hist_a.compact_block:
        lines.append(hist_a.compact_block)
    if hist_b.compact_block:
        lines.append(hist_b.compact_block)
    if rows:
        lines.append("current-batch-analysis-rows:")
        for row in rows[:5]:
            lines.append("- " + compact_row_preview(row))
    else:
        lines.append("current-batch-analysis-rows: none found")
    lines.append("")
    lines.append("Tasks:")
    lines.append("- identify continuity vs change from the historical segment window")
    lines.append("- identify whether current tension is genuinely new or recurring")
    lines.append("- separate stance, mechanism, and confidence/provenance")
    lines.append("```")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pair", required=True, help="expert-a,expert-b")
    ap.add_argument("--history-start", required=True, help="YYYY-MM")
    ap.add_argument("--history-end", required=True, help="YYYY-MM")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print(
            "Specify --dry-run (print bundle to stdout) or --apply (write under artifacts).",
            file=sys.stderr,
        )
        return 2

    expert_a, expert_b = parse_pair(args.pair)

    if not SNAPSHOT_PATH.exists():
        raise SystemExit(f"Snapshot not found: {SNAPSHOT_PATH}")

    snapshot = read_json(SNAPSHOT_PATH)
    rows = find_snapshot_rows(snapshot, expert_a, expert_b)

    hist_a = load_historical_context(expert_a, args.history_start, args.history_end)
    hist_b = load_historical_context(expert_b, args.history_start, args.history_end)

    output = render_output(
        pair=(expert_a, expert_b),
        rows=rows,
        hist_a=hist_a,
        hist_b=hist_b,
        start_seg=args.history_start,
        end_seg=args.history_end,
    )

    if args.dry_run:
        print(output)
        if args.apply:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            out = (
                OUT_DIR
                / f"{expert_a}__{expert_b}__{args.history_start}-to-{args.history_end}.md"
            )
            out.write_text(output, encoding="utf-8")
            print(f"Wrote {out.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{expert_a}__{expert_b}__{args.history_start}-to-{args.history_end}.md"
    out.write_text(output, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
