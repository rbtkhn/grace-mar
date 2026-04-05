#!/usr/bin/env python3
"""
Print a human-readable Markdown-oriented summary of a Change Proposal v1 JSON file.

This is a light operator view only. For structured before/after diffs, use
scripts/generate-identity-diff.py with an identity-diff JSON artifact.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Change Proposal v1 as plain-text summary.")
    parser.add_argument("proposal", help="Path to proposal JSON")
    args = parser.parse_args()

    path = Path(args.proposal)
    if not path.is_file():
        print(f"ERROR: not a file: {path}", file=sys.stderr)
        return 1

    proposal = json.loads(path.read_text(encoding="utf-8"))

    print("# Proposal summary")
    print(f"- **proposalId:** {proposal.get('proposalId')}")
    print(f"- **userSlug:** {proposal.get('userSlug')}")
    print(f"- **status:** {proposal.get('status')}")
    print(f"- **primaryScope:** {proposal.get('primaryScope')}")
    sec = proposal.get("secondaryScopes") or []
    if sec:
        print(f"- **secondaryScopes:** {', '.join(sec)}")
    print(f"- **changeType:** {proposal.get('changeType')}")
    print(f"- **targetSurface:** {proposal.get('targetSurface')}")
    print(f"- **materiality:** {proposal.get('materiality')}")
    print(f"- **reviewType:** {proposal.get('reviewType')}")
    print(f"- **queueSummary:** {proposal.get('queueSummary')}")
    notes = proposal.get("notes")
    if notes:
        print(f"- **notes:** {notes}")
    print(f"- **priorStateRef:** {proposal.get('priorStateRef')}")
    print(f"- **proposedStateRef:** {proposal.get('proposedStateRef')}")
    ev = proposal.get("supportingEvidence") or []
    print("- **supportingEvidence:**")
    for item in ev:
        print(
            f"  - ({item.get('type')}) {item.get('ref')}: {item.get('summary')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
