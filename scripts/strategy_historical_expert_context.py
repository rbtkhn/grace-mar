#!/usr/bin/env python3
"""
Build a compact historical expert context artifact for batch-analysis (WORK-only).

Reads only the human-maintained layer **above** ``<!-- strategy-expert-thread:start -->``.
Month-scale segments use headings ``## YYYY-MM`` (preferred). If none are found,
falls back to ``### YYYY-MM`` in the same layer (after stripping the backfill HTML block).

Strips ``<!-- backfill:<expert_id>:start/end -->`` before segment parsing so the last
month segment does not swallow the reconstructed arc block.

Outputs markdown + JSON under ``artifacts/skill-work/work-strategy/historical-expert-context/``:

- **Rollup (range):** ``<expert_id>-<start>-to-<end>.md`` / ``.json`` — merged window (default on).
- **Per month:** ``<expert_id>/<YYYY-MM>.md`` / ``.json`` — one segment per file (default on).

``strategy_batch_analysis_with_history.py`` prefers **per-month** files when **every** month in the
requested window exists; otherwise it falls back to the rollup file.

Does **not** change ``parse_batch_analysis.py`` — paste the compact block into inbox or prompts manually.

See also: ``scripts/parse_batch_analysis.py`` for ``batch-analysis`` pipe snapshots.

Typical use
-----------
python3 scripts/strategy_historical_expert_context.py \\
  --expert-id scott-ritter \\
  --start-segment 2026-01 \\
  --end-segment 2026-03 \\
  --dry-run

python3 scripts/strategy_historical_expert_context.py \\
  --expert-id scott-ritter \\
  --start-segment 2026-01 \\
  --end-segment 2026-03 \\
  --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
OUT_DIR = REPO_ROOT / "artifacts/skill-work/work-strategy/historical-expert-context"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"

SEGMENT_H2_RE = re.compile(r"^##\s+(\d{4}-\d{2})\s*$", re.MULTILINE)
SEGMENT_H3_RE = re.compile(r"^###\s+(\d{4}-\d{2})\s*$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")
STRENGTH_RE = re.compile(r"\[strength:\s*(high|medium|low)\]", re.IGNORECASE)


def marker_backfill_start(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:start -->"


def marker_backfill_end(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:end -->"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def extract_human_layer(thread_text: str) -> str:
    if THREAD_MARKER_START in thread_text:
        return thread_text.split(THREAD_MARKER_START, 1)[0].rstrip()
    return thread_text.rstrip()


def strip_backfill_block(text: str, expert_id: str) -> str:
    pattern = re.compile(
        re.escape(marker_backfill_start(expert_id))
        + r".*?"
        + re.escape(marker_backfill_end(expert_id)),
        re.DOTALL,
    )
    out = pattern.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


@dataclass
class Segment:
    segment_id: str
    raw_text: str
    bullets: List[str]
    strength_counts: dict
    signal_lines: List[str]
    tension_lines: List[str]
    shift_lines: List[str]
    source: str  # "h2" or "h3"


def _classify_bullets(bullets: List[str]) -> tuple[dict, List[str], List[str], List[str]]:
    strength_counts = {"high": 0, "medium": 0, "low": 0}
    for b in bullets:
        sm = STRENGTH_RE.search(b)
        if sm:
            strength_counts[sm.group(1).lower()] += 1

    signal_lines: List[str] = []
    tension_lines: List[str] = []
    shift_lines: List[str] = []

    for b in bullets:
        low = b.lower()
        if any(
            k in low
            for k in [
                "signal",
                "mechanism",
                "claim",
                "argument",
                "thesis",
                "warning",
            ]
        ):
            signal_lines.append(b)
        if any(
            k in low
            for k in [
                "tension",
                "diverge",
                "conflict",
                "disagree",
                "versus",
                " vs",
            ]
        ):
            tension_lines.append(b)
        if any(
            k in low
            for k in [
                "shift",
                "change",
                "pivot",
                "drift",
                "moved",
                "harder",
                "softer",
            ]
        ):
            shift_lines.append(b)

    return strength_counts, signal_lines, tension_lines, shift_lines


def parse_segments_with_regex(
    human_layer_stripped: str, segment_re: re.Pattern[str], source: str
) -> List[Segment]:
    matches = list(segment_re.finditer(human_layer_stripped))
    segments: List[Segment] = []

    for i, m in enumerate(matches):
        seg_id = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(human_layer_stripped)
        body = human_layer_stripped[start:end].strip()

        bullets: List[str] = []
        for line in body.splitlines():
            bm = BULLET_RE.match(line)
            if bm:
                bullets.append(normalize_space(bm.group(1)))

        strength_counts, signal_lines, tension_lines, shift_lines = _classify_bullets(bullets)

        segments.append(
            Segment(
                segment_id=seg_id,
                raw_text=body,
                bullets=bullets,
                strength_counts=strength_counts,
                signal_lines=signal_lines,
                tension_lines=tension_lines,
                shift_lines=shift_lines,
                source=source,
            )
        )

    return segments


def parse_segments(human_layer_stripped: str) -> tuple[List[Segment], str]:
    """
    Prefer ## YYYY-MM; if none, use ### YYYY-MM. Returns (segments, note).
    """
    h2 = parse_segments_with_regex(human_layer_stripped, SEGMENT_H2_RE, "h2")
    if h2:
        return h2, "parsed `## YYYY-MM` month segments"
    h3 = parse_segments_with_regex(human_layer_stripped, SEGMENT_H3_RE, "h3")
    if h3:
        return h3, "no `## YYYY-MM` headings; used `### YYYY-MM` fallback"
    return [], "no month segments found (`## YYYY-MM` or `### YYYY-MM`)"


def filter_segments(
    segments: List[Segment], start_segment: str, end_segment: str
) -> List[Segment]:
    return [s for s in segments if start_segment <= s.segment_id <= end_segment]


def first_n(items: List[str], n: int) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item)
        if len(out) >= n:
            break
    return out


def render_markdown(
    expert_id: str,
    segments: List[Segment],
    thread_relpath: str,
    parse_note: str,
) -> str:
    total_high = sum(s.strength_counts["high"] for s in segments)
    total_medium = sum(s.strength_counts["medium"] for s in segments)
    total_low = sum(s.strength_counts["low"] for s in segments)

    key_signals = first_n(
        [x for s in segments for x in s.signal_lines]
        or [x for s in segments for x in s.bullets],
        5,
    )
    key_tensions = first_n([x for s in segments for x in s.tension_lines], 4)
    key_shifts = first_n([x for s in segments for x in s.shift_lines], 4)

    lines: List[str] = []
    lines.append(f"# Historical expert context — `{expert_id}`")
    lines.append("")
    lines.append("WORK only; not Record.")
    lines.append(f"Source thread: `{thread_relpath}`")
    lines.append(f"Segments included: {', '.join(s.segment_id for s in segments) if segments else '(none)'}")
    lines.append(f"Parse: {parse_note}")
    lines.append("")
    lines.append("## Batch-analysis handoff")
    lines.append("")
    lines.append(
        f"- Provenance mix across included segments: high={total_high}, medium={total_medium}, low={total_low}"
    )
    lines.append(
        "- Use this as historical context for compare/contrast; do not treat it as verbatim proof."
    )
    lines.append("")

    lines.append("## Historical stance summary")
    lines.append("")
    if key_signals:
        for item in key_signals:
            lines.append(f"- {item}")
    else:
        lines.append("- No strong signal lines detected in selected segments.")
    lines.append("")

    lines.append("## Historical tensions")
    lines.append("")
    if key_tensions:
        for item in key_tensions:
            lines.append(f"- {item}")
    else:
        lines.append("- No explicit tension lines detected.")
    lines.append("")

    lines.append("## Historical shifts / drift")
    lines.append("")
    if key_shifts:
        for item in key_shifts:
            lines.append(f"- {item}")
    else:
        lines.append("- No explicit shift lines detected.")
    lines.append("")

    lines.append("## Prompt-ready compact block")
    lines.append("")
    compact: List[str] = []
    if key_signals:
        compact.append("stance=" + " || ".join(key_signals[:3]))
    if key_tensions:
        compact.append("tensions=" + " || ".join(key_tensions[:2]))
    if key_shifts:
        compact.append("shifts=" + " || ".join(key_shifts[:2]))
    compact.append(f"provenance=high:{total_high},medium:{total_medium},low:{total_low}")
    lines.append("```text")
    lines.append(
        "historical-expert-context | " + expert_id + " | " + " | ".join(compact)
    )
    lines.append("```")
    lines.append("")

    lines.append("## Segment notes")
    lines.append("")
    for s in segments:
        lines.append(f"### {s.segment_id}")
        lines.append("")
        lines.append(
            f"- strength mix: high={s.strength_counts['high']}, "
            f"medium={s.strength_counts['medium']}, low={s.strength_counts['low']} "
            f"({s.source})"
        )
        preview = first_n(s.bullets, 4)
        if preview:
            for item in preview:
                lines.append(f"- {item}")
        else:
            lines.append("- No bullets found.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_single_month_artifact(
    expert_id: str,
    segment: Segment,
    thread_relpath: str,
    parse_note: str,
) -> str:
    """One month per file: same structure as the rollup, title line names the month."""
    md = render_markdown(expert_id, [segment], thread_relpath, parse_note)
    lines = md.splitlines()
    if lines:
        lines[0] = f"# Historical expert context — `{expert_id}` — `{segment.segment_id}`"
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expert-id", required=True)
    ap.add_argument("--start-segment", required=True, help="YYYY-MM")
    ap.add_argument("--end-segment", required=True, help="YYYY-MM")
    ap.add_argument("--thread-path", default=None, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--no-segment-files",
        action="store_true",
        help="Do not write per-month artifacts under historical-expert-context/<expert_id>/<YYYY-MM>.*",
    )
    ap.add_argument(
        "--no-rollup",
        action="store_true",
        help="Do not write the range rollup <expert_id>-<start>-to-<end>.md/.json",
    )
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print(
            "Specify --dry-run (print markdown to stdout) or --apply (write artifacts).",
            file=sys.stderr,
        )
        return 2

    expert_id = args.expert_id.strip()
    thread_path = args.thread_path or NOTEBOOK_DIR / f"strategy-expert-{expert_id}-thread.md"
    if not thread_path.is_file():
        raise SystemExit(f"Thread file not found: {thread_path}")

    thread_text = read_text(thread_path)
    human_layer = extract_human_layer(thread_text)
    stripped = strip_backfill_block(human_layer, expert_id)
    segments, parse_note = parse_segments(stripped)
    selected = filter_segments(segments, args.start_segment, args.end_segment)

    relpath = thread_path.relative_to(REPO_ROOT).as_posix()
    md = render_markdown(expert_id, selected, relpath, parse_note)

    stem = f"{expert_id}-{args.start_segment}-to-{args.end_segment}"
    out_md = OUT_DIR / f"{stem}.md"
    out_json = OUT_DIR / f"{stem}.json"

    payload = {
        "expert_id": expert_id,
        "thread_path": relpath,
        "start_segment": args.start_segment,
        "end_segment": args.end_segment,
        "parse_note": parse_note,
        "segments": [asdict(s) for s in selected],
    }

    def write_all_artifacts() -> bool:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        wrote_any = False
        if not args.no_segment_files and selected:
            seg_dir = OUT_DIR / expert_id
            seg_dir.mkdir(parents=True, exist_ok=True)
            for s in selected:
                smd = render_single_month_artifact(expert_id, s, relpath, parse_note)
                seg_md_path = seg_dir / f"{s.segment_id}.md"
                seg_md_path.write_text(smd, encoding="utf-8")
                seg_payload = {
                    "expert_id": expert_id,
                    "thread_path": relpath,
                    "segment_id": s.segment_id,
                    "parse_note": parse_note,
                    "segment": asdict(s),
                }
                seg_json_path = seg_dir / f"{s.segment_id}.json"
                seg_json_path.write_text(
                    json.dumps(seg_payload, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                print(f"Wrote {seg_md_path.relative_to(REPO_ROOT)}")
                print(f"Wrote {seg_json_path.relative_to(REPO_ROOT)}")
                wrote_any = True
        if not args.no_rollup:
            out_md.write_text(md, encoding="utf-8")
            out_json.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"Wrote {out_md.relative_to(REPO_ROOT)}")
            print(f"Wrote {out_json.relative_to(REPO_ROOT)}")
            wrote_any = True
        if not wrote_any:
            print(
                "Nothing written: use --no-segment-files / --no-rollup only if at least one output remains.",
                file=sys.stderr,
            )
        return wrote_any

    if args.dry_run:
        print(md)
        if args.apply and not write_all_artifacts():
            return 2
        return 0

    if not write_all_artifacts():
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
