#!/usr/bin/env python3
"""
Append a task event to work-jiang/tasks.jsonl.

Each line records a lifecycle transition for a task: created, claimed,
submitted, merged, or cancelled.  Append-only; current state is derived
by reading the latest event per task_id.

Usage:
    python3 scripts/work_jiang/emit_task_event.py create draft-ch07 \
        --type chapter_draft --scope ch07 \
        --depends-on analysis-ch07 \
        --context "lectures/geo-strategy-07-*.md" "chapters/ch07/outline.md"

    python3 scripts/work_jiang/emit_task_event.py claim draft-ch07 --agent agent-b
    python3 scripts/work_jiang/emit_task_event.py submit draft-ch07
    python3 scripts/work_jiang/emit_task_event.py merge draft-ch07
    python3 scripts/work_jiang/emit_task_event.py cancel draft-ch07 --note "superseded"
    python3 scripts/work_jiang/emit_task_event.py list
    python3 scripts/work_jiang/emit_task_event.py list --status available
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_JIANG = REPO_ROOT / "research" / "external" / "work-jiang"
TASKS_PATH = WORK_JIANG / "tasks.jsonl"

VALID_EVENTS = {"created", "claimed", "submitted", "merged", "cancelled"}
VALID_TYPES = {
    "chapter_draft",
    "chapter_analysis",
    "transcript_normalize",
    "asr_audit",
    "prediction_score",
    "divergence_check",
    "pedagogy_analysis",
}
EVENT_TO_STATUS = {
    "created": "available",
    "claimed": "claimed",
    "submitted": "submitted",
    "merged": "merged",
    "cancelled": "cancelled",
}


def new_task_event_id() -> str:
    return f"tevt_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


def append_task_event(
    task_id: str,
    event: str,
    *,
    task_type: str | None = None,
    scope: str | None = None,
    depends_on: list[str] | None = None,
    context_files: list[str] | None = None,
    agent: str | None = None,
    note: str | None = None,
) -> dict:
    if event not in VALID_EVENTS:
        raise ValueError(f"Invalid event '{event}'; must be one of {VALID_EVENTS}")
    if event == "created" and not task_type:
        raise ValueError("--type is required for 'create' events")

    record: dict = {
        "event_id": new_task_event_id(),
        "ts": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
        "event": event,
        "status": EVENT_TO_STATUS[event],
    }
    if task_type:
        record["type"] = task_type
    if scope:
        record["scope"] = scope
    if depends_on:
        record["depends_on"] = depends_on
    if context_files:
        record["context_files"] = context_files
    if agent:
        record["agent"] = agent
    if note:
        record["note"] = note

    TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def read_task_states() -> dict[str, dict]:
    """Return latest state per task_id by replaying the log."""
    states: dict[str, dict] = {}
    if not TASKS_PATH.exists():
        return states
    for line in TASKS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        tid = rec["task_id"]
        if tid not in states:
            states[tid] = {}
        states[tid].update(rec)
    return states


def list_tasks(status_filter: str | None = None) -> None:
    states = read_task_states()
    if not states:
        print("No tasks found.")
        return
    for tid, st in sorted(states.items()):
        if status_filter and st.get("status") != status_filter:
            continue
        parts = [
            f"  {tid}",
            f"status={st.get('status', '?')}",
            f"type={st.get('type', '?')}",
            f"scope={st.get('scope', '?')}",
        ]
        if st.get("agent"):
            parts.append(f"agent={st['agent']}")
        print("  ".join(parts))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Append task events to work-jiang/tasks.jsonl."
    )
    parser.add_argument(
        "action",
        choices=["create", "claim", "submit", "merge", "cancel", "list"],
        help="Lifecycle action",
    )
    parser.add_argument("task_id", nargs="?", help="Task identifier (not needed for 'list')")
    parser.add_argument("--type", dest="task_type", choices=sorted(VALID_TYPES), help="Task type (required for create)")
    parser.add_argument("--scope", help="Scope identifier (e.g. ch07, secret-history-08)")
    parser.add_argument("--depends-on", nargs="*", default=[], help="Task IDs this depends on")
    parser.add_argument("--context", nargs="*", default=[], help="Context file globs")
    parser.add_argument("--agent", help="Agent identifier (for claim)")
    parser.add_argument("--note", help="Free-text note")
    parser.add_argument("--status", help="Filter for list action")
    args = parser.parse_args()

    if args.action == "list":
        list_tasks(args.status)
        return

    if not args.task_id:
        print("task_id is required for this action", file=sys.stderr)
        sys.exit(1)

    event_name = args.action
    if event_name == "cancel":
        event_name = "cancelled"
    elif event_name == "merge":
        event_name = "merged"
    elif event_name == "submit":
        event_name = "submitted"
    elif event_name == "claim":
        event_name = "claimed"
    elif event_name == "create":
        event_name = "created"

    rec = append_task_event(
        args.task_id,
        event_name,
        task_type=args.task_type,
        scope=args.scope,
        depends_on=args.depends_on or None,
        context_files=args.context or None,
        agent=args.agent,
        note=args.note,
    )
    print(f"Emitted {rec['event']} for {rec['task_id']} (status={rec['status']})")


if __name__ == "__main__":
    main()
