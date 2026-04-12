#!/usr/bin/env python3
"""Preview which files each pending candidate will touch on merge.

Read-only — does not modify any files. Uses the same routing logic as
process_approved_candidates.merge_candidate_in_memory to predict impact
before approval.

Usage:
    python3 scripts/preview_candidate_impact.py -u grace-mar
    python3 scripts/preview_candidate_impact.py -u grace-mar --candidate CANDIDATE-0042
    python3 scripts/preview_candidate_impact.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
_SRC = REPO_ROOT / "src"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.merge.impact_preview import (
    format_impact_summary,
    preview_candidate_impact,
)
from recursion_gate_review import filter_review_candidates, parse_review_candidates


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    ap.add_argument("--candidate", default=None, help="Single candidate ID to preview")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")
    ap.add_argument("--status", default="pending", help="Filter by status (default: pending)")
    args = ap.parse_args()

    user_id = args.user.strip()
    rows = parse_review_candidates(user_id)
    filtered = filter_review_candidates(rows, status=args.status)

    if args.candidate:
        filtered = [r for r in filtered if r.get("id") == args.candidate]
        if not filtered:
            print(f"No candidate found: {args.candidate} (status={args.status})", file=sys.stderr)
            return 1

    previews = []
    for row in filtered:
        impact = preview_candidate_impact(row, user_id=user_id)
        previews.append(impact)

    if args.json:
        print(json.dumps(previews, indent=2))
    else:
        if not previews:
            print(f"No {args.status} candidates for {user_id}.")
            return 0
        print(f"Impact preview — {len(previews)} {args.status} candidate(s) for {user_id}\n")
        for p in previews:
            print(format_impact_summary(p))
            print(f"  files: {', '.join(p['files_touched'])}")
            if p["risk_factors"]:
                print(f"  risk:  {', '.join(p['risk_factors'])}")
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
