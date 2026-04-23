#!/usr/bin/env python3
"""
Re-entry context for work-strategy: synthesize notebook day + inbox + brief + index pointers.

Read-only by default. Optional --log appends a WORK-choice receipt to session-transcript.md
via scripts/log_operator_choice.py (same mechanism as work-menu-conventions).

Optional --recent N (or --history for N=20) appends a lightweight **recent strategy activity**
section after state: merges strategy-fold-events.jsonl, filtered WORK-choice blocks from
session-transcript.md, and optional git commits under docs/skill-work/work-strategy.

Usage:
  python3 scripts/strategy_context.py -u grace-mar
  python3 scripts/strategy_context.py -u grace-mar --date 2026-04-13 --compact
  python3 scripts/strategy_context.py -u grace-mar --meta --minds
  python3 scripts/strategy_context.py -u grace-mar --max-words 120 --log
  python3 scripts/strategy_context.py -u grace-mar --recent 20
  python3 scripts/strategy_context.py -u grace-mar --history --recent-git 5
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir, read_path  # noqa: E402

STRATEGY_DIR = REPO_ROOT / "docs" / "skill-work" / "work-strategy"
NOTEBOOK = STRATEGY_DIR / "strategy-notebook"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACCUM_RE = re.compile(
    r"^\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})\b", re.MULTILINE
)

# --- Lightweight history (session-transcript WORK-choice + fold JSONL + optional git) ---
WORK_CHOICE_BLOCK_RE = re.compile(
    r"### \[WORK-choice\]\s+(\S+).*?(?=### \[WORK-choice\]|\Z)",
    re.DOTALL,
)
WC_CONTEXT_RE = re.compile(r"^-\s*context:\s*(\S+)\s*$", re.MULTILINE)
WC_PICKED_RE = re.compile(r"^-\s*picked:\s*(.+)$", re.MULTILINE)
WC_TAGS_RE = re.compile(r"^-\s*tags:\s*(.+)$", re.MULTILINE)
WC_NOTE_RE = re.compile(r"^-\s*note:\s*(.+)$", re.MULTILINE)

STRATEGY_KEYWORDS = (
    "strategy",
    "strategy-context",
    "weave",
    "strategy-page",
    "batch-analysis",
    "thread",
    "inbox",
    "work-strategy",
)


@dataclass(frozen=True)
class HistoryEvent:
    ts: datetime
    kind: str
    summary: str


def _parse_iso_ts(ts_raw: str) -> datetime | None:
    ts_raw = ts_raw.strip()
    try:
        return datetime.strptime(ts_raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def work_choice_is_strategy_adjacent(
    context: str, picked: str, tags: str | None, note: str | None
) -> bool:
    c = (context or "").strip().upper()
    if c == "WORK":
        return True
    blob = f"{picked} {tags or ''} {note or ''}".lower()
    return any(k in blob for k in STRATEGY_KEYWORDS)


def parse_work_choice_strategy_events(transcript_text: str) -> list[HistoryEvent]:
    """Parse session-transcript WORK-choice blocks; keep strategy-adjacent rows only."""
    out: list[HistoryEvent] = []
    for m in WORK_CHOICE_BLOCK_RE.finditer(transcript_text):
        ts_raw = m.group(1).strip()
        block = m.group(0)
        ts = _parse_iso_ts(ts_raw)
        if ts is None:
            continue
        pm = WC_PICKED_RE.search(block)
        if not pm:
            continue
        picked = pm.group(1).strip()
        cm = WC_CONTEXT_RE.search(block)
        context = cm.group(1).strip() if cm else ""
        tm = WC_TAGS_RE.search(block)
        tags = tm.group(1).strip() if tm else None
        nm = WC_NOTE_RE.search(block)
        note = nm.group(1).strip() if nm else None
        if not work_choice_is_strategy_adjacent(context, picked, tags, note):
            continue
        parts = [f"context={context}", f"picked={picked}"]
        if tags:
            parts.append(f"tags={tags[:120]}{'…' if len(tags) > 120 else ''}")
        if note:
            n = note.replace("\n", " ")[:200]
            parts.append(f"note={n}{'…' if len(note) > 200 else ''}")
        out.append(HistoryEvent(ts=ts, kind="WORK-choice", summary=" — ".join(parts)))
    return out


def parse_fold_jsonl_events(path: Path) -> list[HistoryEvent]:
    """Load strategy-fold-events.jsonl; one event per valid JSON line."""
    out: list[HistoryEvent] = []
    raw = read_path(path)
    if not raw.strip():
        return out
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts_s = row.get("ts") or ""
        ts = _parse_iso_ts(ts_s) if isinstance(ts_s, str) else None
        if ts is None:
            continue
        nb = row.get("notebook_date", "")
        fk = row.get("fold_kind", "")
        note = (row.get("note") or "").replace("\n", " ")[:240]
        gref = row.get("git_ref", "")
        tail = f" — {note}" if note else ""
        gbit = f" git={gref[:8]}…" if isinstance(gref, str) and len(gref) >= 8 else ""
        summary = f"fold {fk} — {nb}{tail}{gbit}"
        out.append(HistoryEvent(ts=ts, kind="fold", summary=summary))
    return out


def git_strategy_lane_events(repo_root: Path, limit: int) -> list[HistoryEvent]:
    """Last `limit` commits touching docs/skill-work/work-strategy; empty if git fails."""
    if limit <= 0:
        return []
    try:
        r = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "log",
                f"-n{limit}",
                "--format=%cI%x09%s",
                "--",
                "docs/skill-work/work-strategy",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"strategy-context: git log skipped ({e})", file=sys.stderr)
        return []
    if r.returncode != 0:
        print("strategy-context: git log failed (non-fatal)", file=sys.stderr)
        return []
    out: list[HistoryEvent] = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if "\t" not in line:
            continue
        iso, subj = line.split("\t", 1)
        try:
            ts = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        except ValueError:
            ts = _parse_iso_ts(iso)
            if ts is None:
                continue
        subj = subj.strip()[:200]
        out.append(
            HistoryEvent(ts=ts, kind="git", summary=f"git — {subj}")
        )
    return out


def merge_history_events(
    *,
    fold_events: list[HistoryEvent],
    wc_events: list[HistoryEvent],
    git_events: list[HistoryEvent],
    take: int,
) -> list[HistoryEvent]:
    merged = fold_events + wc_events + git_events
    merged.sort(key=lambda e: e.ts, reverse=True)
    return merged[:take]


def format_history_section(events: list[HistoryEvent]) -> str:
    """Markdown block for stdout; empty string if no events."""
    if not events:
        return ""
    lines = [
        "",
        "### Recent strategy activity (lightweight)",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        ts_s = ev.ts.strftime("%Y-%m-%dT%H:%M:%SZ")
        lines.append(f"{i}. {ts_s} — {ev.kind} — {ev.summary}")
    lines.extend(
        [
            "",
            "_Indicative only; canonical state remains days.md, expert pages, and git._",
            "",
        ]
    )
    return "\n".join(lines)


def _month_path(d: str) -> Path:
    y, m, _ = d.split("-")
    return NOTEBOOK / "chapters" / f"{y}-{m}" / "days.md"


def _knots_dir(d: str) -> Path:
    y, m, _ = d.split("-")
    return NOTEBOOK / "chapters" / f"{y}-{m}" / "knots"


def _meta_path(d: str) -> Path:
    y, m, _ = d.split("-")
    return NOTEBOOK / "chapters" / f"{y}-{m}" / "meta.md"


MINDS_DIR = STRATEGY_DIR / "minds"
MINDS_README = MINDS_DIR / "README.md"
MINDS_OUTPUTS = MINDS_DIR / "outputs"
OBSERVABILITY_JSON = REPO_ROOT / "artifacts" / "work-strategy" / "strategy-observability.json"


def extract_day_block(text: str, day: str) -> str | None:
    header = f"## {day}"
    idx = text.find(header)
    if idx < 0:
        return None
    start = idx + len(header)
    rest = text[start:]
    m = re.search(r"^## \d{4}-\d{2}-\d{2}\s*$", rest, re.MULTILINE)
    if m:
        rest = rest[: m.start()]
    return rest.strip()


def extract_h3_section(block: str, title: str) -> str:
    m = re.search(
        rf"^### {re.escape(title)}\s*\r?\n(.*?)(?=^### |^## |\Z)",
        block,
        re.DOTALL | re.MULTILINE,
    )
    if not m:
        return ""
    return m.group(1).strip()


def open_bullet_lines(open_body: str, *, limit: int = 6) -> list[str]:
    out: list[str] = []
    for line in open_body.splitlines():
        s = line.strip()
        if s.startswith("- "):
            # strip leading markdown noise for length
            t = s[2:].strip()
            t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
            t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
            if t:
                out.append(t)
            if len(out) >= limit:
                break
    return out


def truncate_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    if max_words < 2:
        return "…"
    # Reserve one token for ellipsis so total word-count stays ≤ max_words.
    return " ".join(words[: max_words - 1]).rstrip(",;:") + " …"


def count_expert_table_rows(md: str) -> int:
    """Count data rows in the strategy-commentator-threads expert_id table."""
    return len(re.findall(r"^\|\s*`[a-z0-9-]+`\s*\|", md, re.MULTILINE))


def scratch_metrics(inbox: str) -> tuple[str | None, int, bool]:
    acc = ACCUM_RE.search(inbox)
    accum = acc.group(1) if acc else None
    append_markers = (
        "_(Append below this line during the day.)_",
        "**_(Append below this line during the day.)_**",
    )
    pos = -1
    for mk in append_markers:
        p = inbox.find(mk)
        if p >= 0:
            pos = p + len(mk)
            break
    if pos < 0:
        return accum, 0, False
    tail = inbox[pos:].lstrip("\n")
    retained_idx = tail.find("### Retained reference")
    if retained_idx >= 0:
        between = tail[:retained_idx]
        has_retained = True
    else:
        between = tail
        has_retained = bool(re.search(r"### Retained", tail))
    between = between.strip()
    return accum, len(between), has_retained


def brief_excerpt(path: Path) -> str:
    if not path.is_file():
        return "Daily brief file not found for this date (generate or copy when ready)."
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", raw, re.MULTILINE)
    dline = f"dated {m.group(1)}" if m else "present"
    # First bullet under ## 1b (work-strategy focus)
    m2 = re.search(r"^## 1b\.\s*Work-strategy focus\s*\n", raw, re.MULTILINE)
    if m2:
        tail = raw[m2.end() :]
        for line in tail.splitlines():
            s = line.strip()
            if s.startswith("- "):
                lead = s[2:].strip()
                lead = re.sub(r"\*\*([^*]+)\*\*", r"\1", lead)
                lead = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lead)
                lead = lead[:220] + ("…" if len(lead) > 220 else "")
                return f"Daily brief {dline}; §1b lead: {lead}"
    return f"Daily brief {dline} (open for §1d–§1h watches in file)."


def meta_excerpt(path: Path) -> str:
    if not path.is_file():
        return "month meta.md not found for this chapter folder."
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^\*\*Theme:\*\*\s*(.+)$", raw, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
        return t[:200] + ("…" if len(t) > 200 else "")
    m2 = re.search(r"^\*\*Status:\*\*\s*`([^`]+)`", raw, re.MULTILINE)
    if m2:
        return f"status {m2.group(1).strip()}"
    return "present — see meta.md for month weave and thread rows."


def minds_excerpt(day: str) -> str:
    """Tri-Frame outputs: exact-date files, else recent month scaffolds."""
    y, m, _ = day.split("-")
    if not MINDS_OUTPUTS.is_dir():
        return "minds/outputs/ missing — check minds/README.md workflow."
    exact = sorted(MINDS_OUTPUTS.glob(f"{day}-*.md"))
    if exact:
        names = [p.name for p in exact[:8]]
        tail = f" (+{len(exact) - len(names)} more)" if len(exact) > len(names) else ""
        return f"minds/outputs for {day}: {', '.join(names)}{tail}."
    month_glob = f"{y}-{m}-*.md"
    month_files = sorted(MINDS_OUTPUTS.glob(month_glob), reverse=True)[:10]
    if month_files:
        names = [p.name for p in month_files]
        return (
            f"no outputs prefixed {day}-; recent {y}-{m} scaffolds in minds/outputs: "
            f"{', '.join(names)}."
        )
    return f"no Tri-Frame scaffolds under minds/outputs for {y}-{m} yet; see minds/README.md."


def health_summary() -> str | None:
    """Read observability JSON and return a concise health block, or None."""
    if not OBSERVABILITY_JSON.is_file():
        return None
    import json as _json

    try:
        doc = _json.loads(OBSERVABILITY_JSON.read_text(encoding="utf-8"))
    except Exception:
        return None
    jq = doc.get("metrics", {}).get("judgment_quality", {})
    if not jq:
        return None

    lines: list[str] = []
    lines.append(f"Lane health (observability v{doc.get('schemaVersion', '?')}):")

    total = jq.get("notebook_entries_total", 0)
    inbox = jq.get("inbox_pending_lines", 0)
    promo = jq.get("promotion_date_mentions", 0)
    lines.append(f"  entries={total}  inbox_pending={inbox}  promotion_mentions={promo}")

    months = jq.get("months", {})
    for month, m in sorted(months.items()):
        avg_sec = m.get("avg_sections_per_entry", 0)
        avg_lnk = m.get("avg_links_per_entry", 0)
        carry = m.get("open_carry_forward", 0)
        dated = m.get("dated_entries", 0)
        knots = m.get("legacy_chapter_stubs", m.get("knot_pages", 0))

        def _rate(val: float, green: float, yellow: float) -> str:
            if val >= green:
                return "green"
            if val >= yellow:
                return "yellow"
            return "red"

        sec_rating = _rate(avg_sec, 3.5, 2.5)
        lnk_rating = _rate(avg_lnk, 2.0, 1.0)
        carry_pct = (carry / dated * 100) if dated else 0
        carry_rating = "green" if carry_pct < 50 else ("yellow" if carry_pct < 75 else "red")

        lines.append(
            f"  {month}: {dated} entries, {knots} legacy chapter stubs | sections={avg_sec} ({sec_rating}) | "
            f"links={avg_lnk} ({lnk_rating}) | open_carry={carry}/{dated} ({carry_rating})"
        )

    inbox_rating = "green" if inbox <= 30 else ("yellow" if inbox <= 50 else "red")
    if inbox_rating != "green":
        lines.append(f"  inbox: {inbox_rating} — weave or prune recommended")

    return "\n".join(lines)


def build_paragraph(
    *,
    day: str,
    days_path: Path,
    day_block: str | None,
    open_bullets: list[str],
    accum: str | None,
    scratch_chars: int,
    has_retained: bool,
    brief_line: str,
    strategy_exists: bool,
    ladder_exists: bool,
    expert_rows: int,
    max_words: int,
    meta_line: str | None = None,
    minds_line: str | None = None,
) -> str:
    parts: list[str] = []
    if day_block is None:
        parts.append(
            f"No `## {day}` section in `{days_path.relative_to(REPO_ROOT)}` yet—add or fold inbox into this calendar day before treating the notebook as current."
        )
    else:
        ob = ", ".join(open_bullets[:3]) if open_bullets else "(no ### Open bullets parsed)"
        if len(open_bullets) > 3:
            ob += "; further items in ### Open."
        parts.append(
            f"Notebook {day}: Open queue highlights—{ob}"
        )
    inbox_note = []
    if accum:
        inbox_note.append(f"inbox accumulator targets {accum}")
    if scratch_chars:
        inbox_note.append(f"~{scratch_chars} characters captured below the append line")
    if has_retained:
        inbox_note.append("retained reference / verify buffer present—fold when Judgment is stable, not on empty ritual")
    if inbox_note:
        parts.append("Inbox: " + "; ".join(inbox_note) + ".")
    parts.append(brief_line + ".")
    promo = []
    if strategy_exists:
        promo.append("STRATEGY.md on disk for promotion / CORE checks")
    if ladder_exists:
        promo.append("promotion-ladder.md for stage semantics")
    if promo:
        parts.append("Promotion: " + "; ".join(promo) + ".")
    knot_dir = _knots_dir(day)
    knot_files = list(knot_dir.glob("strategy-notebook-knot-*.md")) if knot_dir.is_dir() else []
    if knot_files:
        parts.append(
            f"Legacy chapter markdown files this month: {len(knot_files)} (superseded layout)."
        )
    if expert_rows:
        parts.append(
            f"Commentator index lists {expert_rows} `expert_id` rows (strategy-commentator-threads.md)."
        )
    if meta_line:
        parts.append(f"Month meta: {meta_line}")
    if minds_line:
        parts.append(f"Minds: {minds_line}")
    text = " ".join(parts)
    return truncate_words(text, max_words)


def run_compact(
    *,
    day: str,
    paths: dict[str, Path],
    exists: dict[str, bool],
    day_block: str | None,
    open_bullets: list[str],
    accum: str | None,
    scratch_chars: int,
    expert_rows: int,
    meta_path: Path | None = None,
    meta_exists: bool = False,
    meta_line: str | None = None,
    include_minds: bool = False,
    minds_line: str | None = None,
) -> str:
    lines_out: list[str] = []
    lines_out.append(f"strategy-context — date {day} (repo-relative paths)")
    for key, p in paths.items():
        rel = p.relative_to(REPO_ROOT)
        ok = exists.get(key, p.is_file())
        tag = "ok" if ok else "missing"
        lines_out.append(f"- {rel} — {tag}")
    if meta_path is not None:
        rel = meta_path.relative_to(REPO_ROOT)
        tag = "ok" if meta_exists else "missing"
        lines_out.append(f"- {rel} — {tag}")
        if meta_line:
            lines_out.append(f"  meta excerpt: {meta_line}")
    if include_minds:
        mr = MINDS_README.relative_to(REPO_ROOT)
        mo = MINDS_OUTPUTS.relative_to(REPO_ROOT)
        lines_out.append(f"- {mr} — {'ok' if MINDS_README.is_file() else 'missing'}")
        lines_out.append(f"- {mo}/ — {'ok' if MINDS_OUTPUTS.is_dir() else 'missing'}")
        if minds_line:
            lines_out.append(f"  minds: {minds_line}")
    knot_dir = _knots_dir(day)
    knot_files = list(knot_dir.glob("strategy-notebook-knot-*.md")) if knot_dir.is_dir() else []
    lines_out.append(
        f"- days.md § {day}: {'present' if day_block else 'missing'}; Open bullets parsed: {len(open_bullets)}"
    )
    lines_out.append(
        f"- legacy chapter .md under chapters/.../knots/: {len(knot_files)} (if any; superseded)"
    )
    lines_out.append(
        f"- inbox accumulator: {accum or '?'}; scratch below append (pre-Retained): {scratch_chars} chars"
    )
    lines_out.append(f"- expert_id rows (table): {expert_rows}")
    return "\n".join(lines_out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument("--date", default="", help="YYYY-MM-DD (default: local calendar today)")
    ap.add_argument("--compact", action="store_true", help="Paths and one-line status only (no prose paragraph)")
    ap.add_argument("--max-words", type=int, default=120, metavar="N", help="Cap for default paragraph (default: 120)")
    ap.add_argument(
        "--log",
        action="store_true",
        help="Append WORK-choice receipt via log_operator_choice.py (session-transcript.md)",
    )
    ap.add_argument(
        "--meta",
        action="store_true",
        help="Include month chapters/YYYY-MM/meta.md excerpt (month weave / Theme line)",
    )
    ap.add_argument(
        "--minds",
        action="store_true",
        help="Include Tri-Frame minds/README + minds/outputs pointers for this date or month",
    )
    ap.add_argument(
        "--health",
        action="store_true",
        help="Append lane health summary from observability v2 JSON (run build_strategy_observability.py first)",
    )
    ap.add_argument(
        "--recent",
        type=int,
        default=0,
        metavar="N",
        help="After state, append last N merged lightweight events (fold JSONL + WORK-choice + optional git). 0=off.",
    )
    ap.add_argument(
        "--history",
        action="store_true",
        help="Same as --recent 20 (ignored if --recent > 0)",
    )
    ap.add_argument(
        "--recent-git",
        type=int,
        default=0,
        metavar="K",
        help="Include up to K latest git commits touching docs/skill-work/work-strategy in the merge pool",
    )
    args = ap.parse_args()
    uid = args.user.strip()
    d = (args.date or "").strip()
    if d:
        if not DATE_RE.match(d):
            print("error: --date must be YYYY-MM-DD", file=sys.stderr)
            return 2
    else:
        d = date.today().isoformat()

    inbox_path = NOTEBOOK / "daily-strategy-inbox.md"
    days_path = _month_path(d)
    brief_path = STRATEGY_DIR / f"daily-brief-{d}.md"
    strategy_path = STRATEGY_DIR / "STRATEGY.md"
    ladder_path = STRATEGY_DIR / "promotion-ladder.md"
    threads_path = NOTEBOOK / "strategy-commentator-threads.md"

    paths_map = {
        "inbox": inbox_path,
        "days": days_path,
        "brief": brief_path,
        "STRATEGY": strategy_path,
        "promotion-ladder": ladder_path,
        "commentator-threads": threads_path,
    }
    exists = {k: p.is_file() for k, p in paths_map.items()}

    inbox_text = inbox_path.read_text(encoding="utf-8", errors="replace") if exists["inbox"] else ""
    accum, scratch_chars, has_retained = scratch_metrics(inbox_text)

    days_text = days_path.read_text(encoding="utf-8", errors="replace") if exists["days"] else ""
    day_block = extract_day_block(days_text, d) if days_text else None
    open_body = extract_h3_section(day_block or "", "Foresight") or extract_h3_section(
        day_block or "", "Open"
    )
    open_bullets = open_bullet_lines(open_body)

    threads_text = (
        threads_path.read_text(encoding="utf-8", errors="replace")
        if exists["commentator-threads"]
        else ""
    )
    expert_rows = count_expert_table_rows(threads_text) if threads_text else 0

    brief_line = brief_excerpt(brief_path)

    meta_path = _meta_path(d)
    meta_exists = meta_path.is_file()
    meta_line: str | None = meta_excerpt(meta_path) if args.meta else None
    minds_line: str | None = minds_excerpt(d) if args.minds else None

    if args.compact:
        out = run_compact(
            day=d,
            paths=paths_map,
            exists=exists,
            day_block=day_block,
            open_bullets=open_bullets,
            accum=accum,
            scratch_chars=scratch_chars,
            expert_rows=expert_rows,
            meta_path=meta_path if args.meta else None,
            meta_exists=meta_exists,
            meta_line=meta_line if args.meta else None,
            include_minds=bool(args.minds),
            minds_line=minds_line,
        )
    else:
        out = build_paragraph(
            day=d,
            days_path=days_path,
            day_block=day_block,
            open_bullets=open_bullets,
            accum=accum,
            scratch_chars=scratch_chars,
            has_retained=has_retained,
            brief_line=brief_line,
            strategy_exists=exists["STRATEGY"],
            ladder_exists=exists["promotion-ladder"],
            expert_rows=expert_rows,
            max_words=max(40, args.max_words),
            meta_line=meta_line,
            minds_line=minds_line,
        )
        if not out.endswith("\n"):
            out += "\n"

    if args.health:
        hs = health_summary()
        if hs:
            out = out.rstrip("\n") + "\n\n" + hs + "\n"
        else:
            out = out.rstrip("\n") + "\n\n(observability JSON not found — run: python3 scripts/build_strategy_observability.py)\n"

    recent_n = args.recent if args.recent > 0 else (20 if args.history else 0)
    if recent_n > 0:
        user_dir = profile_dir(uid)
        fold_path = user_dir / "strategy-fold-events.jsonl"
        transcript_path = user_dir / "session-transcript.md"
        fold_events = parse_fold_jsonl_events(fold_path)
        wc_events = parse_work_choice_strategy_events(read_path(transcript_path))
        git_events = git_strategy_lane_events(REPO_ROOT, max(0, args.recent_git))
        merged = merge_history_events(
            fold_events=fold_events,
            wc_events=wc_events,
            git_events=git_events,
            take=recent_n,
        )
        hist = format_history_section(merged)
        if hist:
            out = out.rstrip("\n") + hist

    sys.stdout.write(out)

    if args.log:
        note = (
            f"strategy-context date={d} compact={bool(args.compact)} max_words={args.max_words}; "
            f"meta={bool(args.meta)} minds={bool(args.minds)}; "
            f"recent={recent_n if recent_n else 'off'} recent_git={args.recent_git}; "
            f"open_bullets={len(open_bullets)} expert_rows={expert_rows}"
        )
        log_script = REPO_ROOT / "scripts" / "log_operator_choice.py"
        r = subprocess.run(
            [
                sys.executable,
                str(log_script),
                "-u",
                uid,
                "--context",
                "WORK",
                "--picked",
                "strategy-context",
                "--tags",
                f"date={d},strategy-context",
                "--note",
                note[:500],
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(r.stderr or r.stdout or "log_operator_choice failed", file=sys.stderr)
            return r.returncode
        if r.stdout.strip():
            print(r.stdout.strip(), file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
