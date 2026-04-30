#!/usr/bin/env python3
"""
Coffee Step 1 — one-line "next task" hints for work-cici and work-dev.

Used by operator_coffee.py after session load. Sources are markdown on disk;
operators maintain canonical surfaces (SYNC-DAILY, workspace § Next actions).

Usage:
    python3 scripts/coffee_lane_next_hints.py
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _extract_next_actions_section(text: str) -> str | None:
    m = re.search(r"^## Next actions\s*$", text, re.MULTILINE)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    m2 = re.search(r"^## \S", rest, re.MULTILINE)
    return rest[: m2.start()] if m2 else rest


def next_work_dev_line(repo: Path) -> str:
    path = repo / "docs/skill-work/work-dev/workspace.md"
    if not path.is_file():
        return "Next work-dev: missing docs/skill-work/work-dev/workspace.md"
    text = path.read_text(encoding="utf-8")
    section = _extract_next_actions_section(text)
    if section is None:
        return "Next work-dev: add a ## Next actions section to workspace.md"
    for raw in section.splitlines():
        line = raw.strip()
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if not m:
            continue
        body = m.group(2).strip()
        if not body:
            continue
        # Skip completed / struck-through items (workspace convention)
        if body.startswith("~~"):
            continue
        # Trim length for terminal paste
        short = body.replace("\n", " ")
        if len(short) > 220:
            short = short[:217] + "…"
        return f"Next work-dev (#{m.group(1)}): {short}"
    return (
        "Next work-dev: no open item in workspace.md § Next actions — "
        "add a numbered line or refresh Operator path"
    )


def _sync_daily_combined_block(text: str) -> str | None:
    if "### 3) Combined next action" not in text:
        return None
    i = text.index("### 3) Combined next action")
    tail = text[i:]
    # Stop at next major section (--- or ## at column 0 after a newline)
    end = re.search(r"\n---\s*\n", tail)
    chunk = tail[: end.start()] if end else tail.split("\n## ", 1)[0]
    return chunk


# SYNC-DAILY sibling bullets — stop scanning before treating these as task text
_SYNC_SIBLING_FIELD = re.compile(
    r"^(owner|done by|status|selected|lane|action|card path)\s*:",
    re.I,
)


def _first_filled_after_label(lines: list[str], label_lower: str) -> str | None:
    for i, raw in enumerate(lines):
        low = raw.lower()
        if label_lower in low and ":" in raw:
            after = raw.split(":", 1)[1].strip()
            if after and not after.startswith("`"):
                return after
            # Value may be on following bullet lines (not sibling form rows)
            j = i + 1
            while j < len(lines):
                ln = lines[j].strip()
                if not ln:
                    j += 1
                    continue
                if ln.startswith("- "):
                    inner = ln[2:].strip()
                    if _SYNC_SIBLING_FIELD.match(inner):
                        break
                    if inner:
                        return inner
                if ln.startswith("#") or ln.startswith("---"):
                    break
                j += 1
    return None


def _hint_from_sync_daily(text: str) -> str | None:
    stale = _sync_daily_stale_reason(text)
    if stale:
        return stale
    block = _sync_daily_combined_block(text)
    if not block:
        return None
    lines = block.splitlines()
    return _first_filled_after_label(lines, "top sync task")


def _sync_daily_stale_reason(text: str, *, today: date | None = None) -> str | None:
    """Return a human action line when SYNC-DAILY should not be treated as fresh."""
    if re.search(r"stale sync state:\*\*\s*`yes`", text, re.I):
        return "SYNC-DAILY is stale; run forced work-dev/work-politics mirror relevance scans before using mirror recommendations."
    m = re.search(r"Date:\s*\*\*(\d{4}-\d{2}-\d{2})\*\*", text)
    if not m:
        return None
    try:
        snapshot_day = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None
    current = today or date.today()
    if (current - snapshot_day).days > 3:
        return "SYNC-DAILY is older than 3 days; mark stale and run forced work-dev/work-politics mirror relevance scans."
    return None


def _first_active_watch(repo: Path) -> str | None:
    path = repo / "docs/skill-work/work-cici/WORK-LEDGER.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if "## II-A. ACTIVE WATCHES" not in text:
        return None
    chunk = text.split("## II-A. ACTIVE WATCHES", 1)[1]
    m = re.search(r"\*\*Watch:\*\*\s*(.+)", chunk)
    if m:
        return m.group(1).strip()
    return None


def next_work_cici_line(repo: Path) -> str:
    sync_path = repo / "docs/skill-work/work-cici/SYNC-DAILY.md"
    if sync_path.is_file():
        st = _hint_from_sync_daily(sync_path.read_text(encoding="utf-8"))
        if st:
            short = st.replace("\n", " ")
            if len(short) > 220:
                short = short[:217] + "…"
            return f"Next work-cici (SYNC-DAILY): {short}"
    w = _first_active_watch(repo)
    if w:
        short = w if len(w) <= 220 else w[:217] + "…"
        return f"Next work-cici (WORK-LEDGER watch): {short}"
    return (
        "Next work-cici: fill SYNC-DAILY § Combined next action or WORK-LEDGER "
        "— see docs/skill-work/work-cici/INDEX.md"
    )


def format_lane_next_hints(repo: Path | None = None) -> str:
    root = repo or REPO_ROOT
    x = next_work_cici_line(root)
    d = next_work_dev_line(root)
    return f"{x}\n{d}"


def main() -> int:
    p = argparse.ArgumentParser(description="Print work-cici + work-dev next-task hints for coffee.")
    p.add_argument(
        "--repo",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    args = p.parse_args()
    print(format_lane_next_hints(args.repo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
