#!/usr/bin/env python3
"""
Rough blended token cost estimate for planning (not billing).

Prices drift constantly — maintain a local JSON config copied from
token_economics_models.example.json. See docs/skill-work/work-dev/economic-benchmarks.md.

Complements emit_compute_ledger.py (actual usage) with what-if math.

Usage:
  cp scripts/token_economics_models.example.json scripts/token_economics_models.json
  python3 scripts/token_economics.py --tokens 50000000 --config scripts/token_economics_models.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "token_economics_models.json"


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def estimate_blended_cost(
    total_tokens: int,
    models: dict[str, dict],
    weights: dict[str, float],
) -> tuple[float, list[tuple[str, float, float]]]:
    """Return (total_usd, [(model_id, weight, usd_share), ...])."""
    lines: list[tuple[str, float, float]] = []
    total_usd = 0.0
    wsum = sum(weights.values())
    if wsum <= 0:
        raise ValueError("weights must sum to a positive number")
    for mid, w in weights.items():
        if mid not in models:
            raise KeyError(f"weight references unknown model: {mid}")
        usd_per_mtok = float(models[mid]["usd_per_million_tokens"])
        frac = w / wsum
        share_tokens = total_tokens * frac
        usd = (share_tokens / 1_000_000.0) * usd_per_mtok
        lines.append((mid, frac, usd))
        total_usd += usd
    return total_usd, lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate blended token cost from a JSON model table.")
    parser.add_argument("--tokens", type=int, required=True, help="Total tokens for the task (rough).")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG if DEFAULT_CONFIG.is_file() else None,
        help=f"JSON config (default: {DEFAULT_CONFIG} if it exists)",
    )
    args = parser.parse_args()
    if args.config is None:
        print(
            "No config found. Copy scripts/token_economics_models.example.json to "
            "scripts/token_economics_models.json and set prices, or pass --config.",
            file=sys.stderr,
        )
        return 2
    cfg = load_config(args.config)
    models = {k: v for k, v in cfg.get("models", {}).items() if not str(k).startswith("_")}
    weights = cfg.get("weights") or {}
    if not models or not weights:
        print("Config must include non-empty 'models' and 'weights'.", file=sys.stderr)
        return 2
    total, lines = estimate_blended_cost(args.tokens, models, weights)
    for mid, frac, usd in lines:
        print(f"{mid}: weight={frac:.4f}  ~${usd:.4f}")
    print(f"Total estimated: ${total:.4f} (for {args.tokens:,} tokens, blended)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
