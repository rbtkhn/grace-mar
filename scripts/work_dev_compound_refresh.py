#!/usr/bin/env python3
"""
Aggregate work-dev compound notes into a regenerable markdown report.
Read-only on notes. Writes only artifacts/work-dev-compound-refresh.md. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "compound-notes"
OUTPUT = REPO_ROOT / "artifacts" / "work-dev-compound-refresh.md"
STALE_DAYS = 90


def _parse_front_matter(text: str) -> dict[str, Any]:
    """Parse first --- ... --- block. Handles generated notes; no PyYAML."""
    if not text.lstrip().startswith("---"):
        return {}
    first = text.find("\n", text.index("---")) + 1
    end_idx = text.find("\n---\n", first)
    if end_idx == -1:
        return {}
    block = text[first:end_idx]
    data: dict[str, Any] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" not in line or not line.split(":", 1)[0].strip():
            i += 1
            continue
        key, rest = line.split(":", 1)
        key = key.strip()
        val = rest.strip()
        if key == "affected_files" and not val:
            j = i + 1
            acc: list[str] = []
            while j < len(lines) and lines[j].lstrip().startswith("- "):
                raw = lines[j].lstrip()
                if raw.startswith("- "):
                    acc.append(raw[2:].strip().strip("'\""))
                j += 1
            i = j
            data[key] = acc
            continue
        if key == "affected_files" and val == "[]":
            data[key] = []
        elif val == "[]":
            data[key] = []
        elif val == "true" or val == "false":
            data[key] = val == "true"
        else:
            s = val
            if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
                s = s[1:-1]
            data[key] = s
        i += 1
    return data


def _parse_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = _parse_front_matter(text)
    g = meta.get("gate_candidate", False)
    if isinstance(g, str):
        gate = g.lower() in ("true", "1", "yes")
    else:
        gate = bool(g)
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "name": path.name,
        "title": str(meta.get("title", path.stem)).strip("'\"") or path.stem,
        "date": str(meta.get("date", "")),
        "problem_type": str(meta.get("problem_type", "")).strip("'\""),
        "reusable_pattern": str(meta.get("reusable_pattern", "")).strip("'\""),
        "self_catching_test": str(meta.get("self_catching_test", "unknown")).strip("'\""),
        "gate_candidate": gate,
        "record_status": str(meta.get("record_status", "")).strip("'\""),
    }


def _parse_date_ymd(s: str) -> date | None:
    s = s[:10] if s else ""
    for fmt in ("%Y-%m-%d",):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            return None
    return None


def _normalize_dup_key(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower()) if s else ""


def run_report() -> str:
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
        return "\n".join(lines) + "\n"

    files = sorted(NOTES_DIR.glob("*.md"))
    if not files:
        lines.append("## Status")
        lines.append("")
        lines.append("No compound notes (`.md` files) in `compound-notes/`.")
        lines.append("")
        return "\n".join(lines) + "\n"

    records = [_parse_file(f) for f in files]
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

    # Stale: >90d, not gate
    today = date.today()
    stale: list[dict] = []
    for r in records:
        d = _parse_date_ymd(r["date"])
        if d is None or r["gate_candidate"]:
            continue
        if (today - d).days > STALE_DAYS:
            stale.append(r)
    lines.append("### Stale (heuristic: older than 90 days, not gate candidate)")
    lines.append("")
    if not stale:
        lines.append("_(none in this run)_")
    else:
        for r in sorted(stale, key=lambda x: x["date"] or ""):
            lines.append(
                f"- review for staleness: [{r['name']}]({r['path']}) (date: {r['date']})"
            )
    lines.append("")

    # Duplicates: normalized title
    title_groups: dict[str, list[str]] = {}
    for r in records:
        nk = _normalize_dup_key(r["title"])
        if nk and nk not in ("compound note", "untitled"):
            title_groups.setdefault(nk, []).append(r["name"])
    dups = {k: v for k, v in title_groups.items() if len(v) > 1}
    lines.append("### Possible duplicate titles (normalized)")
    lines.append("")
    if not dups:
        lines.append("_(none detected)_")
    else:
        for k, v in sorted(dups.items(), key=lambda x: x[0]):
            lines.append(f"- `{k}`: {', '.join(v)}")

    pat_groups: dict[str, list[str]] = {}
    for r in records:
        p = r["reusable_pattern"]
        if p:
            pk = _normalize_dup_key(p)
            pat_groups.setdefault(pk, []).append(r["name"])
    pdups = {k: v for k, v in pat_groups.items() if len(v) > 1}
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
    return "\n".join(lines) + "\n"


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
