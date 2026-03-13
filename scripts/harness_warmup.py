#!/usr/bin/env python3
"""
Harness warmup — paste block so a *new* AI session starts with repo state, not a blank window.

Why this exists
---------------
LLM chats and coding agents have **no memory** across sessions unless you give it. Vendor
harnesses (Cursor, OpenClaw, Claude Code, Codex) each accumulate **their own** habits and
context; Grace-Mar’s canonical memory is **git + gated pipeline** (SELF, EVIDENCE,
RECURSION-GATE, session-log). Warmup **does not** replace reading those files — it **summarizes**
them into one paste so any harness can align on the same facts in message one.

What it pulls
-------------
| Source              | What you get                                              |
|---------------------|-----------------------------------------------------------|
| recursion-gate.md   | Count of **pending** candidates + IDs + one-line summaries |
| self-evidence.md    | **Last ACT-*** activity (date + summary/topic)            |
| session-log.md      | **Tail** of non-noise lines (recent operator/session notes)|

When to run
-----------
- Starting a **new Cursor / agent thread** after a break
- Kicking off **OpenClaw** (same info as the checklist; optional before heartbeat cadence)
- **Switching harnesses** (Codex ↔ Claude Code): paste so the new tool sees gate + last activity

What it does *not* do
---------------------
- Merge or stage (read-only)
- Replace ``session_brief.py`` (warmup is minimal; session_brief adds wisdom, IX, INTENT)
- Include full RECURSION-GATE or EVIDENCE bodies (too large; point the agent at paths if needed)

Usage
-----
    python scripts/harness_warmup.py -u grace-mar
    python scripts/harness_warmup.py -u grace-mar --compact
    python scripts/harness_warmup.py -u grace-mar --tail 8
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_territory import pending_by_territory

DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
DEFAULT_TAIL = 12


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _session_lines_tail(session_md: str, n: int) -> list[str]:
    """Non-empty lines outside ``` fences — avoids yaml dumps polluting the tail."""
    raw = []
    in_fence = False
    for line in session_md.splitlines():
        s = line.rstrip()
        if s.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not s.strip() or s.strip().startswith("#"):
            continue
        if "END OF FILE" in s.upper():
            continue
        if s.strip() == "---":
            continue
        if re.match(r"^\|\s*---+\s*\|", s):
            continue
        raw.append(s)
    return raw[-n:] if len(raw) > n else raw


def _pending_candidates(pr_content: str, territory: str = "all") -> list[tuple[str, str]]:
    """Return [(CANDIDATE-id, summary_one_line), ...] for status: pending. territory: all|wap|companion."""
    wap, companion = pending_by_territory(pr_content)
    if territory == "wap":
        rows = wap
    elif territory == "companion":
        rows = companion
    else:
        rows = wap + companion
    return [(r["id"], (r["summary"] or "(no summary)")[:120]) for r in rows]


def _last_activity_oneliner(evidence_content: str) -> str:
    """Last ACT-* entry in V. ACTIVITY LOG: date + summary or topic."""
    if "## V. ACTIVITY LOG" not in evidence_content:
        return ""
    start = evidence_content.find("## V. ACTIVITY LOG")
    end = evidence_content.find("\n## VI.", start)
    block = evidence_content[start:end] if end > start else evidence_content[start:]
    matches = list(re.finditer(r"\n  - id: (ACT-\d+)", block))
    if not matches:
        return ""
    last = matches[-1]
    chunk_end = matches[-1].end()
    nxt = re.search(r"\n  - id: ", block[chunk_end:])
    chunk = block[last.start() + 1 : chunk_end + nxt.start()] if nxt else block[last.start() + 1 : last.start() + 2500]
    act_id = last.group(1)
    date_m = re.search(r"date:\s*(\S+)", chunk)
    summary_m = re.search(r'summary:\s*"([^"]*)"', chunk)
    topic_m = re.search(r'topic:\s*"([^"]*)"', chunk)
    atype_m = re.search(r"activity_type:\s*(.+)", chunk)
    label = (
        (summary_m.group(1) if summary_m else None)
        or (topic_m.group(1) if topic_m else None)
        or ((atype_m.group(1) or "").strip() if atype_m else None)
        or act_id
    )
    if len(label) > 100:
        label = label[:97] + "…"
    d = date_m.group(1) if date_m else "?"
    return f"{act_id} ({d}) — {label}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Paste-ready Grace-Mar continuity for any harness (read-only).",
        epilog="Canonical memory: users/[id]/ + git. This output is a digest for message 1.",
    )
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User id (default GRACE_MAR_USER_ID or grace-mar)")
    parser.add_argument("--compact", action="store_true", help="Single paragraph")
    parser.add_argument("--tail", type=int, default=DEFAULT_TAIL, metavar="N", help="Session-log lines in full output (default 12)")
    parser.add_argument(
        "--territory",
        choices=("all", "wap", "companion"),
        default="all",
        help="Pending lens: wap | companion | all",
    )
    args = parser.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    pr = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-evidence.md")
    session = _read(user_dir / "session-log.md")

    wap_n = len(pending_by_territory(pr)[0])
    comp_n = len(pending_by_territory(pr)[1])
    pending_list = _pending_candidates(pr, args.territory)
    pending_n = len(pending_list)
    last_act = _last_activity_oneliner(evidence)
    tail = _session_lines_tail(session, max(1, args.tail))
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    if args.compact:
        bits = [
            f"[Grace-Mar warmup · {args.user} · {ts} · territory={args.territory}]",
            f"Pending ({args.territory}): {pending_n} (WAP {wap_n} · Companion {comp_n} total).",
        ]
        if pending_list:
            bits.append("IDs: " + ", ".join(p[0] for p in pending_list[:5]) + ("…" if len(pending_list) > 5 else "") + ".")
        if last_act:
            bits.append(f"Last EVIDENCE: {last_act}.")
        if tail:
            bits.append("Session tail: " + " / ".join(tail[-2:]))
        print(" ".join(bits))
        return 0

    lines = [
        f"<!-- harness_warmup.py · {args.user} · {ts} — paste into first message; read-only digest -->",
        "",
        f"## Grace-Mar warmup (`{args.user}`)",
        "",
        "This block was generated by `python scripts/harness_warmup.py` — **not** part of the Record until merged elsewhere.",
        "",
        f"- **RECURSION-GATE — pending ({args.territory}):** {pending_n} _(WAP {wap_n} · Companion {comp_n} — use `--territory wap` or `companion`)_",
    ]
    if pending_list:
        lines.append("")
        for cid, summ in pending_list[:8]:
            lines.append(f"  - **{cid}** — {summ}")
        if len(pending_list) > 8:
            lines.append(f"  - … and {len(pending_list) - 8} more (open `users/{args.user}/recursion-gate.md`)")
    lines.extend(
        [
            "",
            f"- **Last EVIDENCE (activity log):** {last_act or '_none parsed_'}",
            "",
            f"### Session-log tail (last {len(tail)} non-empty lines)",
            "",
        ]
    )
    if tail:
        lines.append("```")
        lines.extend(tail)
        lines.append("```")
    else:
        lines.append("_session-log.md empty_")
    lines.extend(
        [
            "",
            "### For the agent",
            "",
            f"- Canonical paths: `users/{args.user}/self.md`, `self-evidence.md`, `recursion-gate.md`, `session-log.md`.",
            "- **Do not merge** without companion approval. Stage-only handback: `integrations/openclaw_stage.py`.",
            "- After approved merges: refresh PRP / OpenClaw export if this instance uses them.",
            "",
        ]
    )
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
