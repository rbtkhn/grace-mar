#!/usr/bin/env python3
"""Append one shadow-mode decision line (BUILD-AI-GAP-007)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_LOG = REPO_ROOT / "runtime" / "autonomy" / "shadow_decisions.jsonl"


def append_shadow_decision(
    record: dict,
    *,
    log_path: Path | None = None,
) -> None:
    p = log_path or DEFAULT_LOG
    p.parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": datetime.now(timezone.utc).isoformat(), **record}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Log one shadow decision (JSON fields).")
    ap.add_argument("--runtime", default="openclaw")
    ap.add_argument("--task-type", default="stage_candidate")
    ap.add_argument("--agent-action", default="approve")
    ap.add_argument("--human-action", default="reject")
    ap.add_argument("--divergence", default="false_positive")
    ap.add_argument("--risk-level", default="high")
    ap.add_argument("--boundary-rule", default="continuity_required")
    args = ap.parse_args()
    append_shadow_decision(
        {
            "runtime": args.runtime,
            "task_type": args.task_type,
            "agent_action": args.agent_action,
            "human_action": args.human_action,
            "divergence": args.divergence,
            "risk_level": args.risk_level,
            "boundary_rule": args.boundary_rule,
        }
    )
    print("log_shadow_decision: appended")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
