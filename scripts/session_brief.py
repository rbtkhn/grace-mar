#!/usr/bin/env python3
"""
Session briefing for Grace-Mar.

Reads EVIDENCE, RECURSION-GATE, SELF and produces a markdown brief:
- Last N activity entries
- Pending candidate count (full gate file)
- Suggested wisdom questions (from WISDOM-QUESTIONS, tuned to IX-B)

Run before a tutoring session or via cron. Output to stdout.

Usage:
    python scripts/session_brief.py -u grace-mar
    python scripts/session_brief.py -u grace-mar --minimal
"""

import re
import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_territory import pending_by_territory
STALE_PENDING_DAYS = 3
DEFAULT_USERS_DIR = REPO_ROOT / "users"
WISDOM_PATH = REPO_ROOT / "docs" / "WISDOM-QUESTIONS.md"
LIBRARY_PATH_REL = "self-library.md"  # relative to user_dir
LAST_N_ACTIVITIES = 5
WISDOM_COUNT = 3
SUGGESTED_ACTIVITIES_COUNT = 3
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


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


def _pending_candidate_ids(pr_content: str, territory: str = "all") -> list[str]:
    """All pending IDs — full file. territory: all | wap | companion."""
    wap, companion = pending_by_territory(pr_content)
    if territory == "wap":
        return [r["id"] for r in wap]
    if territory == "companion":
        return [r["id"] for r in companion]
    return [r["id"] for r in wap + companion]


def _pending_count_full(pr_content: str, territory: str = "all") -> int:
    return len(_pending_candidate_ids(pr_content, territory))


def _last_act_oneliner(evidence_content: str) -> str:
    if "## V. ACTIVITY LOG" not in evidence_content:
        return "(none)"
    start = evidence_content.find("## V. ACTIVITY LOG")
    end = evidence_content.find("\n## VI.", start)
    block = evidence_content[start:end] if end > start else evidence_content[start:]
    matches = list(re.finditer(r"\n  - id: (ACT-\d+)", block))
    if not matches:
        return "(none)"
    last = matches[-1]
    act_id = last.group(1)
    chunk_end = last.end()
    nxt = re.search(r"\n  - id: ", block[chunk_end:])
    chunk = block[last.start() + 1 : chunk_end + nxt.start()] if nxt else block[last.start() + 1 : last.start() + 2000]
    date_m = re.search(r"date:\s*(\S+)", chunk)
    summary_m = re.search(r'summary:\s*"([^"]*)"', chunk)
    label = (summary_m.group(1) if summary_m else act_id)[:90]
    d = date_m.group(1) if date_m else "?"
    return f"{act_id} ({d}) — {label}"


def _load_pipeline_events(user_dir: Path) -> list[dict]:
    path = user_dir / "pipeline-events.jsonl"
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            if isinstance(row, dict):
                rows.append(row)
        except json.JSONDecodeError:
            continue
    return rows


def _oldest_pending_age_days(pr_content: str, events: list[dict]) -> int | None:
    pending_ids = set(_pending_candidate_ids(pr_content, "all"))
    if not pending_ids:
        return None
    oldest: datetime | None = None
    for row in events:
        if row.get("event") != "staged":
            continue
        cid = row.get("candidate_id")
        if cid not in pending_ids:
            continue
        ts = str(row.get("ts") or "").strip()
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            continue
        if oldest is None or dt < oldest:
            oldest = dt
    if oldest is None:
        return None
    return max(0, int((datetime.now() - oldest).days))


def _recent_rejection_reasons(events: list[dict], limit: int = 3) -> list[str]:
    reasons: list[str] = []
    for row in reversed(events):
        if row.get("event") != "rejected":
            continue
        reason = str(row.get("rejection_reason") or "").strip()
        if reason:
            reasons.append(reason)
        if len(reasons) >= limit:
            break
    return reasons


def build_operator_reminder(
    user_dir: Path,
    pending_threshold: int,
    stale_days: int,
) -> str:
    pr_content = _read(user_dir / "recursion-gate.md")
    pending_count = _pending_count_full(pr_content)
    events = _load_pipeline_events(user_dir)
    oldest_days = _oldest_pending_age_days(pr_content, events)
    should_notify = pending_count >= pending_threshold or (oldest_days is not None and oldest_days >= stale_days)
    if not should_notify:
        return ""
    reasons = _recent_rejection_reasons(events)
    lines = [
        "Grace-Mar operator reminder:",
        f"- pending candidates: {pending_count}",
        f"- oldest pending age: {oldest_days if oldest_days is not None else 'unknown'} day(s)",
    ]
    if reasons:
        lines.append(f"- recent rejection reasons: {'; '.join(reasons)}")
    lines.append("- next action: run /review in Telegram")
    return "\n".join(lines)


