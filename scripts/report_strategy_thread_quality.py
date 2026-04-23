#!/usr/bin/env python3
"""Strategy thread extraction quality report.

Read-only diagnostic: examines the 21-expert thread ecosystem and flags
coverage gaps, roster drift, stale threads, extraction density outliers,
missing companion files, and batch-analysis alignment issues.

Writes nothing canonical. Optional ``--log-miss`` records gaps to the
retrieval-miss ledger (runtime/retrieval-misses/index.jsonl).

WORK only; not Record.

Usage::

    python3 scripts/report_strategy_thread_quality.py
    python3 scripts/report_strategy_thread_quality.py --json
    python3 scripts/report_strategy_thread_quality.py --log-miss
    python3 scripts/report_strategy_thread_quality.py --days 14
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    THREAD_MARKER_END,
    THREAD_MARKER_START,
    _EXPERT_IDS_SET,
    parse_commentator_index,
    read_transcript_content,
    verify_index_alignment,
)
from strategy_expert_transcript import parse_transcript_file

DEFAULT_NOTEBOOK_DIR = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_THREADS_INDEX = DEFAULT_NOTEBOOK_DIR / "strategy-commentator-threads.md"
DEFAULT_INBOX = DEFAULT_NOTEBOOK_DIR / "daily-strategy-inbox.md"

_RE_THREAD_TAG = re.compile(r"thread:([a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*)")
_RE_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------

@dataclass
class ExpertDiagnostic:
    expert_id: str
    profile_exists: bool = True
    transcript_exists: bool = True
    thread_exists: bool = True
    transcript_line_count: int = 0
    machine_layer_line_count: int = 0
    transcript_dates: list[str] = field(default_factory=list)
    newest_transcript_date: str | None = None
    stale: bool = False
    coverage_gap: bool = False
    density_ratio: float | None = None
    issues: list[str] = field(default_factory=list)


@dataclass
class RosterDrift:
    ok: bool = True
    missing_from_table: list[str] = field(default_factory=list)
    extra_in_table: list[str] = field(default_factory=list)
    order_mismatch: bool = False


@dataclass
class BatchAlignmentIssue:
    line_number: int
    raw_tag: str
    reason: str


@dataclass
class QualityReport:
    generated_at: str = ""
    lookback_days: int = 7
    expert_count: int = len(CANONICAL_EXPERT_IDS)
    roster_drift: RosterDrift = field(default_factory=RosterDrift)
    experts: list[ExpertDiagnostic] = field(default_factory=list)
    batch_alignment_issues: list[BatchAlignmentIssue] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def _check_missing_files(expert_id: str, notebook_dir: Path) -> ExpertDiagnostic:
    """Check whether profile, transcript, and thread files exist."""
    diag = ExpertDiagnostic(expert_id=expert_id)

    from strategy_expert_corpus import (
        expert_paths as _expert_paths,
        expert_thread_paths_for_discovery,
        uses_monthly_thread_layout,
    )
    ep = _expert_paths(expert_id, notebook_dir)
    profile = ep["profile"]
    transcript = ep["transcript"]
    thread = ep["thread"]

    if not profile.is_file():
        diag.profile_exists = False
        diag.issues.append("missing profile file")
    if not transcript.is_file():
        diag.transcript_exists = False
        diag.issues.append("missing transcript file")
    if uses_monthly_thread_layout(notebook_dir, expert_id):
        diag.thread_exists = all(
            p.is_file() for p in expert_thread_paths_for_discovery(notebook_dir, expert_id)
        )
        if not diag.thread_exists:
            diag.issues.append("missing one or more monthly thread files")
    elif not thread.is_file():
        diag.thread_exists = False
        diag.issues.append("missing thread file")

    return diag


def _check_transcript_content(diag: ExpertDiagnostic, notebook_dir: Path, cutoff: date) -> None:
    """Populate transcript stats and staleness."""
    from strategy_expert_corpus import expert_paths as _expert_paths
    transcript_path = _expert_paths(diag.expert_id, notebook_dir)["transcript"]
    if not transcript_path.is_file():
        diag.stale = True
        return

    _, sections = parse_transcript_file(transcript_path)
    total_lines = 0
    dates: list[str] = []
    for date_str, lines in sections.items():
        content_lines = [ln for ln in lines if ln.strip() and not ln.startswith("## ")]
        total_lines += len(content_lines)
        dates.append(date_str)

    diag.transcript_line_count = total_lines
    diag.transcript_dates = sorted(dates, reverse=True)
    diag.newest_transcript_date = diag.transcript_dates[0] if diag.transcript_dates else None

    if diag.newest_transcript_date:
        try:
            newest = datetime.strptime(diag.newest_transcript_date, "%Y-%m-%d").date()
            if newest < cutoff:
                diag.stale = True
                diag.issues.append(f"stale: newest transcript date {diag.newest_transcript_date} before cutoff {cutoff}")
        except ValueError:
            pass
    else:
        diag.stale = True
        diag.issues.append("stale: no dated sections in transcript")


def _check_machine_layer(diag: ExpertDiagnostic, notebook_dir: Path) -> None:
    """Count machine layer lines and detect coverage gaps."""
    from strategy_expert_corpus import expert_thread_paths_for_discovery

    total_lines = 0
    any_markers = False
    no_material_marker = "_(No transcript or page material for extraction.)_"
    for thread_path in expert_thread_paths_for_discovery(notebook_dir, diag.expert_id):
        if not thread_path.is_file():
            continue
        text = thread_path.read_text(encoding="utf-8")
        if THREAD_MARKER_START not in text or THREAD_MARKER_END not in text:
            continue
        any_markers = True
        _, after_start = text.split(THREAD_MARKER_START, 1)
        inner, _ = after_start.split(THREAD_MARKER_END, 1)
        machine_lines = [ln for ln in inner.strip().splitlines() if ln.strip()]
        if len(machine_lines) == 1 and no_material_marker in machine_lines[0]:
            continue
        total_lines += len(machine_lines)

    diag.machine_layer_line_count = total_lines
    if diag.transcript_line_count > 0 and not any_markers:
        diag.coverage_gap = True
        diag.issues.append(
            "coverage gap: transcript has content but thread file(s) have no machine-layer markers"
        )
    elif diag.transcript_line_count > 0 and total_lines == 0:
        diag.coverage_gap = True
        diag.issues.append("coverage gap: transcript has content but machine layer is empty")


def _compute_density(diag: ExpertDiagnostic) -> None:
    """Compute extraction density ratio."""
    if diag.transcript_line_count > 0:
        diag.density_ratio = round(diag.machine_layer_line_count / diag.transcript_line_count, 2)


def _check_roster_drift(threads_index: Path) -> RosterDrift:
    """Compare strategy-commentator-threads.md table against CANONICAL_EXPERT_IDS.

    Falls back to a direct regex scan of ``| `slug` |`` rows when
    ``parse_commentator_index`` returns an empty order (header mismatch).
    """
    drift = RosterDrift()

    if not threads_index.is_file():
        drift.ok = False
        drift.missing_from_table = list(CANONICAL_EXPERT_IDS)
        return drift

    try:
        order, main_rows, _ = parse_commentator_index(threads_index)
    except Exception as exc:
        drift.ok = False
        drift.missing_from_table = [f"(parse error: {exc})"]
        return drift

    if not order:
        order = _fallback_roster_scan(threads_index)

    # Wire the existing verify_index_alignment() — it raises SystemExit on
    # drift, which we catch and convert to report-friendly data.
    if order and main_rows:
        try:
            verify_index_alignment(order, main_rows=main_rows)
        except SystemExit:
            pass  # drift detected; handled below via set comparison

    parsed_set = frozenset(order)
    expected = _EXPERT_IDS_SET

    drift.missing_from_table = sorted(expected - parsed_set)
    drift.extra_in_table = sorted(parsed_set - expected)
    # Order mismatch only meaningful when all canonical IDs are present
    drift.order_mismatch = (
        not drift.missing_from_table
        and not drift.extra_in_table
        and tuple(order) != CANONICAL_EXPERT_IDS
    )
    drift.ok = not drift.missing_from_table and not drift.extra_in_table

    return drift


_RE_TABLE_SLUG = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|")
_RE_ROSTER_HEADER = re.compile(r"^\|\s*expert_id\s*\|\s*Name\b.*Role", re.IGNORECASE)


def _fallback_roster_scan(threads_index: Path) -> list[str]:
    """Regex scan for ``| `slug` |`` rows in the main roster table only.

    Locates the roster table by its ``| expert_id | Name | Role …`` header,
    then collects slugs until a blank line or non-table line ends the block.
    """
    text = threads_index.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_roster = False
    seen: set[str] = set()
    order: list[str] = []

    for line in lines:
        if not in_roster:
            if _RE_ROSTER_HEADER.match(line):
                in_roster = True
            continue

        if line.startswith("|---"):
            continue

        m = _RE_TABLE_SLUG.match(line)
        if m:
            slug = m.group(1)
            if slug not in seen:
                seen.add(slug)
                order.append(slug)
        elif line.strip() and not line.startswith("|"):
            break

    return order


def _check_batch_alignment(inbox_path: Path) -> list[BatchAlignmentIssue]:
    """Check batch-analysis lines for thread tags that aren't in the canonical roster."""
    issues: list[BatchAlignmentIssue] = []

    if not inbox_path.is_file():
        return issues

    text = inbox_path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), start=1):
        if "batch-analysis" not in line.lower():
            continue
        tags = _RE_THREAD_TAG.findall(line)
        for tag in tags:
            if tag not in _EXPERT_IDS_SET:
                issues.append(BatchAlignmentIssue(
                    line_number=i,
                    raw_tag=tag,
                    reason=f"thread:{tag} not in CANONICAL_EXPERT_IDS",
                ))

    return issues


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(
    *,
    notebook_dir: Path,
    threads_index: Path,
    inbox_path: Path,
    lookback_days: int,
    today: date | None = None,
) -> QualityReport:
    today = today or datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=lookback_days)

    report = QualityReport(
        generated_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        lookback_days=lookback_days,
    )

    report.roster_drift = _check_roster_drift(threads_index)

    for expert_id in CANONICAL_EXPERT_IDS:
        diag = _check_missing_files(expert_id, notebook_dir)
        _check_transcript_content(diag, notebook_dir, cutoff)
        _check_machine_layer(diag, notebook_dir)
        _compute_density(diag)
        report.experts.append(diag)

    report.batch_alignment_issues = _check_batch_alignment(inbox_path)

    stale = sum(1 for e in report.experts if e.stale)
    coverage_gap = sum(1 for e in report.experts if e.coverage_gap)
    missing_files = sum(1 for e in report.experts if not e.profile_exists or not e.transcript_exists or not e.thread_exists)
    total_issues = sum(len(e.issues) for e in report.experts)

    report.summary = {
        "total_experts": len(CANONICAL_EXPERT_IDS),
        "stale_threads": stale,
        "coverage_gaps": coverage_gap,
        "missing_files": missing_files,
        "batch_alignment_issues": len(report.batch_alignment_issues),
        "total_issues": total_issues + len(report.batch_alignment_issues),
        "roster_drift_ok": report.roster_drift.ok,
    }

    return report


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_markdown(report: QualityReport) -> str:
    lines: list[str] = []
    lines.append("# Strategy thread quality report\n")
    lines.append(f"Generated: {report.generated_at}  ")
    lines.append(f"Lookback: {report.lookback_days} days\n")

    s = report.summary
    lines.append("## Summary\n")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Experts | {s['total_experts']} |")
    lines.append(f"| Stale threads | {s['stale_threads']} |")
    lines.append(f"| Coverage gaps | {s['coverage_gaps']} |")
    lines.append(f"| Missing files | {s['missing_files']} |")
    lines.append(f"| Batch alignment issues | {s['batch_alignment_issues']} |")
    lines.append(f"| Roster drift | {'ok' if s['roster_drift_ok'] else 'DRIFT'} |")
    lines.append(f"| Total issues | {s['total_issues']} |")
    lines.append("")

    if not report.roster_drift.ok:
        lines.append("## Roster drift\n")
        if report.roster_drift.missing_from_table:
            lines.append(f"Missing from table: {', '.join(report.roster_drift.missing_from_table)}")
        if report.roster_drift.extra_in_table:
            lines.append(f"Extra in table: {', '.join(report.roster_drift.extra_in_table)}")
        if report.roster_drift.order_mismatch:
            lines.append("Row order does not match CANONICAL_EXPERT_IDS tuple.")
        lines.append("")

    flagged = [e for e in report.experts if e.issues]
    if flagged:
        lines.append("## Flagged experts\n")
        for e in flagged:
            lines.append(f"### `{e.expert_id}`\n")
            lines.append(f"- Transcript lines: {e.transcript_line_count}")
            lines.append(f"- Machine layer lines: {e.machine_layer_line_count}")
            if e.density_ratio is not None:
                lines.append(f"- Density ratio: {e.density_ratio}")
            if e.newest_transcript_date:
                lines.append(f"- Newest transcript date: {e.newest_transcript_date}")
            for issue in e.issues:
                lines.append(f"- **{issue}**")
            lines.append("")

    if report.batch_alignment_issues:
        lines.append("## Batch-analysis alignment\n")
        for bi in report.batch_alignment_issues:
            lines.append(f"- Line {bi.line_number}: `thread:{bi.raw_tag}` — {bi.reason}")
        lines.append("")

    clean = [e for e in report.experts if not e.issues]
    if clean:
        lines.append("## Clean experts\n")
        for e in clean:
            density_str = f", density {e.density_ratio}" if e.density_ratio is not None else ""
            lines.append(
                f"- `{e.expert_id}` — transcript {e.transcript_line_count} lines, "
                f"machine {e.machine_layer_line_count} lines{density_str}"
            )
        lines.append("")

    return "\n".join(lines)


