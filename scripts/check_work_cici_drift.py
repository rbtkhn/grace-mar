#!/usr/bin/env python3
"""Fail if work-cici active-prose drifts back to "Xavier as current lane" phrasing.

Scans a fixed set of repo Markdown files. Lines inside ``` fenced code blocks are skipped.
For each un-fenced line, if a FAIL substring matches and no ALLOW substring matches, report.
Exit 1 if any report; 0 if clean. Stdlib only; repo root from script location.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FILES: tuple[str, ...] = (
    "docs/skill-work/README.md",
    "docs/skill-work/work-cici/DAILY-OPS-CARD.md",
    "docs/skill-work/work-cici/GOOD-MORNING.md",
    "docs/skill-work/work-cici/README.md",
    "docs/skill-work/work-cici/INDEX.md",
    "docs/skill-work/work-cici/LANES.md",
    "docs/skill-work/work-cici/LEAKAGE-CHECKLIST.md",
    "docs/skill-work/work-cici/SYNC-DAILY.md",
    "docs/skill-work/work-cici/work-dev-mirror/SYNC-CONTRACT.md",
    "docs/skill-work/work-cici/work-politics-mirror/SYNC-CONTRACT.md",
)

ALLOWS: tuple[str, ...] = (
    "formerly Xavier",
    "legacy Xavier",
    "Xavier-x01",
    "work-xavier",
    "users/xavier",
    "xavier-",
    "TERMS-XAVIER",
    "COMPANION-XAVIER",
    "build_xavier_handbook_bundle.py",
    "generate_smm_xavier_pdf.sh",
    "xavier_journal_ob1_digest.py",
)

_APOS = "\u2019"  # Unicode apostrophe (typographic) in "Xavier's" in some docs

# All fail substrings: straight apostrophe in ASCII plus curly variants for possessive
FAILS: tuple[str, ...] = (
    "Advisor/project module for Xavier",
    "Advisor / Xavier",
    "Daily Ops Card (Xavier)",
    "Daily Ops Card (xavier)",
    "Not Xavier's Record repo",
    "not Xavier's Record repo",
    f"Not Xavier{_APOS} Record repo",
    f"not Xavier{_APOS} Record repo",
    "not Xavier's sovereign Record repository",
    "not Xavier's sovereign Record repository",
    f"not Xavier{_APOS} sovereign Record repository",
    f"not Xavier{_APOS} sovereign Record repository",
    "work-cici = Xavier",
    "work-cici — Xavier",
)


def _skip_due_to_fence(line: str, in_fence: list[bool]) -> bool:
    """Toggle fence on ``` lines; return True if this line is not subject to text checks."""
    stripped = line.lstrip()
    if stripped.startswith("```"):
        in_fence[0] = not in_fence[0]
        return True
    return in_fence[0]


def _line_has_allow(line: str) -> bool:
    return any(allow in line for allow in ALLOWS)


def _check_file(rel: str) -> list[tuple[int, str, str]]:
    path = REPO_ROOT / rel
    if not path.is_file():
        return [(-1, rel, f"missing: {path}")]
    in_fence = [False]
    out: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if _skip_due_to_fence(line, in_fence):
            continue
        if _line_has_allow(line):
            continue
        for pat in FAILS:
            if pat in line:
                show = " ".join(line.split())
                if len(show) > 200:
                    show = show[:200] + "…"
                out.append((lineno, rel, show))
                break
    return out


def main() -> int:
    all_hits: list[tuple[str, int, str]] = []
    for rel in FILES:
        for item in _check_file(rel):
            if item[0] < 0:
                print(f"{item[1]}: {item[2]}", file=sys.stderr)
                return 1
            lineno, r, show = item
            all_hits.append((r, lineno, show))
    for r, lineno, show in all_hits:
        print(f"{r}:{lineno}: {show}", file=sys.stderr)
    return 1 if all_hits else 0


if __name__ == "__main__":
    sys.exit(main())
