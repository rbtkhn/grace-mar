#!/usr/bin/env python3
"""Emit strategy lane observability JSON (WORK-only metrics).

Reads: decision-points/*.md, authorized-sources.yaml, promotion-policy.json,
       strategy-notebook/chapters/*/days.md, daily-strategy-inbox.md,
       STRATEGY.md
Output: artifacts/work-strategy/strategy-observability.json

Usage:
  python3 scripts/build_strategy_observability.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.observability.metric_contract import WORKFLOW_METRIC_KEY, fill_contract  # noqa: E402
OUT = REPO_ROOT / "artifacts/work-strategy/strategy-observability.json"

STRATEGY_ROOT = REPO_ROOT / "docs/skill-work/work-strategy"
NB_ROOT = STRATEGY_ROOT / "strategy-notebook"


def _count_dated_entries(days_path: Path) -> tuple[int, list[str]]:
    """Count ## YYYY-MM-DD headings and return (count, list_of_dates)."""
    if not days_path.is_file():
        return 0, []
    text = days_path.read_text(encoding="utf-8", errors="replace")
    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    return len(dates), dates


def _section_density(days_path: Path) -> dict:
    """Per-entry average of key sections present (Chronicle, Reflection, References, Foresight)."""
    if not days_path.is_file():
        return {"entries": 0, "avg_sections": 0.0}
    text = days_path.read_text(encoding="utf-8", errors="replace")
    entries = re.split(r"^## \d{4}-\d{2}-\d{2}", text, flags=re.MULTILINE)
    entries = [e for e in entries if e.strip()]
    if not entries:
        return {"entries": 0, "avg_sections": 0.0}
    total = 0
    for entry in entries:
        slots = 0
        if "### Chronicle" in entry or "### Signal" in entry:
            slots += 1
        if "### Reflection" in entry or "### Judgment" in entry:
            slots += 1
        if "### References" in entry or "### Links" in entry:
            slots += 1
        if "### Foresight" in entry or "### Open" in entry:
            slots += 1
        total += slots
    return {
        "entries": len(entries),
        "avg_sections": round(total / len(entries), 2),
    }


def _links_density(days_path: Path) -> float:
    """Average number of link/path references per References (or legacy Links) section."""
    if not days_path.is_file():
        return 0.0
    text = days_path.read_text(encoding="utf-8", errors="replace")
    links_blocks = re.findall(
        r"### References\n(.*?)(?=\n### |\n## |\Z)", text, re.DOTALL
    )
    links_blocks.extend(
        re.findall(r"### Links\n(.*?)(?=\n### |\n## |\Z)", text, re.DOTALL)
    )
    if not links_blocks:
        return 0.0
    total_refs = 0
    for block in links_blocks:
        total_refs += len(re.findall(r"(?:\[.*?\]\(|\bhttps?://)", block))
    return round(total_refs / len(links_blocks), 1)


def _open_carry_forward(days_path: Path) -> int:
    """Count Foresight (or legacy Open) sections that mention verify/deferred/? etc."""
    if not days_path.is_file():
        return 0
    text = days_path.read_text(encoding="utf-8", errors="replace")
    open_blocks = re.findall(
        r"### Foresight\n(.*?)(?=\n### |\n## |\Z)", text, re.DOTALL
    )
    open_blocks.extend(
        re.findall(r"### Open\n(.*?)(?=\n### |\n## |\Z)", text, re.DOTALL)
    )
    carry = 0
    for block in open_blocks:
        if re.search(r"verify|deferred|\?|check wire|resolve", block, re.IGNORECASE):
            carry += 1
    return carry


