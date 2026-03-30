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
| self-archive.md     | **Last ACT-*** activity (date + summary/topic)            |
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
    python scripts/harness_warmup.py -u grace-mar --fresh-judge   # clean-context handoff
    python scripts/harness_warmup.py -u grace-mar --receipt      # one-line reentry snapshot (gate + last ACT + git HEAD)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_territory import normalize_territory_cli, pending_by_territory
try:
    from repo_io import read_path, profile_dir, DEFAULT_USER_ID
except ImportError:
    from scripts.repo_io import read_path, profile_dir, DEFAULT_USER_ID

_read = read_path  # backward compat for operator_daily_warmup, operator_handoff_check
DEFAULT_TAIL = 12
_REPO_ROOT = _SCRIPTS.parent


def _git_head_short() -> str:
    """Short git SHA for reentry line; unknown if not a git checkout."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "unknown"


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
    """Return [(CANDIDATE-id, summary_one_line), ...] for status: pending. territory: all|work-politics|companion (pol/wp/wap normalized)."""
    territory = normalize_territory_cli(territory)
    politics, companion = pending_by_territory(pr_content)
    if territory == "work-politics":
        rows = politics
    elif territory == "companion":
        rows = companion
    else:
        rows = politics + companion
    return [(r["id"], (r["summary"] or "(no summary)")[:120]) for r in rows]


def _last_merge_receipt_line(user_dir: Path) -> str:
    """Last JSON line from merge-receipts.jsonl, one-line summary for fresh-judge."""
    p = user_dir / "merge-receipts.jsonl"
    if not p.exists():
        return ""
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return ""
    try:
        import json

        r = json.loads(lines[-1])
        ids = r.get("candidate_ids") or []
        merged = r.get("merged_at") or r.get("approved_at") or "?"
        return f"merged_at={merged} candidates={ids[:5]}{'…' if len(ids) > 5 else ''}"
    except Exception:
        return lines[-1][:200]


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
        choices=("all", "pol", "wap", "wp", "work-politics", "companion"),
        default="all",
        help="Pending lens: work-politics (or pol/wp; legacy wap) | companion | all",
    )
    parser.add_argument(
        "--fresh-judge",
        action="store_true",
        help="Prefix: ignore prior-thread assumptions; canonical state is on disk (gate + last merge receipt)",
    )
    parser.add_argument(
        "--receipt",
        action="store_true",
        help="Print one machine-friendly reentry line (gate counts, last ACT, git HEAD) and exit",
    )
    args = parser.parse_args()
    territory = normalize_territory_cli(args.territory)

    user_dir = profile_dir(args.user)
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    pr = read_path(user_dir / "recursion-gate.md")
    evidence = read_path(user_dir / "self-archive.md") or read_path(user_dir / "self-evidence.md")
    session = read_path(user_dir / "session-log.md")

    politics_n = len(pending_by_territory(pr)[0])
    comp_n = len(pending_by_territory(pr)[1])
    pending_list = _pending_candidates(pr, territory)
    pending_n = len(pending_list)
    last_act = _last_activity_oneliner(evidence)
    tail = _session_lines_tail(session, max(1, args.tail))
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    receipt_one = _last_merge_receipt_line(user_dir)

    if args.receipt:
        gith = _git_head_short()
        gate_label = "clean" if pending_n == 0 else f"{pending_n} pending"
        act_bit = last_act or "none"
        print(
            f"**Reentry** — recursion-gate: {gate_label} "
            f"(view={territory}; work-politics={politics_n}; companion={comp_n}) "
            f"| last_ACTIVITY: {act_bit} | commit: {gith} | user: {args.user}"
        )
        return 0

    fresh_block = ""
    if args.fresh_judge:
        fresh_block = (
            "### Fresh judge (clean context)\n\n"
            "**Ignore prior thread assumptions** about RECURSION-GATE, pending candidates, or last merge. "
            "Canonical state is **only** what appears in the repo paths below (and git).\n\n"
            f"- **Gate:** `users/{args.user}/recursion-gate.md`\n"
            f"- **Last merge receipt:** `users/{args.user}/merge-receipts.jsonl` (tail) — "
            f"{receipt_one or '_no receipts yet_'}\n"
            f"- **SELF / EVIDENCE:** `users/{args.user}/self.md`, `self-archive.md`\n\n"
            "---\n\n"
        )

    if args.compact:
        bits = []
        if args.fresh_judge:
            bits.append(
                f"[FRESH JUDGE · canonical=repo · gate=users/{args.user}/recursion-gate.md · receipt={receipt_one or 'none'}]"
            )
        bits.append(f"[Grace-Mar warmup · {args.user} · {ts} · territory={territory}]")
        bits.append(
            f"Pending ({territory}): {pending_n} (work-politics {politics_n} · Companion {comp_n} total)."
        )
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
    ]
    if args.fresh_judge:
        lines.extend(fresh_block.splitlines())
    lines.extend(
        [
            f"## Grace-Mar warmup (`{args.user}`)",
            "",
            "This block was generated by `python scripts/harness_warmup.py` — **not** part of the Record until merged elsewhere.",
            "",
            f"- **RECURSION-GATE — pending ({territory}):** {pending_n} _(work-politics {politics_n} · Companion {comp_n} — use `--territory work-politics` or `companion`)_",
        ]
    )
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
            f"- Canonical paths: `users/{args.user}/self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`.",
            "- **Do not merge** without companion approval. Stage-only handback: `integrations/openclaw_stage.py`.",
            "- After approved merges: refresh PRP / OpenClaw export if this instance uses them.",
            "",
        ]
    )
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
