#!/usr/bin/env python3
"""
Export session transcript turns to JSONL for optional downstream use (e.g. RL harnesses
like OpenClaw-RL). Read-only; does not train models or merge into the Record.

Each line is one JSON object:
  turn, role, channel, text, ts (ISO-ish from transcript), user_id
Optional enrichment from pipeline-events.jsonl:
  pipeline_events: [{event, candidate_id, ts}, ...] within a short window after this turn

Usage:
  python scripts/export_conversation_trajectories.py -u grace-mar
  python scripts/export_conversation_trajectories.py -u grace-mar -o /tmp/traj.jsonl
  python scripts/export_conversation_trajectories.py -u grace-mar --last-n 200

Not for minors' raw chat in untrusted RL pipelines without operator review — see docs/openclaw-rl-boundary.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

# **[2026-02-24 13:59:16]** `USER` (Test)
HEADER_RE = re.compile(
    r"^\*\*\[([^\]]+)\]\*\*\s*`([^`]+)`\s*\(([^)]*)\)\s*$",
    re.MULTILINE,
)


def _parse_transcript(path: Path) -> list[dict]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8", errors="replace")
    turns: list[dict] = []
    pos = 0
    for m in HEADER_RE.finditer(raw):
        ts_str = m.group(1).strip()
        role = m.group(2).strip()
        channel = m.group(3).strip()
        start = m.end()
        nxt = HEADER_RE.search(raw, start)
        chunk = raw[start : nxt.start() if nxt else len(raw)]
        lines = []
        for line in chunk.splitlines():
            s = line.strip()
            if s.startswith(">"):
                lines.append(s[1:].strip())
            elif s and not s.startswith("---"):
                if lines:
                    lines[-1] = lines[-1] + " " + s
        text = "\n".join(lines) if lines else ""
        text = text.strip()
        if not text and role not in ("USER", "GRACE-MAR"):
            continue
        turns.append(
            {
                "turn": len(turns),
                "role": role,
                "channel": channel or "unknown",
                "text": text[:8000],
                "ts": ts_str,
            }
        )
    return turns


def _load_pipeline_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _attach_events(turns: list[dict], events: list[dict], window_sec: int = 120) -> None:
    """Attach pipeline events whose ts falls within window_sec after turn ts (best-effort)."""
    for t in turns:
        t["pipeline_events"] = []
        ts_turn = _parse_ts(t.get("ts", ""))
        if not ts_turn:
            continue
        for ev in events:
            ts_ev = _parse_ts_iso(ev.get("ts", ""))
            if not ts_ev:
                continue
            if timedelta(seconds=0) <= (ts_ev - ts_turn) <= timedelta(seconds=window_sec):
                t["pipeline_events"].append(
                    {
                        "event": ev.get("event"),
                        "candidate_id": ev.get("candidate_id"),
                        "ts": ev.get("ts"),
                    }
                )


def _parse_ts(s: str) -> datetime | None:
    s = s.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s[:19], fmt)
        except ValueError:
            continue
    return None


def _parse_ts_iso(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00").split("+")[0])
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Export session transcript as JSONL trajectories")
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument("-o", "--output", default="", help="Write JSONL here (default: stdout)")
    ap.add_argument("--last-n", type=int, default=0, help="Only last N turns (0 = all)")
    ap.add_argument("--no-pipeline-events", action="store_true")
    ap.add_argument("--window-sec", type=int, default=120, help="Pipeline event attach window")
    args = ap.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    transcript = user_dir / "session-transcript.md"
    events_path = user_dir / "pipeline-events.jsonl"

    turns = _parse_transcript(transcript)
    if args.last_n > 0:
        turns = turns[-args.last_n :]
    for i, t in enumerate(turns):
        t["turn"] = i
        t["user_id"] = args.user

    if not args.no_pipeline_events:
        _attach_events(turns, _load_pipeline_events(events_path), args.window_sec)

    out_lines = [json.dumps(t, ensure_ascii=False) for t in turns]

    if args.output:
        Path(args.output).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"Wrote {len(out_lines)} turns to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write("\n".join(out_lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
