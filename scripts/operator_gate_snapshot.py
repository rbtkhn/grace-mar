#!/usr/bin/env python3
"""
Quick snapshot of RECURSION-GATE: pending count, last N candidates with one-line summary,
and optional last merge recency (last ACT-* date from EVIDENCE / self-archive.md).

Use at start of session or when checking "what's in the queue?" without opening recursion-gate.md.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from recursion_gate_review import filter_review_candidates, parse_review_candidates
    from recursion_gate_territory import normalize_territory_cli
except ImportError:
    from scripts.recursion_gate_review import filter_review_candidates, parse_review_candidates
    from scripts.recursion_gate_territory import normalize_territory_cli

REPO_ROOT = Path(__file__).resolve().parent.parent


def _last_act_date(user_id: str) -> str | None:
    """Return the most recent ACT-* date from EVIDENCE Activity Log, or None."""
    root = REPO_ROOT / "users" / user_id
    evidence_path = root / "self-archive.md"
    if not evidence_path.exists():
        evidence_path = root / "self-evidence.md"
    if not evidence_path.exists():
        return None
    text = evidence_path.read_text(encoding="utf-8")
    # Match "id: ACT-XXXX" followed by "date: YYYY-MM-DD" on next line
    dates: list[str] = []
    for m in re.finditer(r"id: ACT-\d+\s*\n\s*date:\s*(\d{4}-\d{2}-\d{2})", text):
        dates.append(m.group(1))
    return max(dates) if dates else None


def build_snapshot(
    user_id: str = "grace-mar",
    territory: str = "all",
    last_n: int = 10,
) -> str:
    rows = parse_review_candidates(user_id=user_id)
    territory_filter = "" if territory == "all" else territory
    pending = filter_review_candidates(rows, status="pending", territory=territory_filter)

    last_act = _last_act_date(user_id)
    lines = [
        "# Gate snapshot",
        "",
        f"- User: `{user_id}`",
        f"- Territory: `{territory}`",
        f"- Pending candidates: **{len(pending)}**",
    ]
    if last_act:
        lines.append(f"- Last ACT in EVIDENCE: `{last_act}`")
    lines.extend(["", "## Last {} pending (newest first)".format(min(last_n, len(pending))), ""])

    for row in pending[:last_n]:
        summary = (row.get("summary") or "").strip() or "(no summary)"
        one_line = summary.split("\n")[0].strip()[:120]
        if len(summary.split("\n")[0].strip()) > 120:
            one_line += "..."
        lines.append(f"- **{row['id']}** — {one_line}")

    if not pending:
        lines.append("- No pending candidates.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Quick snapshot of RECURSION-GATE: pending count and last N candidates."
    )
    parser.add_argument("-u", "--user", default="grace-mar", help="User id")
    parser.add_argument(
        "--territory",
        choices=("all", "companion", "pol", "wap", "wp", "work-politics"),
        default="all",
        help="Filter by territory",
    )
    parser.add_argument(
        "-n", "--last",
        type=int,
        default=10,
        metavar="N",
        help="Show last N pending candidates (default: 10)",
    )
    args = parser.parse_args()
    territory = normalize_territory_cli(args.territory)
    print(build_snapshot(user_id=args.user, territory=territory, last_n=args.last))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
