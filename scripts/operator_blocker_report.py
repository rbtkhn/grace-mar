#!/usr/bin/env python3
"""
Anticipate blockers for operator (Wu insight: manager leverage).

Reads SESSION-LOG, RECURSION-GATE, development-handoff, pipeline-events
and produces a short report: staged candidates, open debates, recent events,
and development-handoff summary. Operator can use this to "look around corners"
and focus on what needs attention.

Usage:
    python scripts/operator_blocker_report.py -u grace-mar
    python scripts/operator_blocker_report.py -u grace-mar -o report.md
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


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
            out.append({"id": cid, "summary": summary})
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
    args = parser.parse_args()

    user_id = args.user
    profile_dir = REPO_ROOT / "users" / user_id
    docs_dir = REPO_ROOT / "docs"

    recursion_gate = _read(profile_dir / "recursion-gate.md")
    handoff = _read(REPO_ROOT / "development-handoff.md")
    session_log = _read(profile_dir / "session-log.md")
    pipeline_events = _read_pipeline_events(profile_dir / "pipeline-events.jsonl", args.events)

    pending = _extract_pending_candidates(recursion_gate)
    debates = _extract_unresolved_debates(recursion_gate)
    handoff_excerpt = _handoff_summary(handoff)

    lines: list[str] = []
    lines.append("# Operator Blocker Report")
    lines.append("")
    lines.append(f"**User:** {user_id}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Staged candidates
    lines.append("## Staged candidates (RECURSION-GATE)")
    if not pending:
        lines.append("- None")
    else:
        for c in pending:
            s = c["summary"] or "(no summary)"
            if len(s) > 100:
                s = s[:97] + "..."
            lines.append(f"- **{c['id']}** — {s}")
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
