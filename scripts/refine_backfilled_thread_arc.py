#!/usr/bin/env python3
"""
Refine an existing reconstructed backfill block inside an expert thread.

What this does
--------------
- Reads the existing backfill block inserted by backfill_expert_thread.py
- If the block has ``### YYYY-MM`` month sections with dated bullets, produces a
  month-level "arc" summary (derivative) and keeps the original dated bullets
  under ``#### Dated evidence``
- If there are **no** month headings (e.g. empty-window italic only), exits
  without changing the file (no-op)
- Never touches the machine extraction block (verified on --apply)
- Never rewrites contemporaneous Segment 1 prose outside the backfill block

What this does NOT do
---------------------
- It does not invent facts outside the existing reconstructed bullets
- It does not read external sources
- It does not harmonize contradictions away
- It does not overwrite the machine-maintained thread extraction block

Optional second step after backfill_expert_thread.py when evidence is dense;
skip when the backfill is empty or has no ``###`` month sections.

Typical use
-----------
python3 scripts/refine_backfilled_thread_arc.py \\
  --expert-id ritter \\
  --apply

Dry run
-------
python3 scripts/refine_backfilled_thread_arc.py \\
  --expert-id ritter \\
  --dry-run
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
THREAD_MARKER_END = "<!-- strategy-expert-thread:end -->"


def marker_block_start(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:start -->"


def marker_block_end(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:end -->"


MONTH_HEADING_RE = re.compile(r"^###\s+(\d{4}-\d{2})\s*$", re.MULTILINE)

# Matches backfill_expert_thread.format_bullet (summary one line; source may include
# `` `path` `` and optional " (last touch YYYY-MM-DD sha12)").
BULLET_STRICT_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2})\*\* — (.+?)  \n  _Source:_ (.+)$",
    re.MULTILINE,
)
BULLET_LOOSE_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2})\*\* — (.+?)\s+  \n\s*_Source:_\s*(.+)$",
    re.MULTILINE,
)


@dataclass
class Bullet:
    date: str
    summary: str
    source: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_machine_block(text: str) -> Optional[str]:
    """Bytes between strategy-expert-thread start and end markers (inclusive)."""
    start = text.find(THREAD_MARKER_START)
    end = text.find(THREAD_MARKER_END)
    if start == -1 or end == -1 or end < start:
        return None
    end_full = end + len(THREAD_MARKER_END)
    return text[start:end_full]


def extract_backfill_block(text: str, expert_id: str) -> Optional[str]:
    pattern = re.compile(
        re.escape(marker_block_start(expert_id))
        + r"(.*?)"
        + re.escape(marker_block_end(expert_id)),
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        return None
    return m.group(0)


def inner_content(full_block_with_markers: str, expert_id: str) -> str:
    """Content between backfill HTML markers (exclusive)."""
    start = marker_block_start(expert_id)
    end = marker_block_end(expert_id)
    if not full_block_with_markers.startswith(start):
        raise ValueError("backfill block missing start marker")
    if not full_block_with_markers.rstrip().endswith(end):
        raise ValueError("backfill block missing end marker")
    mid = full_block_with_markers[len(start) :].rsplit(end, 1)[0]
    return mid.strip()


def has_month_sections(inner: str) -> bool:
    return bool(MONTH_HEADING_RE.search(inner))


def parse_month_sections(block: str) -> dict[str, str]:
    matches = list(MONTH_HEADING_RE.finditer(block))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        month = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        sections[month] = block[start:end].strip()
    return sections


def parse_bullets(section: str) -> list[Bullet]:
    bullets: list[Bullet] = []
    for rx in (BULLET_STRICT_RE, BULLET_LOOSE_RE):
        for m in rx.finditer(section):
            bullets.append(
                Bullet(
                    date=m.group(1),
                    summary=" ".join(m.group(2).split()),
                    source=" ".join(m.group(3).split()),
                )
            )
        if bullets:
            break
    return bullets


def sentence_case(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    return text[0].upper() + text[1:]


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item.strip())
    return out


def summarize_month(bullets: list[Bullet], max_points: int = 3) -> list[str]:
    if not bullets:
        return []
    raw_points = [sentence_case(b.summary.rstrip(".")) + "." for b in bullets]
    points = dedupe_preserve_order(raw_points)
    return points[:max_points]


def render_refined_month(month: str, bullets: list[Bullet]) -> str:
    lines: list[str] = []
    lines.append(f"### {month}")
    lines.append("")
    lines.append("#### Month-level arc")
    lines.append("")
    summary_points = summarize_month(bullets)

    if not summary_points:
        lines.append("_No usable dated bullets found for this month._")
        lines.append("")
    else:
        for point in summary_points:
            lines.append(f"- {point}")
        lines.append("")

    lines.append("#### Dated evidence")
    lines.append("")
    for b in bullets:
        lines.append(f"- **{b.date}** — {b.summary}  ")
        lines.append(f"  _Source:_ {b.source}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def preamble_before_first_month(inner: str) -> tuple[str, str]:
    """Return (text before first ### YYYY-MM, rest from first month heading)."""
    m = MONTH_HEADING_RE.search(inner)
    if not m:
        return inner.rstrip(), ""
    return inner[: m.start()].rstrip(), inner[m.start() :].lstrip()


def render_refined_block(expert_id: str, original_full_block: str) -> Optional[str]:
    """
    Return new full backfill block including markers, or None if nothing to refine.
    """
    inner = inner_content(original_full_block, expert_id)

    if not has_month_sections(inner):
        return None

    preamble, month_tail = preamble_before_first_month(inner)
    month_sections = parse_month_sections(month_tail)

    # Preserve original preamble (## title, Scope, Status, Rules) — tweak Status once
    pre_lines = preamble.splitlines()
    refined_pre: list[str] = []
    status_appended = False
    for line in pre_lines:
        refined_pre.append(line)
        if line.startswith("**Status:**") and not status_appended:
            if "month-level arc" not in line.lower():
                refined_pre[-1] = (
                    line.rstrip()
                    + " Refined month-level arc summaries below are **derivative** of dated bullets only."
                )
            status_appended = True
    if not status_appended:
        refined_pre.append(
            "**Status:** Refined month-level arc summaries below are **derivative** of dated bullets only."
        )

    out: list[str] = [marker_block_start(expert_id)]
    out.extend(refined_pre)
    if out[-1].strip() != "":
        out.append("")

    for month in sorted(month_sections.keys()):
        section = month_sections[month]
        bullets = parse_bullets(section)
        out.append(render_refined_month(month, bullets).rstrip())
        out.append("")

    out.append(marker_block_end(expert_id))
    return "\n".join(out).rstrip() + "\n"


def splice_backfill(text: str, expert_id: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(marker_block_start(expert_id))
        + r".*?"
        + re.escape(marker_block_end(expert_id)),
        re.DOTALL,
    )
    return pattern.sub(new_block.rstrip(), text, count=1)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expert-id", required=True)
    p.add_argument("--thread-path", type=Path, default=None)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    expert_id = args.expert_id.strip()
    thread_path = args.thread_path or (NOTEBOOK_DIR / f"strategy-expert-{expert_id}-thread.md")
    if not thread_path.is_file():
        raise SystemExit(f"Thread file not found: {thread_path}")

    text = read_text(thread_path)
    if THREAD_MARKER_START in text and THREAD_MARKER_END not in text:
        raise SystemExit("Thread markers look malformed; refusing to proceed.")

    block = extract_backfill_block(text, expert_id)
    if block is None:
        raise SystemExit(
            f"No existing backfill block found for `{expert_id}`. "
            "Run backfill_expert_thread.py first."
        )

    refined = render_refined_block(expert_id, block)
    if refined is None:
        msg = (
            "No `### YYYY-MM` month sections in backfill — nothing to refine "
            "(empty or italic-only window). Leaving file unchanged."
        )
        print(msg)
        if args.dry_run:
            print("\n(inner backfill preview, unchanged):\n")
            print(inner_content(block, expert_id)[:2000])
        return 0

    if args.dry_run or not args.apply:
        print(refined)
        if not args.apply:
            print("\n(Not applied. Re-run with --apply to write into the thread file.)")
        return 0

    machine_before = extract_machine_block(text)
    if machine_before is None:
        raise SystemExit(
            f"Cannot find {THREAD_MARKER_START!r} … {THREAD_MARKER_END!r}; abort."
        )

    updated = splice_backfill(text, expert_id, refined)
    machine_after = extract_machine_block(updated)
    if machine_after != machine_before:
        raise SystemExit(
            "Refusing to write: machine extraction block would change. Report as bug."
        )

    if updated == text:
        print("No changes needed.")
        return 0

    thread_path.write_text(updated, encoding="utf-8")
    print(f"Refined backfill block in {thread_path.relative_to(REPO_ROOT)}")
    print("Machine extraction block unchanged (verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
