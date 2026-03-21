#!/usr/bin/env python3
"""
Generate a recommendation-oriented review pass over RECURSION-GATE.
"""

from __future__ import annotations

import argparse

try:
    from recursion_gate_review import filter_review_candidates, parse_review_candidates
    from recursion_gate_territory import TERRITORY_LABEL_WAP, normalize_territory_cli
except ImportError:
    from scripts.recursion_gate_review import filter_review_candidates, parse_review_candidates
    from scripts.recursion_gate_territory import TERRITORY_LABEL_WAP, normalize_territory_cli

STALE_DAYS = 7


def _format_candidate(row: dict) -> str:
    age = row.get("age_days")
    age_label = "unknown age" if age is None else f"{age}d old"
    target = row.get("profile_target") or row.get("prompt_section") or "no target"
    return f"{row['id']} [{row['territory_label']}] ({age_label}, {target}) - {row['summary']}"


def build_gate_review_pass(user_id: str = "grace-mar", territory: str = "all") -> str:
    rows = parse_review_candidates(user_id=user_id)
    territory_filter = "" if territory == "all" else territory
    pending = filter_review_candidates(rows, status="pending", territory=territory_filter)
    quick_merge = [row for row in pending if row.get("ready_for_quick_merge")]
    manual_escalate = [row for row in pending if row.get("risk_tier") == "manual_escalate"]
    stale = [row for row in pending if isinstance(row.get("age_days"), int) and row["age_days"] >= STALE_DAYS]
    duplicates = [row for row in pending if row.get("duplicate_hints")]
    review_batch = [
        row
        for row in pending
        if row not in quick_merge and row not in manual_escalate and row not in stale and row not in duplicates
    ]
    companion_count = sum(1 for row in pending if row.get("territory_label") == "Companion")
    wap_count = sum(1 for row in pending if row.get("territory_label") == TERRITORY_LABEL_WAP)

    lines = [
        "# Gate review pass",
        "",
        f"- User: `{user_id}`",
        f"- Territory filter: `{territory}`",
        f"- Pending candidates: {len(pending)} ({companion_count} companion, {wap_count} work-politics)",
        "",
        "## Approve now",
        "",
    ]

    if quick_merge:
        for row in quick_merge[:8]:
            lines.append(f"- {_format_candidate(row)}")
    else:
        lines.append("- No quick-merge-eligible candidates detected.")

    lines.extend(["", "## Investigate duplicates", ""])
    if duplicates:
        for row in duplicates[:8]:
            hints = "; ".join(row.get("duplicate_hints") or [])
            lines.append(f"- {_format_candidate(row)} -> {hints}")
    else:
        lines.append("- No duplicate-hint candidates detected.")

    lines.extend(["", "## Manual escalation", ""])
    if manual_escalate:
        for row in manual_escalate[:8]:
            reasons = []
            if row.get("has_conflict_markers"):
                reasons.append("conflict markers")
            if row.get("advisory_flagged"):
                reasons.append("advisory flagged")
            if row.get("has_multi_target"):
                reasons.append("multi-target")
            if row.get("has_prompt_change"):
                reasons.append("prompt change")
            if row.get("has_artifact_payload"):
                reasons.append("artifact payload")
            reason_text = ", ".join(reasons) or "needs manual review"
            lines.append(f"- {_format_candidate(row)} -> {reason_text}")
    else:
        lines.append("- No manual-escalation candidates detected.")

    lines.extend(["", "## Stale candidates", ""])
    if stale:
        for row in stale[:8]:
            lines.append(f"- {_format_candidate(row)}")
    else:
        lines.append(f"- No candidates older than {STALE_DAYS} day(s).")

    lines.extend(["", "## Defer or batch review", ""])
    if review_batch:
        for row in review_batch[:8]:
            lines.append(f"- {_format_candidate(row)}")
    else:
        lines.append("- No batch-review items beyond the categories above.")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Recommendations only. This workflow does not approve, reject, or merge anything.",
            "- Use the inbox or explicit operator commands for actual gate actions.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a recommendation-oriented RECURSION-GATE review pass.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument(
        "--territory",
        choices=("all", "companion", "wap", "wp", "work-politics"),
        default="all",
        help="Territory lens",
    )
    args = parser.parse_args()
    territory = normalize_territory_cli(args.territory)
    print(build_gate_review_pass(user_id=args.user, territory=territory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
