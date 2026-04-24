#!/usr/bin/env python3
"""Synthesize a cici-notebook daily entry from Xavier's OB1 instance repo (Cici) GitHub activity.

Queries the GitHub REST API for commits on the configured branch within the
calendar day (timezone-aware), then prints or writes **`YYYY-MM-DD.md`** (journal
ordinal inside the body): **Day overview** heuristics from commit messages,
optional **inbox** / **session-transcript** / **artifacts**, plus linked commit
lines. See docs/skill-work/work-cici/cici-notebook/README.md.

Environment:
  GITHUB_TOKEN — optional; raises unauthenticated rate limits (60/hr/IP).
  CICI_JOURNAL_FULL_DAY_SYNTHESIS — if set to 1/true/yes/on, same as --full-day-synthesis.
    (Alias: XAVIER_JOURNAL_FULL_DAY_SYNTHESIS — accepted for older shells and notes.)

Usage:
  python3 scripts/cici_journal_ob1_digest.py
  python3 scripts/cici_journal_ob1_digest.py --date 2026-04-10 --write
  TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py --write
  TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py --catch-up-from-last-dream --write
  python3 scripts/cici_journal_ob1_digest.py --full-day-synthesis --write
  CICI_JOURNAL_FULL_DAY_SYNTHESIS=1 python3 scripts/cici_journal_ob1_digest.py --write
  python3 scripts/cici_journal_ob1_digest.py --include-session-transcript --write
  python3 scripts/cici_journal_ob1_digest.py --no-inbox --write
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
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import TextIO
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

DEFAULT_JOURNAL = REPO_ROOT / "docs/skill-work/work-cici/cici-notebook"
DEFAULT_OWNER = "Xavier-x01"
DEFAULT_REPO = "Cici"
DEFAULT_BRANCH = "main"

SESSION_TRANSCRIPT_MAX_LINES = 80
SESSION_TRANSCRIPT_MAX_CHARS = 12000
DEFAULT_STRATEGY_NOTEBOOK_MAX_CHARS = 10000
DEFAULT_SESSION_TRANSCRIPT = REPO_ROOT / "users" / "grace-mar" / "session-transcript.md"


def _env_truthy(*keys: str) -> bool:
    for k in keys:
        v = os.environ.get(k, "").strip().lower()
        if v in ("1", "true", "yes", "on"):
            return True
    return False


try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    yaml = None  # type: ignore[misc, assignment]


@dataclass(frozen=True)
class CommitLine:
    sha: str
    short_message: str
    html_url: str


@dataclass
class DayContext:
    """L2/L3 inputs merged into the journal (inbox, transcript, strategy notebook, artifacts)."""

    inbox_markdown: str | None = None
    inbox_provenance: list[str] = field(default_factory=list)
    strategy_notebook_excerpt: str | None = None
    strategy_notebook_source: str | None = None
    transcript_excerpt: str | None = None
    artifacts: list[str] = field(default_factory=list)


_RE_TRANSCRIPT_LINE = re.compile(r"^\*\*\[(\d{4}-\d{2}-\d{2})\s+[^\]]+\]\*\*")
_RE_FRONTMATTER = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.DOTALL)


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


_RE_CONV_COMMIT = re.compile(
    r"^(\w+)(?:\([^)]*\))?\s*:\s*(.+)$",
    re.DOTALL,
)

_RE_DATE_ONLY = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
_RE_LEGACY = re.compile(r"^(\d{4}-\d{2}-\d{2})-day-(\d+)\.md$")
_RE_TITLE_DAY = re.compile(
    r"^#\s+(?:Cici|Xavier)\s+(?:journal|notebook)\s+—\s+Day\s+(\d+)\s*$",
    re.MULTILINE,
)
_RE_BODY_JOURNAL_DAY = re.compile(r"\*\*Journal day:\*\*\s*(\d+)")


def _journal_day_from_file(path: Path) -> int | None:
    """Best-effort journal day index from legacy or new daily file."""
    m = _RE_LEGACY.match(path.name)
    if m:
        return int(m.group(2))
    text = path.read_text(encoding="utf-8", errors="ignore")
    bm = _RE_BODY_JOURNAL_DAY.search(text)
    if bm:
        return int(bm.group(1))
    tm = _RE_TITLE_DAY.search(text)
    if tm:
        return int(tm.group(1))
    return None


def next_journal_day_number(journal_dir: Path) -> int:
    """Next ordinal journal day: max(parsed from entries) + 1.

    Supports **new** filenames ``YYYY-MM-DD.md`` (parse ``**Journal day:**`` or title),
    and **legacy** ``YYYY-MM-DD-day-NN.md``. Ignores ``README.md``.
    """
    max_n = 0
    for p in journal_dir.glob("*.md"):
        if p.name == "README.md":
            continue
        if _RE_DATE_ONLY.match(p.name) or _RE_LEGACY.match(p.name):
            n = _journal_day_from_file(p)
            if n is not None:
                max_n = max(max_n, n)
    return max_n + 1


def _conventional_kind(short_message: str) -> str:
    """Best-effort feat/docs/fix label from first line (Conventional Commits or plain)."""
    s = short_message.strip()
    m = _RE_CONV_COMMIT.match(s)
    if m:
        return m.group(1).lower()
    head = s.split(None, 1)[0].lower() if s else "other"
    if head.endswith(":"):
        head = head[:-1]
    return head if head else "other"


def _overview_markdown(commits: list[CommitLine], branch: str) -> list[str]:
    """Deterministic synthesis from commit messages — no LLM."""
    if not commits:
        return [
            "No commits on this branch in the activity window. If you expected activity, "
            "check `TZ`, branch name, or GitHub API rate limits.",
        ]
    n = len(commits)
    kinds: dict[str, int] = {}
    for c in commits:
        k = _conventional_kind(c.short_message)
        kinds[k] = kinds.get(k, 0) + 1
    kind_parts = [f"{k} ×{v}" for k, v in sorted(kinds.items(), key=lambda x: (-x[1], x[0]))]
    unique_msgs = list(dict.fromkeys(c.short_message for c in commits))
    out: list[str] = [
        f"**{n} commit(s)** on `{branch}` in this calendar window.",
        "",
        f"**By label (first token):** {', '.join(kind_parts)}.",
        "",
        "**Distinct first lines:**",
    ]
    cap = 12
    for msg in unique_msgs[:cap]:
        out.append(f"- {msg}")
    if len(unique_msgs) > cap:
        out.append(f"- …and {len(unique_msgs) - cap} more distinct line(s).")
    return out


def _split_frontmatter_body(raw: str) -> tuple[str, str]:
    m = _RE_FRONTMATTER.match(raw)
    if not m:
        return "", raw
    return m.group(1).strip(), raw[m.end() :]


def _artifacts_from_yaml_block(fm: str) -> list[str]:
    if not fm.strip():
        return []
    if yaml is not None:
        try:
            data = yaml.safe_load(fm)
            if isinstance(data, dict):
                a = data.get("artifacts")
                if isinstance(a, list):
                    return [str(x).strip() for x in a if str(x).strip()]
                if isinstance(a, str) and a.strip():
                    return [a.strip()]
        except Exception:
            pass
    # Minimal fallback: lines under artifacts:
    out: list[str] = []
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "artifacts:":
            i += 1
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if stripped and not line.startswith((" ", "\t")) and not stripped.startswith("-"):
                    break
                if stripped.startswith("- "):
                    p = stripped[2:].strip().strip("\"'")
                    if p:
                        out.append(p)
                i += 1
            break
        i += 1
    return out


def _read_artifact_sidecar(sidecar: Path) -> list[str]:
    if not sidecar.is_file():
        return []
    out: list[str] = []
    for line in sidecar.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def load_inbox_for_day(
    journal_dir: Path,
    day: date,
    *,
    no_inbox: bool,
) -> tuple[str | None, list[str], list[str]]:
    """Return (combined markdown body, provenance paths relative to journal_dir, repo-relative artifact paths)."""
    if no_inbox:
        return None, [], []
    iso = day.isoformat()
    inbox_root = journal_dir / "inbox"
    single = inbox_root / f"{iso}.md"
    folder = inbox_root / iso
    sidecar = inbox_root / f"{iso}-artifacts.txt"

    bodies: list[str] = []
    provenance: list[str] = []
    artifacts: list[str] = []

    if single.is_file():
        raw = single.read_text(encoding="utf-8", errors="replace")
        fm, body = _split_frontmatter_body(raw)
        artifacts.extend(_artifacts_from_yaml_block(fm))
        bodies.append(body.strip())
        provenance.append(f"inbox/{iso}.md")

    if folder.is_dir():
        for fp in sorted(folder.glob("*.md")):
            raw = fp.read_text(encoding="utf-8", errors="replace")
            fm, body = _split_frontmatter_body(raw)
            artifacts.extend(_artifacts_from_yaml_block(fm))
            bodies.append(body.strip())
            provenance.append(f"inbox/{iso}/{fp.name}")

    artifacts.extend(_read_artifact_sidecar(sidecar))
    if sidecar.is_file() and f"inbox/{iso}-artifacts.txt" not in provenance:
        provenance.append(f"inbox/{iso}-artifacts.txt")

    # Dedupe artifact paths preserving order
    seen: set[str] = set()
    uniq_art: list[str] = []
    for p in artifacts:
        if p not in seen:
            seen.add(p)
            uniq_art.append(p)

    if not bodies and not uniq_art:
        return None, [], []

    combined = "\n\n---\n\n".join(b for b in bodies if b) if bodies else None
    return combined, provenance, uniq_art


def extract_strategy_notebook_day_block(
    repo_root: Path,
    day: date,
    *,
    max_chars: int = DEFAULT_STRATEGY_NOTEBOOK_MAX_CHARS,
) -> tuple[str | None, str | None]:
    """Return the ``## YYYY-MM-DD`` section from the month ``days.md`` (geopolitical / strategy synthesis)."""
    ym = f"{day.year:04d}-{day.month:02d}"
    iso = day.isoformat()
    rel = f"docs/skill-work/work-strategy/strategy-notebook/chapters/{ym}/days.md"
    path = repo_root / rel
    if not path.is_file():
        return None, rel
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    start_i: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f"## {iso}" or stripped.startswith(f"## {iso} "):
            start_i = i
            break
    if start_i is None:
        return None, rel
    out: list[str] = []
    for j in range(start_i, len(lines)):
        if j > start_i and lines[j].startswith("## ") and not lines[j].strip().startswith(f"## {iso}"):
            break
        out.append(lines[j])
    block = "".join(out).strip()
    if not block:
        return None, rel
    if len(block) > max_chars:
        block = (
            block[: max_chars - 80].rstrip()
            + f"\n\n…(truncated at {max_chars} chars — see `{rel}`)"
        )
    return block, rel


