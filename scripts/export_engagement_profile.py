#!/usr/bin/env python3
"""
Export engagement/motivation profile from the Record.

Produces a compact JSON (and optional markdown) with interests, curiosity (IX-B),
personality (IX-C), and talent_stack — for tutors, platforms, and operators
as the "motivation/engagement substrate" (BUSINESS-ROADMAP priority #1).

Usage:
    python scripts/export_engagement_profile.py --user pilot-001
    python scripts/export_engagement_profile.py -u pilot-001 -o engagement.json
    python scripts/export_engagement_profile.py -u pilot-001 --md -o engagement.md
"""

import argparse
import json
import re
from datetime import datetime, timezone
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


def _subsection(content: str, title: str) -> str | None:
    pattern = rf"^### {re.escape(title)}\s*\n(.*?)(?=^### |^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _yaml_list(block: str, key: str) -> list[str]:
    """Extract a YAML list like key: [a, b] or key: - a."""
    m = re.search(rf"^{re.escape(key)}:\s*\n((?:\s+-\s+.+\n?)*)", block, re.MULTILINE)
    if m:
        return [
            line.strip().strip("- \t").strip("\"'")
            for line in m.group(1).strip().splitlines()
            if line.strip().startswith("-")
        ]
    m = re.search(rf"^{re.escape(key)}:\s*\[(.*?)\]", block, re.DOTALL)
    if m:
        return [x.strip().strip("\"'") for x in re.findall(r"[^,\[\]]+", m.group(1)) if x.strip()]
    return []


def _scalar(block: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("\"'").split("#")[0].strip()


def _ix_b_topics(content: str) -> list[str]:
    """Extract IX-B curiosity topics (CUR- entries or bullet topics)."""
    idx = content.find("### IX-B. CURIOSITY")
    if idx < 0:
        return []
    block = content[idx : idx + 3000]
    topics = []
    for m in re.finditer(r'id:\s*CUR-\d+.*?topic:\s*["\']([^"\']+)["\']', block, re.DOTALL):
        topics.append(m.group(1).strip())
    if not topics:
        for m in re.finditer(r"-\s+([^\n—]+?)(?:\s+—|\n|$)", block):
            line = m.group(1).strip()
            if line and len(line) > 2 and "provenance" not in line and "evidence" not in line:
                topics.append(line[:80])
    return topics[:30]


def _ix_c_snippets(content: str) -> list[str]:
    """Extract IX-C personality observations (PER- entries or bullets)."""
    idx = content.find("### IX-C. PERSONALITY")
    if idx < 0:
        return []
    block = content[idx : idx + 3000]
    snippets = []
    for m in re.finditer(r'id:\s*PER-\d+.*?observation:\s*["\']([^"\']+)["\']', block, re.DOTALL):
        snippets.append(m.group(1).strip())
    if not snippets:
        for m in re.finditer(r'observation:\s*["\']([^"\']+)["\']', block):
            snippets.append(m.group(1).strip())
    return snippets[:20]


def export_engagement_profile(user_id: str = "pilot-001") -> dict:
    """Build engagement profile dict: interests, curiosity, personality, talent_stack."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "SELF.md"
    self_raw = _read(self_path)
    if not self_raw:
        return {
            "user_id": user_id,
            "ok": False,
            "error": f"No SELF.md at {self_path}",
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

    prefs = _section(self_raw, "II. PREFERENCES (Survey Seeded)")
    interests_block = _subsection(self_raw, "V. INTERESTS") if _section(self_raw, "V. INTERESTS") else prefs or ""

    movies = _yaml_list(prefs or "", "movies") or _yaml_list(interests_block, "movies")
    books = _yaml_list(prefs or "", "books") or _yaml_list(interests_block, "books")
    places = _yaml_list(prefs or "", "places") or _yaml_list(interests_block, "places")
    activities = _yaml_list(prefs or "", "activities") or _yaml_list(interests_block, "activities")
    foods = _yaml_list(prefs or "", "food") or _yaml_list(prefs or "", "foods")

    talent_stack = _scalar(self_raw, "talent_stack") or _scalar(prefs or "", "talent_stack")
    if not talent_stack and "talent_stack:" in self_raw:
        m = re.search(r"talent_stack:\s*[\"']([^\"']+)[\"']", self_raw)
        if m:
            talent_stack = m.group(1).strip()

    curiosity = _ix_b_topics(self_raw)
    personality = _ix_c_snippets(self_raw)

    return {
        "ok": True,
        "format": "grace-mar-engagement-profile",
        "user_id": user_id,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "interests": {
            "movies": movies,
            "books": books,
            "places": places,
            "activities": activities,
            "foods": foods,
        },
        "curiosity_topics": curiosity,
        "personality_snippets": personality,
        "talent_stack": talent_stack or None,
    }


def export_engagement_profile_md(profile: dict) -> str:
    """Render engagement profile as short markdown for humans."""
    if not profile.get("ok"):
        return f"# Engagement Profile — {profile.get('user_id', '?')}\n\nError: {profile.get('error', 'unknown')}\n"
    lines = [
        "# Engagement Profile",
        "",
        f"*Generated: {profile.get('generated_at', '')}*",
        "",
        "## Interests",
        "",
    ]
    for key, label in [("movies", "Movies"), ("books", "Books"), ("places", "Places"), ("activities", "Activities"), ("foods", "Foods")]:
        vals = (profile.get("interests") or {}).get(key) or []
        if vals:
            lines.append(f"**{label}:** " + ", ".join(str(v) for v in vals[:15]))
            lines.append("")
    if profile.get("curiosity_topics"):
        lines.append("## Curiosity (IX-B)")
        lines.append("")
        for t in profile["curiosity_topics"][:15]:
            lines.append(f"- {t}")
        lines.append("")
    if profile.get("personality_snippets"):
        lines.append("## Personality (IX-C)")
        lines.append("")
        for s in profile["personality_snippets"][:10]:
            lines.append(f"- {s}")
        lines.append("")
    if profile.get("talent_stack"):
        lines.append("## Talent Stack")
        lines.append("")
        lines.append(profile["talent_stack"])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export engagement/motivation profile from Record")
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--md", action="store_true", help="Emit markdown instead of JSON")
    args = parser.parse_args()

    profile = export_engagement_profile(user_id=args.user)
    if args.md:
        content = export_engagement_profile_md(profile)
    else:
        content = json.dumps(profile, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(content, end="")
    return 0 if profile.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
