#!/usr/bin/env python3
"""
Derived operator dashboard for the work-dev compound layer.
Read-only; writes a single markdown file under artifacts/. Stdlib only.
Does not touch Record surfaces, recursion-gate.md, or stage_gate_candidate.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from work_dev.compound_notes import (  # noqa: E402
    NOTES_DIR,
    REPO_ROOT,
    STALE_DAYS,
    derived_compound_artifact_preamble,
    duplicate_pattern_groups,
    duplicate_title_groups,
    load_compound_records,
    compound_note_paths,
    parse_date_ymd,
    stale_non_gate_records,
)

DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev-compound-dashboard.md"

SECTION_IDS = (
    "boundary",
    "summary",
    "inventory",
    "gate",
    "stale",
    "duplicates",
    "reports",
    "docs",
    "scripts",
    "actions",
)

ARTIFACTS_CHECK = [
    "work-dev-compound-refresh.md",
    "work-dev-compound-gate-candidates.md",
    "work-dev-compound-dashboard.md",
]

DOCS_CHECK: list[tuple[str, str]] = [
    ("docs/skill-work/work-dev/three-compounding-loops.md", "Record vs WORK vs CI compounding"),
    ("docs/skill-work/work-dev/derived-regeneration.md", "Derived regeneration roadmap / rebuildability"),
    ("docs/skill-work/work-dev/compound-loop.md", "Compound work loop process and boundary"),
    ("docs/skill-work/work-dev/compound-gate-export.md", "Gate candidate export — boundary and command"),
    ("docs/skill-work/work-dev/reviewer-matrix.md", "Review lenses and promotion rules"),
    ("docs/skill-work/work-dev/compound-note-template.md", "Compound note front matter and sections"),
]

SCRIPTS_CHECK: list[tuple[str, str]] = [
    ("scripts/new_work_dev_compound_note.py", "python3 scripts/new_work_dev_compound_note.py --title \"…\""),
    ("scripts/work_dev_compound_refresh.py", "python3 scripts/work_dev_compound_refresh.py"),
    (
        "scripts/export_work_dev_compound_gate_candidates.py",
        "python3 scripts/export_work_dev_compound_gate_candidates.py",
    ),
    ("scripts/build_work_dev_compound_dashboard.py", "python3 scripts/build_work_dev_compound_dashboard.py"),
]


def _resolve(p: Path, root: Path) -> Path:
    if p.is_absolute():
        return p
    return (root / p).resolve()


def _parse_include_sections(raw: str | None) -> set[str] | None:
    if raw is None or not str(raw).strip():
        return None
    out: set[str] = set()
    for part in str(raw).split(","):
        k = part.strip().lower()
        if k in SECTION_IDS:
            out.add(k)
    return out if out else None


def _include(section: str, want: set[str] | None) -> bool:
    if want is None:
        return True
    return section in want


def _artifact_status(repo: Path, name: str) -> tuple[str, str, str]:
    p = repo / "artifacts" / name
    rel = str(p.relative_to(repo))
    if not p.is_file():
        return ("absent", rel, "—")
    try:
        ts = datetime.fromtimestamp(
            p.stat().st_mtime, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M UTC")
    except OSError:
        ts = "—"
    return ("present", rel, ts)


def _path_status(repo: Path, rel: str) -> tuple[str, str, str]:
    p = (repo / rel).resolve()
    try:
        rel2 = str(p.relative_to(repo))
    except ValueError:
        rel2 = rel
    if not p.is_file():
        return ("absent", rel2, "—")
    try:
        ts = datetime.fromtimestamp(
            p.stat().st_mtime, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M UTC")
    except OSError:
        ts = "—"
    return ("present", rel2, ts)


def _script_cmd(repo_root: Path, rel: str, suggested: str) -> str:
    p = repo_root / rel
    if p.is_file():
        return f"`{suggested}`"
    return "—"


def _newest_n_records(
    records: list[dict[str, Any]], n: int
) -> list[dict[str, Any]]:
    def sort_key(r: dict[str, Any]) -> tuple[str, str]:
        d = parse_date_ymd(str(r.get("date") or ""))
        dkey = d.isoformat() if d else "0000-00-00"
        return (dkey, str(r.get("title", "")))

    return sorted(records, key=sort_key, reverse=True)[:n]


def _month_key(date_str: str) -> str:
    s = (date_str or "")[:7]
    if len(s) == 7 and s[4] == "-":
        return s
    return "_(unparsed or missing)_"


def build_dashboard(
    repo_root: Path,
    notes_dir: Path,
    sections: set[str] | None,
) -> str:
    pre = derived_compound_artifact_preamble("work_dev_compound_dashboard")
    want = sections
    lines: list[str] = []
    today = date.today()
    lines.append("# Work-Dev Compound Dashboard")
    lines.append("")

    if _include("boundary", want):
        lines.append("> **Boundary:** This dashboard is a derived **WORK** artifact. It does not update")
        lines.append("> canonical **Record** surfaces, does not **approve** gate candidates, does not")
        lines.append("> write to `recursion-gate.md`, and does not **promote** anything into durable memory.")
        lines.append("")

    # Load notes
    if not notes_dir.is_dir():
        records: list[dict[str, Any]] = []
        notes_missing = True
    else:
        files = compound_note_paths(notes_dir)
        records = load_compound_records(notes_dir, repo_root) if files else []
        notes_missing = len(files) == 0

    n_total = len(records)
    n_gate = sum(1 for r in records if r.get("gate_candidate"))
    stale_dash = stale_non_gate_records(
        records, notes_dir, today, stale_days=STALE_DAYS, mtime_if_no_date=True
    )
    n_stale = len(stale_dash)
    dtitle = duplicate_title_groups(records)
    dpat = duplicate_pattern_groups(records)
    n_dup_title_groups = len(dtitle)
    n_dup_pat_groups = len(dpat)
    r_pres, _, _ = _artifact_status(repo_root, "work-dev-compound-refresh.md")
    g_pres, _, _ = _artifact_status(repo_root, "work-dev-compound-gate-candidates.md")

    if _include("summary", want):
        lines.append("## 1. Summary")
        lines.append("")
        lines.append(f"- **Generated (UTC date):** {today.isoformat()}")
        lines.append(f"- **Total compound notes:** {n_total}")
        lines.append(f"- **Gate-candidate notes (`gate_candidate` truthy):** {n_gate}")
        lines.append(
            f"- **Stale review candidates (>{STALE_DAYS}d, not gate, date or file mtime):** {n_stale}"
        )
        lines.append(
            f"- **Duplicate title groups (normalized, 2+ files):** {n_dup_title_groups}"
        )
        lines.append(
            f"- **Duplicate `reusable_pattern` groups (normalized, 2+ files):** {n_dup_pat_groups}"
        )
        lines.append(
            f"- **Refresh report artifact:** {'present' if r_pres == 'present' else 'absent'}"
        )
        lines.append(
            f"- **Gate-candidate export artifact:** {'present' if g_pres == 'present' else 'absent'}"
        )
        lines.append("")

    if _include("inventory", want):
        lines.append("## 2. Compound notes inventory")
        lines.append("")
        if notes_missing or n_total == 0:
            lines.append("There are **no** compound notes in the configured `compound-notes/` path, or the directory is missing. This is OK — add notes as you complete work.")
            lines.append("")
        else:
            by_pt = Counter(r["problem_type"] for r in records if r.get("problem_type"))
            lines.append("### By `problem_type`")
            lines.append("")
            if not by_pt:
                lines.append("_(none set)_")
            else:
                for k, c in sorted(by_pt.items(), key=lambda x: (-x[1], x[0])):
                    lines.append(f"- `{k}`: {c}")
            lines.append("")

            by_sct = Counter(r["self_catching_test"] for r in records)
            lines.append("### By `self_catching_test`")
            lines.append("")
            for k, c in sorted(by_sct.items(), key=lambda x: (-x[1], str(x[0]))):
                lines.append(f"- `{k}`: {c}")
            lines.append("")

            n_true = sum(1 for r in records if r.get("gate_candidate"))
            n_false = n_total - n_true
            lines.append("### By `gate_candidate` (normalized)")
            lines.append("")
            lines.append(f"- `true` / truthy: {n_true}")
            lines.append(f"- `false` / not truthy: {n_false}")
            lines.append("")

            by_month: Counter[str] = Counter()
            for r in records:
                by_month[_month_key(str(r.get("date") or ""))] += 1
            lines.append("### By month (from front matter `date`, first 7 chars)")
            lines.append("")
            for mkey in sorted(by_month.keys(), reverse=True):
                lines.append(f"- **{mkey}:** {by_month[mkey]}")
            lines.append("")

            lines.append("### Newest 10 notes (by `date` in front matter; missing dates sort last)")
            lines.append("")
            for r in _newest_n_records(records, 10):
                gc = "true" if r.get("gate_candidate") else "false"
                lines.append(
                    f"- **{r.get('date') or '_(no date)_'}** — {r.get('title', r.get('name'))} "
                    f"— `problem_type`: {r.get('problem_type') or '_(not set)_'} — "
                    f"`gate_candidate`: {gc} — `{r.get('path')}`"
                )
            lines.append("")

    if _include("gate", want):
        lines.append("## 3. Gate-candidate notes")
        lines.append("")
        lines.append(
            "> `gate_candidate: true` (or `yes`, etc.) means **review recommended**, not **approved**."
        )
        lines.append("")
        gate_list = [r for r in records if r.get("gate_candidate")]
        if not gate_list:
            lines.append("_(none)_")
        else:
            for r in sorted(
                gate_list, key=lambda x: (str(x.get("date") or ""), str(x.get("title", "")))
            ):
                lines.append(
                    f"- **{r.get('title', r.get('name'))}** — date: {r.get('date') or '—'} — "
                    f"`problem_type`: {r.get('problem_type') or '—'} — "
                    f"`self_catching_test`: {r.get('self_catching_test', 'unknown')} — "
                    f"`{r.get('path')}`"
                )
        lines.append("")

    if _include("stale", want):
        lines.append("## 4. Stale review candidates")
        lines.append("")
        lines.append(
            f"Notes older than **{STALE_DAYS}** days with `gate_candidate` false. "
            "If the front matter `date` is missing, **file mtime** is used for the age check."
        )
        lines.append("")
        if not stale_dash:
            lines.append("_(none)_")
        else:
            for r in stale_dash:
                eff = r.get("_effective_date", "—")
                src = r.get("_date_source", "—")
                lines.append(
                    f"- **{r.get('title', r.get('name'))}** — FM date: {r.get('date') or '—'} — "
                    f"effective: {eff} ({src}) — `{r.get('path')}`"
                )
        lines.append("")

    if _include("duplicates", want):
        lines.append("## 5. Duplicate hints (not modifications)")
        lines.append("")
        lines.append("Review only; this dashboard does not edit note files.")
        lines.append("")
        if not dtitle:
            lines.append("### Normalized title duplicates")
            lines.append("")
            lines.append("_(none detected)_")
        else:
            lines.append("### Normalized title duplicates")
            lines.append("")
            for k, v in sorted(dtitle.items(), key=lambda x: x[0]):
                lines.append(f"- `{k[:120]}`: {', '.join(v)}")
        lines.append("")
        if not dpat:
            lines.append("### Normalized `reusable_pattern` duplicates")
            lines.append("")
            lines.append("_(none detected)_")
        else:
            lines.append("### Normalized `reusable_pattern` duplicates")
            lines.append("")
            for k, v in sorted(dpat.items(), key=lambda x: x[0]):
                lines.append(f"- `{k[:120]}`: {', '.join(v)}")
        lines.append("")

    if _include("reports", want):
        lines.append("## 6. Generated reports (artifacts)")
        lines.append("")
        for name in ARTIFACTS_CHECK:
            st, rel, mts = _artifact_status(repo_root, name)
            lines.append(f"- **{name}** — {st} — `{rel}` — last modified: {mts}")
        lines.append("")

    if _include("docs", want):
        lines.append("## 7. Related work-dev compound docs")
        lines.append("")
        for rel, purpose in DOCS_CHECK:
            st, rel2, mts = _path_status(repo_root, rel)
            lines.append(
                f"- **{Path(rel).name}** — {st} — `{rel2}` — {purpose} — mtime: {mts}"
            )
        lines.append("")

    if _include("scripts", want):
        lines.append("## 8. Scripts (compound layer)")
        lines.append("")
        for rel, cmd in SCRIPTS_CHECK:
            p = repo_root / rel
            st = "present" if p.is_file() else "absent"
            c = _script_cmd(repo_root, rel, cmd) if p.is_file() else "—"
            lines.append(f"- **`{Path(rel).name}`** — {st} — `{rel}` — {c}")
        lines.append("")

    if _include("actions", want):
        lines.append("## 9. Suggested next actions")
        lines.append("")
        if not notes_dir.is_dir():
            lines.append(
                "- The `compound-notes/` path does not exist yet; add it when you start capturing sessions."
            )
        elif n_total == 0:
            lines.append(
                "- After the next completed PR, create the first real compound note: "
                "`python3 scripts/new_work_dev_compound_note.py --title \"…\"`"
            )
        if n_total > 0 and r_pres != "present":
            lines.append(
                "- Run `python3 scripts/work_dev_compound_refresh.py` to generate the refresh report."
            )
        if n_gate > 0 and g_pres != "present":
            lines.append(
                "- Run `python3 scripts/export_work_dev_compound_gate_candidates.py` to materialize the gate-candidate export."
            )
        if n_stale > 0:
            lines.append(
                "- Review **stale** non-gate notes before promoting new durable patterns elsewhere."
            )
        if n_dup_title_groups or n_dup_pat_groups:
            lines.append(
                "- If duplicates reflect the same lesson, **consolidate** conceptually in a new note; do not delete originals without operator approval."
            )
        lines.append(
            "- After **refresh** or **export** runs, regenerate this dashboard: "
            "`python3 scripts/build_work_dev_compound_dashboard.py`"
        )
        lines.append("")

    return pre + "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build work-dev compound layer operator dashboard (derived markdown)",
    )
    ap.add_argument(
        "--notes-dir",
        type=Path,
        default=NOTES_DIR,
        help="Compound notes directory (default: docs/.../compound-notes)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output markdown (default: artifacts/work-dev-compound-dashboard.md)",
    )
    ap.add_argument(
        "--include-sections",
        type=str,
        default="",
        help="Comma-separated: boundary,summary,inventory,…; omit = all",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: inferred from grace-mar layout)",
    )
    args = ap.parse_args()
    repo = (
        args.repo_root.resolve()
        if args.repo_root.is_absolute()
        else (REPO_ROOT / args.repo_root).resolve()
    )
    if args.notes_dir.is_absolute():
        nd = args.notes_dir.resolve()
    else:
        nd = (repo / args.notes_dir).resolve()
    if args.output.is_absolute():
        out = args.output.resolve()
    else:
        out = (repo / args.output).resolve()
    want = _parse_include_sections(args.include_sections.strip() or None)
    text = build_dashboard(repo, nd, want)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())