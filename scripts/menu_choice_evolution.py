#!/usr/bin/env python3
"""
Aggregate ### [WORK-choice] entries from session-transcript.md (last N days).

Read-only on the fork; prints a markdown report. Optional --print-gate-stub emits
YAML prose for operator paste into recursion-gate (does not write gate file).

Usage:
  python3 scripts/menu_choice_evolution.py -u grace-mar --days 30
  python3 scripts/menu_choice_evolution.py -u grace-mar --days 30 --print-gate-stub
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir, read_path  # noqa: E402

BLOCK_RE = re.compile(
    r"### \[WORK-choice\]\s+(\S+).*?(?=### \[WORK-choice\]|\Z)",
    re.DOTALL,
)
PICKED_RE = re.compile(r"^-\s*picked:\s*(.+)$", re.MULTILINE)
CONTEXT_RE = re.compile(r"^-\s*context:\s*(\S+)\s*$", re.MULTILINE)


def parse_blocks(text: str, *, since: datetime) -> list[dict]:
    rows: list[dict] = []
    for m in BLOCK_RE.finditer(text):
        ts_raw = m.group(1).strip()
        block = m.group(0)
        try:
            ts = datetime.strptime(ts_raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            except ValueError:
                continue
        if ts < since:
            continue
        pm = PICKED_RE.search(block)
        cm = CONTEXT_RE.search(block)
        if not pm:
            continue
        rows.append(
            {
                "ts": ts,
                "picked": pm.group(1).strip(),
                "context": cm.group(1).strip() if cm else "?",
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument("--days", type=int, default=30, help="Rolling window (default 30)")
    ap.add_argument(
        "--print-gate-stub",
        action="store_true",
        help="Print optional gate paste stub (stdout only; operator merges via normal flow)",
    )
    args = ap.parse_args()
    uid = args.user.strip()
    user_dir = profile_dir(uid)
    path = user_dir / "session-transcript.md"
    raw = read_path(path)
    if not raw.strip():
        print(f"No session-transcript.md content for {uid}.")
        return 0

    days = max(1, min(365, args.days))
    since = datetime.now(timezone.utc) - timedelta(days=days)
    rows = parse_blocks(raw, since=since)
    if not rows:
        print(f"No [WORK-choice] blocks in the last {days} days for {uid}.")
        return 0

    by_pick = Counter(r["picked"] for r in rows)
    by_ctx = Counter(r["context"] for r in rows)

    lines = [
        f"# Menu choice report — `{uid}`",
        "",
        f"_Window: last {days} days · {len(rows)} picks_",
        "",
        "## Counts by `picked`",
        "",
    ]
    for pick, n in by_pick.most_common():
        lines.append(f"- **{pick}** — {n}")
    lines.extend(["", "## Counts by `context`", ""])
    for ctx, n in by_ctx.most_common():
        lines.append(f"- **{ctx}** — {n}")
    lines.append("")
    print("\n".join(lines))

    if args.print_gate_stub:
        top = by_pick.most_common(3)
        top_s = ", ".join(f"{p} ({c})" for p, c in top) if top else "insufficient data"
        stub = f"""### CANDIDATE-XXXX (operator — menu evolution summary)

```yaml
territory: work-politics
channel_key: operator:work-strategy
source: operator — menu_choice_evolution.py --print-gate-stub
summary: Menu picks last {days}d — top: {top_s}; suggest template/menu tweaks if drift vs intent.
suggested_entry: "(none — operator edits templates or skills from report)"
```
"""
        print(stub)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
