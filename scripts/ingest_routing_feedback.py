#!/usr/bin/env python3
"""Normalize operator `routing:` one-liners to JSONL (append-only).

Reads stdin or file paths. Does not edit YAML — human applies config changes.

Usage:
  echo 'routing:wrong_profile:latin:mediterranean' | python3 scripts/ingest_routing_feedback.py
  python3 scripts/ingest_routing_feedback.py feedback.txt

Output: appends to artifacts/skill-work/work-civ-mem/routing-feedback.jsonl
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "artifacts" / "skill-work" / "work-civ-mem" / "routing-feedback.jsonl"

ROUTING_LINE = re.compile(
    r"^routing:(wrong_profile|missing_keyword|seed_bad|seed_good|civ_order|upstream):(.+)$"
)


def _parse_line(line: str) -> dict | None:
    line = line.strip()
    if not line.startswith("routing:"):
        return None
    m = ROUTING_LINE.match(line)
    if not m:
        return {"raw": line, "parse": "partial"}
    action, rest = m.group(1), m.group(2)
    return {"action": action, "payload": rest, "raw": line}


def main() -> int:
    lines: list[str] = []
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            lines.extend(Path(path).read_text(encoding="utf-8").splitlines())
    else:
        lines = sys.stdin.read().splitlines()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    n = 0
    with OUT.open("a", encoding="utf-8") as f:
        for line in lines:
            rec = _parse_line(line)
            if rec is None:
                continue
            row = {"ts": ts, **rec}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    print(f"Appended {n} row(s) to {OUT.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
