#!/usr/bin/env python3
"""
Aggregate work-dev compound notes into a regenerable markdown report.
Read-only on notes. Writes only artifacts/work-dev-compound-refresh.md. Stdlib only.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from work_dev.compound_notes import (
    NOTES_DIR,
    REPO_ROOT,
    STALE_DAYS,
    derived_compound_artifact_preamble,
    duplicate_pattern_groups,
    duplicate_title_groups,
    load_compound_records,
    compound_note_paths,
    stale_non_gate_records,
)

OUTPUT = REPO_ROOT / "artifacts" / "work-dev-compound-refresh.md"


def run_report() -> str:
    pre = derived_compound_artifact_preamble("work_dev_compound_refresh")
    lines: list[str] = []
    lines.append("# Work-dev compound notes — refresh report")
    lines.append("")
    lines.append("**Boundary:** This report is derived from work-dev compound notes. It does not")
    lines.append("update canonical Record surfaces and does not promote any item by itself.")
    lines.append("")
    lines.append(f"**Generated (UTC date):** {date.today().isoformat()}")
    lines.append("")

    if not NOTES_DIR.is_dir():
        lines.append("## Status")
        lines.append("")
        lines.append("No `compound-notes/` directory yet. Create a note with:")
        lines.append("")
        lines.append("```")
        lines.append("python3 scripts/new_work_dev_compound_note.py --title \"...\"")
        lines.append("```")
        lines.append("")
        return pre + "\n".join(lines) + "\n"

    files = compound_note_paths(NOTES_DIR)
    if not files:
        lines.append("## Status")
        lines.append("")
        lines.append("No compound notes (`.md` files) in `compound-notes/`.")
        lines.append("")
        return pre + "\n".join(lines) + "\n"

    records = load_compound_records(NOTES_DIR, REPO_ROOT)
    n = len(records)
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total notes:** {n}")
    lines.append("")

    by_pt = Counter(r["problem_type"] for r in records if r["problem_type"])
    lines.append("### By problem_type")
    lines.append("")
    if not by_pt:
        lines.append("_(no problem_type set)_")
    else:
        for k, c in sorted(by_pt.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- `{k}`: {c}")
    lines.append("")

    by_sct = Counter(r["self_catching_test"] for r in records)
    lines.append("### By self_catching_test")
    lines.append("")
    for k, c in sorted(by_sct.items(), key=lambda x: (-x[1], str(x[0]))):
        lines.append(f"- `{k}`: {c}")
    lines.append("")

    gate_tr = [r for r in records if r["gate_candidate"]]
    lines.append(f"### gate_candidate: true count: {len(gate_tr)}")
    lines.append("")
    for r in gate_tr:
        lines.append(f"- [{r['name']}]({r['path']}) — {r['title'][:80]}")
    lines.append("")

    today = date.today()
    stale = stale_non_gate_records(
        records, NOTES_DIR, today, stale_days=STALE_DAYS, mtime_if_no_date=False
    )
    lines.append("### Stale (heuristic: older than 90 days, not gate candidate)")
    lines.append("")
    if not stale:
        lines.append("_(none in this run)_")
    else:
        for r in stale:
            lines.append(
                f"- review for staleness: [{r['name']}]({r['path']}) (date: {r['date']})"
            )
    lines.append("")

    dups = duplicate_title_groups(records)
    lines.append("### Possible duplicate titles (normalized)")
    lines.append("")
    if not dups:
        lines.append("_(none detected)_")
    else:
        for k, v in sorted(dups.items(), key=lambda x: x[0]):
            lines.append(f"- `{k}`: {', '.join(v)}")

    pdups = duplicate_pattern_groups(records)
    lines.append("")
    lines.append("### Possible duplicate reusable_pattern (normalized)")
    lines.append("")
    if not pdups:
        lines.append("_(none detected)_")
    else:
        for k, v in sorted(pdups.items(), key=lambda x: x[0]):
            lines.append(f"- `{k[:120]}`: {', '.join(v)}")
    lines.append("")

    lines.append("### Recurring problem_type (2+ notes)")
    lines.append("")
    rec = {k: c for k, c in by_pt.items() if c >= 2}
    if not rec:
        lines.append("_(none)_")
    else:
        for k, c in sorted(rec.items(), key=lambda x: -x[1]):
            lines.append(f"- `{k}`: {c} notes")
    lines.append("")

    lines.append("## Recommended next actions")
    lines.append("")
    if stale:
        lines.append("- Open stale notes; archive, refresh content, or close as obsolete.")
    if dups or pdups:
        lines.append("- Merge or cross-link notes that cover the same lesson.")
    if gate_tr:
        lines.append(
            "- Review `gate_candidate: true` notes in the normal gate / companion workflow (no auto-promote)."
        )
    if not stale and not dups and not pdups and not rec:
        lines.append("- Add compound notes as you finish work; re-run this script occasionally.")
    lines.append("")
    return pre + "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Regenerate work-dev compound refresh report")
    ap.add_argument(
        "--output",
        type=Path,
        default=OUTPUT,
        help="Output markdown path (default: artifacts/work-dev-compound-refresh.md)",
    )
    args = ap.parse_args()
    out = args.output
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    text = run_report()
    out.write_text(text, encoding="utf-8", newline="\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
