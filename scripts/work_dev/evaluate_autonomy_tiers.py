#!/usr/bin/env python3
"""Summarize shadow JSONL and emit stay_shadow | limited_expand | insufficient_data.

Thresholds load from docs/skill-work/work-dev/autonomy/tier_thresholds.yaml (BUILD-AI-GAP-007).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_LOG = REPO_ROOT / "runtime" / "autonomy" / "shadow_decisions.jsonl"
DEFAULT_THRESHOLDS = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "autonomy" / "tier_thresholds.yaml"


def load_tier_config(thresholds_path: Path, profile: str) -> dict[str, Any]:
    raw = yaml.safe_load(thresholds_path.read_text(encoding="utf-8")) or {}
    tiers = raw.get("tiers") or {}
    if profile not in tiers:
        known = ", ".join(sorted(tiers)) or "(none)"
        raise KeyError(f"unknown tier profile {profile!r}; known: {known}")
    cfg = tiers[profile]
    return {
        "min_agreement_rate": float(cfg["min_agreement_rate"]),
        "max_high_risk_violations_in_window": int(cfg["max_high_risk_violations_in_window"]),
        "window_cases": int(cfg["window_cases"]),
    }


def evaluate(
    log_path: Path,
    *,
    window: int | None = None,
    profile: str = "low_risk_staging_suggestions",
    thresholds_path: Path | None = None,
) -> str:
    path = thresholds_path or DEFAULT_THRESHOLDS
    cfg = load_tier_config(path, profile)
    effective_window = int(window if window is not None else cfg["window_cases"])

    if not log_path.is_file():
        return "insufficient_data"
    raw_lines = [ln.strip() for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    lines = raw_lines[-effective_window:]
    if len(lines) < 5:
        return "insufficient_data"

    agree = 0
    high_risk_violations = 0
    total = 0
    for ln in lines:
        try:
            o = json.loads(ln)
        except json.JSONDecodeError:
            continue
        total += 1
        if o.get("agent_action") == o.get("human_action"):
            agree += 1
        hr = str(o.get("risk_level") or "").lower() == "high"
        if hr and o.get("agent_action") != o.get("human_action"):
            high_risk_violations += 1

    if total == 0:
        return "insufficient_data"

    if high_risk_violations > cfg["max_high_risk_violations_in_window"]:
        return "stay_shadow"

    rate = agree / total
    if rate >= cfg["min_agreement_rate"]:
        return "limited_expand"
    return "stay_shadow"


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate autonomy tier from shadow JSONL.")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    ap.add_argument(
        "--window",
        type=int,
        default=None,
        help="Last N lines (default: window_cases from tier profile)",
    )
    ap.add_argument(
        "--profile",
        default="low_risk_staging_suggestions",
        help="Key under tiers: in tier_thresholds.yaml",
    )
    ap.add_argument(
        "--thresholds",
        type=Path,
        default=DEFAULT_THRESHOLDS,
        help="Path to tier_thresholds.yaml",
    )
    args = ap.parse_args()
    print(
        evaluate(
            args.log,
            window=args.window,
            profile=args.profile,
            thresholds_path=args.thresholds,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
