#!/usr/bin/env python3
"""
Filter a manual job JSON list by keywords (substring match on title, company, notes, skill_tags).

No network. Default keywords align with agentic / eval / guardrail discourse; override with --keywords-file (one keyword per line, # comments ok).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_KEYWORDS = (
    "agentic",
    "evaluation",
    "eval harness",
    "failure",
    "guardrail",
    "multi-agent",
    "context",
    "token",
    "reliability",
    "llm",
    "machine learning",
    "ai engineer",
    "ai reliability",
    "anthropic",
    "openai",
)


def load_keywords(path: Path | None) -> list[str]:
    if path is None:
        return list(DEFAULT_KEYWORDS)
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s.lower())
    return out if out else list(DEFAULT_KEYWORDS)


def job_text(job: dict) -> str:
    parts = [
        str(job.get("title", "")),
        str(job.get("company", "")),
        str(job.get("notes", "")),
        " ".join(job.get("skill_tags") or []),
    ]
    return " ".join(parts).lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter manual job JSON by keywords.")
    parser.add_argument("--input", type=Path, required=True, help="JSON array of jobs")
    parser.add_argument("--keywords-file", type=Path, default=None, help="One keyword per line")
    parser.add_argument("--min-matches", type=int, default=1, help="Min keyword hits per job")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"Missing: {args.input}", file=sys.stderr)
        return 2

    try:
        jobs = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(jobs, list):
        print("JSON root must be an array", file=sys.stderr)
        return 2

    kws = load_keywords(args.keywords_file)
    matched = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        text = job_text(job)
        hits = sum(1 for k in kws if k in text)
        if hits >= args.min_matches:
            matched.append((hits, job))

    matched.sort(key=lambda x: -x[0])
    for hits, job in matched:
        title = job.get("title", "?")
        company = job.get("company", "?")
        url = job.get("url", "")
        print(f"{hits}\t{title}\t{company}\t{url}")

    print(f"# {len(matched)} / {len(jobs)} jobs matched", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
