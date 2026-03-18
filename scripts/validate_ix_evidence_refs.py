#!/usr/bin/env python3
"""
Warn if SELF IX entries reference missing ACT-* or READ-* in self-evidence.md.

Non-blocking: exit 0. Run manually or from CI as advisory.

  python3 scripts/validate_ix_evidence_refs.py -u grace-mar
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _ix_yaml_blocks(self_md: str) -> list[str]:
    out: list[str] = []
    for m in re.finditer(
        r"### IX-[ABC]\..*?```yaml\n(.*?)```", self_md, re.DOTALL | re.IGNORECASE
    ):
        out.append(m.group(1))
    return out


def _collect_ids(yaml_chunk: str, key: str) -> set[str]:
    found: set[str] = set()
    for m in re.finditer(rf"^\s*{re.escape(key)}:\s*(\S+)\s*$", yaml_chunk, re.MULTILINE):
        val = m.group(1).strip().strip('"').strip("'")
        if val and val.lower() not in ("null", "none"):
            found.add(val)
    return found


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-u", "--user", default="grace-mar", help="users/<id>/")
    args = p.parse_args()
    base = REPO / "users" / args.user
    self_path = base / "self.md"
    ev_path = base / "self-evidence.md"
    if not self_path.is_file():
        print(f"skip: missing {self_path}", file=sys.stderr)
        return 0
    self_content = self_path.read_text(encoding="utf-8", errors="replace")
    ev_content = ev_path.read_text(encoding="utf-8", errors="replace") if ev_path.is_file() else ""

    act_ids = set(re.findall(r"\b(ACT-\d+)\b", ev_content))
    read_uc = {m.group(1).upper() for m in re.finditer(r"\b(READ-[\w-]+)\b", ev_content, re.I)}

    warnings = 0
    for block in _ix_yaml_blocks(self_content):
        for eid in _collect_ids(block, "evidence_id"):
            if eid.startswith("ACT-") and eid not in act_ids:
                print(f"WARN: IX entry references {eid} not found in self-evidence.md")
                warnings += 1
        for rid in _collect_ids(block, "intake_evidence_id"):
            if rid.upper().startswith("READ-") and rid.upper() not in read_uc:
                print(
                    f"WARN: IX intake_evidence_id {rid} not found as READ-* in self-evidence.md"
                )
                warnings += 1

    if warnings == 0:
        print("IX evidence refs: OK (no missing ACT/READ pointers in scanned IX blocks).")
    else:
        print(f"IX evidence refs: {warnings} warning(s) — see docs/we-read-think-self-pipeline.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
