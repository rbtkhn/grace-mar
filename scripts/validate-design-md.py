#!/usr/bin/env python3
"""
Validate Grace-Mar DESIGN.md against the creative-pipeline structure.

Stdlib only. Checks required H2 sections, core colors, spacing language, and
agent rules. Not a substitute for human design review or RECURSION-GATE.

Usage:
  python3 scripts/validate-design-md.py
  python3 scripts/validate-design-md.py --file users/grace-mar/DESIGN.md --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# Each tuple is one required section: any listed phrase may appear in the ## heading (substring match).
H2_ALTERNATIVES: Tuple[Tuple[str, ...], ...] = (
    ("Principles",),
    ("Color Palette",),
    ("Typography",),
    ("Spacing Rules", "Spacing & Layout"),
    ("Component Library", "Component Patterns"),
    ("Rules for Agents",),
)

REQUIRED_HEX_IN_FILE = ("#0A84FF", "#0F0F0F", "#E0E0E0")


def _h2_headings(content: str) -> List[str]:
    headings: List[str] = []
    for line in content.splitlines():
        if line.startswith("###"):
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            headings.append(m.group(1).strip())
    return headings


def _h2_present(required: str, headings: List[str]) -> bool:
    r = required.lower()
    for h in headings:
        if r in h.lower():
            return True
    return False


def _h2_group_satisfied(alternatives: Tuple[str, ...], headings: List[str]) -> bool:
    return any(_h2_present(alt, headings) for alt in alternatives)


def _section_after_any_h2(content: str, title_prefixes: Tuple[str, ...]) -> str | None:
    for prefix in title_prefixes:
        block = _section_after_h2(content, prefix)
        if block is not None:
            return block
    return None


def _section_after_h2(content: str, title_prefix: str) -> str | None:
    """Return body after first ## heading whose text starts with title_prefix (case-insensitive)."""
    lines = content.splitlines()
    prefix_l = title_prefix.lower()
    start: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("###"):
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and m.group(1).strip().lower().startswith(prefix_l):
            start = i + 1
            break
    if start is None:
        return None
    chunk: List[str] = []
    for j in range(start, len(lines)):
        line = lines[j]
        # Stop at next H2 (## ), not at ### headings.
        if re.match(r"^##\s+[^#]", line):
            break
        chunk.append(line)
    return "\n".join(chunk)


class DesignMDValidator:
    def __init__(self, design_md_path: Path) -> None:
        self.design_md_path = design_md_path
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load(self) -> str:
        if not self.design_md_path.is_file():
            self.errors.append(f"DESIGN.md not found: {self.design_md_path}")
            return ""
        try:
            return self.design_md_path.read_text(encoding="utf-8")
        except OSError as e:
            self.errors.append(f"Failed to read DESIGN.md: {e}")
            return ""

    def validate_structure(self, content: str) -> None:
        if not content:
            return
        headings = _h2_headings(content)
        if not headings:
            self.errors.append("No ## (level-2) headings found")
            return
        missing_labels: List[str] = []
        for alts in H2_ALTERNATIVES:
            if not _h2_group_satisfied(alts, headings):
                missing_labels.append(alts[0])
        if missing_labels:
            self.errors.append(
                f"Missing or unmatched H2 sections (expected phrases): {', '.join(missing_labels)}"
            )

    def validate_color_palette(self, content: str) -> None:
        cl = content.lower()
        for req in REQUIRED_HEX_IN_FILE:
            if req.lower() not in cl:
                self.errors.append(f"Missing required Grace-Mar color token in file: {req}")
        block = _section_after_h2(content, "Color Palette")
        if block is None:
            return
        hexes = re.findall(r"(#[0-9A-Fa-f]{6})\b", block)
        if not hexes:
            self.warnings.append("Color Palette section: no #RRGGBB hex codes found")

    def validate_spacing(self, content: str) -> None:
        block = _section_after_any_h2(content, ("Spacing Rules", "Spacing & Layout"))
        if block is None:
            return
        low = block.lower()
        if "8px" not in block and "8 px" not in block and "base unit" not in low:
            self.errors.append("Spacing Rules must mention 8px base unit (or 'base unit')")

    def validate_agent_rules(self, content: str) -> None:
        if not _h2_present("Rules for Agents", _h2_headings(content)):
            self.warnings.append("Recommended: add a 'Rules for Agents' H2 for agent UI guardrails")

    def run(self) -> Tuple[bool, List[str], List[str]]:
        content = self.load()
        if not content:
            return False, self.errors, self.warnings

        self.validate_structure(content)
        self.validate_color_palette(content)
        self.validate_spacing(content)
        self.validate_agent_rules(content)

        return (len(self.errors) == 0, self.errors, self.warnings)

    def print_report(self) -> None:
        rel = self.design_md_path
        try:
            rel = self.design_md_path.relative_to(ROOT)
        except ValueError:
            pass
        print("=== DESIGN.md validation ===")
        print(f"File: {rel}")
        if self.errors:
            print("\nERRORS:")
            for err in self.errors:
                print(f"  - {err}")
        if self.warnings:
            print("\nWARNINGS:")
            for warn in self.warnings:
                print(f"  - {warn}")
        if not self.errors and not self.warnings:
            print("\nOK: no errors or warnings.")
        print("============================")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Grace-Mar DESIGN.md")
    parser.add_argument(
        "--file",
        type=Path,
        default=ROOT / "users/grace-mar/DESIGN.md",
        help="Path to DESIGN.md",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error if there are warnings",
    )
    args = parser.parse_args()
    path = args.file if args.file.is_absolute() else ROOT / args.file

    v = DesignMDValidator(path)
    ok, errors, warnings = v.run()
    v.print_report()

    if not ok or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
