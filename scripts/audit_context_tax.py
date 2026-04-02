#!/usr/bin/env python3
"""
Approximate context "tax" for operator ritual paste surfaces.

Not byte-identical to full `build_operator_daily_warmup` output — measures
representative chunks so budget changes show up in before/after comparisons.
Operator scaffolding only; not Record truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from context_budget import get_int, load_context_budget
    from harness_warmup import _pending_candidates, _read, _session_lines_tail
    from operator_daily_warmup import _format_last_dream_block, _read_last_dream
    from operator_depth_hint import velocity_oneliner
    from work_politics_ops import get_work_politics_snapshot
except ImportError:
    from scripts.context_budget import get_int, load_context_budget
    from scripts.harness_warmup import _pending_candidates, _read, _session_lines_tail
    from scripts.operator_daily_warmup import _format_last_dream_block, _read_last_dream
    from scripts.operator_depth_hint import velocity_oneliner
    from scripts.work_politics_ops import get_work_politics_snapshot

USERS_DIR = REPO_ROOT / "users"


def _count_block(label: str, text: str) -> dict[str, object]:
    lines = text.splitlines()
    return {
        "label": label,
        "lines": len(lines),
        "chars": len(text),
    }


def build_context_tax_report(*, user_id: str) -> dict[str, object]:
    user_dir = USERS_DIR / user_id
    coffee_budget = load_context_budget("coffee")
    tail_n = get_int(coffee_budget, "max_session_tail_lines", 3)

    blocks: list[dict[str, object]] = []

    dream = _read_last_dream(user_dir)
    if dream:
        collapsed = "\n".join(
            _format_last_dream_block(
                dream,
                verbose_dream=False,
                show_civ_mem=None,
                show_rollup=None,
            )
        )
        blocks.append(_count_block("last_dream_collapsed", collapsed))
        verbose = "\n".join(
            _format_last_dream_block(
                dream,
                verbose_dream=True,
                show_civ_mem=None,
                show_rollup=None,
            )
        )
        blocks.append(_count_block("last_dream_verbose", verbose))

    session = _read(user_dir / "session-log.md")
    tail_lines = _session_lines_tail(session, tail_n)
    blocks.append(_count_block("session_tail", "\n".join(tail_lines)))

    gate = _read(user_dir / "recursion-gate.md") or ""
    pending = _pending_candidates(gate, "all")
    pend_text = "\n".join(f"{a} {b}" for a, b in pending[:20])
    blocks.append(_count_block("pending_candidates_head", pend_text))

    blocks.append(_count_block("velocity_oneliner", velocity_oneliner(user_id)))

    snap = get_work_politics_snapshot(user_id)
    snap_text = json.dumps(snap, indent=2, default=str)[:8000]
    blocks.append(_count_block("work_politics_snapshot_trim", snap_text))

    total_chars = sum(int(b["chars"]) for b in blocks)
    total_lines = sum(int(b["lines"]) for b in blocks)
    return {
        "user_id": user_id,
        "blocks": blocks,
        "total_chars": total_chars,
        "total_lines": total_lines,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Audit approximate context tax for operator warmup surfaces.")
    p.add_argument("-u", "--user", default="grace-mar", help="User id")
    p.add_argument("--json", action="store_true", help="Emit JSON report")
    args = p.parse_args()
    report = build_context_tax_report(user_id=args.user)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Context tax (approx) user={args.user}")
        print(f"  total_lines={report['total_lines']} total_chars={report['total_chars']}")
        for b in report["blocks"]:
            print(f"  - {b['label']}: lines={b['lines']} chars={b['chars']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
