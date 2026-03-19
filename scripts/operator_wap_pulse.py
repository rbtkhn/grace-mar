#!/usr/bin/env python3
"""
Generate a concise operator pulse for work-politics.
"""

from __future__ import annotations

import argparse

try:
    from generate_wap_weekly_brief import build_wap_weekly_brief
    from work_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.generate_wap_weekly_brief import build_wap_weekly_brief
    from scripts.work_politics_ops import get_wap_snapshot


def build_wap_pulse(user_id: str = "grace-mar", include_brief_preview: bool = False) -> str:
    snapshot = get_wap_snapshot(user_id)
    campaign = snapshot["campaign_status"]
    brief = snapshot["brief_readiness"]
    content = snapshot["content_queue"]
    gate = snapshot["gate"]
    blockers = snapshot["territory_blockers"]
    docs = snapshot["doc_statuses"]

    lines = [
        "# WAP pulse",
        "",
        f"- Territory: `{snapshot['territory']}`",
        f"- Principal: {snapshot['principal']['name']} ({snapshot['principal']['district']})",
        f"- Phase: {snapshot['principal']['phase']}",
        f"- Primary date: {campaign['primary_date']} ({campaign['days_until_primary']} day(s) remaining)",
        "",
        "## Upcoming dates",
        "",
    ]
    for row in campaign["upcoming_dates"][:4]:
        lines.append(f"- {row['date']} - {row['event']} - {row['decision']}")
    if not campaign["upcoming_dates"]:
        lines.append("- No upcoming dates parsed.")

    lines.extend(
        [
            "",
            "## Readiness",
            "",
            f"- Brief sources: ready={brief['status_counts'].get('ready', 0)}, watch={brief['status_counts'].get('watch', 0)}, needs_refresh={brief['status_counts'].get('needs_refresh', 0)}",
            f"- Content queue: idea={content['status_counts'].get('idea', 0)}, draft={content['status_counts'].get('draft', 0)}, review={content['status_counts'].get('review', 0)}, posted={content['status_counts'].get('posted', 0)}",
            f"- Pending WAP gate items: {gate['pending_count']}",
            "",
            "## Blockers",
            "",
        ]
    )
    if blockers:
        for item in blockers:
            lines.append(f"- {item['title']} -> {item['action']}")
    else:
        lines.append("- No WAP blockers detected.")

    lines.extend(["", "## Doc freshness", ""])
    for doc in docs:
        age = doc["age_days"]
        age_label = "unknown" if age is None else f"{age} day(s)"
        placeholder = "yes" if doc["has_placeholders"] else "no"
        lines.append(f"- {doc['label']} -> age={age_label}, placeholders={placeholder}, path=`{doc['path']}`")

    lines.extend(["", "## Next actions", ""])
    for action in snapshot["next_actions"]:
        lines.append(f"- {action}")
    if not snapshot["next_actions"]:
        lines.append("- No next actions derived.")

    if include_brief_preview:
        preview = build_wap_weekly_brief(user_id=user_id).splitlines()[:18]
        lines.extend(["", "## Brief preview", ""])
        lines.extend(preview)

    lines.extend(["", "## Guardrail", "", "- WORK surface only. Record changes still go through the gate.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a WAP operator pulse.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--brief-preview", action="store_true", help="Append the top of the weekly brief scaffold.")
    args = parser.parse_args()
    print(build_wap_pulse(user_id=args.user, include_brief_preview=args.brief_preview))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
