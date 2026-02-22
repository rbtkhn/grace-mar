#!/usr/bin/env python3
"""
Session briefing for Grace-Mar.

Reads EVIDENCE, PENDING-REVIEW, SELF and produces a markdown brief:
- Last N activity entries
- Pending candidate count
- Suggested wisdom questions (from WISDOM-QUESTIONS, tuned to IX-B)

Run before a tutoring session or via cron. Output to stdout.

Usage:
    python scripts/session_brief.py [users_dir]
    python scripts/session_brief.py users/pilot-001
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
WISDOM_PATH = REPO_ROOT / "docs" / "WISDOM-QUESTIONS.md"
LAST_N_ACTIVITIES = 5
WISDOM_COUNT = 3


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _last_activities(evidence_content: str, n: int) -> list[dict]:
    """Extract last n ACT-* entries from EVIDENCE Activity Log."""
    if "## V. ACTIVITY LOG" not in evidence_content:
        return []
    idx = evidence_content.find("## V. ACTIVITY LOG")
    block = evidence_content[idx:]
    # Find activities YAML
    m = re.search(r"```yaml\s*\nactivities:\s*\n(.*?)```", block, re.DOTALL)
    if not m:
        return []
    yaml_block = m.group(1)
    entries = []
    for m in re.finditer(r"-\s+id:\s*(ACT-\d+)(.*?)(?=-\s+id:\s*ACT-|\Z)", yaml_block, re.DOTALL):
        act_id, chunk = m.group(1), m.group(2)
        date_m = re.search(r"date:\s*(\S+)", chunk)
        activity_m = re.search(r"activity_type:\s*(.+?)(?:\n|$)", chunk)
        topic_m = re.search(r"topic:\s*\"([^\"]+)\"", chunk)
        question_m = re.search(r'question:\s*"([^"]+)"', chunk)
        entries.append({
            "id": act_id,
            "date": date_m.group(1) if date_m else "?",
            "activity_type": (activity_m.group(1) or "?").strip(),
            "topic": topic_m.group(1) if topic_m else (question_m.group(1)[:60] + "..." if question_m and len(question_m.group(1)) > 60 else (question_m.group(1) if question_m else "")),
        })
    return entries[-n:] if len(entries) > n else entries


def _pending_count(pr_content: str) -> int:
    """Count pending candidates in PENDING-REVIEW."""
    if "## Candidates" not in pr_content or "## Processed" not in pr_content:
        return 0
    candidates = pr_content.split("## Processed")[0]
    return len(re.findall(r"### CANDIDATE-\d+", candidates))


def _ix_b_topics(self_content: str) -> list[str]:
    """Extract IX-B curiosity topics for wisdom question selection."""
    topics = []
    if "### IX-B. CURIOSITY" not in self_content:
        return topics
    idx = self_content.find("### IX-B. CURIOSITY")
    block = self_content[idx : idx + 2000]
    # Simple extraction: look for - topic or CUR- entries
    for m in re.finditer(r"-\s+([^\n]+)", block):
        line = m.group(1).strip()
        if line.startswith("#") or "provenance" in line or "evidence" in line:
            continue
        if len(line) > 3 and not line.startswith("curated"):
            topics.append(line.split("—")[0].strip()[:40])
    return topics[:10]


def _wisdom_questions(wisdom_content: str, ix_b_topics: list[str], n: int) -> list[str]:
    """Extract n wisdom questions. Prefer curiosity/creativity sections (IX-B)."""
    questions = []
    # Parse tables: | # | Question | Notes |
    for m in re.finditer(r"\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]*)\|", wisdom_content):
        num, q, notes = m.groups()
        q = q.strip()
        if not q or q == "Question":
            continue
        questions.append((int(num), q, notes.strip().lower()))
    # Prefer curiosity (19–23), creativity (24–28), teach (60–62)
    curiosity = [(n, q, notes) for n, q, notes in questions if 19 <= n <= 23 or 24 <= n <= 28 or 60 <= n <= 62]
    if curiosity:
        chosen = curiosity[:n]
    else:
        chosen = questions[:n] if len(questions) >= n else questions
    return [q for _, q, _ in chosen]


def main() -> int:
    users_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_USERS_DIR
    if not users_dir.exists():
        print(f"Users dir not found: {users_dir}", file=sys.stderr)
        return 1

    # For now, assume pilot-001
    user_dir = users_dir / "pilot-001"
    if not user_dir.exists():
        user_dir = next(users_dir.iterdir(), None) if users_dir.is_dir() else None
    if not user_dir or not user_dir.is_dir():
        print("No user dir found.", file=sys.stderr)
        return 1

    evidence_content = _read(user_dir / "EVIDENCE.md")
    pr_content = _read(user_dir / "PENDING-REVIEW.md")
    self_content = _read(user_dir / "SELF.md")
    wisdom_content = _read(WISDOM_PATH)

    activities = _last_activities(evidence_content, LAST_N_ACTIVITIES)
    pending_count = _pending_count(pr_content)
    ix_b = _ix_b_topics(self_content)
    wisdom = _wisdom_questions(wisdom_content, ix_b, WISDOM_COUNT)

    # Build brief
    lines = [
        "# Session Brief",
        "",
        f"*Generated for {user_dir.name}*",
        "",
        "## Pending Review",
        "",
        f"**{pending_count}** candidate(s) awaiting review. Type `/review` in Telegram to see them.",
        "",
        "## Recent Activity",
        "",
    ]
    if activities:
        for a in reversed(activities):
            topic = a.get("topic") or a.get("activity_type", "?")
            lines.append(f"- **{a['id']}** ({a['date']}) — {topic}")
    else:
        lines.append("(no recent activities)")
    lines.extend(["", "## Suggested Wisdom Questions", ""])
    if wisdom:
        for q in wisdom:
            lines.append(f"- {q}")
    else:
        lines.append("(see docs/WISDOM-QUESTIONS.md)")
    lines.append("")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