def _from_the_record_topics(self_content: str, n: int = 3) -> list[str]:
    """Extract 1–3 topics from IX-A, IX-B, IX-C for 'From the Record' section."""
    knowledge = re.findall(r'id: LEARN-\d+.*?topic:\s*["\']([^"\']+)["\']', self_content, re.DOTALL)
    curiosity = re.findall(r'id: CUR-\d+.*?topic:\s*["\']([^"\']+)["\']', self_content, re.DOTALL)
    personality = re.findall(r'id: PER-\d+.*?observation:\s*["\']([^"\']+)["\']', self_content, re.DOTALL)
    if not personality:
        personality = [m.group(1).strip() for m in re.finditer(r'id: PER-\d+.*?observation:\s*([^\n]+)', self_content, re.DOTALL)]
    topics = []
    if knowledge:
        topics.append(knowledge[-1].strip()[:40])
    if curiosity and len(topics) < n:
        topics.append(curiosity[-1].strip()[:40])
    if personality and len(topics) < n:
        topics.append(personality[-1].strip()[:40])
    return topics[:n]


def _ix_b_topics(self_content: str) -> list[str]:
    """Extract IX-B curiosity topics for wisdom question selection."""
    topics = []
    if "### IX-B. CURIOSITY" not in self_content:
        return topics
    idx = self_content.find("### IX-B. CURIOSITY")
    block = self_content[idx : idx + 4000]
    # Prefer topic: "..." lines
    for m in re.finditer(r'topic:\s*["\']([^"\']+)["\']', block):
        t = m.group(1).strip()[:60]
        if t and t not in topics:
            topics.append(t)
    # Fallback: lines that look like content (not id:, provenance, evidence)
    if not topics:
        for m in re.finditer(r"-\s+([^\n]+)", block):
            line = m.group(1).strip()
            if line.startswith("id:") or "provenance" in line or "evidence" in line:
                continue
            if len(line) > 5 and not line.startswith("curated"):
                topics.append(line.split("—")[0].strip()[:40])
    return topics[:10]


def _suggested_activities(
    ix_b_topics: list[str],
    from_record: list[str],
    library_titles: list[str],
    n: int = 3,
) -> list[str]:
    """Derive 2–3 suggested activities from Record and LIBRARY."""
    activities = []
    seen = set()
    for t in ix_b_topics[:2]:
        t = t.strip()
        if t and t.lower() not in seen:
            seen.add(t.lower())
            activities.append(f"Ask Grace-Mar about {t} — or teach her what you've learned.")
    for t in from_record[:1]:
        t = t.strip()
        if t and t.lower() not in seen and len(activities) < n:
            seen.add(t.lower())
            activities.append(f"Explore {t} further.")
    for title in library_titles[:1]:
        if title and len(activities) < n:
            activities.append(f"From LIBRARY: {title[:50]} — consider reading or discussing.")
    return activities[:n]


def _library_titles(library_content: str, n: int = 3) -> list[str]:
    """Extract up to n active library entry titles."""
    titles = []
    for m in re.finditer(r'title:\s*["\']([^"\']+)["\']', library_content):
        titles.append(m.group(1).strip())
        if len(titles) >= n:
            break
    return titles


