#!/usr/bin/env python3
"""
Draft WORK / COMPANION markdown blocks for users/<id>/self-history.md from:
  - docs/skill-work/work-*/*-history.md (## Log bullets)
  - users/<id>/self-archive.md § V ACTIVITY LOG (YAML activities)

Default: print to stdout (--dry-run). Use --write to replace log sections in self-history.md.

Examples:
  python3 scripts/draft_self_history.py -u grace-mar
  python3 scripts/draft_self_history.py -u grace-mar --companion-style per-act --max 15
  python3 scripts/draft_self_history.py -u grace-mar --write
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_WORK = REPO_ROOT / "docs" / "skill-work"

SECTION_V_START = "## V. ACTIVITY LOG"
LOG_HEADING = "## Log — WORK (aggregate)"
COMPANION_HEADING = "## Log — COMPANION (gate-approved)"


def extract_activity_yaml(archive_text: str) -> str | None:
    m = re.search(
        r"## V\. ACTIVITY LOG\n.*?\n```yaml\n(.*?)```",
        archive_text,
        re.DOTALL,
    )
    return m.group(1) if m else None


def parse_activities(yaml_blob: str) -> list[tuple[str, str, str, str]]:
    """Return list of (act_id, date, activity_type, summary)."""
    blocks = re.split(r"\n  - id: (ACT-\d+)", yaml_blob)
    out: list[tuple[str, str, str, str]] = []
    for i in range(1, len(blocks), 2):
        aid = blocks[i]
        body = blocks[i + 1]
        dm = re.search(r"date: (\d{4}-\d{2}-\d{2})", body)
        tm = re.search(r"activity_type: (.+)", body)
        date = dm.group(1) if dm else ""
        atype = tm.group(1).strip() if tm else ""
        qm = re.search(r"question: \"([^\"]*)\"", body)
        topicm = re.search(r"topic: \"([^\"]*)\"", body)
        if qm:
            summary = qm.group(1)[:120]
        elif topicm:
            summary = topicm.group(1)[:120]
        else:
            summary = ""
        out.append((aid, date, atype, summary))
    return out


def companion_monthly_lines(activities: list[tuple[str, str, str, str]]) -> list[str]:
    by_month: dict[str, list[str]] = defaultdict(list)
    for aid, date, _, _ in activities:
        if len(date) >= 7:
            by_month[date[:7]].append(aid)
    lines = []
    for ym in sorted(by_month.keys()):
        ids = sorted(by_month[ym], key=lambda x: int(x.split("-")[1]))
        lines.append(
            f"- **COMPANION: {ym}** — {len(ids)} activities in `self-archive.md` § V "
            f"(`{ids[0]}`–`{ids[-1]}`). Canonical: `users/<id>/self-archive.md` **§ V. ACTIVITY LOG**."
        )
    return lines


def companion_per_act_lines(
    activities: list[tuple[str, str, str, str]],
    *,
    max_n: int | None = None,
) -> list[str]:
    lines = []
    for aid, date, atype, summary in activities:
        suf = f" — {summary}" if summary else ""
        lines.append(
            f"- **COMPANION: {aid}** ({date}) — {atype}{suf}"
        )
    if max_n is not None:
        lines = lines[:max_n]
    return lines


def territory_from_path(path: Path) -> str:
    # docs/skill-work/work-dev/work-dev-history.md -> work-dev
    return path.parent.name


def extract_work_log_bullets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if "## Log" not in text:
        return []
    after = text.split("## Log", 1)[1]
    # drop optional ### or first line
    lines_out: list[str] = []
    for line in after.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and lines_out:
            break
        if stripped.startswith("- "):
            lines_out.append(line.rstrip())
        elif stripped.startswith("_(Append") or stripped == "---":
            continue
        elif lines_out and not stripped:
            continue
        elif lines_out and stripped and not stripped.startswith("-"):
            # narrative under log without dash — stop
            if stripped.startswith("#"):
                break
    return lines_out


def work_aggregate_lines() -> list[str]:
    paths = sorted(SKILL_WORK.glob("work-*/*-history.md"))
    lines: list[str] = []
    for p in paths:
        terr = territory_from_path(p)
        bullets = extract_work_log_bullets(p)
        rel = p.relative_to(REPO_ROOT)
        for b in bullets:
            inner = b.lstrip("- ").strip()
            if inner.startswith("**") and "—" in inner:
                lines.append(f"- **WORK:{terr}** — {inner}")
            else:
                lines.append(f"- **WORK:{terr}** — {inner}")
        if not bullets:
            lines.append(
                f"- **WORK:{terr}** — _(no bullets under `## Log` in `{rel.as_posix()}`)_"
            )
    return lines


def render_log_sections(
    *,
    companion_style: str,
    max_n: int | None,
    user_id: str,
) -> str:
    archive_path = REPO_ROOT / "users" / user_id / "self-archive.md"
    if not archive_path.is_file():
        activities: list[tuple[str, str, str, str]] = []
    else:
        blob = extract_activity_yaml(archive_path.read_text(encoding="utf-8"))
        activities = parse_activities(blob) if blob else []

    wlines = work_aggregate_lines()
    if companion_style == "month":
        clines = companion_monthly_lines(activities)
    else:
        clines = companion_per_act_lines(activities, max_n=max_n)

    # Substitute user id in companion lines for display
    clines = [s.replace("users/<id>/", f"users/{user_id}/") for s in clines]

    parts = [
        LOG_HEADING,
        "",
        *wlines,
        "",
        "---",
        "",
        COMPANION_HEADING,
        "",
        *clines,
    ]
    if not clines:
        parts.extend(["", "_(`self-archive.md` § V missing or empty)_"])
    return "\n".join(parts) + "\n"


def write_self_history(user_id: str, new_log_block: str) -> Path:
    path = REPO_ROOT / "users" / user_id / "self-history.md"
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    full = path.read_text(encoding="utf-8")
    if LOG_HEADING not in full:
        raise SystemExit(f"anchor {LOG_HEADING!r} not found in {path}")
    head, _rest = full.split(LOG_HEADING, 1)
    updated = head.rstrip() + "\n\n" + new_log_block
    path.write_text(updated, encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="Draft self-history WORK/COMPANION log sections.")
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    ap.add_argument(
        "--companion-style",
        choices=("month", "per-act"),
        default="month",
        help="COMPANION rollup: monthly summary or one line per ACT",
    )
    ap.add_argument(
        "--max",
        type=int,
        default=None,
        metavar="N",
        help="With --companion-style per-act, cap number of lines",
    )
    ap.add_argument(
        "--write",
        action="store_true",
        help=f"Replace from {LOG_HEADING!r} through end of self-history.md",
    )
    args = ap.parse_args()

    body = render_log_sections(
        companion_style=args.companion_style,
        max_n=args.max,
        user_id=args.user,
    )

    if args.write:
        out = write_self_history(args.user, body)
        print(f"wrote log sections: {out}", file=sys.stderr)
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
