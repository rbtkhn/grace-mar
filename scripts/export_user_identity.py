#!/usr/bin/env python3
"""
Export the grace-mar Record to USER.md or SOUL.md format for OpenClaw.

Reads users/[id]/SELF.md and produces a condensed, agent-friendly markdown
file suitable for OpenClaw's identity layer. Use this so the agent knows
who it serves — identity, preferences, interests, values, personality,
and post-seed growth (IX-A, IX-B, IX-C).

Usage:
    python scripts/export_user_identity.py --user pilot-001
    python scripts/export_user_identity.py -u pilot-001 -o ../openclaw/USER.md
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
    """Extract a section between ## TITLE and the next ## or end of file."""
    pattern = rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _subsection(content: str, title: str) -> str | None:
    """Extract a subsection between ### TITLE and the next ### or ## or end."""
    pattern = rf"^### {re.escape(title)}\s*\n(.*?)(?=^### |^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def export_user_identity(user_id: str = "pilot-001") -> str:
    """
    Build USER.md / SOUL.md compatible markdown from the Record.

    Returns a single string suitable for writing to a file.
    """
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "SELF.md"
    self_raw = _read(self_path)
    if not self_raw:
        return f"# USER — {user_id}\n\nNo SELF.md found at {self_path}.\n"

    out_lines = [
        "# USER — Grace-Mar Record Export",
        "",
        "> Identity source for OpenClaw. Exported from grace-mar Record (SELF.md).",
        "> Update by re-running: `python scripts/export_user_identity.py -u pilot-001 -o USER.md`",
        "",
        "---",
        "",
    ]

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
        if block:
            out_lines.append(f"## {short_name}")
            out_lines.append("")
            out_lines.append(block)
            out_lines.append("")
            out_lines.append("---")
            out_lines.append("")

    return "\n".join(out_lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export grace-mar Record to USER.md / SOUL.md for OpenClaw"
    )
    parser.add_argument("--user", "-u", default="pilot-001", help="User id (e.g. pilot-001)")
    parser.add_argument(
        "--output", "-o", default=None, help="Output file (default: stdout)"
    )
    args = parser.parse_args()
    content = export_user_identity(user_id=args.user)
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
