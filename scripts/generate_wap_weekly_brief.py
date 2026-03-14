#!/usr/bin/env python3
"""
Generate a first-pass weekly brief scaffold for work-american-politics.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WAP_DIR = REPO_ROOT / "docs" / "skill-work" / "work-american-politics"

try:
    from work_american_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.work_american_politics_ops import get_wap_snapshot


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _extract_table_field(path: Path, row_label: str) -> str:
    content = _read(path)
    pattern = rf"\|\s*\*\*?{re.escape(row_label)}\*\*?\s*\|\s*([^|]+)\|"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else ""


def _extract_opposition_lines() -> list[str]:
    content = _read(WAP_DIR / "opposition-brief.md")
    lines: list[str] = []
    for match in re.finditer(r"\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|", content):
        subject, field, detail = [part.strip() for part in match.groups()]
        if "*(Add" in detail:
            continue
        lines.append(f"{subject}: {field} — {detail}")
    return lines[:4]


def _extract_principal_lines() -> list[str]:
    profile = WAP_DIR / "principal-profile.md"
    fields = [
        ("Primary opponent", _extract_table_field(profile, "Primary opponent")),
        ("Trump posture", _extract_table_field(profile, "Trump posture")),
        ("Principal posture", _extract_table_field(profile, "Principal’s posture")),
    ]
    out = [f"{label}: {value}" for label, value in fields if value]
    return out[:3]


def _extract_message_angles() -> list[str]:
    queue_path = WAP_DIR / "content-queue.md"
    lines = []
    for raw in _read(queue_path).splitlines():
        if not raw.startswith("| X-"):
            continue
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if len(cells) < 7:
            continue
        status = cells[1]
        topic = cells[5]
        if status in {"draft", "review", "idea"}:
            lines.append(f"{topic} ({status})")
    return lines[:3]


def _format_date_range(start_text: str = "") -> str:
    if start_text:
        try:
            start = datetime.strptime(start_text, "%Y-%m-%d")
        except ValueError:
            return start_text
    else:
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"


def build_wap_weekly_brief(start_text: str = "", user_id: str = "grace-mar") -> str:
    snapshot = get_wap_snapshot(user_id)
    brief_ready = snapshot["brief_readiness"]
    content = snapshot["content_queue"]
    campaign = snapshot["campaign_status"]
    date_range = _format_date_range(start_text)

    lines = [
        "# Weekly brief — work-american-politics",
        "",
        f"## Week of {date_range}",
        "",
        "_This is a first-pass scaffold built from documented WAP surfaces. Refresh live sources and citations before treating it as final._",
        "",
        "### 1. Headlines (principal-relevant)",
        "",
        "- Review live sources marked `watch` in `brief-source-registry.md`.",
        "- Pull 2-5 principal-relevant headlines before finalizing this brief.",
        "",
        "### 2. Principal (Massie)",
        "",
    ]
    for item in _extract_principal_lines():
        lines.append(f"- {item}")
    lines.extend([
        "- Add any new votes, statements, or media hits from this week with citations.",
        "",
        "### 3. Opposition",
        "",
    ])
    for item in _extract_opposition_lines():
        lines.append(f"- {item}")
    lines.extend([
        "- Refresh Gallrein narrative, spending, and Trump/MAGA activity before relying on this section heavily.",
        "",
        "### 4. Social / narrative",
        "",
        "- Check `@RepThomasMassie`, opposition social, and local Kentucky coverage.",
        "- Add what narrative to reinforce and what narrative needs pushback this week.",
        "",
        "### 5. Key dates this week",
        "",
    ])
    for row in campaign["upcoming_dates"][:3]:
        lines.append(f"- {row['date']} — {row['event']} — {row['decision']}")
    lines.extend([
        "",
        "### 6. Suggested X / message angles",
        "",
    ])
    for angle in _extract_message_angles():
        lines.append(f"- {angle}")
    lines.extend([
        "",
        "### 7. Source readiness",
        "",
        f"- Brief sources ready: {brief_ready['status_counts'].get('ready', 0)}",
        f"- Brief sources to watch live: {brief_ready['status_counts'].get('watch', 0)}",
        f"- Brief sources needing refresh: {brief_ready['status_counts'].get('needs_refresh', 0)}",
        f"- Content items in motion: {len(content['next_items'])}",
        "",
        "### 8. Human review before use",
        "",
        "- Confirm live dates and compliance timing.",
        "- Confirm opposition/spending lines with citations.",
        "- Confirm any X draft aligns with documented Massie posture and shadow-account rules.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate work-american-politics weekly brief scaffold")
    parser.add_argument("--start", default="", help="Week start date (YYYY-MM-DD). Defaults to current week.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default="", help="Optional output file")
    args = parser.parse_args()
    content = build_wap_weekly_brief(start_text=args.start, user_id=args.user)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        print(output)
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
