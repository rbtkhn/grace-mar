#!/usr/bin/env python3
"""
Merge a manually exported CSV of job rows into a single JSON list (dedupe by url).

No network. Expected CSV columns (header row, case-insensitive):
  title, company, url, source, date_added, notes, skill_tags, status

skill_tags may be comma-separated in one cell.

If --output already exists as a JSON array, new rows are appended and deduped by url.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

EXPECTED = ("title", "company", "url", "source", "date_added")


def _norm_url(u: str) -> str:
    u = (u or "").strip().lower()
    try:
        p = urlparse(u)
        return f"{p.netloc}{p.path}".rstrip("/")
    except Exception:
        return u


def _row_to_job(row: dict[str, str]) -> dict:
    tags = row.get("skill_tags") or ""
    skill_tags = [t.strip() for t in tags.split(",") if t.strip()]
    return {
        "title": (row.get("title") or "").strip(),
        "company": (row.get("company") or "").strip(),
        "url": (row.get("url") or "").strip(),
        "source": (row.get("source") or "csv_export").strip(),
        "date_added": (row.get("date_added") or "").strip(),
        "notes": (row.get("notes") or "").strip(),
        "skill_tags": skill_tags,
        "status": (row.get("status") or "interested").strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge CSV job export into JSON list.")
    parser.add_argument("--input", type=Path, required=True, help="Input CSV path")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output JSON path (array of job objects)",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"Missing input: {args.input}", file=sys.stderr)
        return 2

    existing: list[dict] = []
    if args.output.is_file():
        try:
            data = json.loads(args.output.read_text(encoding="utf-8"))
            if isinstance(data, list):
                existing = data
        except json.JSONDecodeError as e:
            print(f"Invalid existing JSON: {e}", file=sys.stderr)
            return 2

    seen = {_norm_url(j.get("url", "")) for j in existing if j.get("url")}
    new_jobs: list[dict] = []

    with args.input.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("CSV has no header row", file=sys.stderr)
            return 2
        fields_lower = {h.lower().strip(): h for h in reader.fieldnames}
        for req in EXPECTED:
            if req not in fields_lower:
                print(f"CSV missing column: {req}", file=sys.stderr)
                return 2

        for raw in reader:
            row = {k.lower().strip(): (v or "").strip() for k, v in raw.items()}
            job = _row_to_job(row)
            if not job["title"] or not job["url"]:
                continue
            key = _norm_url(job["url"])
            if key in seen:
                continue
            seen.add(key)
            new_jobs.append(job)

    merged = existing + new_jobs
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(merged)} jobs ({len(new_jobs)} new) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
