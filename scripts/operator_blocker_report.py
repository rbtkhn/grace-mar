#!/usr/bin/env python3
"""
Anticipate blockers for operator (Wu insight: manager leverage).

Reads SESSION-LOG, RECURSION-GATE, development-handoff, pipeline-events
and produces a short report: **stale pending** (coordination tax), staged candidates,
open debates, recent events, development-handoff summary.

Usage:
    python scripts/operator_blocker_report.py -u grace-mar
    python scripts/operator_blocker_report.py -u grace-mar --stale-days 7
    python scripts/operator_blocker_report.py -u grace-mar -o report.md
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_territory import TERRITORY_WAP, normalize_territory_cli, territory_from_yaml_block


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_gate_timestamp(block: str) -> datetime | None:
    """Best-effort timestamp from candidate yaml (timestamp: YYYY-MM-DD or with time)."""
    tm = re.search(r"timestamp:\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}:\d{2}))?", block)
    if not tm:
        return None
    date_part = tm.group(1)
    time_part = tm.group(2) or "00:00:00"
    try:
        return datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _extract_pending_candidates(content: str) -> list[dict]:
    """Extract candidates with status: pending from recursion-gate."""
    out: list[dict] = []
    for m in re.finditer(r"### (CANDIDATE-\d+).*?```yaml\n(.*?)```", content, re.DOTALL):
        cid = m.group(1)
        block = m.group(2)
        if "status: pending" in block or "status: pending\n" in block:
            summary = ""
            sm = re.search(r"summary:\s*(.+?)(?:\n|$)", block)
            if sm:
                summary = sm.group(1).strip().strip('"\'')
            ts = _parse_gate_timestamp(block)
            out.append(
                {
                    "id": cid,
                    "summary": summary,
                    "timestamp": ts,
                    "territory": territory_from_yaml_block(block),
                }
            )
    return out


def _extract_unresolved_debates(content: str) -> list[dict]:
    """Extract debate packets that have no resolution."""
    out: list[dict] = []
    for m in re.finditer(r"### (DEBATE-\d+).*?```yaml\n(.*?)```", content, re.DOTALL):
        did = m.group(1)
        block = m.group(2)
        if "resolution:" not in block or re.search(r"resolution:\s*$", block):
            rule_id = ""
            rm = re.search(r"rule_id:\s*(\S+)", block)
            if rm:
                rule_id = rm.group(1)
            sources: list[str] = []
            sm = re.search(r"source_agents:\s*\[(.*?)\]", block, re.DOTALL)
            if sm:
                sources = [s.strip().strip('"').strip("'") for s in sm.group(1).split(",") if s.strip()]
            out.append({"id": did, "rule_id": rule_id, "sources": sources})
    return out


def _read_pipeline_events(path: Path, last_n: int = 15) -> list[dict]:
    """Read last N pipeline events."""
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    events: list[dict] = []
    for line in reversed(lines[-last_n:]):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return list(reversed(events))


def _handoff_summary(content: str, max_lines: int = 80) -> str:
    """Extract key sections from development-handoff (current baseline, recommended tasks)."""
    lines = content.splitlines()
    out: list[str] = []
    in_baseline = False
    in_tasks = False
    for i, line in enumerate(lines):
        if line.strip().startswith("## Current Baseline"):
            in_baseline = True
            out.append(line)
            continue
        if line.strip().startswith("## Recommended Next Tasks"):
            in_baseline = False
            in_tasks = True
            out.append("")
            out.append(line)
            continue
        if in_baseline and line.startswith("## "):
            in_baseline = False
        if in_tasks and line.startswith("## ") and "Recommended" not in line:
            in_tasks = False
        if in_baseline or in_tasks:
            out.append(line)
        if len(out) >= max_lines:
            break
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Anticipate blockers for Grace-Mar operator")
    parser.add_argument("-u", "--user", default="grace-mar", help="User id (e.g. grace-mar)")
    parser.add_argument("-o", "--output", help="Write report to file instead of stdout")
    parser.add_argument("--events", type=int, default=15, help="Number of pipeline events to include")
    parser.add_argument(
        "--stale-days",
        type=int,
        default=3,
        metavar="N",
        help="Flag pending candidates older than N days (default 3)",
    )
    parser.add_argument(
        "--territory",
        choices=("all", "wap", "wp", "work-politics", "companion"),
        default="all",
        help="Pending lens: work-politics (or wap/wp) only; companion = Record only; all = both sections",
    )
    args = parser.parse_args()
    territory = normalize_territory_cli(args.territory)

    user_id = args.user
    profile_dir = REPO_ROOT / "users" / user_id
    docs_dir = REPO_ROOT / "docs"

    recursion_gate = _read(profile_dir / "recursion-gate.md")
    handoff = _read(REPO_ROOT / "development-handoff.md")
    session_log = _read(profile_dir / "session-log.md")
    pipeline_events = _read_pipeline_events(profile_dir / "pipeline-events.jsonl", args.events)

    all_pending = _extract_pending_candidates(recursion_gate)
    wap_pending = [c for c in all_pending if c.get("territory") == TERRITORY_WAP]
    companion_pending = [c for c in all_pending if c.get("territory") != TERRITORY_WAP]
    if territory == "work-politics":
        pending = wap_pending
    elif territory == "companion":
        pending = companion_pending
    else:
        pending = all_pending
    debates = _extract_unresolved_debates(recursion_gate)
    handoff_excerpt = _handoff_summary(handoff)

    lines: list[str] = []
    lines.append("# Operator Blocker Report")
    lines.append("")
    lines.append(f"**User:** {user_id}")
    if territory == "all":
        lines.append(
            f"**Pending by territory:** work-politics {len(wap_pending)} · Companion {len(companion_pending)} · Total {len(all_pending)}"
        )
        lines.append(
            f"_Lens:_ `--territory work-politics` | `--territory companion` | `all` (default). Work-politics territory = `territory: work-politics` or `channel_key: operator:wap`."
        )
    else:
        lines.append(f"**Territory lens:** {territory} ({len(pending)} pending)")
    lines.append("")
    lines.append("---")
    lines.append("")

    now = datetime.now(timezone.utc)
    stale_days = max(1, args.stale_days)
    stale = [
        c
        for c in pending
        if c.get("timestamp") and (now - c["timestamp"]).total_seconds() >= stale_days * 86400
    ]
    no_ts = [c for c in pending if not c.get("timestamp")]

    # Stale pending (coordination tax)
    lines.append("## Stale pending (coordination tax)")
    lines.append(
        f"Candidates still **pending** after **{stale_days}+ days** — same cost as standing meetings: attention without closure. "
        "Approve, reject, or batch-process."
    )
    lines.append("")
    if stale:
        for c in stale:
            s = c["summary"] or "(no summary)"
            if len(s) > 80:
                s = s[:77] + "..."
            age = (now - c["timestamp"]).days
            lines.append(f"- **{c['id']}** — ~{age}d old — {s}")
    else:
        lines.append("- None over threshold")
    if no_ts and pending:
        lines.append(f"- _{len(no_ts)} pending without parseable timestamp — check manually_")
    lines.append("")

    # Staged candidates
    if territory == "all" and (wap_pending or companion_pending):
        lines.append("## Staged — work-politics")
        if not wap_pending:
            lines.append("- None")
        else:
            for c in wap_pending:
                s = (c["summary"] or "(no summary)")[:100]
                lines.append(f"- **{c['id']}** — {s}")
        lines.append("")
        lines.append("## Staged — companion Record")
        if not companion_pending:
            lines.append("- None")
        else:
            for c in companion_pending:
                s = (c["summary"] or "(no summary)")[:100]
                age_note = f" ({c['timestamp'].strftime('%Y-%m-%d')})" if c.get("timestamp") else ""
                lines.append(f"- **{c['id']}**{age_note} — {s}")
        lines.append("")
    else:
        lines.append("## Staged candidates (RECURSION-GATE)")
        if not pending:
            lines.append("- None")
        else:
            for c in pending:
                s = c["summary"] or "(no summary)"
                if len(s) > 100:
                    s = s[:97] + "..."
                age_note = ""
                if c.get("timestamp"):
                    age_note = f" ({c['timestamp'].strftime('%Y-%m-%d')})"
                tag = f" [{c.get('territory', '?')}]" if territory == "all" else ""
                lines.append(f"- **{c['id']}**{age_note}{tag} — {s}")
        lines.append("")
    lines.append("**Action:** Review in recursion-gate.md; approve or reject.")
    lines.append("")

    # Open debates
    lines.append("## Unresolved debate packets")
    if not debates:
        lines.append("- None")
    else:
        for d in debates:
            src = ", ".join(d["sources"]) if d["sources"] else "?"
            lines.append(f"- **{d['id']}** — rule={d['rule_id']}, sources={src}")
    lines.append("")
    lines.append("**Action:** Use /resolve_debate DEBATE-XXXX <resolution> in Telegram.")
    lines.append("")

    # Recent pipeline events
    lines.append("## Recent pipeline events")
    if not pipeline_events:
        lines.append("- None")
    else:
        for e in pipeline_events[-10:]:
            ts = e.get("ts", "")[:16].replace("T", " ")
            ev = e.get("event", "?")
            cid = e.get("candidate_id", "")
            extra = f" ({cid})" if cid else ""
            lines.append(f"- {ts} — {ev}{extra}")
    lines.append("")

    # Development handoff excerpt
    lines.append("## Development handoff (excerpt)")
    lines.append("")
    lines.append("```")
    lines.append(handoff_excerpt)
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Run: `python scripts/operator_blocker_report.py -u grace-mar`*")

    report = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Wrote report to {args.output}", file=sys.stderr)
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