def extract_session_transcript_for_day(
    path: Path,
    day: date,
    *,
    max_lines: int = SESSION_TRANSCRIPT_MAX_LINES,
    max_chars: int = SESSION_TRANSCRIPT_MAX_CHARS,
) -> str | None:
    """Lines from session-transcript whose bracket date matches day (YYYY-MM-DD in timestamp)."""
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    target = day.isoformat()
    segments: list[str] = []
    i = 0
    while i < len(lines):
        m = _RE_TRANSCRIPT_LINE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        day_str = m.group(1)
        start = i
        i += 1
        while i < len(lines) and not _RE_TRANSCRIPT_LINE.match(lines[i].strip()):
            i += 1
        if day_str == target:
            segments.append("\n".join(lines[start:i]).strip())
    if not segments:
        return None
    blob = "\n\n".join(segments)
    lines_out = blob.splitlines()
    if len(lines_out) > max_lines:
        blob = "\n".join(lines_out[:max_lines]) + f"\n\n…({len(lines_out) - max_lines} more lines truncated)"
    if len(blob) > max_chars:
        blob = blob[: max_chars - 20] + "\n\n…(truncated)"
    return blob


def _artifacts_render_lines(paths: list[str], repo_root: Path, stderr: TextIO) -> list[str]:
    lines: list[str] = []
    for rel in paths:
        p = (repo_root / rel).resolve()
        try:
            p.relative_to(repo_root.resolve())
        except ValueError:
            stderr.write(f"Warning: artifact path escapes repo root, skip: {rel}\n")
            continue
        if p.is_file():
            lines.append(f"- [`{rel}`]({rel})")
        else:
            stderr.write(f"Warning: artifact missing, skip: {rel}\n")
    return lines


