#!/usr/bin/env python3
"""Promote an accepted self-proposal artifact into the canonical gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SELF_PROPOSALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SELF_PROPOSALS_DIR.parents[1]
SHARED_DIR = REPO_ROOT / "auto-research" / "_shared"

if str(SELF_PROPOSALS_DIR) not in sys.path:
    sys.path.insert(0, str(SELF_PROPOSALS_DIR))
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from artifact_promotion import build_promoted_candidate_block, promote_artifact_to_gate


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote an accepted self-proposal artifact into recursion-gate.md")
    parser.add_argument(
        "--artifact",
        type=Path,
        required=True,
        help="Accepted artifact JSON",
    )
    parser.add_argument("--user", "-u", default="grace-mar", help="User id (default: grace-mar)")
    parser.add_argument("--dry-run", action="store_true", help="Print the candidate block without writing the gate")
    parser.add_argument(
        "--review-note",
        default="",
        help="Required when writing to the gate; records the operator's reason for promotion",
    )
    args = parser.parse_args()

    try:
        result = promote_artifact_to_gate(
            args.artifact,
            user_id=args.user,
            review_note=args.review_note.strip(),
            dry_run=args.dry_run,
            lane_name="self-proposals",
            candidate_source="auto-research/self-proposals",
        )
    except ValueError as exc:
        raise SystemExit(str(exc))

    if args.dry_run:
        print(result["candidate_block"])
        return 0

    print(f"{result['gate_path']}: inserted {result['candidate_id']} from {result['artifact_relpath']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
