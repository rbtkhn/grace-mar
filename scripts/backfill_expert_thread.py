#!/usr/bin/env python3
"""
Backfill an expert thread with a clearly labeled reconstructed historical arc.

Design goals
------------
- WORK-only; not Record.
- Do NOT touch the machine extraction block between:
    <!-- strategy-expert-thread:start -->
    <!-- strategy-expert-thread:end -->
- Write only above the thread markers (after Segment 1 / bridge lines, immediately
  before <!-- strategy-expert-thread:start -->).
- Preserve existing narrative journal text by default.
- Make reconstruction provenance explicit.
- Prefer primary notebook artifacts in this repo:
    * strategy-expert-<expert_id>-transcript.md
    * chapters/YYYY-MM/days.md
    * chapters/YYYY-MM/knots/strategy-notebook-knot-*.md
    * git log (best-effort, no content invention)

Typical use
-----------
python3 scripts/backfill_expert_thread.py \\
  --expert-id scott-ritter \\
  --start 2026-01-01 \\
  --end 2026-03-31 \\
  --apply

Dry run
-------
python3 scripts/backfill_expert_thread.py \\
  --expert-id scott-ritter \\
  --start 2026-01-01 \\
  --end 2026-03-31 \\
  --dry-run

Notes
-----
- This script intentionally produces dated bullets, not smooth faux-contemporaneous prose.
- It is conservative: if evidence is weak, it emits less.
- It creates/updates a dedicated backfill block:
    <!-- backfill:<expert_id>:start -->
    <!-- backfill:<expert_id>:end -->
  above the thread markers, so reruns are idempotent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
CHAPTERS_DIR = NOTEBOOK_DIR / "chapters"
ARTIFACT_DIR = REPO_ROOT / "artifacts/skill-work/work-strategy/backfills"

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
THREAD_MARKER_END = "<!-- strategy-expert-thread:end -->"

SCRIPT_VERSION = "1"

DEFAULT_ALIASES = {
    "scott-ritter": ["scott ritter", "ritter", "thread:scott-ritter"],
}

DATE_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
KNOT_DATE_RE = re.compile(r"strategy-notebook-knot-(\d{4}-\d{2}-\d{2})-")
WHITESPACE_RE = re.compile(r"\s+")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+")
CODE_FENCE_RE = re.compile(r"^\s*```")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass
class Evidence:
    event_date: str
    source_type: str
    path: str
    title: str
    summary: str
    anchors: list[str]
    git_last_commit: Optional[str] = None
    git_last_commit_date: Optional[str] = None
    confidence: str = "medium"


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def month_key(d: date) -> str:
    return d.strftime("%Y-%m")


def ensure_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def truncate(text: str, max_len: int = 220) -> str:
    text = normalize_space(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def marker_block_start(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:start -->"


def marker_block_end(expert_id: str) -> str:
    return f"<!-- backfill:{expert_id}:end -->"


def run_git(args: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def git_available() -> bool:
    cp = run_git(["rev-parse", "--is-inside-work-tree"])
    return cp.returncode == 0 and "true" in cp.stdout.lower()


def git_last_touch(path: Path) -> tuple[Optional[str], Optional[str]]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    cp = run_git(["log", "-1", "--format=%H|%cs", "--", rel])
    if cp.returncode != 0 or not cp.stdout.strip():
        return None, None
    raw = cp.stdout.strip().splitlines()[0]
    if "|" not in raw:
        return raw, None
    sha, d = raw.split("|", 1)
    return sha[:12], d.strip()


def git_mentions_for_expert(
    expert_id: str, aliases: list[str], start: date, end: date
) -> list[Evidence]:
    """Best-effort: commits in date range touching strategy-notebook with -G match."""
    if not git_available():
        return []

    # Match expert id or thread: form in diffs
    needles = sorted({expert_id, f"thread:{expert_id}", *aliases[:5]}, key=len, reverse=True)
    pattern = "|".join(re.escape(n) for n in needles if n)

    cp = run_git(
        [
            "log",
            f"--since={start.isoformat()}",
            f"--until={end.isoformat()}T23:59:59",
            "--regexp-ignore-case",
            "-G",
            pattern,
            "--format=%H|%cs|%s",
            "--",
            "docs/skill-work/work-strategy/strategy-notebook",
        ]
    )

    if cp.returncode != 0 or not cp.stdout.strip():
        return []

    results: list[Evidence] = []
    for line in cp.stdout.strip().splitlines():
        if "|" not in line:
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        sha, d, subj = parts[0], parts[1], parts[2]
        try:
            commit_d = parse_date(d[:10])
        except ValueError:
            continue
        if not (start <= commit_d <= end):
            continue
        results.append(
            Evidence(
                event_date=d[:10],
                source_type="git",
                path="docs/skill-work/work-strategy/strategy-notebook",
                title="Git commit touching notebook",
                summary=truncate(subj, 180),
                anchors=[sha[:12]],
                git_last_commit=sha[:12],
                git_last_commit_date=d[:10],
                confidence="low",
            )
        )
    return dedupe_evidence(results)


def aliases_for(expert_id: str, extra_aliases: list[str]) -> list[str]:
    aliases = list(DEFAULT_ALIASES.get(expert_id, []))
    aliases.extend(extra_aliases)
    aliases.append(expert_id.replace("-", " "))
    last = expert_id.split("-")[-1]
    if last not in aliases:
        aliases.append(last)
    seen: set[str] = set()
    out: list[str] = []
    for a in aliases:
        a_norm = a.strip().lower()
        if a_norm and a_norm not in seen:
            seen.add(a_norm)
            out.append(a_norm)
    return out


def text_mentions_any(text: str, aliases: list[str]) -> bool:
    lowered = text.lower()
    return any(alias in lowered for alias in aliases)


def extract_nontrivial_lines(block: str) -> list[str]:
    lines: list[str] = []
    in_code = False
    for raw in block.splitlines():
        line = raw.rstrip()
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            continue
        if HEADING_RE.match(line):
            continue
        if "Accumulator for:" in line:
            continue
        if line.strip() in {"---", "___"}:
            continue
        stripped = HTML_COMMENT_RE.sub("", line).strip()
        if stripped:
            lines.append(stripped)
    return lines


def best_summary_from_block(block: str) -> str:
    lines = extract_nontrivial_lines(block)

    bullet_candidates: list[str] = []
    plain_candidates: list[str] = []

    for line in lines:
        m = BULLET_RE.match(line)
        if m:
            bullet_candidates.append(m.group(1))
        else:
            plain_candidates.append(line)

    for candidate in bullet_candidates + plain_candidates:
        summary = MARKDOWN_LINK_RE.sub(r"\1", candidate)
        summary = summary.strip("` ")
        summary = normalize_space(summary)
        if len(summary) >= 28:
            return truncate(summary, 220)

    joined = normalize_space(" ".join(lines))
    return truncate(joined, 220) if joined else ""


def parse_date_sections(text: str) -> dict[str, str]:
    matches = list(DATE_HEADING_RE.finditer(text))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        d = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[d] = text[start:end].strip()
    return sections


def source_anchor_label(path: Path, d: str) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return f"{rel}#{d}"


def collect_transcript_evidence(
    expert_id: str, aliases: list[str], start: date, end: date
) -> list[Evidence]:
    path = NOTEBOOK_DIR / f"strategy-expert-{expert_id}-transcript.md"
    if not path.is_file():
        return []
    text = ensure_text(path)
    sections = parse_date_sections(text)
    sha, sha_date = git_last_touch(path)
    out: list[Evidence] = []

    for d_str, block in sections.items():
        try:
            d = parse_date(d_str)
        except ValueError:
            continue
        if not (start <= d <= end):
            continue
        summary = best_summary_from_block(block)
        if not summary:
            continue
        out.append(
            Evidence(
                event_date=d_str,
                source_type="transcript",
                path=path.relative_to(REPO_ROOT).as_posix(),
                title="Transcript section",
                summary=summary,
                anchors=[source_anchor_label(path, d_str)],
                git_last_commit=sha,
                git_last_commit_date=sha_date,
                confidence="high",
            )
        )
    return out


def iter_days_files(start: date, end: date) -> Iterable[Path]:
    seen: set[Path] = set()
    cur = date(start.year, start.month, 1)
    end_month = date(end.year, end.month, 1)
    while cur <= end_month:
        p = CHAPTERS_DIR / cur.strftime("%Y-%m") / "days.md"
        if p not in seen:
            seen.add(p)
            yield p
        if cur.month == 12:
            cur = date(cur.year + 1, 1, 1)
        else:
            cur = date(cur.year, cur.month + 1, 1)


def collect_days_evidence(
    expert_id: str, aliases: list[str], start: date, end: date
) -> list[Evidence]:
    out: list[Evidence] = []
    for path in iter_days_files(start, end):
        if not path.is_file():
            continue
        text = ensure_text(path)
        sections = parse_date_sections(text)
        sha, sha_date = git_last_touch(path)

        for d_str, block in sections.items():
            try:
                d = parse_date(d_str)
            except ValueError:
                continue
            if not (start <= d <= end):
                continue
            if not text_mentions_any(block, aliases):
                continue
            summary = best_summary_from_block(block)
            if not summary:
                continue
            out.append(
                Evidence(
                    event_date=d_str,
                    source_type="days",
                    path=path.relative_to(REPO_ROOT).as_posix(),
                    title="days.md dated block",
                    summary=summary,
                    anchors=[source_anchor_label(path, d_str)],
                    git_last_commit=sha,
                    git_last_commit_date=sha_date,
                    confidence="high",
                )
            )
    return out


def knot_date_from_path(path: Path) -> Optional[date]:
    m = KNOT_DATE_RE.search(path.name)
    if not m:
        return None
    try:
        return parse_date(m.group(1))
    except ValueError:
        return None


def collect_knot_evidence(
    expert_id: str, aliases: list[str], start: date, end: date
) -> list[Evidence]:
    """Knots live under chapters/YYYY-MM/knots/ (not notebook root)."""
    out: list[Evidence] = []
    for path in sorted(CHAPTERS_DIR.rglob("strategy-notebook-knot-*.md")):
        d = knot_date_from_path(path)
        if d is None or not (start <= d <= end):
            continue
        text = ensure_text(path)
        if not text_mentions_any(text, aliases):
            continue
        sha, sha_date = git_last_touch(path)
        summary = best_summary_from_block(text)
        if not summary:
            summary = truncate(
                path.stem.replace("strategy-notebook-knot-", "").replace("-", " "),
                180,
            )
        out.append(
            Evidence(
                event_date=d.isoformat(),
                source_type="knot",
                path=path.relative_to(REPO_ROOT).as_posix(),
                title=path.name,
                summary=summary,
                anchors=[path.relative_to(REPO_ROOT).as_posix()],
                git_last_commit=sha,
                git_last_commit_date=sha_date,
                confidence="medium",
            )
        )
    return out


def dedupe_evidence(items: list[Evidence]) -> list[Evidence]:
    seen: set[tuple[str, str, str, str]] = set()
    out: list[Evidence] = []
    for item in sorted(items, key=lambda x: (x.event_date, x.source_type, x.path, x.summary)):
        key = (item.event_date, item.source_type, item.path, item.summary)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def grouped_by_month(items: list[Evidence]) -> dict[str, list[Evidence]]:
    groups: dict[str, list[Evidence]] = defaultdict(list)
    for item in sorted(items, key=lambda x: (x.event_date, x.source_type, x.path)):
        try:
            d = parse_date(item.event_date)
            groups[month_key(d)].append(item)
        except ValueError:
            continue
    return dict(sorted(groups.items()))


def format_bullet(item: Evidence) -> str:
    source_stub = f"{item.source_type}: `{item.path}`"
    if item.git_last_commit and item.git_last_commit_date:
        source_stub += f" (last touch {item.git_last_commit_date} {item.git_last_commit})"
    return f"- **{item.event_date}** — {item.summary}  \n  _Source:_ {source_stub}"


def render_backfill_block(expert_id: str, start: date, end: date, evidence: list[Evidence]) -> str:
    groups = grouped_by_month(evidence)
    lines: list[str] = []
    lines.append(marker_block_start(expert_id))
    lines.append("## Backfilled historical arc (reconstructed from notebook artifacts)")
    lines.append("")
    lines.append(
        f"**Scope:** `{expert_id}` from **{start.isoformat()}** through **{end.isoformat()}**."
    )
    lines.append(
        "**Status:** Reconstructed summary from primary notebook artifacts and best-effort git "
        "history; not contemporaneous journal prose."
    )
    lines.append(
        "**Rules:** Dated bullets only; contradictions should be preserved in source materials "
        "rather than harmonized here."
    )
    lines.append("")

    if not groups:
        lines.append("_No eligible evidence found in the requested window._")
        lines.append(marker_block_end(expert_id))
        return "\n".join(lines) + "\n"

    for month, items in groups.items():
        lines.append(f"### {month}")
        lines.append("")
        for item in items:
            lines.append(format_bullet(item))
        lines.append("")

    lines.append(marker_block_end(expert_id))
    return "\n".join(lines).rstrip() + "\n"


def extract_machine_block(text: str) -> Optional[str]:
    """Bytes between strategy-expert-thread start and end markers (inclusive)."""
    start = text.find(THREAD_MARKER_START)
    end = text.find(THREAD_MARKER_END)
    if start == -1 or end == -1 or end < start:
        return None
    end_full = end + len(THREAD_MARKER_END)
    return text[start:end_full]


def splice_backfill_into_thread(
    thread_text: str, expert_id: str, block: str, replace_backfill: bool
) -> str:
    start_marker = marker_block_start(expert_id)
    end_marker = marker_block_end(expert_id)

    existing_re = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )

    if existing_re.search(thread_text):
        return existing_re.sub(block.rstrip(), thread_text, count=1)

    idx = thread_text.find(THREAD_MARKER_START)
    if idx != -1:
        prefix = thread_text[:idx].rstrip() + "\n\n"
        suffix = thread_text[idx:].lstrip("\n")
        return prefix + block.rstrip() + "\n\n" + suffix

    m = re.search(r"^###\s+Machine extraction.*$", thread_text, re.MULTILINE)
    if m:
        prefix = thread_text[: m.start()].rstrip() + "\n\n"
        suffix = thread_text[m.start() :].lstrip("\n")
        return prefix + block.rstrip() + "\n\n" + suffix

    return thread_text.rstrip() + "\n\n" + block.rstrip() + "\n"


def build_report(
    expert_id: str, start: date, end: date, aliases: list[str]
) -> dict:
    evidence: list[Evidence] = []
    evidence.extend(collect_transcript_evidence(expert_id, aliases, start, end))
    evidence.extend(collect_days_evidence(expert_id, aliases, start, end))
    evidence.extend(collect_knot_evidence(expert_id, aliases, start, end))
    evidence.extend(git_mentions_for_expert(expert_id, aliases, start, end))
    evidence = dedupe_evidence(evidence)

    script_path = Path(__file__).resolve()
    script_sha = hashlib.sha256(script_path.read_bytes()).hexdigest()[:12]

    return {
        "tool": "backfill_expert_thread.py",
        "tool_version": SCRIPT_VERSION,
        "script_sha256_12": script_sha,
        "expert_id": expert_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "aliases": aliases,
        "evidence_count": len(evidence),
        "evidence": [asdict(e) for e in evidence],
    }


def write_json_report(expert_id: str, start: date, end: date, report: dict) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    out = ARTIFACT_DIR / f"{expert_id}-{start.isoformat()}-{end.isoformat()}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def validate_expert_id(expert_id: str) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        from strategy_expert_corpus import CANONICAL_EXPERT_IDS  # type: ignore
    except Exception:
        return
    if expert_id not in CANONICAL_EXPERT_IDS:
        raise SystemExit(
            f"Unknown expert_id `{expert_id}`. "
            f"Expected one of the canonical ids from strategy_expert_corpus.py."
        )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expert-id", required=True)
    p.add_argument("--start", required=True, help="YYYY-MM-DD")
    p.add_argument("--end", required=True, help="YYYY-MM-DD")
    p.add_argument(
        "--alias",
        action="append",
        default=[],
        help="Extra alias to match, repeatable. Example: --alias 'Scott Ritter'",
    )
    p.add_argument(
        "--thread-path",
        type=Path,
        default=None,
        help="Override thread path. Default: notebook strategy-expert-<expert_id>-thread.md",
    )
    p.add_argument("--apply", action="store_true", help="Write into the thread file")
    p.add_argument("--dry-run", action="store_true", help="Print block and summary only")
    p.add_argument(
        "--replace-backfill",
        action="store_true",
        help="Replace existing backfill block if present (default: replace for idempotency)",
    )
    p.add_argument(
        "--no-json-report",
        action="store_true",
        help="Skip writing JSON provenance sidecar",
    )
    args = p.parse_args()

    expert_id = args.expert_id.strip()
    validate_expert_id(expert_id)

    start = parse_date(args.start)
    end = parse_date(args.end)
    if end < start:
        raise SystemExit("--end must be on or after --start")

    aliases = aliases_for(expert_id, args.alias)

    thread_path = args.thread_path or (NOTEBOOK_DIR / f"strategy-expert-{expert_id}-thread.md")
    if not thread_path.is_file():
        raise SystemExit(f"Thread file not found: {thread_path}")

    report = build_report(expert_id, start, end, aliases)
    evidence = [Evidence(**item) for item in report["evidence"]]
    block = render_backfill_block(expert_id, start, end, evidence)

    print(f"expert_id: {expert_id}")
    print(f"window:    {start.isoformat()} → {end.isoformat()}")
    print(f"aliases:   {', '.join(aliases)}")
    print(f"evidence:  {len(evidence)}")
    print(f"thread:    {thread_path.relative_to(REPO_ROOT)}")
    print("")

    if not args.no_json_report:
        report_path = write_json_report(expert_id, start, end, report)
        print(f"json:      {report_path.relative_to(REPO_ROOT)}")
        print("")

    if args.dry_run or not args.apply:
        print(block)
        if not args.apply:
            print("\n(Not applied. Re-run with --apply to write into the thread file.)")
        return 0

    original = ensure_text(thread_path)
    machine_before = extract_machine_block(original)
    if machine_before is None:
        raise SystemExit(
            f"Cannot find {THREAD_MARKER_START!r} … {THREAD_MARKER_END!r} in {thread_path}; abort."
        )

    updated = splice_backfill_into_thread(
        original,
        expert_id=expert_id,
        block=block,
        replace_backfill=args.replace_backfill,
    )

    machine_after = extract_machine_block(updated)
    if machine_after != machine_before:
        raise SystemExit(
            "Refusing to write: machine extraction block would change. "
            "This should never happen — report as bug."
        )

    if updated == original:
        print("No changes needed.")
        return 0

    thread_path.write_text(updated, encoding="utf-8")
    print(f"Applied backfill block to {thread_path.relative_to(REPO_ROOT)}")
    print("Machine extraction block unchanged (verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