def collect_day_context(
    journal_dir: Path,
    day: date,
    repo_root: Path,
    *,
    no_inbox: bool,
    include_transcript: bool,
    transcript_path: Path,
    include_strategy_notebook: bool,
    strategy_notebook_max_chars: int,
    stderr: TextIO,
) -> DayContext:
    inbox_md, prov, arts = load_inbox_for_day(journal_dir, day, no_inbox=no_inbox)
    tr: str | None = None
    if include_transcript:
        tr = extract_session_transcript_for_day(transcript_path, day)
    sn_ex: str | None = None
    sn_src: str | None = None
    if include_strategy_notebook:
        sn_ex, sn_src = extract_strategy_notebook_day_block(
            repo_root, day, max_chars=strategy_notebook_max_chars
        )
        if sn_ex is None and sn_src:
            sp = repo_root / sn_src
            if not sp.is_file():
                stderr.write(f"Note: strategy-notebook file not found: `{sn_src}`\n")
            else:
                stderr.write(
                    f"Note: no `## {day.isoformat()}` section in `{sn_src}` — "
                    "add a strategy pass for this date or capture geo/transcript in inbox.\n"
                )
    return DayContext(
        inbox_markdown=inbox_md,
        inbox_provenance=prov,
        strategy_notebook_excerpt=sn_ex,
        strategy_notebook_source=sn_src,
        transcript_excerpt=tr,
        artifacts=arts,
    )


