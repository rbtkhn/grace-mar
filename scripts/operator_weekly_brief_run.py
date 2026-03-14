#!/usr/bin/env python3
"""
Run a disciplined weekly brief workflow for work-political-consulting.

This wrapper adds readiness checks and a stable operator-facing output around
the existing weekly brief scaffold generator.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from generate_wap_weekly_brief import build_wap_weekly_brief
    from work_american_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.generate_wap_weekly_brief import build_wap_weekly_brief
    from scripts.work_american_politics_ops import get_wap_snapshot


def _write_output(path_text: str, content: str) -> str:
    output = Path(path_text)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return str(output)


def build_weekly_brief_run(
    user_id: str = "grace-mar",
    start_text: str = "",
    *,
    allow_stale_sources: bool = False,
    output_path: str = "",
) -> str:
    snapshot = get_wap_snapshot(user_id)
    brief = snapshot["brief_readiness"]
    content = snapshot["content_queue"]
    blockers = snapshot["territory_blockers"]
    needs_refresh = brief["status_counts"].get("needs_refresh", 0)
    ready_sources = brief["status_counts"].get("ready", 0)
    watch_sources = brief["status_counts"].get("watch", 0)
    verdict = "READY" if needs_refresh == 0 else "BLOCKED"
    emit_scaffold = needs_refresh == 0 or allow_stale_sources
    scaffold = build_wap_weekly_brief(start_text=start_text, user_id=user_id) if emit_scaffold else ""
    written_path = _write_output(output_path, scaffold) if output_path and scaffold else ""

    lines = [
        "# Weekly brief run",
        "",
        f"- User: `{user_id}`",
        f"- Verdict: {verdict}",
        f"- Override stale sources: {'yes' if allow_stale_sources else 'no'}",
        "",
        "## Readiness",
        "",
        f"- Brief sources ready: {ready_sources}",
        f"- Brief sources to watch: {watch_sources}",
        f"- Brief sources needing refresh: {needs_refresh}",
        f"- Content items in motion: {len(content.get('next_items') or [])}",
        f"- Pending WAP gate items: {snapshot['gate']['pending_count']}",
        "",
        "## Blocking items",
        "",
    ]

    if needs_refresh:
        for source in brief.get("needs_refresh") or []:
            lines.append(f"- Refresh `{source}` before treating the brief as final-use campaign output.")
    else:
        lines.append("- No source freshness blockers detected.")

    if blockers:
        lines.extend(["", "## Territory blockers", ""])
        for item in blockers:
            lines.append(f"- {item['title']} -> {item['action']}")

    lines.extend(["", "## Next actions", ""])
    if needs_refresh:
        lines.append("- Refresh items marked `needs_refresh` in `brief-source-registry.md`.")
    lines.append("- Review `content-queue.md` for any draft or review items that should shape this week's framing.")
    lines.append("- Human-review the scaffold before using it for campaign output.")

    lines.extend(["", "## Brief scaffold", ""])
    if scaffold:
        if written_path:
            lines.append(f"- Wrote scaffold to `{written_path}`.")
            lines.append("")
        lines.extend(scaffold.rstrip().splitlines())
    else:
        lines.append("- Scaffold not emitted because sources need refresh.")
        lines.append("- Re-run with `--allow-stale-sources` to generate a first-pass draft anyway.")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- This workflow generates a first-pass scaffold, not final-use campaign output.",
            "- Record changes still require the normal gate and approval flow.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the work-political-consulting weekly brief workflow.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--start", default="", help="Week start date (YYYY-MM-DD). Defaults to current week.")
    parser.add_argument("--allow-stale-sources", action="store_true", help="Emit the scaffold even if sources need refresh.")
    parser.add_argument("--output", "-o", default="", help="Optional path for the emitted scaffold.")
    args = parser.parse_args()
    print(
        build_weekly_brief_run(
            user_id=args.user,
            start_text=args.start,
            allow_stale_sources=args.allow_stale_sources,
            output_path=args.output,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
