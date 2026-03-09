#!/usr/bin/env python3
"""
Calibrate-on-miss: stage a candidate when Voice missed or got something wrong.

When the companion reports "Voice didn't know X" or "that was wrong", run this
to create a candidate for the gated pipeline. Operator or companion reviews;
approval merges into Record.

Usage:
    python scripts/calibrate_from_miss.py -u grace-mar --miss "Voice didn't know we went to the aquarium"
    python scripts/calibrate_from_miss.py -u grace-mar --miss "Voice gave wrong info about Casa Bonita" --suggested "Add to IX-A: Casa Bonita reopened 2023, Trey and Matt bought it"
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _next_candidate_id(gate_path: Path) -> str:
    if not gate_path.exists():
        return "CANDIDATE-0001"
    content = gate_path.read_text(encoding="utf-8")
    ids = [int(m) for m in re.findall(r"CANDIDATE-(\d+)", content)]
    return f"CANDIDATE-{max(ids) + 1:04d}" if ids else "CANDIDATE-0001"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage a calibrate-from-miss candidate when Voice missed or was wrong"
    )
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID, help="User id")
    parser.add_argument("--miss", required=True, help="What Voice missed or got wrong")
    parser.add_argument(
        "--suggested",
        help="Optional: what to add to Record (IX-A, IX-B, or IX-C entry)",
    )
    parser.add_argument(
        "--mind",
        choices=["knowledge", "curiosity", "personality"],
        default="knowledge",
        help="Mind category (default: knowledge)",
    )
    args = parser.parse_args()

    user_dir = REPO_ROOT / "users" / args.user
    gate_path = user_dir / "recursion-gate.md"
    if not user_dir.exists() or not gate_path.exists():
        print(f"User dir or recursion-gate not found: {user_dir}", file=sys.stderr)
        return 1

    miss = (args.miss or "").strip()
    if not miss:
        print("--miss is required", file=sys.stderr)
        return 1

    suggested = (args.suggested or "").strip()
    if not suggested:
        suggested = f"Review and add entry for: {miss[:200]}"

    profile_target = {
        "knowledge": "IX-A. KNOWLEDGE",
        "curiosity": "IX-B. CURIOSITY",
        "personality": "IX-C. PERSONALITY",
    }[args.mind]

    candidate_id = _next_candidate_id(gate_path)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    miss_escaped = miss[:200].replace('"', "'").replace("\n", " ")
    block = f"""### {candidate_id} (Calibrate — Voice missed / was wrong)

```yaml
status: pending
timestamp: {ts}
channel_key: operator:calibrate_from_miss
source: calibrate_from_miss (Voice miss or error)
source_exchange:
  user: "Voice missed or was wrong: {miss_escaped}"
  grace_mar: "[Calibrate-from-miss: operator staging to close feedback loop]"
mind_category: {args.mind}
signal_type: calibrate_from_miss
priority_score: 4
summary: Calibrate — {miss[:80]}{"..." if len(miss) > 80 else ""}
profile_target: {profile_target}
suggested_entry: {suggested[:500]}
prompt_section: YOUR KNOWLEDGE
prompt_addition: |
  [Review suggested_entry — may need to merge into appropriate IX section]
```

"""
    content = gate_path.read_text(encoding="utf-8")
    insert_marker = "## Processed"
    idx = content.find(insert_marker)
    if idx >= 0:
        content = content[:idx] + block + "\n" + content[idx:]
    else:
        content = content + "\n" + block
    gate_path.write_text(content, encoding="utf-8")

    # Emit pipeline event
    subprocess.run(
        [
            sys.executable,
            REPO_ROOT / "scripts" / "emit_pipeline_event.py",
            "-u",
            args.user,
            "staged",
            candidate_id,
            "source=calibrate_from_miss",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    print(f"Staged {candidate_id}. Review in recursion-gate.md, approve or reject, then say 'approve'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
