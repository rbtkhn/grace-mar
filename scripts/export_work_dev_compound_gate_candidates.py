#!/usr/bin/env python3
"""
Read-only export: aggregate compound notes with gate_candidate set into one markdown
artifact. Does not call stage_gate_candidate.py; does not edit notes or Record paths.
Stdlib only.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from work_dev.compound_notes import (  # noqa: E402
    NOTES_DIR,
    REPO_ROOT,
    extract_h2_section,
    gate_candidate_truthy,
    parse_note_for_export,
)

DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev-compound-gate-candidates.md"

DEFAULT_GATE_DISCLAIMER = (
    "No explicit gate action is stated in the note body. This remains a **work-only** "
    "learning artifact until you choose to review it in the normal companion gate process."
)
STAGING_LINE = (
    "Manual review only. No automatic promotion to Record, SELF, SKILLS, EVIDENCE, "
    "or `recursion-gate` from this export."
)


def _section_or_not_provided(s: str) -> str:
    t = (s or "").strip()
    return t if t else "Not provided."


def _resolve(p: Path, root: Path) -> Path:
    if p.is_absolute():
        return p
    return (root / p).resolve()


def _fmt_list(items: list[str]) -> str:
    if not items:
        return "_(none listed)_"
    if len(items) == 1:
        return f"`{items[0]}`"
    return ", ".join(f"`{x}`" for x in items)


def _sort_key(rec: dict[str, Any]) -> tuple[str, str]:
    d = (rec.get("date") or "")[:10]
    title = str(rec.get("title") or "")
    return (d, title)


def build_markdown(
    records: list[dict[str, Any]],
    include_all: bool,
    empty_reason: str | None = None,
) -> str:
    lines: list[str] = []
    lines.append("# Work-dev compound notes — gate candidate export")
    lines.append("")
    lines.append("> **Boundary:** This file is a **derived staging aid**. It is not ")
    lines.append("> canonical memory, not an **approval**, and does not promote anything ")
    lines.append("> to the Record, SELF, SKILLS, EVIDENCE, the Library, or the recursion gate.")
    lines.append("> **Appearing in this list is not the same as companion approval** — it ")
    lines.append("> is only a consolidated view of notes that *request* or *warrant* review.")
    lines.append("")
    lines.append(
        f"**Generated (UTC date):** {date.today().isoformat()}"
    )
    lines.append("")

    if empty_reason:
        lines.append("## Status")
        lines.append("")
        lines.append(empty_reason)
        lines.append("")
        return "\n".join(lines) + "\n"

    if not include_all:
        cands = [r for r in records if r.get("gate_candidate")]
        if not cands and records:
            lines.append("## Status")
            lines.append("")
            lines.append(
                "No `gate_candidate` notes matched in this run (treat as **false** or "
                "unset for every scanned file). This export is intentionally empty. "
                "Re-run with `--include-all` to list every note with an explicit flag line."
            )
            lines.append("")
            return "\n".join(lines) + "\n"

    work: list[dict[str, Any]] = (
        records if include_all else [r for r in records if r.get("gate_candidate")]
    )
    for rec in sorted(work, key=_sort_key):
        title = str(rec.get("title") or rec.get("name") or "untitled")
        body = str(rec.get("body") or "")
        meta: dict[str, Any] = rec.get("meta") or {}

        lines.append("---")
        lines.append("")
        lines.append(f"**Candidate:** {title}")
        if include_all:
            raw_gc = (meta or {}).get("gate_candidate", False)
            lines.append(
                f"- **gate_candidate:** {str(gate_candidate_truthy(raw_gc)).lower()}"
            )
        lines.append(f"- **date:** {rec.get('date') or '_(not set)_'}")
        lines.append(f"- **source:** `{rec.get('path', '')}`")
        lines.append(f"- **source_pr:** {rec.get('source_pr') or '_(not set)_'}")
        lines.append(f"- **source_commit:** {rec.get('source_commit') or '_(not set)_'}")
        lines.append(
            f"- **problem_type:** {rec.get('problem_type') or '_(not set)_'}"
        )
        lines.append(
            f"- **self_catching_test:** {rec.get('self_catching_test') or 'unknown'}"
        )
        lines.append(f"- **affected_files:** {_fmt_list(list(rec.get('affected_files') or []))}")
        lines.append("")

        pat_fm = str(meta.get("reusable_pattern", "") or "").strip()
        pat_h2 = extract_h2_section(body, "Reusable pattern")
        pattern_display = _section_or_not_provided(
            pat_fm or (pat_h2 or "").strip()
        )
        lines.append("### Reusable pattern")
        lines.append("")
        lines.append(pattern_display)
        lines.append("")

        lesson = extract_h2_section(body, "Reusable lesson")
        lines.append("### Reusable lesson")
        lines.append("")
        lines.append(_section_or_not_provided(lesson))
        lines.append("")

        gate_text = extract_h2_section(body, "Gate recommendation")
        lines.append("### Gate recommendation")
        lines.append("")
        if (gate_text or "").strip():
            lines.append((gate_text or "").strip())
        else:
            lines.append(DEFAULT_GATE_DISCLAIMER)
        lines.append("")

        lines.append("### Proposed staging disposition")
        lines.append("")
        lines.append(STAGING_LINE)
        lines.append("")

    return "\n".join(lines) + "\n"


def _gather_simplified(notes_dir: Path) -> tuple[list[dict[str, Any]], str | None]:
    if not notes_dir.is_dir():
        return (
            [],
            f"No `{notes_dir.relative_to(REPO_ROOT)}` directory yet. Create notes with `python3 scripts/new_work_dev_compound_note.py`.",
        )
    files = sorted(notes_dir.glob("*.md"))
    if not files:
        return (
            [],
            f"No `.md` files in `{notes_dir.relative_to(REPO_ROOT)}`.",
        )
    out: list[dict[str, Any]] = []
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        if not t.lstrip().startswith("---"):
            continue
        rec = parse_note_for_export(p)
        if not rec:
            continue
        out.append(rec)
    return (out, None)


def run_export(
    notes_dir: Path,
    include_all: bool,
) -> str:
    records, err = _gather_simplified(notes_dir)
    if err:
        return build_markdown([], include_all, empty_reason=err)
    if not records:
        return build_markdown(
            [],
            include_all,
            empty_reason="No valid compound notes (expected YAML front matter starting with `---`) were found.",
        )
    return build_markdown(records, include_all, empty_reason=None)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Export gate_candidate compound notes to a single markdown file",
    )
    ap.add_argument(
        "--notes-dir",
        type=Path,
        default=NOTES_DIR,
        help="Compound notes directory (default: docs/skill-work/work-dev/compound-notes)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output markdown (default: artifacts/work-dev-compound-gate-candidates.md)",
    )
    ap.add_argument(
        "--include-all",
        action="store_true",
        help="Include every note; each block shows gate_candidate as true or false",
    )
    args = ap.parse_args()
    nd = _resolve(args.notes_dir, REPO_ROOT)
    out = _resolve(args.output, REPO_ROOT)
    text = run_export(nd, include_all=bool(args.include_all))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