def _inbox_line_count() -> int:
    """Count non-blank, non-heading lines below the append marker in inbox."""
    inbox = NB_ROOT / "daily-strategy-inbox.md"
    if not inbox.is_file():
        return 0
    text = inbox.read_text(encoding="utf-8", errors="replace")
    marker = "<!-- append below -->"
    idx = text.find(marker)
    if idx < 0:
        return 0
    below = text[idx + len(marker) :]
    lines = [
        ln
        for ln in below.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    return len(lines)


def _promotion_activity() -> int:
    """Count dated §IV log entries in STRATEGY.md."""
    strat = STRATEGY_ROOT / "STRATEGY.md"
    if not strat.is_file():
        return 0
    text = strat.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r"\d{4}-\d{2}-\d{2}", text))


def main() -> int:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required", file=sys.stderr)
        return 1

    dp_dir = STRATEGY_ROOT / "decision-points"
    decision_files = [p for p in dp_dir.glob("*.md") if p.name != "README.md"]
    open_count = 0
    status_re = re.compile(r"^\*\*Status:\*\*\s*(\S+)", re.MULTILINE)
    for p in decision_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        m = status_re.search(text)
        st = (m.group(1) if m else "").lower().rstrip(".")
        if st == "open":
            open_count += 1

    yaml_path = STRATEGY_ROOT / "authorized-sources.yaml"
    src_count = 0
    if yaml_path.is_file():
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        src_count = len(data.get("sources", []))

    policy_path = STRATEGY_ROOT / "promotion-policy.json"
    policy_ok = policy_path.is_file()

    # --- Judgment quality metrics (phase 2) ---
    chapters_dir = NB_ROOT / "chapters"
    total_entries = 0
    month_summaries = {}
    all_days_files = sorted(chapters_dir.glob("*/days.md")) if chapters_dir.is_dir() else []

    for days_file in all_days_files:
        month = days_file.parent.name
        count, dates = _count_dated_entries(days_file)
        density = _section_density(days_file)
        links_avg = _links_density(days_file)
        open_carry = _open_carry_forward(days_file)
        knots_dir = days_file.parent / "knots"
        knot_count = len(list(knots_dir.glob("strategy-notebook-knot-*.md"))) if knots_dir.is_dir() else 0
        total_entries += count
        month_summaries[month] = {
            "dated_entries": count,
            "legacy_chapter_stubs": knot_count,
            "knot_pages": knot_count,
            "avg_sections_per_entry": density["avg_sections"],
            "avg_links_per_entry": links_avg,
            "open_carry_forward": open_carry,
        }

    inbox_pending = _inbox_line_count()
    promotion_dates = _promotion_activity()

    doc = {
        "schemaVersion": "2.0.0-work-strategy",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "lane": "work-strategy",
        "metrics": {
            "structure": {
                "decision_point_files": len(decision_files),
                "decision_points_open": open_count,
                "authorized_sources_yaml_entries": src_count,
                "promotion_policy_present": policy_ok,
            },
            "judgment_quality": {
                "notebook_entries_total": total_entries,
                "inbox_pending_lines": inbox_pending,
                "promotion_date_mentions": promotion_dates,
                "months": month_summaries,
            },
        },
        "interpretation": {
            "avg_sections_per_entry": "4.0 = Chronicle/Reflection/References/Foresight (or legacy headings) present; <3.0 = sections skipped regularly",
            "avg_links_per_entry": ">2 healthy; <1 = judgment may be under-cited",
            "open_carry_forward": "High = active threads; very high relative to entries = unresolved debt",
            "inbox_pending_lines": "0 = clean; >30 = overdue weave; >50 = prune candidate",
            "promotion_date_mentions": "0 is fine early; sustained 0 over months = notebook may not be feeding STRATEGY.md",
        },
        "notes": [
            "Recommendation acceptance/rejection rates: need operator workflow.",
            "Cross-lane references: manual until automated extract.",
            "judgment_quality metrics are computed from on-disk notebook state.",
        ],
    }
    wf_approx = len(decision_files) + total_entries + inbox_pending
    doc[WORKFLOW_METRIC_KEY] = fill_contract(
        "work-strategy",
        workflow_count=max(1, wf_approx),
        stale_count=min(inbox_pending, 10_000),
        partial=True,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
