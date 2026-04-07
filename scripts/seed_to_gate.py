#!/usr/bin/env python3
"""
Convert a promotion-ready seed claim into a RECURSION-GATE candidate YAML block.

Instance-specific (grace-mar only). Not template-portable.

Usage:
  python3 scripts/seed_to_gate.py --seed-id seed-demo-005
  python3 scripts/seed_to_gate.py --seed-id seed-demo-005 --append
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = "grace-mar"


def _load_latest(user_id: str) -> dict[str, dict[str, Any]]:
    path = REPO_ROOT / "users" / user_id / "seed-registry.jsonl"
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            sid = row.get("seed_id", "")
            if sid:
                latest[sid] = row
        except json.JSONDecodeError:
            continue
    return latest


_CATEGORY_TO_IX = {
    "identity": "IX-C",
    "curiosity": "IX-B",
    "pedagogy": "IX-A",
    "expression": "IX-C",
    "memory_governance": "IX-A",
    "safety": "IX-A",
    "preference": "IX-C",
}


def seed_to_gate_yaml(claim: dict[str, Any], candidate_id: str) -> str:
    """Generate a RECURSION-GATE candidate YAML block from a seed claim."""
    ix_target = _CATEGORY_TO_IX.get(claim.get("category", ""), "IX-A")

    sources_str = ", ".join(claim.get("source_events", [])[:5])
    contradiction_note = ""
    if claim.get("contradiction_count", 0) > 0:
        refs = ", ".join(claim.get("contradiction_refs", []))
        contradiction_note = f"\nnote: Contradictions ({claim['contradiction_count']}): {refs}. Review before merging."

    return textwrap.dedent(f"""\
        ### {candidate_id} (Seed promotion — {claim['claim_text'][:60]})

        ```yaml
        status: pending
        timestamp: {claim.get('last_seen', '')[:10]}
        channel_key: operator:seed-registry
        source: seed-registry promotion ({claim['seed_id']})
        source_exchange:
          - "{claim.get('claim_text', '')}"
        mind_category: {claim.get('category', '')}
        target: {ix_target}
        summary: "Seed claim promoted after {claim.get('observation_count', 0)} observations over {_span_desc(claim)}, recurrence={claim.get('recurrence_score', 0):.2f}, confidence={claim.get('confidence', 0):.2f}."
        provenance: seed_registry
        seed_id: {claim['seed_id']}
        source_events: [{sources_str}]
        sensitivity: {claim.get('sensitivity', 'standard')}{contradiction_note}
        ```
    """)


def _span_desc(claim: dict[str, Any]) -> str:
    from datetime import datetime
    try:
        fs = datetime.fromisoformat(claim.get("first_seen", ""))
        ls = datetime.fromisoformat(claim.get("last_seen", ""))
        days = (ls - fs).days
        return f"{days} days"
    except (ValueError, TypeError):
        return "unknown span"


def _next_candidate_id(gate_text: str) -> str:
    import re
    ids = re.findall(r"CANDIDATE-(\d+)", gate_text)
    if ids:
        max_id = max(int(i) for i in ids)
        return f"CANDIDATE-{max_id + 1:04d}"
    return "CANDIDATE-0100"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a seed claim to a RECURSION-GATE candidate.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--seed-id", required=True, help="Seed claim ID to promote")
    parser.add_argument("--append", action="store_true",
                        help="Append to recursion-gate.md (above ## Processed)")
    parser.add_argument("--candidate-id", help="Override candidate ID")
    args = parser.parse_args()

    latest = _load_latest(args.user)
    if args.seed_id not in latest:
        print(f"Seed claim {args.seed_id} not found.", file=sys.stderr)
        return 1

    claim = latest[args.seed_id]
    if claim.get("status") in ("promoted", "rejected", "expired"):
        print(f"Seed claim {args.seed_id} is already {claim['status']}.", file=sys.stderr)
        return 1

    gate_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"
    if args.candidate_id:
        cid = args.candidate_id
    elif gate_path.exists():
        cid = _next_candidate_id(gate_path.read_text(encoding="utf-8"))
    else:
        cid = "CANDIDATE-0100"

    yaml_block = seed_to_gate_yaml(claim, cid)

    if args.append:
        if not gate_path.exists():
            print("recursion-gate.md not found.", file=sys.stderr)
            return 1
        text = gate_path.read_text(encoding="utf-8")
        marker = "## Processed"
        if marker not in text:
            print(f"'{marker}' section not found in gate file.", file=sys.stderr)
            return 1
        text = text.replace(marker, yaml_block + "\n" + marker)
        gate_path.write_text(text, encoding="utf-8")
        print(f"Appended {cid} (from {args.seed_id}) to recursion-gate.md")
    else:
        print(yaml_block)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
