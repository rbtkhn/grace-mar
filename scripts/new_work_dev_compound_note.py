#!/usr/bin/env python3
"""
Create a new work-dev compound note from the compound note template.
Does not write to any canonical Record surface. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "compound-notes"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "compound-note"


def _yaml_list(paths: list[str], indent: str) -> str:
    if not paths:
        return "[]"
    return "\n" + "\n".join(f"{indent}- {p}" for p in paths)


def _bool_yaml(b: bool) -> str:
    return "true" if b else "false"


def _yaml_dq(s: str) -> str:
    """Double-quoted YAML scalar, minimal escaping."""
    if not s:
        return '""'
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_note(
    title: str,
    *,
    note_date: str,
    source_pr: str,
    source_commit: str,
    problem_type: str,
    reusable_pattern: str,
    gate_candidate: bool,
    affected_files: list[str],
) -> str:
    if not affected_files:
        af_line = "affected_files: []"
    else:
        af_line = "affected_files:" + _yaml_list(affected_files, "  ")

    return f"""---
date: {note_date}
work_lane: work-dev
title: {_yaml_dq(title)}
source_pr: {_yaml_dq(source_pr)}
source_commit: {_yaml_dq(source_commit)}
{af_line}
problem_type: {_yaml_dq(problem_type)}
reusable_pattern: {_yaml_dq(reusable_pattern)}
self_catching_test: unknown
gate_candidate: {_bool_yaml(gate_candidate)}
record_status: work-only
---

# Compound Note: {title}

## Context



## What happened



## Reusable lesson



## Failure pattern



## Self-catching test

Would the current Grace-Mar system catch this issue next time?

Choose one:

- yes
- no
- only-if-invoked-manually
- only-after-gate-promotion
- unclear

## Candidate follow-up



## Gate recommendation

No gate action by default. This remains a work-only learning artifact unless explicitly staged.

"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create a new work-dev compound note under docs/skill-work/work-dev/compound-notes/"
    )
    ap.add_argument("--title", required=True, help="Title for the note and filename slug")
    ap.add_argument("--date", default="", help="YYYY-MM-DD (default: today, local date)")
    ap.add_argument("--source-pr", default="", help="Source PR reference")
    ap.add_argument("--source-commit", default="", help="Source commit")
    ap.add_argument("--problem-type", default="", help="Problem type tag")
    ap.add_argument("--reusable-pattern", default="", help="Reusable pattern tag")
    ap.add_argument(
        "--gate-candidate",
        action="store_true",
        help="Set gate_candidate true (default: false)",
    )
    ap.add_argument(
        "--affected-file",
        action="append",
        default=[],
        help="File path (repeatable)",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite if the target file already exists",
    )
    args = ap.parse_args()

    title = args.title.strip()
    if not title:
        print("error: --title must be non-empty", file=sys.stderr)
        return 1

    if args.date:
        d = args.date.strip()
    else:
        d = date.today().isoformat()

    slug = _slugify(title)
    out_name = f"{d}-{slug}.md"
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = NOTES_DIR / out_name

    if out_path.is_file() and not args.force:
        print(
            f"error: {out_path} already exists (use --force to overwrite)",
            file=sys.stderr,
        )
        return 1

    # YAML title: if contains special chars, use quoted form; keep simple
    body = build_note(
        title,
        note_date=d,
        source_pr=args.source_pr.strip(),
        source_commit=args.source_commit.strip(),
        problem_type=args.problem_type.strip(),
        reusable_pattern=args.reusable_pattern.strip(),
        gate_candidate=bool(args.gate_candidate),
        affected_files=[x.strip() for x in (args.affected_file or []) if x.strip()],
    )
    out_path.write_text(body, encoding="utf-8", newline="\n")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