def build_markdown(
    *,
    day_label: date,
    journal_day: int,
    tz_name: str,
    owner: str,
    repo: str,
    branch: str,
    commits: list[CommitLine],
    day_context: DayContext | None = None,
    repo_root: Path | None = None,
    stderr: TextIO | None = None,
) -> str:
    err = stderr or sys.stderr
    root = repo_root or REPO_ROOT
    ctx = day_context or DayContext()

    repo_url = f"https://github.com/{owner}/{repo}"
    lines = [
        f"# Cici notebook — Day {journal_day}",
        "",
        f"**Date:** {day_label.isoformat()}  ",
        f"**Journal day:** {journal_day} (OB1-focused learning)  ",
        f"**OB1 repo:** [{owner}/{repo}]({repo_url}) (`{branch}`)  ",
        f"**Activity window:** local calendar day in `{tz_name}` (commits from GitHub API `since`/`until`)  ",
        "",
        "---",
        "",
        "## Day overview (auto from commits)",
        "",
        *_overview_markdown(commits, branch),
        "",
        "---",
        "",
    ]

    has_operator = bool(
        (ctx.inbox_markdown and ctx.inbox_markdown.strip())
        or (ctx.transcript_excerpt and ctx.transcript_excerpt.strip())
        or (ctx.strategy_notebook_excerpt and ctx.strategy_notebook_excerpt.strip())
    )
    if has_operator:
        lines.append("## Operator context (ingested)")
        lines.append("")
        prov_bits: list[str] = []
        if ctx.inbox_provenance:
            prov_bits.extend(f"`{p}`" for p in ctx.inbox_provenance)
        if ctx.strategy_notebook_excerpt and ctx.strategy_notebook_excerpt.strip():
            prov_bits.append(f"`{ctx.strategy_notebook_source or 'strategy-notebook/days.md'}`")
        if ctx.transcript_excerpt and ctx.transcript_excerpt.strip():
            prov_bits.append("`session-transcript.md`")
        lines.append(f"*Sources: {', '.join(prov_bits)}*")
        lines.append("")
        if ctx.inbox_markdown and ctx.inbox_markdown.strip():
            lines.append("### Inbox")
            lines.append("")
            lines.append(ctx.inbox_markdown.strip())
            lines.append("")
        if ctx.strategy_notebook_excerpt and ctx.strategy_notebook_excerpt.strip():
            lines.append("### From strategy-notebook (same day)")
            lines.append("")
            lines.append(ctx.strategy_notebook_excerpt.strip())
            lines.append("")
        if ctx.transcript_excerpt and ctx.transcript_excerpt.strip():
            lines.append("### From session-transcript.md")
            lines.append("")
            lines.append(ctx.transcript_excerpt.strip())
            lines.append("")
        lines.append("---")
        lines.append("")

    if ctx.artifacts:
        art_lines = _artifacts_render_lines(ctx.artifacts, root, err)
        if art_lines:
            lines.append("## Artifacts referenced")
            lines.append("")
            lines.extend(art_lines)
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.extend(
        [
            "## OB1 repo activity (links to GitHub)",
            "",
        ]
    )
    if not commits:
        lines.extend(
            [
                "*No commit rows — window empty or API returned none.*",
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
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build cici-notebook day file from OB1 GitHub commits.")
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
        help="Path to cici-notebook folder",
    )
    ap.add_argument("--day", type=int, default=None, help="Journal day number (default: next from existing files)")
    ap.add_argument(
        "--write",
        action="store_true",
        help="Write YYYY-MM-DD.md under --journal-dir (won't overwrite unless --force)",
    )
    ap.add_argument("--force", action="store_true", help="Overwrite existing day file")
    ap.add_argument("--stdout-only", action="store_true", help="Print markdown only; do not write")
    ap.add_argument(
        "--catch-up-from-last-dream",
        action="store_true",
        help="Use dream_catchup window (last-dream.json before overwrite): write one file per local day in range (skip existing unless --force).",
    )
    ap.add_argument(
        "--users-dir",
        type=Path,
        default=REPO_ROOT / "users",
        help="Users directory (for last-dream.json when using --catch-up-from-last-dream)",
    )
    ap.add_argument(
        "--user-id",
        default="grace-mar",
        help="User id for last-dream.json path",
    )
    ap.add_argument(
        "--no-inbox",
        action="store_true",
        help="Skip inbox/ and artifact sidecar (git overview + OB1 links only)",
    )
    ap.add_argument(
        "--include-session-transcript",
        action="store_true",
        help="Include lines from session-transcript.md for the calendar day (default: off)",
    )
    ap.add_argument(
        "--session-transcript-path",
        type=Path,
        default=DEFAULT_SESSION_TRANSCRIPT,
        help="Path to session-transcript.md (default: users/grace-mar/session-transcript.md)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Grace-mar repo root (artifact path resolution; default: auto)",
    )
    ap.add_argument(
        "--include-strategy-notebook",
        action="store_true",
        help="Include the ## YYYY-MM-DD block from strategy-notebook chapters/…/days.md (geopolitical synthesis)",
    )
    ap.add_argument(
        "--strategy-notebook-max-chars",
        type=int,
        default=DEFAULT_STRATEGY_NOTEBOOK_MAX_CHARS,
        help=f"Max chars for strategy-notebook excerpt (default: {DEFAULT_STRATEGY_NOTEBOOK_MAX_CHARS})",
    )
    ap.add_argument(
        "--full-day-synthesis",
        action="store_true",
        help="Shorthand: enable --include-session-transcript and --include-strategy-notebook",
    )
    args = ap.parse_args()

    if args.full_day_synthesis:
        args.include_session_transcript = True
        args.include_strategy_notebook = True
    if _env_truthy("CICI_JOURNAL_FULL_DAY_SYNTHESIS", "CICI_JOURNAL_FULL_DAY_SYNTHESIS"):
        args.include_session_transcript = True
        args.include_strategy_notebook = True

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    if args.catch_up_from_last_dream:
        try:
            from dream_catchup import catch_up_window_dict
        except ImportError:
            from scripts.dream_catchup import catch_up_window_dict  # type: ignore

        dc = catch_up_window_dict(
            users_dir=args.users_dir,
            user_id=args.user_id,
            now_utc=datetime.now(timezone.utc),
        )
        raw_dates = dc.get("local_calendar_dates") or []
        if not raw_dates:
            print("catch-up: no local calendar dates in window", file=sys.stderr)
            return
        if not args.write:
            print(
                "Catch-up window (since previous dream): "
                + ", ".join(raw_dates)
                + "\nRe-run with --write to create missing journal files.",
                file=sys.stderr,
            )
            return
        written: list[str] = []
        skipped: list[str] = []
        for iso in raw_dates:
            day_label = date.fromisoformat(iso)
            primary = args.journal_dir / f"{iso}.md"
            legacy = sorted(args.journal_dir.glob(f"{iso}-day-*.md"))
            if primary.exists() and not args.force:
                skipped.append(primary.name)
                continue
            if legacy and not args.force:
                skipped.append(legacy[0].name)
                continue
            commits = fetch_commits_for_day(
                args.owner, args.repo, args.branch, day_label, args.tz, token
            )
            journal_day = next_journal_day_number(args.journal_dir)
            dctx = collect_day_context(
                args.journal_dir,
                day_label,
                args.repo_root,
                no_inbox=args.no_inbox,
                include_transcript=args.include_session_transcript,
                transcript_path=args.session_transcript_path,
                include_strategy_notebook=args.include_strategy_notebook,
                strategy_notebook_max_chars=args.strategy_notebook_max_chars,
                stderr=sys.stderr,
            )
            md = build_markdown(
                day_label=day_label,
                journal_day=journal_day,
                tz_name=args.tz,
                owner=args.owner,
                repo=args.repo,
                branch=args.branch,
                commits=commits,
                day_context=dctx,
                repo_root=args.repo_root,
                stderr=sys.stderr,
            )
            out_path = args.journal_dir / f"{day_label.isoformat()}.md"
            args.journal_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            written.append(str(out_path))
        for w in written:
            print(w)
        if skipped:
            print(f"skipped (exists): {skipped}", file=sys.stderr)
        return

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

    dctx = collect_day_context(
        args.journal_dir,
        day_label,
        args.repo_root,
        no_inbox=args.no_inbox,
        include_transcript=args.include_session_transcript,
        transcript_path=args.session_transcript_path,
        include_strategy_notebook=args.include_strategy_notebook,
        strategy_notebook_max_chars=args.strategy_notebook_max_chars,
        stderr=sys.stderr,
    )
    md = build_markdown(
        day_label=day_label,
        journal_day=journal_day,
        tz_name=args.tz,
        owner=args.owner,
        repo=args.repo,
        branch=args.branch,
        commits=commits,
        day_context=dctx,
        repo_root=args.repo_root,
        stderr=sys.stderr,
    )

    out_path = args.journal_dir / f"{day_label.isoformat()}.md"

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
