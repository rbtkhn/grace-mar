#!/usr/bin/env python3
"""Strategy run wrapper — start / inspect / resume / complete (WORK only).

Derived operational state; does not mutate canonical strategy notebook Markdown.
See docs/run-contract.md, docs/skill-work/work-strategy/STRATEGY-RUN-OPERATOR.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
# Tests may set STRATEGY_RUN_ARTIFACT_ROOT to a temp tree (repo-shaped) for isolation.
ARTIFACT_ROOT = Path(os.environ.get("STRATEGY_RUN_ARTIFACT_ROOT", str(REPO_ROOT))).resolve()
DEFAULT_NOTEBOOK = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "strategy-notebook"
ARTIFACTS_RUNS = ARTIFACT_ROOT / "artifacts" / "strategy-runs"
ARTIFACTS_RECEIPTS = ARTIFACT_ROOT / "artifacts" / "run-receipts"


@dataclass
class InputResolution:
    notebook_dir: str
    inbox_path: str
    days_md_path: str
    raw_input_dir: str
    inbox_exists: bool
    days_md_exists: bool
    raw_input_exists: bool
    warnings: list[str]

    @property
    def files_examined(self) -> list[str]:
        out = [self.notebook_dir, self.inbox_path, self.days_md_path, self.raw_input_dir]
        return sorted(out)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(ARTIFACT_ROOT.resolve()).as_posix()
    except ValueError:
        return p.resolve().as_posix()


def _run_dir(run_id: str) -> Path:
    return ARTIFACTS_RUNS / run_id


def _state_path(run_id: str) -> Path:
    return _run_dir(run_id) / "state.json"


def _generate_run_id(d: date) -> str:
    import secrets

    return f"stratrun-{d.strftime('%Y%m%d')}-{secrets.token_hex(4)}"


def _resolve_inputs(notebook_dir: Path, target: date) -> InputResolution:
    ymd = target.isoformat()
    ym = ymd[:7]
    nb = _rel(notebook_dir)
    inbox = notebook_dir / "daily-strategy-inbox.md"
    days = notebook_dir / "chapters" / ym / "days.md"
    raw = notebook_dir / "raw-input" / ymd
    warnings: list[str] = []
    inbox_ex = inbox.is_file()
    days_ex = days.is_file()
    raw_ex = raw.is_dir()
    if not inbox_ex:
        warnings.append(f"missing_inbox: {_rel(inbox)}")
    if not days_ex:
        warnings.append(f"missing_days_md: {_rel(days)}")
    if not raw_ex:
        warnings.append(f"missing_raw_input_dir: {_rel(raw)}")

    return InputResolution(
        notebook_dir=nb,
        inbox_path=_rel(inbox),
        days_md_path=_rel(days),
        raw_input_dir=_rel(raw),
        inbox_exists=inbox_ex,
        days_md_exists=days_ex,
        raw_input_exists=raw_ex,
        warnings=warnings,
    )


def _initial_status(res: InputResolution) -> str:
    if res.inbox_exists:
        return "inputs_resolved"
    return "started"


def _build_state(
    run_id: str,
    target: date,
    intent: str,
    session_type: str,
    res: InputResolution,
    status: str,
    receipt_refs: list[str],
) -> dict[str, Any]:
    ts = _now_iso()
    return {
        "run_id": run_id,
        "lane": "work-strategy",
        "intent": intent,
        "session_type": session_type,
        "target_date": target.isoformat(),
        "status": status,
        "approval_state": "none",
        "inputs": {
            "notebook_dir": res.notebook_dir,
            "inbox_path": res.inbox_path,
            "days_md_path": res.days_md_path,
            "raw_input_dir": res.raw_input_dir,
            "inbox_exists": res.inbox_exists,
            "days_md_exists": res.days_md_exists,
            "raw_input_exists": res.raw_input_exists,
        },
        "proposed_outputs": {
            "day_proposal_path": None,
            "page_proposal_path": None,
        },
        "receipt_refs": receipt_refs,
        "warnings": res.warnings,
        "created_at": ts,
        "updated_at": ts,
    }


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_state(run_id: str) -> dict[str, Any]:
    p = _state_path(run_id)
    if not p.is_file():
        raise FileNotFoundError(f"no state for run_id: {run_id} ({p})")
    return json.loads(p.read_text(encoding="utf-8"))


def _receipt(
    command: str,
    run_id: str,
    files_read: list[str],
    files_touched: list[str],
    result_status: str,
    warnings: list[str],
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "timestamp": _now_iso(),
        "command": command,
        "run_id": run_id,
        "files_read": files_read,
        "files_touched": files_touched,
        "result_status": result_status,
        "warnings": warnings,
        "error": error,
        "model": None,
        "provider": None,
    }


def cmd_start(args: argparse.Namespace) -> int:
    target = date.fromisoformat(args.date)
    nb = args.notebook_dir.resolve()
    if not nb.is_dir():
        print(f"error: notebook-dir not found: {nb}", file=sys.stderr)
        return 1
    res = _resolve_inputs(nb, target)
    run_id = _generate_run_id(target)
    status = _initial_status(res)
    receipt_name = f"{run_id}-start.json"
    receipt_path = ARTIFACTS_RECEIPTS / receipt_name
    rec = _receipt(
        "start",
        run_id,
        files_read=res.files_examined,
        files_touched=[_rel(_state_path(run_id)), _rel(receipt_path)],
        result_status="ok",
        warnings=res.warnings,
    )
    receipt_rel = _rel(receipt_path)
    state = _build_state(
        run_id, target, args.intent, args.session_type, res, status, [receipt_rel]
    )
    _write_json(_state_path(run_id), state)
    _write_json(receipt_path, rec)
    print(run_id, flush=True)
    print(f"state: {_rel(_state_path(run_id))}", flush=True)
    print(f"receipt: {receipt_rel}", flush=True)
    return 0


def _print_summary(st: dict[str, Any], *, label: str) -> None:
    print(f"--- {label} ---", flush=True)
    print(f"run_id:        {st.get('run_id')}", flush=True)
    print(f"lane:          {st.get('lane')}", flush=True)
    print(f"intent:        {st.get('intent')}", flush=True)
    print(f"session_type:  {st.get('session_type')}", flush=True)
    print(f"target_date:   {st.get('target_date')}", flush=True)
    print(f"status:        {st.get('status')}", flush=True)
    print(f"approval_state: {st.get('approval_state')}", flush=True)
    print("inputs:", flush=True)
    for k, v in (st.get("inputs") or {}).items():
        print(f"  {k}: {v}", flush=True)
    po = st.get("proposed_outputs") or {}
    print("proposed_outputs:", flush=True)
    print(f"  day_proposal_path:  {po.get('day_proposal_path')}", flush=True)
    print(f"  page_proposal_path: {po.get('page_proposal_path')}", flush=True)
    print("receipt_refs:", flush=True)
    for r in st.get("receipt_refs") or []:
        print(f"  {r}", flush=True)
    print("warnings:", flush=True)
    for w in st.get("warnings") or []:
        print(f"  - {w}", flush=True)


def cmd_inspect(args: argparse.Namespace) -> int:
    try:
        st = _read_state(args.run_id)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    _print_summary(st, label="inspect")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    try:
        st = _read_state(args.run_id)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    _print_summary(st, label="resume (no files mutated)")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    try:
        st = _read_state(args.run_id)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    cur = st.get("status", "")
    if cur == "completed":
        print("note: run already completed", file=sys.stderr)
        return 0
    if cur == "failed" and not args.force:
        print(
            "error: run status is 'failed'; use --force to mark completed",
            file=sys.stderr,
        )
        return 1
    st["status"] = "completed"
    st["updated_at"] = _now_iso()
    receipt_name = f"{args.run_id}-complete.json"
    receipt_path = ARTIFACTS_RECEIPTS / receipt_name
    sp = _state_path(args.run_id)
    rec = _receipt(
        "complete",
        args.run_id,
        files_read=[_rel(sp)],
        files_touched=[_rel(sp), _rel(receipt_path)],
        result_status="ok",
        warnings=[],
    )
    rlist = list(st.get("receipt_refs") or [])
    rrel = _rel(receipt_path)
    if rrel not in rlist:
        rlist.append(rrel)
    st["receipt_refs"] = rlist
    _write_json(sp, st)
    _write_json(receipt_path, rec)
    print("completed", flush=True)
    print(f"state: {_rel(sp)}", flush=True)
    print(f"receipt: {rrel}", flush=True)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="Allocate run id, resolve inputs, write state + receipt")
    s.add_argument("--date", required=True, help="YYYY-MM-DD")
    s.add_argument("--intent", default="eod", help="Operator intent label")
    s.add_argument(
        "--session-type",
        default="eod_strategy",
        dest="session_type",
        help="Session kind (default: eod_strategy)",
    )
    s.add_argument("--notebook-dir", type=Path, default=DEFAULT_NOTEBOOK)
    s.set_defaults(func=cmd_start)

    i = sub.add_parser("inspect", help="Print run state summary")
    i.add_argument("--run-id", required=True, dest="run_id")
    i.set_defaults(func=cmd_inspect)

    r = sub.add_parser("resume", help="Print resumable state (no notebook mutation)")
    r.add_argument("--run-id", required=True, dest="run_id")
    r.set_defaults(func=cmd_resume)

    c = sub.add_parser("complete", help="Mark run completed; write final receipt")
    c.add_argument("--run-id", required=True, dest="run_id")
    c.add_argument(
        "--force",
        action="store_true",
        help="Allow completion when status is failed",
    )
    c.set_defaults(func=cmd_complete)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
