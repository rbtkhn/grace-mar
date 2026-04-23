#!/usr/bin/env python3
"""Strategy Console — derived orientation for strategy-notebook (WORK only).

Read-only on notebook materials; writes only strategy-console/console-view.md
and optionally appends a v1 strategy-notebook JSONL receipt.

No LLM. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_notebook.receipts import (  # noqa: E402
    NotebookReceipt,
    PageOperation,
    append_receipt,
    rel_posix,
)

# Heuristic windows
RECENT_HOURS_DEFAULT = 72
MAX_EXPERT_TABLE_ROWS = 15
INBOX_TAIL_LINES = 400
DAYS_TAIL_LINES = 120
FORECAST_TAIL_LINES = 200
MAX_THREAD_BYTES = 1_200_000
STRATEGY_PAGE_PATTERNS = (
    "strategy-page:start",
    "<!-- strategy-page:start",
)
MARKER_TOKENS = ("[watch]", "[decision]", "[promote]")

RE_ROSTER_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|", re.IGNORECASE)
RE_METRICS_HEADER = re.compile(r"^\|\s*expert_id\s*\|\s*SCI\s*\|", re.IGNORECASE)


def _path_display(p: Path) -> str:
    """Path for markdown; works when notebook-dir is outside the repo (tests)."""
    try:
        return p.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return p.resolve().as_posix()
RE_IRAN = re.compile(r"\bIRAN\b|\bTEHRAN\b", re.IGNORECASE)
RE_ACCUM = re.compile(r"Accumulator\s+for:\s*(\d{4}-\d{2}-\d{2})")


@dataclass
class BuildContext:
    notebook_root: Path
    today: date
    mode: str
    watch: str | None
    since: datetime
    input_gaps: list[str] = field(default_factory=list)
    sources_read: list[Path] = field(default_factory=list)

    @property
    def month_str(self) -> str:
        return f"{self.today.year:04d}-{self.today.month:02d}"

    @property
    def day_str(self) -> str:
        return self.today.isoformat()


def _note_read(ctx: BuildContext, p: Path | None) -> None:
    if p is None:
        return
    try:
        ctx.sources_read.append(p.resolve())
    except OSError:
        pass


def safe_read_text(path: Path, max_bytes: int = MAX_THREAD_BYTES) -> str | None:
    if not path.is_file():
        return None
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="replace")


def safe_stat_mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def parse_expert_ids(roster_path: Path) -> list[str]:
    text = safe_read_text(roster_path, 800_000)
    if not text:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for line in text.splitlines():
        if RE_METRICS_HEADER.search(line):
            break
        m = RE_ROSTER_ROW.match(line)
        if m:
            eid = m.group(1).lower()
            if eid not in seen and eid != "expert_id":
                seen.add(eid)
                out.append(eid)
    return out


def count_strategy_page_markers(text: str) -> int:
    n = 0
    for pat in STRATEGY_PAGE_PATTERNS:
        n += text.count(pat)
    return n


def fresh_inputs_section(
    ctx: BuildContext, inbox: Path, raw_today: Path
) -> tuple[list[str], list[str]]:
    bullets: list[str] = []
    gaps: list[str] = []

    _note_read(ctx, raw_today)
    if not raw_today.is_dir():
        gaps.append(f"No directory `{raw_today.relative_to(ctx.notebook_root)}/` for today.")
    else:
        files = sorted(raw_today.iterdir(), key=lambda p: p.name)
        only_md = [p for p in files if p.is_file()]
        if not only_md:
            bullets.append(
                f"`{raw_today.relative_to(ctx.notebook_root)}/` — empty (no files today)."
            )
        else:
            names = [p.name for p in only_md[:30]]
            more = "" if len(only_md) <= 30 else f" (+{len(only_md) - 30} more)"
            bullets.append(
                f"`{raw_today.relative_to(ctx.notebook_root)}/`: {len(only_md)} file(s) — {', '.join(names[:8])}{more}"
            )

    _note_read(ctx, inbox)
    inbox_text = safe_read_text(inbox, 2_000_000)
    if inbox_text is None:
        gaps.append(f"Missing: `{inbox.relative_to(ctx.notebook_root)}`")
        return bullets, gaps

    tail_lines = inbox_text.splitlines()[-INBOX_TAIL_LINES:]
    tail = "\n".join(tail_lines)
    if ctx.day_str in tail or f"**{ctx.day_str}" in tail:
        bullets.append(
            f"Inbox tail mentions **{ctx.day_str}** (see `{inbox.relative_to(ctx.notebook_root)}`)."
        )
    m_accum = list(RE_ACCUM.finditer(tail))
    if m_accum:
        last = m_accum[-1].group(1)
        if last == ctx.day_str:
            bullets.append(
                f"Inbox: **Accumulator for:** {ctx.day_str} (in recent tail)."
            )
    if not any(ctx.day_str in x for x in bullets) and "Accumulator" in tail:
        bullets.append(
            f"Inbox has recent `Accumulator` / batch lines; verify date alignment in `{inbox.name}`."
        )
    if "batch-analysis" in tail.lower():
        c = tail.lower().count("batch-analysis")
        bullets.append(f"Inbox tail: `batch-analysis` appears ~{c} time(s) (heuristic).")

    return bullets, gaps


def recent_movement_bullets(ctx: BuildContext) -> list[str]:
    out: list[str] = []
    month_chapter = ctx.notebook_root / "chapters" / ctx.month_str / "days.md"
    _note_read(ctx, month_chapter)
    mtime = safe_stat_mtime(month_chapter)
    if mtime and datetime.fromtimestamp(mtime, tz=timezone.utc) >= ctx.since:
        out.append(
            f"`{month_chapter.relative_to(ctx.notebook_root)}` — mtime within {RECENT_HOURS_DEFAULT}h window (UTC-compare of file mtime)."
        )
    elif month_chapter.is_file():
        out.append(
            f"`{month_chapter.relative_to(ctx.notebook_root)}` — present; no mtime in recent window (heuristic only)."
        )

    st = ctx.notebook_root / "STATUS.md"
    _note_read(ctx, st)
    if st.is_file() and safe_stat_mtime(st) and datetime.fromtimestamp(
        safe_stat_mtime(st), tz=timezone.utc
    ) >= ctx.since:
        out.append(f"`STATUS.md` — touched within recent window.")
    elif st.is_file():
        out.append("`STATUS.md` — present; no recent mtime signal.")

    cv = ctx.notebook_root / "compiled-views"
    if cv.is_dir():
        _note_read(ctx, cv)
        md_files = [p for p in cv.rglob("*.md") if p.is_file()]
        if md_files:
            latest = max(md_files, key=lambda p: safe_stat_mtime(p) or 0)
            lm = safe_stat_mtime(latest)
            if lm:
                out.append(
                    f"`compiled-views/`: {len(md_files)} `*.md`; newest: `{latest.relative_to(ctx.notebook_root)}`."
                )
    else:
        out.append("`compiled-views/` — not found (optional).")

    return out


def expert_rows(ctx: BuildContext, roster_ids: list[str]) -> list[dict[str, str]]:
    """Experts with `experts/<id>/thread.md`, sorted by mtime, capped for readability."""
    rows: list[dict[str, str]] = []
    experts_dir = ctx.notebook_root / "experts"
    scored: list[
        tuple[float, str, str, int, bool, bool]
    ] = []  # mtime, eid, sig, n_pages, recent, has_day
    for eid in roster_ids:
        th = experts_dir / eid / "thread.md"
        if not th.is_file():
            continue
        _note_read(ctx, th)
        mtime = float(safe_stat_mtime(th) or 0.0)
        recent = mtime and datetime.fromtimestamp(mtime, tz=timezone.utc) >= ctx.since
        text = safe_read_text(th) or ""
        n_pages = count_strategy_page_markers(text)
        has_day = ctx.day_str in text or ctx.month_str in text
        if recent:
            sig = f"mtime within {RECENT_HOURS_DEFAULT}h; `strategy-page` marker count ≈{n_pages}"
        elif n_pages > 0 or has_day:
            sig = f"no recent mtime; markers≈{n_pages}; month/day string hit={'yes' if has_day else 'no'}"
        else:
            sig = "no clear movement signal (mtime outside window; low marker signal)"
        scored.append((mtime, eid, sig, n_pages, recent, has_day))
    scored.sort(key=lambda x: -x[0])
    for _mtime, eid, sig, n_pages, recent, has_day in scored[:MAX_EXPERT_TABLE_ROWS]:
        if recent:
            h = "Review `thread.md` before EOD compose; check inbox `thread:` alignment."
        elif n_pages > 0 or has_day:
            h = "Open if promoting; otherwise **cold** unless inbox pulls the lane."
        else:
            h = "**Available** — not active in this heuristic window."
        rows.append({"lane": f"`{eid}`", "signal": sig, "handling": h})
    if len(scored) > MAX_EXPERT_TABLE_ROWS:
        rows.append(
            {
                "lane": "_(other roster lanes)_",
                "signal": f"{len(scored) - MAX_EXPERT_TABLE_ROWS} more expert(s) with `thread.md` (not shown; mtime-sorted in script).",
                "handling": "Use inbox `thread:` lines to prioritize among remaining lanes.",
            }
        )
    if not rows:
        return [
            {
                "lane": "—",
                "signal": "No `experts/<id>/thread.md` for roster entries (or empty roster).",
                "handling": "Add experts per strategy-commentator-threads; verify paths.",
            }
        ]
    return rows


def state_watch_rows(ctx: BuildContext) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    wdir = ctx.notebook_root / "watches"
    _note_read(ctx, wdir)
    if wdir.is_dir():
        files = [p for p in wdir.iterdir() if p.suffix == ".md" and p.is_file()]
        for p in sorted(files)[:20]:
            mtime = safe_stat_mtime(p)
            recent = mtime and datetime.fromtimestamp(
                mtime, tz=timezone.utc
            ) >= ctx.since
            rel = p.relative_to(ctx.notebook_root)
            rows.append(
                {
                    "lane": f"`{rel.as_posix()}`",
                    "signal": "recent" if recent else "present; stale mtime in window",
                    "handling": "Skim for alignment with today inbox / MCQ (structural).",
                }
            )
        if not files and (wdir / "README.md").is_file():
            _note_read(ctx, wdir / "README.md")
            rows.append(
                {
                    "lane": "`watches/README.md`",
                    "signal": "folder present; no `*.md` child files in scan",
                    "handling": "Read README; add watch files as needed.",
                }
            )
    else:
        rows.append(
            {
                "lane": "`watches/`",
                "signal": "missing",
                "handling": "See `watches/README.md` if present elsewhere or restore folder.",
            }
        )

    ssi = ctx.notebook_root / "strategy-state-iran"
    if ssi.is_dir():
        _note_read(ctx, ssi / "README.md")
        for sub, label in (("weave", "weave/"), ("channels", "channels/"), ("clusters", "clusters/")):
            p = ssi / sub
            if p.is_dir():
                n = len(list(p.rglob("*.md")))
                rows.append(
                    {
                        "lane": f"`strategy-state-iran/{label}`",
                        "signal": f"institutional lane; ~{n} `*.md` under subtree (count heuristic)",
                        "handling": "**State / institutional** — do not merge into `thread:` without routing rules.",
                    }
                )
    else:
        rows.append(
            {
                "lane": "`strategy-state-iran/`",
                "signal": "not present (optional state lane).",
                "handling": "N/A unless Iran institutional work is active.",
            }
        )

    if ctx.mode == "crisis" and (ctx.watch or "").lower() == "iran":
        ukt = ctx.notebook_root / "US-IRAN-KINETIC-TRACKER.md"
        _note_read(ctx, ukt)
        if ukt.is_file():
            rows.insert(
                0,
                {
                    "lane": "`US-IRAN-KINETIC-TRACKER.md`",
                    "signal": "crisis scan surface (read-only)",
                    "handling": "Open for kinetic framing; still route EOD through MCQ.",
                },
            )
    return rows


def marker_scan(ctx: BuildContext) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    paths: list[Path] = [
        ctx.notebook_root / "daily-strategy-inbox.md",
        ctx.notebook_root / "forecast-watch-log.md",
        ctx.notebook_root / "chapters" / ctx.month_str / "days.md",
    ]
    for path in paths:
        _note_read(ctx, path)
        text = safe_read_text(path, 2_000_000)
        if not text:
            continue
        if path.name == "days.md":
            text = "\n".join(text.splitlines()[-DAYS_TAIL_LINES:])
        elif path.name == "daily-strategy-inbox.md":
            text = "\n".join(text.splitlines()[-INBOX_TAIL_LINES:])
        elif path.name == "forecast-watch-log.md":
            text = "\n".join(text.splitlines()[-FORECAST_TAIL_LINES:])
        counts = {tok: text.count(tok) for tok in MARKER_TOKENS}
        tot = sum(counts.values())
        if tot == 0:
            continue
        cstr = ", ".join(f"{k}×{v}" for k, v in counts.items() if v)
        found.append(
            {
                "tension": f"Escalation markers in `{path.relative_to(ctx.notebook_root)}`",
                "evidence": cstr,
                "handling": "Cross-check in EOD before promotion; use MCQ for threshold.",
            }
        )
    if not found:
        return [
            {
                "tension": "—",
                "evidence": "No watch / decision / promote tokens in scanned tails (heuristic).",
                "handling": "Add markers in source material if tension should surface.",
            }
        ]
    return found


def iran_inbox_hits(ctx: BuildContext) -> int:
    inbox = ctx.notebook_root / "daily-strategy-inbox.md"
    t = safe_read_text(inbox, 2_000_000)
    if not t:
        return 0
    tail = "\n".join(t.splitlines()[-INBOX_TAIL_LINES:])
    return len(RE_IRAN.findall(tail))


def recommend_route(
    ctx: BuildContext,
    expert_data: list[dict[str, str]],
    has_batch: bool,
) -> dict[str, str]:
    # Count "recent" expert signals in table (substring)
    n_recent = sum(1 for r in expert_data if "within" in r.get("signal", ""))
    jiang_mentioned = False
    inbox_path = ctx.notebook_root / "daily-strategy-inbox.md"
    it = safe_read_text(inbox_path, 2_000_000)
    if it:
        low = it.lower()[-INBOX_TAIL_LINES * 200 :]
        jiang_mentioned = "thread:jiang" in low or "jiang" in low

    st = f"EOD orientation — mode={ctx.mode}"
    if has_batch and n_recent >= 2:
        session = "Dual-lane contrast or **Tri-mind** (C) if operator selects in MCQ"
        lanes = "Top two mtime lanes from expert table (verify in evidence pile)"
        prom = "Match MCQ menu 3; defer promotion if **cold** / uncertain"
    elif n_recent == 1 and not has_batch:
        session = "Single-lane synthesis (A) — **confirm in MCQ**"
        lanes = "The lane with recent mtime signal (see table)"
        prom = "Summary-only or draft per MCQ; avoid auto-promote"
    elif jiang_mentioned and ("history" in (it or "").lower() or "ph" in (it or "").lower()):
        session = "Bridge session (F) **candidate** — confirm in MCQ"
        lanes = "Jiang + one expert lane as applicable"
        prom = "Per MCQ; PH routing per strategy-commentator-threads"
    elif n_recent == 0 and not has_batch:
        session = "**Triage-and-defer (E)** or **Continuity-only (D)** — confirm"
        lanes = "Keep **cold** / unresolved where evidence thin"
        prom = "Prefer defer; no automatic promotion from console"
    else:
        session = "Operator choice — use MCQ menu 1 after evidence pile"
        lanes = "From inbox `thread:` lines + table"
        prom = "MCQ menu 3 per lane"
    if ctx.mode == "crisis" and (ctx.watch or "").lower() == "iran":
        st += "; **crisis / Iran** — separate institutional state from commentator `thread:` in MCQ"
    return {
        "session": session,
        "lanes": lanes,
        "promo": prom,
        "page_shape": "From MCQ menu 4 + [NOTEBOOK-PREFERENCES](../NOTEBOOK-PREFERENCES.md) — not chosen here",
        "page_action": "Use full EOD-MCQ; fast path per protocol if operator selects",
        "days": "From MCQ menu 6 + architecture same-day rules — not chosen here",
        "rationale": "Heuristic only; [EOD-MCQ-PROTOCOL.md](../EOD-MCQ-PROTOCOL.md) authorizes decisions.",
    }


def build_markdown(ctx: BuildContext) -> str:
    roster = ctx.notebook_root / "strategy-commentator-threads.md"
    roster_ids = parse_expert_ids(roster)
    if roster_path_missing := (not roster.is_file()):
        ctx.input_gaps.append("Missing: `strategy-commentator-threads.md` — expert roster not parsed.")
    _note_read(ctx, roster if roster.is_file() else None)

    inbox = ctx.notebook_root / "daily-strategy-inbox.md"
    raw_today = ctx.notebook_root / "raw-input" / ctx.day_str
    fresh_bullets, more_gaps = fresh_inputs_section(ctx, inbox, raw_today)
    ctx.input_gaps.extend(more_gaps)
    if not fresh_bullets:
        fresh_bullets = ["_No strong fresh-input heuristics (check paths under Input gaps)._"]
    rec_bul = recent_movement_bullets(ctx)
    if not rec_bul:
        rec_bul = ["_No recent notebook movement detected (mtime window)._"]

    if not inbox.is_file() and not (ctx.notebook_root / "chapters" / ctx.month_str / "days.md").is_file():
        ctx.input_gaps.append("Critical: missing both `daily-strategy-inbox.md` and month `days.md`.")

    # Expert table
    ex_rows = expert_rows(ctx, roster_ids if not roster_path_missing else [])
    if ctx.mode == "crisis" and (ctx.watch or "").lower() == "iran":
        ihan = iran_inbox_hits(ctx)
        if ihan:
            for r in ex_rows:
                r["handling"] += (
                    f" (Iran inbox tail hits: ~{ihan} on IRAN/TEHRAN keyword scan—see inbox)"
                )

    st_rows = state_watch_rows(ctx)
    tens = marker_scan(ctx)

    inbox_path = ctx.notebook_root / "daily-strategy-inbox.md"
    itext = safe_read_text(inbox_path, 2_000_000) or ""
    has_batch = "batch-analysis" in itext.lower()[-INBOX_TAIL_LINES * 200 :]

    # Emerging decision points (simple)
    em: list[dict[str, str]] = []
    if has_batch and len(ex_rows) > 1:
        em.append(
            {
                "q": "Multiple lanes + `batch-analysis` present — single vs dual synthesis?",
                "src": "Inbox + expert table heuristics",
                "route": "MCQ menu 1: **A** vs **B** vs **C** per operator",
            }
        )
    if any(
        t.get("tension", "") != "—" and (MARKER_TOKENS[0] in t.get("evidence", "") or MARKER_TOKENS[1] in t.get("evidence", ""))
        for t in tens
    ):
        em.append(
            {
                "q": "Escalation markers in scanned tails — promote now or hold?",
                "src": "Marker scan",
                "route": "MCQ menu 3; avoid silent promotion",
            }
        )
    if not em:
        em.append(
            {
                "q": "No strong structural decision signal",
                "src": "Heuristic pass",
                "route": "**Triage-and-defer (E)** or **cold (H)** in MCQ if evidence thin",
            }
        )

    rec = recommend_route(ctx, ex_rows, has_batch)

    # Review queue
    rq: list[str] = [
        f"`daily-strategy-inbox.md`",
        f"`chapters/{ctx.month_str}/days.md` (tail for continuity)",
    ]
    if (ctx.notebook_root / "STATUS.md").is_file():
        rq.insert(1, "`STATUS.md`")
    if ctx.mode == "crisis" and (ctx.watch or "").lower() == "iran":
        rq.insert(0, "`US-IRAN-KINETIC-TRACKER.md` (if present)")
        rq.insert(1, "`strategy-state-iran/README.md` (institutional; do not conflate with expert lanes)")
    rq.append("[EOD-MCQ-PROTOCOL.md](../EOD-MCQ-PROTOCOL.md)")

    gen_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    wfilter = (ctx.watch or "none") if ctx.mode == "crisis" else "none"
    if ctx.mode == "crisis" and not ctx.watch:
        wfilter = "none (use `--watch iran` for crisis scan)"

    out_status = "degraded" if ctx.input_gaps and any("Critical" in x for x in ctx.input_gaps) else "ok"
    if ctx.input_gaps and out_status == "ok" and len(ctx.input_gaps) >= 2:
        out_status = "degraded"

    lines: list[str] = [
        "# Strategy Console",
        "",
        "> Derived refresh-only operator-orientation surface.",
        "> The Strategy Console does not automate judgment. It automates orientation.",
        "",
        "## Snapshot",
        "",
        f"- Generated: {gen_ts}",
        f"- Mode: {ctx.mode}",
        f"- Watch filter: {wfilter}",
        f"- Notebook root: `{_path_display(ctx.notebook_root)}`",
        f"- Current month: {ctx.month_str}",
        f"- Current day: {ctx.day_str}",
        f"- Output status: {out_status}",
        "",
        "## What changed",
        "",
        "### Fresh inputs",
        "",
    ]
    for b in fresh_bullets:
        lines.append(f"- {b}")
    lines.extend(
        [
            "",
            "### Recent notebook movement",
            "",
        ]
    )
    for b in rec_bul:
        lines.append(f"- {b}")
    lines.extend(["", "### Input gaps", ""])
    if ctx.input_gaps:
        for g in ctx.input_gaps:
            lines.append(f"- {g}")
    else:
        lines.append("- _No input path gaps for this run._")
    lines.extend(
        [
            "",
            "## Expert thread movement",
            "",
            "| Expert lane | Movement signal | Suggested handling |",
            "|---|---|---|",
        ]
    )
    for r in ex_rows:
        lines.append(f"| {r['lane']} | {r['signal']} | {r['handling']} |")
    lines.extend(
        [
            "",
            "## State watch pressure",
            "",
            "| Watch / state lane | Signal | Suggested handling |",
            "|---|---|---|",
        ]
    )
    for r in st_rows:
        lines.append(f"| {r['lane']} | {r['signal']} | {r['handling']} |")
    lines.extend(
        [
            "",
            "## Tightening tensions",
            "",
            "| Tension | Evidence pointers | Suggested handling |",
            "|---|---|---|",
        ]
    )
    for t in tens:
        lines.append(
            f"| {t.get('tension', '—')} | {t.get('evidence', '—')} | {t.get('handling', '—')} |"
        )
    lines.extend(
        [
            "",
            "## Emerging decision points",
            "",
            "| Decision question | Source signals | Recommended EOD route |",
            "|---|---|---|",
        ]
    )
    for e in em:
        lines.append(
            f"| {e.get('q', '—')} | {e.get('src', '—')} | {e.get('route', '—')} |"
        )
    lines.extend(
        [
            "",
            "## Recommended EOD route",
            "",
            f"- Session type: {rec['session']}",
            f"- Active lanes: {rec['lanes']}",
            f"- Promotion threshold: {rec['promo']}",
            f"- Page shape: {rec['page_shape']}",
            f"- Optional page action: {rec['page_action']}",
            f"- days.md continuity mode: {rec['days']}",
            f"- Rationale: {rec['rationale']}",
            "",
            "## Tonight review queue",
            "",
        ]
    )
    for i, item in enumerate(rq, 1):
        lines.append(f"{i}. {item}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Derived surface only.",
            "- Does not edit expert threads.",
            "- Does not edit days.md.",
            "- Does not create or revise strategy-pages.",
            "- Does not promote WORK into Record.",
            "- Use EOD MCQ protocol before drafting judgment.",
            "",
        ]
    )
    return "\n".join(lines)


def _sources_relative(ctx: BuildContext) -> list[str]:
    out: list[str] = []
    for p in sorted(set(ctx.sources_read), key=lambda x: str(x)):
        out.append(_path_display(p))
    return sorted(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Generate strategy-console console-view.md (read-only on notebook; WORK only)."
    )
    p.add_argument(
        "--mode",
        choices=("eod", "morning", "crisis"),
        default="eod",
        help="Console mode (default: eod).",
    )
    p.add_argument(
        "--watch",
        default=None,
        help="Crisis focus tag (e.g. iran). Used with --mode crisis.",
    )
    p.add_argument(
        "--notebook-dir",
        type=Path,
        default=REPO_ROOT
        / "docs"
        / "skill-work"
        / "work-strategy"
        / "strategy-notebook",
        help="Path to strategy-notebook root.",
    )
    p.add_argument(
        "--recent-hours",
        type=int,
        default=RECENT_HOURS_DEFAULT,
        help="Recent mtime window in hours (default: 72).",
    )
    p.add_argument(
        "--no-receipt",
        action="store_true",
        help="Do not append strategy-notebook JSONL receipt.",
    )
    args = p.parse_args()

    notebook_dir = args.notebook_dir.resolve()
    if not notebook_dir.is_dir():
        print(f"error: --notebook-dir not a directory: {notebook_dir}", file=sys.stderr)
        return 1

    today = date.today()
    since = datetime.now(timezone.utc) - timedelta(hours=args.recent_hours)

    ctx = BuildContext(
        notebook_root=notebook_dir,
        today=today,
        mode=args.mode,
        watch=args.watch,
        since=since,
    )
    out_path = notebook_dir / "strategy-console" / "console-view.md"

    try:
        md = build_markdown(ctx)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    _note_read(ctx, out_path)
    print(out_path)

    if not args.no_receipt:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out_rel = rel_posix(REPO_ROOT, out_path)
        rec = NotebookReceipt(
            ts=ts,
            entrypoint="strategy_console",
            page_operation=PageOperation.NOOP.value,
            status="ok",
            sources_read=_sources_relative(ctx),
            outputs_touched=[out_rel],
            decision="wrote strategy-console console-view (derived orientation only)",
            details={
                "mode": args.mode,
                "watch": args.watch,
                "day": today.isoformat(),
            },
        )
        log = append_receipt(REPO_ROOT, rec)
        try:
            print(f"receipt: {log.relative_to(REPO_ROOT)}", flush=True)
        except ValueError:
            print(f"receipt: {log}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
