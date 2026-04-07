#!/usr/bin/env python3
"""
Warrant expiration scanner for IX entries in self.md.

Reads IX-A/B/C entries with a warrant: field, classifies by theme, checks age,
and flags entries that may need review.  Optional --suggest-candidates emits
ready-to-paste stage_gate_candidate.py CLI lines.

Read-only operator tooling — no Record writes.

Usage:
  python scripts/scan_warrant_expiration.py -u grace-mar
  python scripts/scan_warrant_expiration.py -u grace-mar --threshold-days 90 --json
  python scripts/scan_warrant_expiration.py -u grace-mar --suggest-candidates
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import fork_root, read_path  # noqa: E402

THEME_KEYWORDS: dict[str, list[str]] = {
    "development-stage": [
        "limited", "developing", "growing", "emerging", "early",
        "immature", "beginning", "novice", "learning",
    ],
    "environment": [
        "school", "environment", "classroom", "home", "setting",
        "context", "situation", "arrangement",
    ],
    "skill-level": [
        "skill", "ability", "proficiency", "fluency", "competence",
        "mastery", "level", "capable",
    ],
    "relationship": [
        "friend", "relationship", "peer", "sibling", "parent",
        "teacher", "social", "group",
    ],
    "temporal": [
        "current", "while", "until", "temporary", "for now",
        "at this stage", "right now", "assumes", "present",
    ],
}


def classify_warrant_theme(warrant_text: str) -> str:
    lower = warrant_text.lower()
    scores: dict[str, int] = {}
    for theme, keywords in THEME_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in lower)
        if hits:
            scores[theme] = hits
    if not scores:
        return "general"
    return max(scores, key=scores.get)  # type: ignore[arg-type]


_IX_ENTRY_RE = re.compile(
    r"  - id:\s*((?:LEARN|CUR|PER)-\d+)(.*?)(?=\n  - id:|\n## |\Z)",
    re.DOTALL,
)


def _yaml_field(block: str, key: str) -> str:
    m = re.search(rf'^\s*{key}:\s*"?(.+?)"?\s*$', block, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else ""


def scan_self(
    user_id: str,
    threshold_days: int = 90,
    now: datetime | None = None,
) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    self_path = fork_root(user_id) / "self.md"
    content = read_path(self_path)
    if not content:
        return []

    results: list[dict] = []
    for m in _IX_ENTRY_RE.finditer(content):
        entry_id = m.group(1)
        block = m.group(0)
        warrant = _yaml_field(block, "warrant")
        if not warrant:
            continue

        date_str = _yaml_field(block, "date")
        try:
            entry_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            entry_date = now

        age_days = (now - entry_date).days
        theme = classify_warrant_theme(warrant)

        review_threshold = threshold_days
        if theme == "development-stage":
            review_threshold = min(threshold_days, 90)
        elif theme == "environment":
            review_threshold = min(threshold_days, 120)

        needs_review = age_days >= review_threshold

        topic = _yaml_field(block, "topic")
        mind_cat = "knowledge"
        if entry_id.startswith("CUR"):
            mind_cat = "curiosity"
        elif entry_id.startswith("PER"):
            mind_cat = "personality"

        results.append({
            "entry_id": entry_id,
            "date": date_str,
            "warrant": warrant,
            "theme": theme,
            "age_days": age_days,
            "needs_review": needs_review,
            "threshold": review_threshold,
            "topic": topic,
            "mind_category": mind_cat,
        })

    return results


def scan_evidence_warrants(user_id: str) -> list[str]:
    """Extract warrant lines from self-archive.md § VIII (informational only)."""
    archive_path = fork_root(user_id) / "self-archive.md"
    content = read_path(archive_path)
    if not content:
        return []
    section_match = re.search(r"## .*VIII.*Gated Approved", content, re.IGNORECASE)
    if not section_match:
        return []
    section = content[section_match.start():]
    return re.findall(r"> warrant:\s*(.+)", section)


def format_text_report(results: list[dict], user_id: str) -> str:
    warranted = [r for r in results]
    lines = [f"Warrant scan ({user_id}) — {len(warranted)} entries carry warrants"]
    if not warranted:
        lines.append("  (none)")
        return "\n".join(lines)
    for r in warranted:
        status = "REVIEW" if r["needs_review"] else "OK"
        lines.append(
            f"  {r['entry_id']} ({r['date']}): \"{r['warrant'][:60]}\" "
            f"— {r['theme']}, {r['age_days']} days — {status}"
        )
    return "\n".join(lines)


def format_suggest_candidates(results: list[dict], user_id: str) -> str:
    """Emit copy-pasteable stage_gate_candidate.py CLI lines for REVIEW entries."""
    review = [r for r in results if r["needs_review"]]
    if not review:
        return "# No warrants flagged for review."
    lines: list[str] = []
    for r in review:
        safe_warrant = r["warrant"].replace('"', '\\"')[:200]
        safe_topic = (r["topic"] or r["entry_id"]).replace('"', '\\"')[:100]
        lines.append(
            f'# {r["entry_id"]} warrant may have expired: "{r["warrant"][:60]}"\n'
            f"python3 scripts/stage_gate_candidate.py -u {user_id} \\\n"
            f'  --title "Revalidate {r["entry_id"]} — warrant review" \\\n'
            f'  --summary "Warrant \'{safe_warrant}\' is {r["age_days"]} days old '
            f'({r["theme"]}). Verify if the entry still holds: {safe_topic}." \\\n'
            f"  --mind {r['mind_category']} \\\n"
            f'  --warrant "{safe_warrant}"'
        )
    return "\n\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Warrant expiration scanner for IX entries.")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    ap.add_argument(
        "--threshold-days",
        type=int,
        default=90,
        help="Flag warrants older than this (default 90; development-stage uses min(this, 90))",
    )
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")
    ap.add_argument(
        "--suggest-candidates",
        action="store_true",
        help="Emit draft stage_gate_candidate.py CLI lines for REVIEW entries",
    )
    args = ap.parse_args()

    results = scan_self(args.user, threshold_days=args.threshold_days)
    evidence_warrants = scan_evidence_warrants(args.user)

    if args.json:
        out = {
            "user_id": args.user,
            "threshold_days": args.threshold_days,
            "entries": results,
            "evidence_warrant_count": len(evidence_warrants),
        }
        print(json.dumps(out, indent=2, default=str))
    elif args.suggest_candidates:
        print(format_suggest_candidates(results, args.user))
    else:
        print(format_text_report(results, args.user))
        if evidence_warrants:
            print(f"\n  ({len(evidence_warrants)} warrant line(s) in § VIII gated approved log)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
