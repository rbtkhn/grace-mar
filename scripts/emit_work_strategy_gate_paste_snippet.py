#!/usr/bin/env python3
"""
Emit a canonical ### CANDIDATE-* snippet for work-strategy milestones (RECURSION-GATE paste).

Default rows match existing gate convention: territory: work-politics, channel_key: operator:work-strategy.
Writes users/<user>/recursion-gate-staging/work-strategy-<date>.paste-snippet.md.
See docs/skill-work/work-strategy/LANE-CI.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stage_gate_candidate import next_candidate_id  # noqa: E402

DEFAULT_USER = "grace-mar"


def build_snippet(
    *,
    user_id: str,
    ts_date: str,
    ts_full: str,
    channel_key: str,
    territory: str,
    summary: str,
) -> str:
    gate_path = REPO_ROOT / "users" / user_id / "recursion-gate.md"
    content = (
        gate_path.read_text(encoding="utf-8")
        if gate_path.is_file()
        else "## Candidates\n\n## Processed\n"
    )
    cid = next_candidate_id(content)
    safe_summary = '"' + summary.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return "\n".join(
        [
            f"<!-- work-strategy gate paste — {ts_date} — next id from gate -->",
            "",
            f"### {cid} (work-strategy)",
            "```yaml",
            "status: pending",
            f"timestamp: {ts_full}",
            f"channel_key: {channel_key}",
            f"territory: {territory}",
            "mind_category: knowledge",
            "signal_type: pol_milestone",
            "priority_score: 6",
            f"summary: {safe_summary}",
            "```",
            "",
            "_Add source, source_exchange, suggested_entry, profile_target per docs/skill-work/work-politics/pol-candidate-template.md if using work-politics channel_key bucket._",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument(
        "--channel-key",
        default="operator:work-strategy",
        help="Default: operator:work-strategy (see LANE-CI.md)",
    )
    ap.add_argument(
        "--territory",
        default="work-politics",
        help="Default: work-politics (WAP bucket + operator:work-strategy channel; override to companion if needed)",
    )
    ap.add_argument(
        "--summary",
        default="work-strategy milestone — edit YAML before pasting into recursion-gate.md.",
    )
    ap.add_argument("--staging-dir", type=Path, default=None)
    args = ap.parse_args()
    uid = args.user.strip() or DEFAULT_USER
    now = datetime.now(timezone.utc)
    ts_date = now.strftime("%Y-%m-%d")
    ts_full = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    out_dir = args.staging_dir or (REPO_ROOT / "users" / uid / "recursion-gate-staging")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"work-strategy-{ts_date}.paste-snippet.md"
    path.write_text(
        build_snippet(
            user_id=uid,
            ts_date=ts_date,
            ts_full=ts_full,
            channel_key=args.channel_key.strip(),
            territory=args.territory.strip(),
            summary=args.summary.strip(),
        ),
        encoding="utf-8",
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
