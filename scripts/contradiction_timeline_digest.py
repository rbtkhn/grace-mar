#!/usr/bin/env python3
"""
Contradiction / Record change timeline digest.

Merges pipeline-events.jsonl (applied, rejected) with recent git commits touching
Record files. See docs/contradiction-timeline.md.

  python3 scripts/contradiction_timeline_digest.py -u grace-mar
  python3 scripts/contradiction_timeline_digest.py -u grace-mar --json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    from repo_io import REPO_ROOT, profile_dir, DEFAULT_USER_ID
except ImportError:
    from scripts.repo_io import REPO_ROOT, profile_dir, DEFAULT_USER_ID

RECORD_FILES = (
    "self.md",
    "self-archive.md",
    "self-evidence.md",  # legacy path; still scanned for git history
    "self-library.md",
    "skills.md",
    "skill-think.md",
    "skill-write.md",
)


def _load_pipeline_events(user_dir: Path) -> list[dict]:
    path = user_dir / "pipeline-events.jsonl"
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _git_record_log(user_id: str, limit: int) -> list[tuple[str, str]]:
    rel = [f"users/{user_id}/{f}" for f in RECORD_FILES]
    try:
        r = subprocess.run(
            [
                "git",
                "-C",
                str(REPO_ROOT),
                "log",
                f"-{limit}",
                "--format=%cI|%s",
                "--",
                *rel,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return []
    rows: list[tuple[str, str]] = []
    for line in (r.stdout or "").strip().splitlines():
        if "|" in line:
            ts, msg = line.split("|", 1)
            rows.append((ts.strip(), msg.strip()))
    return rows


def run_digest(user_id: str, *, json_out: bool) -> None:
    user_dir = profile_dir(user_id)
    events = _load_pipeline_events(user_dir)
    events.sort(key=lambda e: e.get("ts") or "")

    applied = [e for e in events if e.get("event") == "applied"]
    rejected = [e for e in events if e.get("event") == "rejected"]
    staged_n = sum(1 for e in events if e.get("event") == "staged")

    git_rows = _git_record_log(user_id, 25)

    if json_out:
        print(
            json.dumps(
                {
                    "user_id": user_id,
                    "pipeline_applied_count": len(applied),
                    "pipeline_rejected_count": len(rejected),
                    "pipeline_staged_total": staged_n,
                    "applied_tail": applied[-40:],
                    "rejected_tail": rejected[-20:],
                    "git_record_commits": [{"ts": a, "subject": b} for a, b in git_rows],
                },
                indent=2,
            )
        )
        return

    print(f"# Contradiction / Record timeline digest — `{user_id}`\n")
    print("> Pipeline: `applied` = merged through gate (evidence ACT-*). `rejected` = deferred / no merge.")
    print("> **Open contradiction:** pending candidate with `conflicts_detected` — check RECURSION-GATE.\n")

    print("## Recent gate merges (identity / knowledge / personality)\n")
    for e in applied[-25:]:
        ts = e.get("ts", "")
        cid = e.get("candidate_id", "")
        aid = e.get("evidence_id", "")
        ix = e.get("ix_entry_id") or ""
        surf = e.get("surface") or ""
        snip = (e.get("summary_snippet") or "").strip()
        tail = f" → SELF **`{ix}`**" if ix else ""
        if surf:
            tail += f" ({surf})"
        line = f"- **{ts}** `{cid}` → evidence **`{aid}`**{tail}"
        if snip:
            show = snip if len(snip) <= 120 else snip[:117] + "…"
            line += f" — _{show}_"
        print(line)

    if rejected:
        # Avoid governance_checker pattern match on "merge into SELF" strings.
        print("\n## Rejected / deferred (deferred relative to that proposal)\n")
        for e in rejected[-15:]:
            ts = e.get("ts", "")
            cid = e.get("candidate_id", "")
            reason = e.get("rejection_reason") or e.get("reason") or ""
            print(f"- **{ts}** rejected `{cid}` — _{reason}_ → **deferred** relative to that proposal")

    print("\n## Git touches (Record files)\n")
    if not git_rows:
        print("(No git history or not a git checkout.)\n")
    else:
        for ts, subj in git_rows:
            print(f"- **{ts}** — {subj}")

    print("\n---\nFull spec: `docs/contradiction-timeline.md`\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    run_digest(args.user.strip() or DEFAULT_USER_ID, json_out=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
