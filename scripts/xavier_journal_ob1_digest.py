#!/usr/bin/env python3
"""Synthesize a xavier-journal daily entry from Xavier's OB1 instance repo (Cici) GitHub activity.

Queries the GitHub REST API for commits on the configured branch within the
calendar day (timezone-aware), then prints or writes a markdown skeleton that
matches docs/skill-work/work-xavier/xavier-journal/README.md conventions.

Environment:
  GITHUB_TOKEN — optional; raises unauthenticated rate limits (60/hr/IP).

Usage:
  python3 scripts/xavier_journal_ob1_digest.py
  python3 scripts/xavier_journal_ob1_digest.py --date 2026-04-10 --write
  TZ=America/New_York python3 scripts/xavier_journal_ob1_digest.py --write
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JOURNAL = REPO_ROOT / "docs/skill-work/work-xavier/xavier-journal"
DEFAULT_OWNER = "Xavier-x01"
DEFAULT_REPO = "Cici"
DEFAULT_BRANCH = "main"


@dataclass(frozen=True)
class CommitLine:
    sha: str
    short_message: str
    html_url: str


def _utc_bounds_for_local_day(d: date, tz_name: str) -> tuple[datetime, datetime]:
    z = ZoneInfo(tz_name)
    start_local = datetime.combine(d, datetime.min.time(), tzinfo=z)
    end_local = start_local + timedelta(days=1)
    return (
        start_local.astimezone(timezone.utc),
        end_local.astimezone(timezone.utc),
    )


def _github_iso(dt: datetime) -> str:
    """ISO 8601 with Z for UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _http_json(url: str, token: str | None) -> list | dict:
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API error {e.code} for {url}: {detail[:500]}") from e
    return json.loads(body)


def fetch_commits_for_day(
    owner: str,
    repo: str,
    branch: str,
    day: date,
    tz_name: str,
    token: str | None,
) -> list[CommitLine]:
    start_utc, end_utc = _utc_bounds_for_local_day(day, tz_name)
    params = {
        "sha": branch,
        "since": _github_iso(start_utc),
        "until": _github_iso(end_utc),
        "per_page": "100",
    }
    q = urllib.parse.urlencode(params)
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?{q}"
    raw = _http_json(url, token)
    if not isinstance(raw, list):
        return []
    out: list[CommitLine] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        sha = str(item.get("sha", ""))[:7]
        html_url = str(item.get("html_url", ""))
        commit = item.get("commit") or {}
        msg = ""
        if isinstance(commit, dict):
            message = commit.get("message") or ""
            if isinstance(message, str):
                msg = message.strip().split("\n", 1)[0].strip()
        if sha:
            out.append(CommitLine(sha=sha, short_message=msg or "(no message)", html_url=html_url))
    return out


def next_journal_day_number(journal_dir: Path) -> int:
    max_n = 0
    for p in journal_dir.glob("*-day-*.md"):
        m = re.match(r".*-day-(\d+)\.md$", p.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def build_markdown(
    *,
    day_label: date,
    journal_day: int,
    tz_name: str,
    owner: str,
    repo: str,
    branch: str,
    commits: list[CommitLine],
) -> str:
    repo_url = f"https://github.com/{owner}/{repo}"
    lines = [
        f"# Xavier journal — Day {journal_day}",
        "",
        f"**Date:** {day_label.isoformat()}  ",
        f"**Journal day:** {journal_day} (OB1-focused learning)  ",
        f"**OB1 repo:** [{owner}/{repo}]({repo_url}) (`{branch}`)  ",
        f"**Activity window:** local calendar day in `{tz_name}` (commits from GitHub API `since`/`until`)  ",
        "",
        "---",
        "",
        "## OB1 repo activity (synthesized from GitHub)",
        "",
    ]
    if not commits:
        lines.extend(
            [
                "*No commits on this branch in the activity window — or API returned none (check branch name, timezone, rate limit).*",
                "",
            ]
        )
    else:
        for c in commits:
            if c.html_url:
                lines.append(f"- [`{c.sha}`]({c.html_url}) — {c.short_message}")
            else:
                lines.append(f"- `{c.sha}` — {c.short_message}")
        lines.append("")
        lines.append(
            f"*Summary:* {len(commits)} commit(s) in window. Edit this section to add narrative; keep secrets out of the journal."
        )
        lines.append("")
    lines.extend(
        [
            "---",
            "",
            "## Focus",
            "",
            "(Fill: what mattered today in *your* words — not only git.)",
            "",
            "## What I did today",
            "",
            "- ",
            "",
            "## What clicked",
            "",
            "- ",
            "",
            "## Friction / questions",
            "",
            "- ",
            "",
            f"## Tomorrow (Day {journal_day + 1})",
            "",
            "- ",
            "",
            "## One line for my advisor",
            "",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build xavier-journal day file from OB1 GitHub commits.")
    ap.add_argument("--owner", default=DEFAULT_OWNER)
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--branch", default=DEFAULT_BRANCH)
    ap.add_argument(
        "--date",
        help="Calendar day YYYY-MM-DD (default: today in TZ)",
        default=None,
    )
    ap.add_argument(
        "--timezone",
        dest="tz",
        default=os.environ.get("TZ", "UTC"),
        help="IANA timezone for day boundaries (default: TZ env or UTC)",
    )
    ap.add_argument(
        "--journal-dir",
        type=Path,
        default=DEFAULT_JOURNAL,
        help="Path to xavier-journal folder",
    )
    ap.add_argument("--day", type=int, default=None, help="Journal day number (default: next from existing files)")
    ap.add_argument(
        "--write",
        action="store_true",
        help=f"Write YYYY-MM-DD-day-NN.md under --journal-dir (won't overwrite unless --force)",
    )
    ap.add_argument("--force", action="store_true", help="Overwrite existing day file")
    ap.add_argument("--stdout-only", action="store_true", help="Print markdown only; do not write")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    if args.date:
        day_label = date.fromisoformat(args.date)
    else:
        # "Today" in the chosen timezone
        z = ZoneInfo(args.tz)
        day_label = datetime.now(z).date()

    commits = fetch_commits_for_day(
        args.owner, args.repo, args.branch, day_label, args.tz, token
    )
    journal_day = args.day if args.day is not None else next_journal_day_number(args.journal_dir)

    md = build_markdown(
        day_label=day_label,
        journal_day=journal_day,
        tz_name=args.tz,
        owner=args.owner,
        repo=args.repo,
        branch=args.branch,
        commits=commits,
    )

    out_path = args.journal_dir / f"{day_label.isoformat()}-day-{journal_day:02d}.md"

    if args.stdout_only or not args.write:
        print(md)
        if not args.write:
            sys.stderr.write(
                f"\n# To write: {out_path}\n#   add --write (use GITHUB_TOKEN if rate-limited)\n"
            )
        return

    args.journal_dir.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not args.force:
        sys.stderr.write(f"Refusing to overwrite {out_path} (use --force)\n")
        raise SystemExit(1)
    out_path.write_text(md, encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
