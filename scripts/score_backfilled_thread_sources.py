#!/usr/bin/env python3
"""
Score source strength inside an existing expert backfill block (WORK-only).

Reads the backfill region created by ``backfill_expert_thread.py`` (optionally
after ``refine_backfilled_thread_arc.py``). Each bullet's ``_Source:_`` line
uses ``format_bullet`` shape: ``{source_type}: `path``` with
``source_type`` in ``transcript`` | ``days`` | ``knot`` | ``git`` — this
script maps those conservatively to **high** / **medium** / **low** and
prefixes each summary with ``[strength: …]``.

- **high** — ``transcript:`` or ``days:``
- **medium** — ``knot:``
- **low** — ``git:`` or unrecognized stubs

Rewrites **only** the ``<!-- backfill:<id>:start/end -->`` region. Verifies the
machine extraction block is unchanged on ``--apply``. No-op when there are no
``### YYYY-MM`` sections with dated bullets (empty window).

Typical use
-----------
python3 scripts/score_backfilled_thread_sources.py \\
  --expert-id ritter \\
  --dry-run

python3 scripts/score_backfilled_thread_sources.py \\
  --expert-id ritter \\
  --apply
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
THREAD_MARKER_END = "<!-- strategy-expert-thread:end -->"

MONTH_HEADING_RE = re.compile(r"^###\s+(\d{4}-\d{2})\s*$", re.MULTILINE)
DATED_EVIDENCE_HEADING_RE = re.compile(r"^####\s+Dated evidence\s*$", re.MULTILINE)
MONTH_ARC_HEADING_RE = re.compile(r"^####\s+Month-level arc\s*$", re.MULTILINE)

# Optional prior [strength: …] tag; matches backfill/refine two-space line break.
BULLET_SCORE_STRICT_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2})\*\* — "
    r"(?:\[strength:\s*(high|medium|low)\]\s+)?"
    r"(.+?)  \n  _Source:_ (.+)$",
    re.MULTILINE,
)
BULLET_SCORE_LOOSE_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2})\*\* — "
    r"(?:\[strength:\s*(high|medium|low)\]\s+)?"
    r"(.+?)\s+  \n\s*_Source:_\s*(.+)$",
    re.MULTILINE,
)


def marker_block_start(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:start -->"


def marker_block_end(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:end -->"


@dataclass
class ScoredBullet:
    date: str
    summary: str
    source: str
    strength: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_machine_block(text: str) -> Optional[str]:
    """Substring between strategy-expert-thread start and end markers (inclusive)."""
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


def preamble_before_first_month(inner: str) -> tuple[str, str]:
    m = MONTH_HEADING_RE.search(inner)
    if not m:
        return inner.rstrip(), ""
    return inner[: m.start()].rstrip(), inner[m.start() :].lstrip()


def parse_month_sections(block: str) -> dict[str, str]:
    matches = list(MONTH_HEADING_RE.finditer(block))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        month = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        sections[month] = block[start:end].strip()
    return sections


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def score_from_source_stub(source: str) -> str:
    """Conservative tier from ``format_bullet`` ``_Source:_`` stub (leading source_type)."""
    s = source.strip()
    if s.startswith("transcript:"):
        return "high"
    if s.startswith("days:"):
        return "high"
    if s.startswith("knot:"):
        return "medium"
    if s.startswith("git:"):
        return "low"
    if s.startswith("web:"):
        return "low"
    return "low"


def extract_dated_evidence_body(section: str) -> str:
    """If refined layout, only the dated-evidence subsection; else whole month section."""
    m = DATED_EVIDENCE_HEADING_RE.search(section)
    if not m:
        return section
    body = section[m.end() :]
    # Stop before next month
    m2 = re.search(r"^###\s+\d{4}-\d{2}\s*$", body, re.MULTILINE)
    if m2:
        body = body[: m2.start()]
    return body


def extract_month_arc_raw(section: str) -> Optional[str]:
    """
    If ``#### Month-level arc`` exists, return verbatim body up to ``#### Dated evidence``.
    Otherwise None.
    """
    if not MONTH_ARC_HEADING_RE.search(section):
        return None
    m_arc = MONTH_ARC_HEADING_RE.search(section)
    if not m_arc:
        return None
    rest = section[m_arc.end() :]
    m_dated = DATED_EVIDENCE_HEADING_RE.search(rest)
    if not m_dated:
        return rest.strip()
    return rest[: m_dated.start()].strip()


def parse_bullets_scored(section: str) -> list[ScoredBullet]:
    body = extract_dated_evidence_body(section)
    bullets: list[ScoredBullet] = []
    for rx in (BULLET_SCORE_STRICT_RE, BULLET_SCORE_LOOSE_RE):
        for m in rx.finditer(body):
            date = m.group(1)
            summary = normalize_space(m.group(3))
            source = normalize_space(m.group(4))
            strength = score_from_source_stub(source)
            bullets.append(
                ScoredBullet(date=date, summary=summary, source=source, strength=strength)
            )
        if bullets:
            break
    return bullets


def format_scored_bullet_line(b: ScoredBullet) -> list[str]:
    return [
        f"- **{b.date}** — [strength: {b.strength}] {b.summary}  ",
        f"  _Source:_ {b.source}",
    ]


def month_has_refined_headings(section: str) -> bool:
    return bool(DATED_EVIDENCE_HEADING_RE.search(section))


EMPTY_MONTH_LINE = "_No eligible evidence for this month._"


def render_month_plain(month: str, bullets: list[ScoredBullet]) -> str:
    counts = Counter(b.strength for b in bullets)
    lines: list[str] = [f"### {month}", ""]
    lines.append(
        f"_Strength mix:_ high={counts.get('high', 0)}, "
        f"medium={counts.get('medium', 0)}, low={counts.get('low', 0)}"
    )
    lines.append("")
    if not bullets:
        lines.append(EMPTY_MONTH_LINE)
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"
    for b in bullets:
        lines.extend(format_scored_bullet_line(b))
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_month_refined(
    month: str, has_arc_heading: bool, arc_raw: str, bullets: list[ScoredBullet]
) -> str:
    counts = Counter(b.strength for b in bullets)
    lines: list[str] = [f"### {month}", ""]
    if has_arc_heading:
        lines.append("#### Month-level arc")
        lines.append("")
        if arc_raw.strip():
            lines.append(arc_raw.rstrip())
            lines.append("")
    lines.append("#### Dated evidence")
    lines.append("")
    lines.append(
        f"_Strength mix:_ high={counts.get('high', 0)}, "
        f"medium={counts.get('medium', 0)}, low={counts.get('low', 0)}"
    )
    lines.append("")
    if not bullets:
        lines.append(EMPTY_MONTH_LINE)
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"
    for b in bullets:
        lines.extend(format_scored_bullet_line(b))
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_month(month: str, section: str, bullets: list[ScoredBullet]) -> str:
    if not month_has_refined_headings(section):
        return render_month_plain(month, bullets)
    has_arc = bool(MONTH_ARC_HEADING_RE.search(section))
    arc_raw = extract_month_arc_raw(section) if has_arc else ""
    return render_month_refined(month, has_arc, arc_raw, bullets)


def strip_preamble_meta_lines(preamble: str) -> str:
    """Remove prior strength key / score totals so we can re-insert fresh totals."""
    out: list[str] = []
    for line in preamble.splitlines():
        if line.startswith("**Strength key:**"):
            continue
        if line.startswith("**Score totals (window):**"):
            continue
        out.append(line)
    return "\n".join(out).rstrip()


def augment_preamble(preamble: str, totals: Counter) -> str:
    base = strip_preamble_meta_lines(preamble)
    sk = (
        "**Strength key:** `high` = `transcript:` or `days:`; "
        "`medium` = `knot:`; `low` = `git:` or unrecognized stub."
    )
    tot = (
        f"**Score totals (window):** high={totals.get('high', 0)}, "
        f"medium={totals.get('medium', 0)}, low={totals.get('low', 0)}."
    )
    return base + "\n\n" + sk + "\n" + tot + "\n"


def render_scored_block(expert_id: str, original_full_block: str) -> Optional[str]:
    inner = inner_content(original_full_block, expert_id)
    if not has_month_sections(inner):
        return None

    preamble, month_tail = preamble_before_first_month(inner)
    month_sections = parse_month_sections(month_tail)

    all_bullets: list[ScoredBullet] = []
    for _m, section in sorted(month_sections.items()):
        all_bullets.extend(parse_bullets_scored(section))

    totals = Counter(b.strength for b in all_bullets)
    new_preamble = augment_preamble(preamble, totals)

    out: list[str] = [marker_block_start(expert_id)]
    out.extend(new_preamble.splitlines())
    if out[-1].strip() != "":
        out.append("")
    out.append("")

    for month in sorted(month_sections.keys()):
        section = month_sections[month]
        bullets = parse_bullets_scored(section)
        out.append(render_month(month, section, bullets).rstrip())
        out.append("")

    out.append(marker_block_end(expert_id))
    return "\n".join(out).rstrip() + "\n"


def splice_backfill(text: str, expert_id: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(marker_block_start(expert_id)) + r".*?" + re.escape(marker_block_end(expert_id)),
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
    from strategy_expert_corpus import expert_paths as _expert_paths
    thread_path = args.thread_path or _expert_paths(expert_id, NOTEBOOK_DIR)["thread"]
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

    scored = render_scored_block(expert_id, block)
    if scored is None:
        print(
            "No `### YYYY-MM` month sections in backfill — nothing to score "
            "(empty or italic-only window). Leaving file unchanged."
        )
        return 0

    if args.dry_run or not args.apply:
        print(scored)
        if not args.apply:
            print("\n(Not applied. Re-run with --apply to write into the thread file.)")
        return 0

    machine_before = extract_machine_block(text)
    if machine_before is None:
        raise SystemExit(
            f"Cannot find {THREAD_MARKER_START!r} … {THREAD_MARKER_END!r}; abort."
        )

    updated = splice_backfill(text, expert_id, scored)
    machine_after = extract_machine_block(updated)
    if machine_after != machine_before:
        raise SystemExit(
            "Refusing to write: machine extraction block would change. Report as bug."
        )

    if updated == text:
        print("No changes needed.")
        return 0

    thread_path.write_text(updated, encoding="utf-8")
    print(f"Scored backfill block in {thread_path.relative_to(REPO_ROOT)}")
    print("Machine extraction block unchanged (verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
