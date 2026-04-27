#!/usr/bin/env python3
"""Preflight checker for recursion-gate merge readiness.

Focuses on failure modes observed in bookshelf MCQ -> IX-A flows:
- placeholder suggested_entry
- missing IX-A scaffold in self.md
- missing topic anchor in source_exchange for IX-A candidates
- methodology-style wording in IX-A suggested_entry
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from gate_block_parser import pending_candidates_region, iter_candidate_yaml_blocks

PLACEHOLDER_RE = re.compile(r"see source_exchange\.operator \(staged paste\)", re.IGNORECASE)
TOPIC_HINT_RE = re.compile(
    r"(\b\d{3,4}\s*(BCE|CE)?\b|Westphalia|Tanzimat|Fort Sumter|Barbarossa|Marathon|Qing|Ottoman|Decolonization|WWI|World War I)",
    re.IGNORECASE,
)
METHOD_RE = re.compile(r"\b(method|workflow|process|how i work|curation as method|extraction channel)\b", re.IGNORECASE)


def yaml_get(body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", body, re.MULTILINE)
    return (m.group(1).strip().strip('"').strip("'")) if m else ""


def has_ix_a_scaffold(self_md: str) -> bool:
    pat = re.compile(r"#### Facts \(LEARN-nnn\)\s*\n\n```yaml\nentries:\s*\n", re.DOTALL)
    return bool(pat.search(self_md))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero when any blocker exists")
    args = ap.parse_args()

    gate_path = REPO / "users" / args.user / "recursion-gate.md"
    self_path = REPO / "users" / args.user / "self.md"
    if not gate_path.is_file():
        print(f"ERROR: missing gate file: {gate_path}")
        return 1
    if not self_path.is_file():
        print(f"ERROR: missing self file: {self_path}")
        return 1

    gate = gate_path.read_text(encoding="utf-8")
    self_md = self_path.read_text(encoding="utf-8")

    blockers: list[str] = []
    warnings: list[str] = []

    if not has_ix_a_scaffold(self_md):
        blockers.append("self.md IX-A scaffold missing `Facts (LEARN-nnn)` entries block")

    region = pending_candidates_region(gate)
    pending = list(iter_candidate_yaml_blocks(region))
    if not pending:
        print("ok: no pending candidates in gate")
        return 0

    for cid, title, body in pending:
        profile_target = yaml_get(body, "profile_target").upper()
        suggested = yaml_get(body, "suggested_entry")

        if not suggested:
            blockers.append(f"{cid}: missing suggested_entry")
        elif PLACEHOLDER_RE.search(suggested):
            blockers.append(f"{cid}: placeholder suggested_entry")

        if "IX-A" in profile_target:
            if not TOPIC_HINT_RE.search(body):
                warnings.append(f"{cid}: IX-A candidate has weak/absent explicit topic anchor")
            if METHOD_RE.search(suggested):
                blockers.append(f"{cid}: IX-A suggested_entry appears methodology-framed")

    print(f"pending candidates checked: {len(pending)}")
    if warnings:
        print("warnings:")
        for w in warnings:
            print(f"- {w}")
    if blockers:
        print("blockers:")
        for b in blockers:
            print(f"- {b}")
        return 1 if args.strict else 0

    print("ok: pending candidates pass merge-readiness checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
