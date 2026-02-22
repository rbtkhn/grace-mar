#!/usr/bin/env python3
"""
Export the grace-mar Record with privacy redaction for sharing.

Produces view_school (school-safe: no addresses, family details) or view_public
(portfolio-only: interests, skills summary, no raw evidence).

Usage:
    python scripts/export_view.py --view school -u pilot-001 -o school-export.md
    python scripts/export_view.py --view public -u pilot-001

See docs/PRIVACY-REDACTION.md for what each view excludes.
"""

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _section(content: str, title: str) -> str | None:
    pattern = rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _redact_birthdate(block: str) -> str:
    return re.sub(r"birthdate:\s*\S+", "birthdate: [redacted]", block, flags=re.IGNORECASE)


def _redact_location(block: str) -> str:
    return re.sub(r"location:\s*[^\n]+", "location: [state/region only]", block, flags=re.IGNORECASE)


def _redact_places_lived(block: str) -> str:
    return re.sub(r"places_lived:\s*\[.*?\]", "places_lived: [redacted]", block, flags=re.DOTALL)


def _redact_relationships(block: str) -> str:
    return re.sub(r"relationships:\s*\{[^}]*\}|relationships:\s*\[.*?\]", "relationships: [redacted]", block, flags=re.DOTALL)


def _redact_family_notes(block: str) -> str:
    block = re.sub(r"members:\s*\[.*?\]", "members: [redacted]", block, flags=re.DOTALL)
    block = re.sub(r"dynamics:\s*[^\n]+", "dynamics: [redacted]", block, flags=re.IGNORECASE)
    return block


def export_view(user_id: str, view: str) -> str:
    """
    Export Record with redaction. view in (school, public).
    """
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "SELF.md"
    skills_path = profile_dir / "SKILLS.md"
    self_raw = _read(self_path)

    if view == "school":
        return _export_school(self_raw, profile_dir, user_id)
    if view == "public":
        return _export_public(self_raw, _read(skills_path), user_id)
    raise ValueError(f"view must be 'school' or 'public', got {view!r}")


def _export_school(self_raw: str, profile_dir: Path, user_id: str) -> str:
    """School-safe: identity generalized, no birthdate, no places_lived, no family details."""
    out = ["# Grace-Mar Record — School View", "", "> Redacted for school sharing. See docs/PRIVACY-REDACTION.md.", ""]

    sections = [
        ("I. IDENTITY", "Identity"),
        ("II. PREFERENCES (Survey Seeded)", "Preferences"),
        ("III. LINGUISTIC STYLE", "Linguistic style"),
        ("IV. PERSONALITY", "Personality"),
        ("V. INTERESTS", "Interests"),
        ("VI. VALUES", "Values"),
        ("VII. REASONING PATTERNS", "Reasoning"),
        ("VIII. NARRATIVE", "Narrative"),
        ("IX. MIND (Post-Seed Growth)", "Post-seed growth"),
    ]

    for section_title, short_name in sections:
        block = _section(self_raw, section_title)
        if not block:
            continue
        if section_title == "I. IDENTITY":
            block = _redact_birthdate(block)
            block = _redact_location(block)
        if section_title == "VIII. NARRATIVE":
            block = _redact_places_lived(block)
            block = _redact_relationships(block)
            block = _redact_family_notes(block)
        out.append(f"## {short_name}")
        out.append("")
        out.append(block)
        out.append("")
        out.append("---")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _export_public(self_raw: str, skills_raw: str, user_id: str) -> str:
    """Portfolio-only: interests, skills summary, no identity, no raw evidence."""
    out = ["# Grace-Mar Record — Public View", "", "> Portfolio summary. See docs/PRIVACY-REDACTION.md.", ""]

    for section_title, short_name in [
        ("II. PREFERENCES (Survey Seeded)", "Preferences"),
        ("V. INTERESTS", "Interests"),
        ("VI. VALUES", "Values"),
        ("IX. MIND (Post-Seed Growth)", "Post-seed growth"),
    ]:
        block = _section(self_raw, section_title)
        if block:
            out.append(f"## {short_name}")
            out.append("")
            out.append(block)
            out.append("")
            out.append("---")
            out.append("")

    if skills_raw:
        summary = re.search(r"## I\. CONTAINER STATUS.*?(?=## II\.|$)", skills_raw, re.DOTALL)
        if summary:
            out.append("## Skills Summary")
            out.append("")
            out.append(summary.group(0).strip()[:1500])
            out.append("")
            out.append("---")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Record with privacy redaction (school, public)"
    )
    parser.add_argument("--view", "-v", required=True, choices=["school", "public"])
    parser.add_argument("--user", "-u", default="pilot-001")
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()
    content = export_view(user_id=args.user, view=args.view)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
