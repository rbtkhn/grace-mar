#!/usr/bin/env python3
"""
cadence-coffee.py — consolidated coffee runner for companion-self instances.

Single entry point for all morning startup modes.  Assembles the right
combination of good-morning-brief.py options (and optional git snapshot)
depending on the chosen mode.

Modes
-----
  standard   Full coffee: good-morning-brief (standard) + branch snapshot
  light      Quieter sip: good-morning-brief (minimal) + compact branch line
  deep       Deep coffee: good-morning-brief (deep, --check-sync) + branch snapshot
  closeout   Night closeout: good-night-brief (--write-closeout --suggest-gate)

Usage
-----
    python3 scripts/cadence-coffee.py --user demo
    python3 scripts/cadence-coffee.py --user demo --mode light
    python3 scripts/cadence-coffee.py --user demo --mode deep
    python3 scripts/cadence-coffee.py --user demo --lane write
    python3 scripts/cadence-coffee.py --user demo --max-lines 120
    python3 scripts/cadence-coffee.py --user demo --no-log-cadence
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO = Path(__file__).resolve().parent.parent
MODES = ("standard", "light", "deep", "closeout")
STATE_NAME = "last-coffee-state.json"
CONTEXT_NAME = ".coffee-run-context.json"


def _run(argv: list[str], *, label: str | None = None) -> int:
    display = label or " ".join(argv)
    print(f"\n{'=' * 60}\n$ {display}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def _git_status_sb() -> str:
    r = subprocess.run(
        ["git", "status", "-sb"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    return (r.stdout or "").strip()


def _git_branch_vv() -> str:
    r = subprocess.run(
        ["git", "branch", "-vv"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    return r.stdout or ""


def _git_head_short() -> str:
    r = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(_REPO),
        capture_output=True,
        text=True,
    )
    return (r.stdout or "").strip() or "unknown"


def _branch_triage() -> Tuple[str, str, Dict[str, Any]]:
    """Return (branchHygieneClass, recommendedBranchAction, detail)."""
    status_out = _git_status_sb()
    branch_out = _git_branch_vv()
    body = [ln for ln in status_out.splitlines() if ln.strip() and not ln.startswith("## ")]
    dirty = len(body) > 0
    non_main = [
        line.strip()
        for line in branch_out.splitlines()
        if line.strip()
        and not line.strip().startswith("* main")
        and not line.strip().startswith("main ")
    ]
    n = len(non_main)
    if n > 4 or (dirty and len(body) > 12):
        cls, act = "risky", "reconcile"
    elif n > 0 or dirty:
        cls, act = "watch", "inspect"
    else:
        cls, act = "clean", "none"
    return cls, act, {
        "nonMainBranchCount": n,
        "worktreeDirty": dirty,
        "statusLine": status_out.splitlines()[0] if status_out else "",
    }


def _branch_snapshot_text(*, compact: bool = False, triage: Tuple[str, str, Dict[str, Any]] | None = None) -> str:
    status_out = _git_status_sb()
    if triage is None:
        triage = _branch_triage()
    cls, action, _detail = triage
    triage_line = f"Branch hygiene: {cls} — recommended: {action}."

    if compact:
        return f"Branch: {status_out}\n{triage_line}"

    branch_out = _git_branch_vv()
    non_main = [
        line.strip()
        for line in branch_out.splitlines()
        if line.strip()
        and not line.strip().startswith("* main")
        and not line.strip().startswith("main ")
    ]
    if not non_main:
        return f"{triage_line}\n{status_out}"
    return (
        f"{triage_line}\n\nBranch snapshot:\n{status_out}\n\n"
        f"Branches:\n{branch_out}\n\n"
        f"Non-main branches: {len(non_main)} — review before next merge."
    )


def _gate_fingerprint(gate_path: Path) -> str:
    if not gate_path.is_file():
        return "0"
    st = gate_path.stat()
    raw = f"{st.st_mtime_ns}:{st.st_size}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _read_state(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _build_delta(prev: Dict[str, Any], cur: Dict[str, Any]) -> List[str]:
    if not prev:
        return ["(first coffee state recorded — no prior delta)"]
    out: List[str] = []
    if prev.get("gitHead") != cur.get("gitHead"):
        out.append("Git HEAD changed since last coffee.")
    if prev.get("nightHandoffDate") != cur.get("nightHandoffDate"):
        out.append("Dream handoff date changed since last coffee.")
    if prev.get("gateFingerprint") != cur.get("gateFingerprint"):
        out.append("Gate file changed since last coffee.")
    if prev.get("worktreeDirty") != cur.get("worktreeDirty"):
        out.append(
            "Worktree dirtiness changed since last coffee."
            if cur.get("worktreeDirty")
            else "Worktree is cleaner than at last coffee."
        )
    return out[:4] if out else ["No material delta since last coffee."]


def _suggest_mode(
    *,
    handoff: Dict[str, Any],
    branch_class: str,
    has_delta_head_change: bool,
) -> str:
    if branch_class == "risky":
        return "deep"
    if handoff.get("quietRun") and branch_class == "clean":
        return "light"
    if has_delta_head_change and branch_class == "watch":
        return "standard"
    return "standard"


def _write_coffee_context(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _log_coffee(
    user: str,
    mode: str,
    *,
    ok: bool,
    helpful: str | None,
) -> None:
    py = sys.executable
    kv: List[str] = []
    if helpful:
        kv.extend(["--kv", f"helpful={helpful}"])
    cmd = [
        py,
        str(_REPO / "scripts" / "log_cadence_event.py"),
        "--kind",
        "coffee",
        "-u",
        user,
        "--ok" if ok else "--no-ok",
        "--mode",
        mode,
    ] + kv
    subprocess.run(cmd, cwd=str(_REPO))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Coffee — consolidated morning cadence runner for companion-self instances."
    )
    p.add_argument("--user", required=True, help="Instance user id (users/<id>/)")
    p.add_argument(
        "--mode",
        "-m",
        choices=MODES,
        default="standard",
        help="Coffee mode (default: standard). Use light for a quieter sip.",
    )
    p.add_argument(
        "--lane",
        default="",
        help="Optional lane hook: write|gate|build|research|none",
    )
    p.add_argument(
        "--max-lines",
        type=int,
        default=160,
        help="Forward to good-morning-brief.py (cap printed lines).",
    )
    p.add_argument(
        "--write-intention",
        action="store_true",
        help="Write daily intention note via good-morning-brief.py",
    )
    p.add_argument(
        "--check-sync",
        action="store_true",
        help="Force sync checks even outside deep mode",
    )
    p.add_argument(
        "--no-log-cadence",
        action="store_true",
        help="Skip appending work-cadence-events.md coffee line after success.",
    )
    p.add_argument(
        "--coffee-helpful",
        choices=["yes", "no", "partial"],
        default=None,
        help="Optional: record usefulness on the cadence coffee line (kv helpful=).",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable
    user_dir = _REPO / "users" / user
    handoff_dir = user_dir / "daily-handoff"
    state_path = handoff_dir / STATE_NAME
    context_path = handoff_dir / CONTEXT_NAME

    morning = [py, "scripts/good-morning-brief.py", "--user", user, "--max-lines", str(args.max_lines)]
    night = [py, "scripts/good-night-brief.py", "--user", user]

    steps: list[list[str]] = []

    if args.mode == "standard":
        cmd = morning + ["--mode", "standard"]
        if args.check_sync:
            cmd.append("--check-sync")
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "light":
        cmd = morning + ["--mode", "minimal"]
        if args.check_sync:
            cmd.append("--check-sync")
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "deep":
        cmd = morning + ["--mode", "deep", "--check-sync"]
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "closeout":
        steps.append(night + ["--write-closeout", "--suggest-gate"])

    triage = _branch_triage()
    branch_class, branch_action, tri_detail = triage
    handoff: Dict[str, Any] = {}
    nh_path = handoff_dir / "night-handoff.json"
    if nh_path.is_file():
        try:
            handoff = json.loads(nh_path.read_text(encoding="utf-8"))
        except Exception:
            handoff = {}
    gate_path = user_dir / "recursion-gate.md"
    prev = _read_state(state_path)
    cur_snapshot = {
        "gitHead": _git_head_short(),
        "nightHandoffDate": str(handoff.get("date") or ""),
        "gateFingerprint": _gate_fingerprint(gate_path),
        "worktreeDirty": bool(tri_detail.get("worktreeDirty")),
        "coffeeMode": args.mode,
    }
    delta_lines = _build_delta(prev, cur_snapshot)
    has_head_change = bool(prev.get("gitHead") and prev.get("gitHead") != cur_snapshot["gitHead"])
    suggested = _suggest_mode(
        handoff=handoff,
        branch_class=branch_class,
        has_delta_head_change=has_head_change,
    )

    if args.mode != "closeout":
        print(
            f"\n{'=' * 60}\n$ coffee mode suggestion (optional)\n{'=' * 60}\n",
            flush=True,
        )
        print(
            f"Suggested next run (if you re-sip): {suggested} "
            f"(current run: {args.mode}, branch hygiene: {branch_class}).\n",
            flush=True,
        )
        ctx_payload: Dict[str, Any] = {
            "deltaLines": delta_lines,
            "branchHygieneClass": branch_class,
            "recommendedBranchAction": branch_action,
            "suggestedCoffeeMode": suggested,
            "nonMainBranchCount": tri_detail.get("nonMainBranchCount"),
            "worktreeDirty": tri_detail.get("worktreeDirty"),
        }
        _write_coffee_context(context_path, ctx_payload)
        for step in steps:
            step.append("--coffee-context-file")
            step.append(str(context_path))
            if (args.lane or "").strip():
                step.extend(["--coffee-lane", args.lane.strip()])

    for argv in steps:
        code = _run(argv)
        if code != 0:
            if not args.no_log_cadence and args.mode != "closeout":
                _log_coffee(user, args.mode, ok=False, helpful=args.coffee_helpful)
            return code

    if args.mode != "closeout":
        cur_snapshot["runIso"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        state_path.write_text(json.dumps(cur_snapshot, indent=2) + "\n", encoding="utf-8")
        compact = args.mode == "light"
        print(f"\n{'=' * 60}\n$ git branch snapshot\n{'=' * 60}\n", flush=True)
        print(_branch_snapshot_text(compact=compact, triage=triage))
        if not args.no_log_cadence:
            _log_coffee(user, args.mode, ok=True, helpful=args.coffee_helpful)

    return 0


if __name__ == "__main__":
    sys.exit(main())
