#!/usr/bin/env python3
"""
Assemble smm-xavier-handbook-bundle.md: mission + handbook + all key SMM training files
for one self-contained PDF (Xavier / print edition).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Order matters. Paths relative to REPO.
BUNDLE_PARTS: list[tuple[str, Path]] = [
    ("Handbook — operator summary (Xavier)", REPO / "docs/skill-work/work-politics/smm-xavier-handbook.md"),
    ("SMM training — civics, voice, allies/adversaries, checklist", REPO / "docs/skill-work/work-politics/smm-training.md"),
    ("Account spec — @usa_first_ky", REPO / "docs/skill-work/work-politics/account-x.md"),
    ("Principal profile — Thomas Massie (KY-4)", REPO / "docs/skill-work/work-politics/principal-profile.md"),
    ("Principal profile — Ro Khanna (CA-17, demo context)", REPO / "docs/skill-work/work-politics/khanna-principal-profile.md"),
    ("Opposition brief — Gallrein, Trump/MAGA", REPO / "docs/skill-work/work-politics/opposition-brief.md"),
    ("Massie KY-4 — operator checklist (doctrine, brief template, monitoring)", REPO / "docs/skill-work/work-politics/clients/massie-ky4-operator-checklist.md"),
    ("Massie — issue asymmetry map (primary + general)", REPO / "docs/skill-work/work-politics/clients/massie-issue-asymmetry.md"),
    ("SMM onboarding curriculum — modules M0–M5", REPO / "docs/skill-work/work-politics/smm-onboarding-curriculum.md"),
    ("SMM — Day 1 checklist", REPO / "docs/skill-work/work-politics/smm-day1-checklist.md"),
    ("SMM — job description & compensation", REPO / "docs/skill-work/work-politics/smm-job-description.md"),
    ("SMM — access checklist (companion)", REPO / "docs/skill-work/work-politics/smm-access-checklist.md"),
    ("Content queue — @usa_first_ky", REPO / "docs/skill-work/work-politics/content-queue.md"),
    ("Calendar — KY-4 2026", REPO / "docs/skill-work/work-politics/calendar-2026.md"),
    ("Iran / foreign policy — Massie context", REPO / "docs/skill-work/work-politics/iran-foreign-policy-brief.md"),
    ("Work-politics internal dashboard (/pol)", REPO / "docs/pol-dashboard.md"),
    ("Externals — Day 1 quickstart", REPO / "docs/externals/massie/smm-training/day-1-quickstart.md"),
    ("Externals — Week 1 ramp", REPO / "docs/externals/massie/smm-training/week-1-ramp-plan.md"),
    ("Externals — Daily operating rhythm", REPO / "docs/externals/massie/smm-training/daily-operating-rhythm.md"),
    ("Externals — Approval workflow", REPO / "docs/externals/massie/smm-training/approval-workflow.md"),
    ("Externals — KPI scorecard", REPO / "docs/externals/massie/smm-training/kpi-scorecard.md"),
    ("Externals — Content playbook", REPO / "docs/externals/massie/smm-training/content-playbook.md"),
    ("Externals — Templates", REPO / "docs/externals/massie/smm-training/templates.md"),
    ("High-stakes messaging — guardrail stress-test", REPO / "docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md"),
    ("High-stakes messaging — stress-test brief template", REPO / "docs/skill-work/work-politics/america-first-ky/stress-test-brief-template.md"),
]


def strip_pdf_export_section(text: str) -> str:
    if "## PDF export" in text:
        return text.split("## PDF export")[0].rstrip()
    return text


def strip_first_h1(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# ") and not lines[0].startswith("##"):
        return "\n".join(lines[1:]).lstrip("\n")
    return text


def strip_xavier_handbook_h1(text: str) -> str:
    """Remove top # title line; bundle supplies its own part title."""
    lines = text.splitlines()
    if lines and lines[0].startswith("# Xavier"):
        return "\n".join(lines[1:]).lstrip("\n")
    return text


def strip_handbook_mission_block(text: str) -> str:
    """Remove handbook's ## Mission section; bundle already prints mission at top."""
    pattern = r"^## Mission — America First Kentucky\n\n.*?\n\n---\n\n"
    stripped, n = re.subn(pattern, "", text, count=1, flags=re.DOTALL)
    return stripped if n else text


def demote_headings(text: str) -> str:
    """Add one # level so Part titles stay # and body uses ##+."""
    out_lines: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            line = "#" + line
        out_lines.append(line)
    return "\n".join(out_lines)


def main() -> int:
    out_path = REPO / "docs/skill-work/work-politics/smm-xavier-handbook-bundle.md"
    mission_path = REPO / "docs/externals/massie/mission-short.md"
    if not mission_path.exists():
        print(f"Missing {mission_path}", file=sys.stderr)
        return 1

    mission_raw = mission_path.read_text(encoding="utf-8").strip()
    mission_body = strip_first_h1(mission_raw)

    chunks: list[str] = [
        "# Xavier — Complete SMM training pack (print edition)\n\n",
        "This single document bundles the **mission**, the **operator handbook**, and **key training materials** for Xavier. "
        "It is generated from repo sources; regenerate with `scripts/build_xavier_handbook_bundle.py`.\n\n",
        "---\n\n",
        "# Mission — America First Kentucky\n\n",
        mission_body + "\n\n",
        "---\n\n",
    ]

    for title, path in BUNDLE_PARTS:
        if not path.exists():
            print(f"Warning: skip missing {path}", file=sys.stderr)
            continue
        body = path.read_text(encoding="utf-8")
        if path.name == "smm-xavier-handbook.md":
            body = strip_pdf_export_section(body)
            body = strip_xavier_handbook_h1(body)
            body = strip_handbook_mission_block(body)
        else:
            body = strip_first_h1(body)
        body = demote_headings(body)
        rel = path.relative_to(REPO)
        chunks.append(f"# {title}\n\n")
        chunks.append(f"*Source file: `{rel}`*\n\n")
        chunks.append(body.rstrip() + "\n\n")
        chunks.append("---\n\n")

    out_path.write_text("".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