def format_json(report: QualityReport) -> str:
    return json.dumps(asdict(report), indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Miss ledger integration
# ---------------------------------------------------------------------------

def log_misses_from_report(report: QualityReport) -> int:
    """Log coverage gaps and stale threads to retrieval-miss ledger. Returns count logged."""
    log_script = REPO_ROOT / "scripts" / "runtime" / "log_retrieval_miss.py"
    if not log_script.is_file():
        print("warning: log_retrieval_miss.py not found; skipping miss logging", file=sys.stderr)
        return 0

    logged = 0

    for e in report.experts:
        if e.coverage_gap:
            cmd = [
                sys.executable, str(log_script),
                "--surface", "notebook_lookup",
                "--query", f"strategy-expert-{e.expert_id} machine layer extraction",
                "--failure-class", "aggregation_failure",
                "--notes", f"Transcript has {e.transcript_line_count} lines but machine layer is empty",
                "--related-path", f"docs/skill-work/work-strategy/strategy-notebook/strategy-expert-{e.expert_id}-thread.md",
                "--related-path", f"docs/skill-work/work-strategy/strategy-notebook/strategy-expert-{e.expert_id}-transcript.md",
                "--lane", "work-strategy",
                "--recorded-by", "report_strategy_thread_quality",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logged += 1
                print(f"  miss logged: {e.expert_id} (coverage_gap)")
            else:
                print(f"  miss log failed for {e.expert_id}: {result.stderr.strip()}", file=sys.stderr)

        if e.stale and not e.coverage_gap:
            cmd = [
                sys.executable, str(log_script),
                "--surface", "notebook_lookup",
                "--query", f"strategy-expert-{e.expert_id} recent transcript content",
                "--failure-class", "stale_ranking",
                "--notes", f"No transcript content within lookback window; newest date: {e.newest_transcript_date or 'none'}",
                "--related-path", f"docs/skill-work/work-strategy/strategy-notebook/strategy-expert-{e.expert_id}-transcript.md",
                "--lane", "work-strategy",
                "--recorded-by", "report_strategy_thread_quality",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logged += 1
                print(f"  miss logged: {e.expert_id} (stale)")
            else:
                print(f"  miss log failed for {e.expert_id}: {result.stderr.strip()}", file=sys.stderr)

    for bi in report.batch_alignment_issues:
        cmd = [
            sys.executable, str(log_script),
            "--surface", "notebook_lookup",
            "--query", f"batch-analysis thread:{bi.raw_tag}",
            "--failure-class", "vocabulary_mismatch",
            "--notes", bi.reason,
            "--related-path", "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md",
            "--lane", "work-strategy",
            "--recorded-by", "report_strategy_thread_quality",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logged += 1
            print(f"  miss logged: thread:{bi.raw_tag} (batch alignment)")
        else:
            print(f"  miss log failed for thread:{bi.raw_tag}: {result.stderr.strip()}", file=sys.stderr)

    return logged


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--notebook-dir", type=Path, default=DEFAULT_NOTEBOOK_DIR)
    p.add_argument("--threads-index", type=Path, default=DEFAULT_THREADS_INDEX)
    p.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    p.add_argument("--days", type=int, default=7, help="Lookback window for staleness (default 7)")
    p.add_argument("--today", help="Override today (YYYY-MM-DD)")
    p.add_argument("--json", action="store_true", help="Output as JSON instead of markdown")
    p.add_argument("--log-miss", action="store_true", dest="log_miss", help="Log gaps to retrieval-miss ledger")
    args = p.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else None

    report = build_report(
        notebook_dir=args.notebook_dir,
        threads_index=args.threads_index,
        inbox_path=args.inbox,
        lookback_days=max(1, args.days),
        today=today,
    )

    if args.json:
        print(format_json(report))
    else:
        print(format_markdown(report))

    if args.log_miss:
        count = log_misses_from_report(report)
        print(f"\n{count} miss(es) logged to retrieval-miss ledger.")

    total = report.summary.get("total_issues", 0)
    return 1 if total > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
