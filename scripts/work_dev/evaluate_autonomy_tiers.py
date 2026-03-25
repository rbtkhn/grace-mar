#!/usr/bin/env python3
"""Summarize shadow JSONL and emit stay_shadow | limited_expand | promote | insufficient_data."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_LOG = REPO_ROOT / "runtime" / "autonomy" / "shadow_decisions.jsonl"


def evaluate(log_path: Path, *, window: int = 50) -> str:
    if not log_path.is_file():
        return "insufficient_data"
    lines = [ln.strip() for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()][-window:]
    if len(lines) < 5:
        return "insufficient_data"
    agree = 0
    high_risk = 0
    total = 0
    for ln in lines:
        try:
            o = json.loads(ln)
        except json.JSONDecodeError:
            continue
        total += 1
        if o.get("agent_action") == o.get("human_action"):
            agree += 1
        if str(o.get("risk_level") or "").lower() == "high" and o.get("agent_action") != o.get("human_action"):
            high_risk += 1
    if total == 0:
        return "insufficient_data"
    rate = agree / total
    if high_risk > 0:
        return "stay_shadow"
    if rate >= 0.97:
        return "limited_expand"
    if rate >= 0.95:
        return "stay_shadow"
    return "stay_shadow"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    ap.add_argument("--window", type=int, default=50)
    args = ap.parse_args()
    print(evaluate(args.log, window=args.window))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
