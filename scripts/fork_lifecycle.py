#!/usr/bin/env python3
"""
Fork lifecycle CLI — fork history (state, sessions, lineage).

Usage (global -u before subcommand):
  python scripts/fork_lifecycle.py -u grace-mar init
  python scripts/fork_lifecycle.py -u grace-mar begin-session --channel telegram
  python scripts/fork_lifecycle.py -u grace-mar end-session --session-id SES-...
  python scripts/fork_lifecycle.py -u grace-mar measure-drift
  python scripts/fork_lifecycle.py -u grace-mar merge-checkpoint --receipt /path/receipt.json
  python scripts/fork_lifecycle.py -u grace-mar snapshot --tag grace-mar-age-7
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.fork_lifecycle import (  # noqa: E402
    begin_session,
    end_session,
    merge_checkpoint,
    session_manifest_path,
)
from grace_mar.fork_state import (  # noqa: E402
    ensure_fork_state,
    fork_state_path,
    load_fork_state,
    transition_fork_phase,
)


def _cmd_init(args: argparse.Namespace) -> int:
    st = ensure_fork_state(REPO_ROOT, args.user)
    if args.seed_commit:
        st["seed_commit"] = args.seed_commit
        from grace_mar.fork_state import write_fork_state

        write_fork_state(REPO_ROOT, args.user, st)
    print(fork_state_path(REPO_ROOT, args.user))
    return 0


def _cmd_begin_session(args: argparse.Namespace) -> int:
    m = begin_session(REPO_ROOT, args.user, channel=args.channel or "operator")
    print(m["session_id"])
    print(session_manifest_path(REPO_ROOT, args.user, m["session_id"]))
    return 0


def _cmd_end_session(args: argparse.Namespace) -> int:
    m = end_session(
        REPO_ROOT,
        args.user,
        args.session_id,
        drift_score_after=args.drift_after,
        git_commit=args.git_commit or "",
    )
    print(json.dumps(m, indent=2))
    return 0


def _cmd_measure_drift(args: argparse.Namespace) -> int:
    from grace_mar.drift import compute_drift_report

    path = compute_drift_report(REPO_ROOT, args.user)
    print(path)
    return 0


def _cmd_merge_checkpoint(args: argparse.Namespace) -> int:
    p = Path(args.receipt)
    if not p.is_file():
        print(f"Missing receipt: {p}", file=sys.stderr)
        return 1
    receipt = json.loads(p.read_text(encoding="utf-8"))
    st = merge_checkpoint(REPO_ROOT, args.user, receipt)
    print(json.dumps(st, indent=2))
    return 0


def _cmd_snapshot(args: argparse.Namespace) -> int:
    from grace_mar.snapshot import create_snapshot

    path = create_snapshot(REPO_ROOT, args.user, args.tag, skip_git_tag=args.no_git_tag)
    print(path)
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    st = load_fork_state(REPO_ROOT, args.user)
    if not st:
        print("no fork_state.json — run init", file=sys.stderr)
        return 1
    print(json.dumps(st, indent=2))
    return 0


def _cmd_transition(args: argparse.Namespace) -> int:
    st = transition_fork_phase(REPO_ROOT, args.user, args.phase)
    print(json.dumps(st, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Fork lifecycle (fork history)")
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")

    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Create fork_state.json and dirs")
    p_init.add_argument("--seed-commit", default="", help="Git commit at fork seed")
    p_init.set_defaults(func=_cmd_init)

    p_begin = sub.add_parser("begin-session", help="Open a lifecycle session")
    p_begin.add_argument("--channel", default="operator")
    p_begin.set_defaults(func=_cmd_begin_session)

    p_end = sub.add_parser("end-session", help="Close session manifest")
    p_end.add_argument("--session-id", required=True)
    p_end.add_argument("--drift-after", type=float, default=None)
    p_end.add_argument("--git-commit", default="")
    p_end.set_defaults(func=_cmd_end_session)

    p_drift = sub.add_parser("measure-drift", help="Write drift-report.json")
    p_drift.set_defaults(func=_cmd_measure_drift)

    p_mc = sub.add_parser("merge-checkpoint", help="Record merge receipt checkpoint")
    p_mc.add_argument("--receipt", required=True)
    p_mc.set_defaults(func=_cmd_merge_checkpoint)

    p_sn = sub.add_parser("snapshot", help="Create snapshot manifest (and optional git tag)")
    p_sn.add_argument("--tag", required=True)
    p_sn.add_argument("--no-git-tag", action="store_true")
    p_sn.set_defaults(func=_cmd_snapshot)

    p_st = sub.add_parser("status", help="Print fork_state.json")
    p_st.set_defaults(func=_cmd_status)

    p_tr = sub.add_parser("transition", help="Force legal phase transition (operator)")
    p_tr.add_argument("--phase", required=True)
    p_tr.set_defaults(func=_cmd_transition)

    args = ap.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
