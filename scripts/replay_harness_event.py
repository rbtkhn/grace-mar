#!/usr/bin/env python3
"""
Harness Event Replay — correlate audit-lane JSONL + gate YAML for a candidate or bundle.

Does not reconstruct full LLM prompts unless logged elsewhere. See docs/harness-replay.md.
Implementation: grace_mar.replay (loaders use profile root with runtime-bundle fallback).

  python scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0089
  python scripts/replay_harness_event.py -u grace-mar --bundle-id abc123
  python scripts/replay_harness_event.py -u grace-mar --event-id evt_20260320_120000_a1b2c3d4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

try:
    from repo_io import profile_dir
except ImportError:
    from scripts.repo_io import profile_dir

from grace_mar.replay.report import build_report


def main() -> int:
    ap = argparse.ArgumentParser(description="Replay harness/pipeline audit context for a candidate or bundle.")
    ap.add_argument("-u", "--user", default="grace-mar", help="User id")
    ap.add_argument("--candidate", default="", help="CANDIDATE-nnnn")
    ap.add_argument("--bundle-id", default="", help="Harness bundle_id")
    ap.add_argument(
        "--event-id",
        default="",
        help="Single pipeline event_id (evt_…); optional candidate follow-on from row",
    )
    ap.add_argument("--evidence", default="", metavar="ACT-nnnn", help="Optional: show hint line from self-archive.md")
    ap.add_argument(
        "--transcript-snippet",
        action="store_true",
        help="Append tail of session-transcript.md (runtime; may be large)",
    )
    ap.add_argument("-o", "--output", default="", help="Write markdown to this path")
    args = ap.parse_args()
    if not args.candidate.strip() and not args.bundle_id.strip() and not args.event_id.strip():
        print("Provide --candidate, --bundle-id, or --event-id", file=sys.stderr)
        return 1
    user_dir = profile_dir(args.user.strip())
    text = build_report(
        user_dir,
        candidate_id=args.candidate.strip(),
        bundle_id=args.bundle_id.strip(),
        event_id=args.event_id.strip(),
        evidence_id=args.evidence.strip(),
        transcript_snippet=args.transcript_snippet,
    )
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