def _intent_primary_goal(user_dir: Path) -> str | None:
    """Load primary goal from intent.md if present."""
    path = user_dir / "intent.md"
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"primary:\s*[\"']([^\"']+)[\"']", raw)
    return m.group(1).strip() if m else None


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
    import argparse

    parser = argparse.ArgumentParser(description="Generate session brief or operator reminder.")
    parser.add_argument("--users-dir", default=str(DEFAULT_USERS_DIR), help="Users directory")
    parser.add_argument("--user", "-u", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument("--reminder", action="store_true", help="Emit operator reminder text (if thresholds exceeded)")
    parser.add_argument("--pending-threshold", type=int, default=5, help="Reminder trigger: pending count")
    parser.add_argument("--stale-days", type=int, default=7, help="Reminder trigger: oldest pending age days")
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="One screen: pending count + IDs + last ACT + next action",
    )
    parser.add_argument(
        "--territory",
        choices=("all", "wap", "companion"),
        default="all",
        help="Pending lens: wap | companion | all (default). Same as operator_blocker_report.",
    )
    args = parser.parse_args()

    users_dir = Path(args.users_dir)
    if not users_dir.exists():
        print(f"Users dir not found: {users_dir}", file=sys.stderr)
        return 1

    user_dir = users_dir / args.user
    if not user_dir.exists():
        user_dir = next(users_dir.iterdir(), None) if users_dir.is_dir() else None
    if not user_dir or not user_dir.is_dir():
        print("No user dir found.", file=sys.stderr)
        return 1

    if args.reminder:
        text = build_operator_reminder(
            user_dir=user_dir,
            pending_threshold=args.pending_threshold,
            stale_days=args.stale_days,
        )
        if text:
            print(text)
        return 0

    if args.minimal:
        pr_content = _read(user_dir / "recursion-gate.md")
        evidence_content = _read(user_dir / "self-evidence.md")
        wap_rows, comp_rows = pending_by_territory(pr_content)
        n = _pending_count_full(pr_content, args.territory)
        ids = _pending_candidate_ids(pr_content, args.territory)
        last_act = _last_act_oneliner(evidence_content)
        lines = [
            "# Session brief (minimal)",
            "",
            f"**Territory lens:** {args.territory}",
            f"**Pending (this lens):** {n} — {', '.join(ids) if ids else 'none'}",
        ]
        if args.territory == "all":
            lines.append(
                f"**Split:** WAP {len(wap_rows)} · Companion {len(comp_rows)} — use `--territory wap` or `companion`"
            )
        lines.extend(
            [
                "",
                f"**Last activity:** {last_act}",
                "",
                "**Next action:** "
                + (
                    "/review in Telegram → approve or reject each pending."
                    if n
                    else "Nothing in gate (this lens) — send \"we did X\" when something worth recording happens."
                ),
                "",
            ]
        )
        print("\n".join(lines))
        return 0

    evidence_content = _read(user_dir / "self-evidence.md")
    pr_content = _read(user_dir / "recursion-gate.md")
    self_content = _read(user_dir / "self.md")
    wisdom_content = _read(WISDOM_PATH)
    library_content = _read(user_dir / LIBRARY_PATH_REL)

    activities = _last_activities(evidence_content, LAST_N_ACTIVITIES)
    wap_rows, comp_rows = pending_by_territory(pr_content)
    pending_count = _pending_count_full(pr_content, args.territory)
    ix_b = _ix_b_topics(self_content)
    wisdom = _wisdom_questions(wisdom_content, ix_b, WISDOM_COUNT)
    from_record = _from_the_record_topics(self_content)
    suggested_activities = _suggested_activities(
        ix_b, from_record, _library_titles(library_content), SUGGESTED_ACTIVITIES_COUNT
    )
    intent_goal = _intent_primary_goal(user_dir)
    pr_path = user_dir / "recursion-gate.md"
    pending_stale = False
    if pending_count > 0 and pr_path.exists():
        mtime = datetime.fromtimestamp(pr_path.stat().st_mtime)
        pending_stale = (datetime.now() - mtime) > timedelta(days=STALE_PENDING_DAYS)

    # Nudge: no "we did X" in the last 7 days
    no_activity_nudge = ""
    if activities:
        last_date_str = activities[-1].get("date", "")
        try:
            last_dt = datetime.strptime(last_date_str, "%Y-%m-%d")
            if (datetime.now() - last_dt).days >= 7:
                no_activity_nudge = "\n\n**Ritual nudge:** No activity in the last 7 days — when something worth recording happens, send \"we did X\" in the bot, then /review."
        except (ValueError, TypeError):
            pass
    else:
        no_activity_nudge = "\n\n**Ritual nudge:** When something worth recording happens, send \"we did X\" in the bot, then /review to approve what gets added."

    # Build brief
    pending_section = (
        f"**Territory lens:** `{args.territory}` — **{pending_count}** pending (this lens). "
        f"WAP **{len(wap_rows)}** · Companion **{len(comp_rows)}**. "
        f"`--territory wap` = work-politics only. Type `/review` in Telegram to see them."
    )
    if pending_stale:
        pending_section += "\n\nYou have candidates waiting — consider bringing them into the Record (type /review)."
    if no_activity_nudge:
        pending_section += no_activity_nudge

    lines = [
        "# Session Brief",
        "",
        f"*Generated for {user_dir.name}*",
        "",
        "## Recursion Gate",
        "",
        pending_section,
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
    lines.extend(["", "## From the Record", ""])
    if from_record:
        topics_str = ", ".join(from_record)
        lines.append(f"The Record holds: {topics_str}. Ask Grace-Mar to recall any of these.")
    else:
        lines.append("(nothing yet — pipeline will grow the Record)")
    lines.extend(["", "## Suggested Activities", ""])
    if suggested_activities:
        for a in suggested_activities:
            lines.append(f"- {a}")
        if intent_goal:
            lines.append(f"\n*Aligned with INTENT: {intent_goal}*")
    else:
        lines.append("(Record will suggest activities as IX-B and LIBRARY grow)")
    lines.extend(["", "## Suggested Wisdom Questions", ""])
    if wisdom:
        for q in wisdom:
            lines.append(f"- {q}")
    else:
        lines.append("(see docs/wisdom-questions.md)")
    lines.append("")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
