#!/usr/bin/env python3
"""
Append one strategy-notebook fold event to users/<id>/strategy-fold-events.jsonl.

WORK-only ledger — not Record, not MEMORY. See docs/skill-work/work-strategy/strategy-notebook/FOLD-LEARNING.md.

Usage:
  python3 scripts/log_strategy_fold.py -u grace-mar --notebook-date 2026-04-13 --fold-kind manual
  python3 scripts/log_strategy_fold.py -u grace-mar --notebook-date 2026-04-13 --fold-kind dream \\
    --inbox-chars 12000 --days-delta-chars 4200 --note "merged Parsi cluster"
  python3 scripts/log_strategy_fold.py -u grace-mar --notebook-date 2026-04-13 --fold-kind manual \\
    --ratings verify_depth=2,judgment_freshness=3 --would-reread --auto-git
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir  # noqa: E402

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FOLD_KINDS = frozenset({"manual", "dream", "explicit"})
LEDGER_NAME = "strategy-fold-events.jsonl"
NOTE_MAX = 200


def default_jsonl_path(user_id: str) -> Path:
    return profile_dir(user_id) / LEDGER_NAME


def parse_ratings(s: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in s.split(","):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, _, v = part.partition("=")
        k = k.strip()
        v = v.strip()
        if k not in ("verify_depth", "judgment_freshness"):
            raise ValueError(f"unknown rating key: {k}")
        n = int(v)
        if n < 1 or n > 3:
            raise ValueError(f"{k} must be 1–3, got {n}")
        out[k] = n
    return out


def parse_counts_json(s: str) -> dict[str, int]:
    raw = json.loads(s)
    if not isinstance(raw, dict):
        raise ValueError("counts JSON must be an object")
    out: dict[str, int] = {}
    for k, v in raw.items():
        if not isinstance(k, str):
            raise ValueError("counts keys must be strings")
        if not isinstance(v, int) or isinstance(v, bool):
            raise ValueError(f"counts[{k}] must be int")
        out[k] = v
    return out


def git_head_sha(repo: Path) -> str | None:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if p.returncode != 0 or not p.stdout.strip():
            return None
        return p.stdout.strip()[:40]
    except OSError:
        return None


def append_event(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument("--notebook-date", required=True, help="YYYY-MM-DD (target ## in days.md)")
    ap.add_argument("--fold-kind", required=True, choices=sorted(FOLD_KINDS))
    ap.add_argument("--jsonl", type=Path, default=None, help="Override ledger path (default: users/<id>/strategy-fold-events.jsonl)")
    ap.add_argument("--inbox-chars", type=int, default=None, metavar="N")
    ap.add_argument("--days-delta-chars", type=int, default=None, metavar="N")
    ap.add_argument("--counts-json", default="", help='JSON object, e.g. \'{"signal_bullets":3,"judgment_bullets":2}\'')
    ap.add_argument("--ratings", default="", help="verify_depth=2,judgment_freshness=3")
    ap.add_argument("--would-reread", action=argparse.BooleanOptionalAction, default=None)
    ap.add_argument("--note", default="", help="Max 200 chars")
    ap.add_argument("--git-ref", default="", help="Commit SHA (optional)")
    ap.add_argument("--auto-git", action="store_true", help="Set git_ref from git rev-parse HEAD")
    args = ap.parse_args()
    uid = args.user.strip()
    nd = args.notebook_date.strip()
    if not DATE_RE.match(nd):
        print("error: --notebook-date must be YYYY-MM-DD", file=sys.stderr)
        return 2

    path = args.jsonl if args.jsonl is not None else default_jsonl_path(uid)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    event: dict = {
        "ts": ts,
        "notebook_date": nd,
        "fold_kind": args.fold_kind,
    }
    if args.inbox_chars is not None:
        if args.inbox_chars < 0:
            print("error: --inbox-chars must be >= 0", file=sys.stderr)
            return 2
        event["inbox_chars"] = args.inbox_chars
    if args.days_delta_chars is not None:
        event["days_delta_chars"] = args.days_delta_chars
    if args.counts_json.strip():
        try:
            event["counts"] = parse_counts_json(args.counts_json.strip())
        except (json.JSONDecodeError, ValueError) as e:
            print(f"error: --counts-json: {e}", file=sys.stderr)
            return 2
    if args.ratings.strip():
        try:
            r = parse_ratings(args.ratings.strip())
            if r:
                event["ratings"] = r
        except ValueError as e:
            print(f"error: --ratings: {e}", file=sys.stderr)
            return 2
    if args.would_reread is not None:
        event["would_reread"] = args.would_reread
    if args.note.strip():
        note = args.note.strip().replace("\n", " ")[:NOTE_MAX]
        event["note"] = note
    git_ref = args.git_ref.strip()
    if args.auto_git and not git_ref:
        git_ref = git_head_sha(REPO_ROOT) or ""
    if git_ref:
        event["git_ref"] = git_ref[:40]

    append_event(path, event)
    try:
        disp = path.relative_to(REPO_ROOT)
    except ValueError:
        disp = path
    print(disp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
