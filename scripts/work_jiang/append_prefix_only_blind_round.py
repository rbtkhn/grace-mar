#!/usr/bin/env python3
"""Append one round section to prefix-only BLIND + one JSONL line.

Usage:
  python3 scripts/work_jiang/append_prefix_only_blind_round.py '<json-object>'
  # stdin: markdown body for the round (no trailing marker)

Operator lane; not CI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLIND = (
    ROOT
    / "research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND-prefix-only.md"
)
JSONL = (
    ROOT
    / "research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain-blind-prefix-only.jsonl"
)
MARKER = "<!-- END_ROUNDS -->"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: append_prefix_only_blind_round.py '<json>' <stdin markdown>")
    row = json.loads(sys.argv[1])
    md = sys.stdin.read()
    text = BLIND.read_text(encoding="utf-8")
    if MARKER not in text:
        sys.exit(f"error: {MARKER} not found in {BLIND}")
    text = text.replace(MARKER, md.strip() + "\n\n" + MARKER, 1)
    BLIND.write_text(text, encoding="utf-8")
    with JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
