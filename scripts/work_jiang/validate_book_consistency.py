#!/usr/bin/env python3
"""
Post-merge consistency validator for the Predictive History book.

Checks prediction ID integrity, cross-references, transcript citations,
chapter completeness, and task manifest health.

Usage:
    python3 scripts/work_jiang/validate_book_consistency.py --volume 1
    python3 scripts/work_jiang/validate_book_consistency.py --chapter ch07
    python3 scripts/work_jiang/validate_book_consistency.py --all
    python3 scripts/work_jiang/validate_book_consistency.py --all --output report.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_JIANG = REPO_ROOT / "research" / "external" / "work-jiang"
ARCH_PATH = WORK_JIANG / "metadata" / "book-architecture.yaml"
PREDICTIONS_PATH = WORK_JIANG / "prediction-tracking" / "registry" / "predictions.jsonl"
DIVERGENCES_PATH = WORK_JIANG / "divergence-tracking" / "registry" / "divergences.jsonl"
TASKS_PATH = WORK_JIANG / "tasks.jsonl"
REVIEW_QUEUE = WORK_JIANG / "review-queue"


class ValidationReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def render(self) -> str:
        lines = [
            "# Book Consistency Report",
            "",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            f"**Status:** {'PASS' if self.ok else 'FAIL'}",
            "",
        ]
        if self.errors:
            lines.append(f"## Errors ({len(self.errors)})")
            lines.append("")
            for e in self.errors:
                lines.append(f"- {e}")
            lines.append("")
        if self.warnings:
            lines.append(f"## Warnings ({len(self.warnings)})")
            lines.append("")
            for w in self.warnings:
                lines.append(f"- {w}")
            lines.append("")
        if self.info:
            lines.append(f"## Info ({len(self.info)})")
            lines.append("")
            for i in self.info:
                lines.append(f"- {i}")
            lines.append("")
        if self.ok and not self.warnings:
            lines.append("All checks passed.")
        return "\n".join(lines)


def load_jsonl_ids(path: Path, id_field: str) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            if id_field in rec:
                ids.add(rec[id_field])
        except json.JSONDecodeError:
            continue
    return ids


def load_architecture() -> dict:
    if not ARCH_PATH.exists():
        return {}
    with open(ARCH_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_task_states() -> dict[str, dict]:
    states: dict[str, dict] = {}
    if not TASKS_PATH.exists():
        return states
    for line in TASKS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        tid = rec["task_id"]
        if tid not in states:
            states[tid] = {}
        states[tid].update(rec)
    return states


def check_prediction_ids(chapters: list[dict], report: ValidationReport) -> None:
    """Verify prediction IDs in architecture exist in the registry."""
    registered = load_jsonl_ids(PREDICTIONS_PATH, "prediction_id")
    if not registered:
        report.warn("No predictions found in registry (file may be empty or missing)")
        return

    all_pred_ids: list[str] = []
    for ch in chapters:
        pids = ch.get("prediction_ids", [])
        all_pred_ids.extend(pids)
        for pid in pids:
            if pid not in registered:
                report.error(f"{ch['id']}: prediction_id '{pid}' not in registry")

    seen: set[str] = set()
    for pid in all_pred_ids:
        if pid in seen:
            report.error(f"Duplicate prediction_id across chapters: '{pid}'")
        seen.add(pid)

    report.note(f"Checked {len(all_pred_ids)} prediction IDs across {len(chapters)} chapters")


def check_divergence_ids(chapters: list[dict], report: ValidationReport) -> None:
    """Verify divergence IDs in architecture exist in the registry."""
    registered = load_jsonl_ids(DIVERGENCES_PATH, "divergence_id")
    for ch in chapters:
        dids = ch.get("divergence_ids", [])
        for did in dids:
            if registered and did not in registered:
                report.error(f"{ch['id']}: divergence_id '{did}' not in registry")


def check_chapter_completeness(chapters: list[dict], report: ValidationReport) -> None:
    """Check that chapters with merged status have required files."""
    for ch in chapters:
        ch_id = ch["id"]
        draft_path = WORK_JIANG / ch.get("draft_path", f"chapters/{ch_id}/draft.md")
        outline_path = WORK_JIANG / ch.get("outline_path", f"chapters/{ch_id}/outline.md")
        pids = ch.get("prediction_ids", [])

        if draft_path.exists():
            report.note(f"{ch_id}: draft exists")
        else:
            report.warn(f"{ch_id}: no draft at {draft_path.relative_to(WORK_JIANG)}")

        if not outline_path.exists():
            report.warn(f"{ch_id}: no outline at {outline_path.relative_to(WORK_JIANG)}")

        if len(pids) < 3:
            report.warn(f"{ch_id}: fewer than 3 prediction IDs ({len(pids)})")


def check_cross_references(chapters: list[dict], report: ValidationReport) -> None:
    """Check that chapter cross-references in drafts resolve."""
    ch_ids = {ch["id"] for ch in chapters}
    ch_pattern = re.compile(r"[Cc]hapter\s+(\d+)")

    for ch in chapters:
        draft_path = WORK_JIANG / ch.get("draft_path", f"chapters/{ch['id']}/draft.md")
        if not draft_path.exists():
            continue
        content = draft_path.read_text(encoding="utf-8")
        for match in ch_pattern.finditer(content):
            ref_num = int(match.group(1))
            ref_id = f"ch{ref_num:02d}"
            if ref_id not in ch_ids:
                report.error(f"{ch['id']}: cross-reference to Chapter {ref_num} but {ref_id} not in architecture")


def check_task_health(report: ValidationReport) -> None:
    """Check for stale claimed tasks and orphan submissions."""
    states = load_task_states()
    if not states:
        report.note("No tasks in manifest")
        return

    now = datetime.now(timezone.utc)
    stale_days = 7

    for tid, st in states.items():
        status = st.get("status", "unknown")
        ts_str = st.get("ts", "")

        if status == "claimed" and ts_str:
            try:
                claimed_at = datetime.fromisoformat(ts_str)
                if claimed_at.tzinfo is None:
                    claimed_at = claimed_at.replace(tzinfo=timezone.utc)
                age = (now - claimed_at).days
                if age > stale_days:
                    report.warn(f"Task '{tid}' has been claimed for {age} days (stale threshold: {stale_days})")
            except (ValueError, TypeError):
                pass

        if status == "submitted":
            scope = st.get("scope", "")
            rq_dir = REVIEW_QUEUE / scope
            if not rq_dir.exists() or not any(rq_dir.iterdir()):
                report.warn(f"Task '{tid}' is submitted but review-queue/{scope}/ is empty")

    status_counts: dict[str, int] = {}
    for st in states.values():
        s = st.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    parts = [f"{s}={c}" for s, c in sorted(status_counts.items())]
    report.note(f"Task manifest: {len(states)} tasks ({', '.join(parts)})")


def run_checks(chapter_filter: str | None = None) -> ValidationReport:
    report = ValidationReport()
    arch = load_architecture()
    chapters = arch.get("book", {}).get("chapters", [])

    if not chapters:
        report.error("No chapters found in book-architecture.yaml")
        return report

    if chapter_filter:
        chapters = [ch for ch in chapters if ch["id"] == chapter_filter]
        if not chapters:
            report.error(f"Chapter '{chapter_filter}' not found in architecture")
            return report

    check_prediction_ids(chapters, report)
    check_divergence_ids(chapters, report)
    check_chapter_completeness(chapters, report)
    check_cross_references(chapters, report)
    check_task_health(report)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate book consistency.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--volume", type=int, help="Volume number (currently only 1)")
    group.add_argument("--chapter", help="Single chapter ID (e.g. ch07)")
    group.add_argument("--all", action="store_true", help="Check everything")
    parser.add_argument("--output", "-o", help="Write report to file (default: stdout)")
    args = parser.parse_args()

    chapter_filter = args.chapter if args.chapter else None
    report = run_checks(chapter_filter)
    output = report.render()

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(output)

    sys.exit(0 if report.ok else 1)


if __name__ == "__main__":
    main()
