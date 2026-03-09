#!/usr/bin/env python3
"""
Proactive proposal brief — 3–5 concrete activities from Record, INTENT, LIBRARY, and gaps.

Based on IX-A/B/C, SKILLS gaps, self-library, and intent. Companion chooses what to do.
Run before a session or via cron. Output to stdout.

Usage:
    python scripts/proposal_brief.py -u grace-mar
    python scripts/proposal_brief.py -u grace-mar -n 5
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
WISDOM_PATH = REPO_ROOT / "docs" / "wisdom-questions.md"
PROPOSAL_COUNT = 5


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _ix_b_topics(self_content: str, n: int = 5) -> list[str]:
    """Extract IX-B curiosity topics."""
    topics = []
    if "### IX-B. CURIOSITY" not in self_content:
        return topics
    idx = self_content.find("### IX-B. CURIOSITY")
    block = self_content[idx : idx + 4000]
    for m in re.finditer(r'topic:\s*["\']([^"\']+)["\']', block):
        t = m.group(1).strip()[:80]
        if t and t not in topics:
            topics.append(t)
        if len(topics) >= n:
            break
    return topics


def _ix_a_recent(self_content: str, n: int = 2) -> list[str]:
    """Extract recent IX-A knowledge topics."""
    topics = []
    for m in re.finditer(r'topic:\s*["\']([^"\']+)["\']', self_content):
        t = m.group(1).strip()[:60]
        if t and t not in topics:
            topics.append(t)
        if len(topics) >= n:
            break
    return topics[-n:] if len(topics) > n else topics


def _gaps(skills_content: str) -> list[str]:
    """Extract capability gaps from skills.md yaml blocks."""
    gaps = []
    m = re.search(r"gaps:\s*\n((?:\s+-\s+.+\n?)*)", skills_content)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("- ") and len(line) > 2:
                g = line[2:].strip().strip('"\'')
                if g and g not in ("[]", "null"):
                    gaps.append(g[:80])
    return gaps[:3]


def _library_unread(library_content: str, n: int = 2) -> list[dict]:
    """Extract unread/active library entries."""
    entries = []
    blocks = re.split(r"^\s*-\s+id:\s+", library_content, flags=re.MULTILINE)[1:]
    for block in blocks:
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        status_m = re.search(r"^status:\s*(\w+)", block, re.MULTILINE)
        read_m = re.search(r"read_status:\s*(\w+)", block)
        if not title_m:
            continue
        status = status_m.group(1) if status_m else "active"
        if status == "deprecated":
            continue
        read_status = read_m.group(1) if read_m else "unread"
        if read_status not in ("unread", "reading", "in_progress"):
            continue
        entries.append({"title": title_m.group(1).strip(), "read_status": read_status})
        if len(entries) >= n:
            break
    return entries


def _intent_goals(intent_content: str) -> dict[str, str]:
    """Extract primary and secondary goals from intent."""
    goals = {}
    m = re.search(r"primary:\s*[\"']([^\"']+)[\"']", intent_content)
    if m:
        goals["primary"] = m.group(1).strip()
    m = re.search(r"secondary:\s*[\"']([^\"']+)[\"']", intent_content)
    if m:
        goals["secondary"] = m.group(1).strip()
    return goals


def _build_proposals(
    user_dir: Path,
    n: int,
) -> list[dict]:
    """Build 3–5 proposals with rationale."""
    self_content = _read(user_dir / "self.md")
    skills_content = _read(user_dir / "skills.md")
    library_content = _read(user_dir / "self-library.md")
    intent_content = _read(user_dir / "intent.md")

    ix_b = _ix_b_topics(self_content, n=5)
    ix_a = _ix_a_recent(self_content, n=2)
    gaps = _gaps(skills_content)
    lib_unread = _library_unread(library_content, n=2)
    goals = _intent_goals(intent_content)

    proposals = []

    # 1–2 from IX-B curiosity
    for i, topic in enumerate(ix_b[:2]):
        proposals.append({
            "activity": f"Ask Grace-Mar about {topic} — or teach her what you've learned.",
            "rationale": f"Curiosity (IX-B): {topic[:50]}",
        })

    # 1 from IX-A if available
    if ix_a and len(proposals) < n:
        t = ix_a[-1]
        proposals.append({
            "activity": f"Deepen: explore {t} further with a lookup or discussion.",
            "rationale": f"Knowledge (IX-A): {t[:50]}",
        })

    # 1 from LIBRARY unread
    for e in lib_unread:
        if len(proposals) >= n:
            break
        title = e.get("title", "?")[:50]
        proposals.append({
            "activity": f"From LIBRARY: {title} — consider reading or discussing.",
            "rationale": "Unread or in-progress in self-library",
        })

    # 1 from gaps if any
    if gaps and len(proposals) < n:
        g = gaps[0]
        proposals.append({
            "activity": f"Skill gap: {g} — practice or document progress.",
            "rationale": "Capability gap in SKILLS",
        })

    # 1 wisdom-style prompt
    wisdom = _read(WISDOM_PATH)
    for m in re.finditer(r"\|\s*(?:19|20|21|60|61|62)\s*\|\s*([^|]+)\|", wisdom):
        q = m.group(1).strip()
        if q and len(proposals) < n:
            proposals.append({
                "activity": f"Reflection: {q}",
                "rationale": "Wisdom question (curiosity/teach tier)",
            })
            break

    return proposals[:n]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate proactive proposal brief from Record")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument("-n", "--count", type=int, default=PROPOSAL_COUNT, help="Max proposals (default 5)")
    args = parser.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    proposals = _build_proposals(user_dir, args.count)
    goals = _intent_goals(_read(user_dir / "intent.md"))

    lines = [
        "# Proposal Brief",
        "",
        f"*Generated for {user_dir.name}*",
        "",
        "## Proposed Activities",
        "",
        "Pick one or more. The Record suggests these based on curiosity, knowledge, LIBRARY, and gaps.",
        "",
    ]
    if goals.get("primary"):
        lines.append(f"*INTENT: {goals['primary']}*")
        lines.append("")

    for i, p in enumerate(proposals, 1):
        lines.append(f"### {i}. {p['activity']}")
        lines.append("")
        lines.append(f"*{p['rationale']}*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Companion chooses what to do. Staging and merge remain gated.*")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
