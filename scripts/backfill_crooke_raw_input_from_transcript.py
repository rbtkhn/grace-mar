#!/usr/bin/env python3
"""One-shot / reusable: extract Conflicts Forum Crooke Substack pastes from agent transcript JSONL into strategy-notebook raw-input."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RE_URL = re.compile(r"https://conflictsforum\.substack\.com/p/[a-z0-9-]+")
RE_USER_QUERY = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL)
# Transcript pastes often omit "###"; Substack line is "Alastair Crooke, 8 January 2026".
RE_PUB = re.compile(
    r"(?:###\s*)?Alastair Crooke,\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})",
    re.I,
)
# Substack UI date line: "Jan 08, 2026" (fallback when byline year is wrong).
RE_UI_DATE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),\s*(\d{4})\b",
    re.I,
)
MONTHS = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
}
MONTH_ABBR = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/p/")[-1]


def _month_token_to_mm(token: str) -> str | None:
    t = token.strip()
    for name, mm in MONTHS.items():
        if t.lower() == name.lower():
            return mm
    pref = t.lower()[:3]
    return MONTH_ABBR.get(pref)


def _ui_date_to_iso(m: re.Match[str]) -> str:
    mon, day, year = m.group(1), m.group(2), m.group(3)
    mm = MONTH_ABBR[mon.lower()[:3]]
    return f"{year}-{mm}-{int(day):02d}"


def pub_date_from_body(body: str, slug: str) -> str | None:
    m = RE_PUB.search(body)
    if m:
        day, month_name, year = m.group(1), m.group(2), m.group(3)
        mm = _month_token_to_mm(month_name)
        if mm:
            iso = f"{year}-{mm}-{int(day):02d}"
            # Known typo: Epstein byline "2025" vs UI "Feb 05, 2026".
            if slug == "the-slow-epstein-earthquake-the-rupture" and year == "2025":
                ui = RE_UI_DATE.search(body)
                if ui:
                    return _ui_date_to_iso(ui)
            return iso
    ui = RE_UI_DATE.search(body)
    if ui:
        return _ui_date_to_iso(ui)
    return None


def extract_operator_paste(full_text: str) -> str:
    """Prefer content inside <user_query> when present (full operator paste)."""
    m = RE_USER_QUERY.search(full_text)
    if m:
        return m.group(1).strip()
    return full_text.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--transcript",
        type=Path,
        required=True,
        help="Path to agent transcript .jsonl",
    )
    ap.add_argument(
        "--notebook-root",
        type=Path,
        default=Path("docs/skill-work/work-strategy/strategy-notebook"),
        help="Strategy notebook root",
    )
    ap.add_argument(
        "--ingest-date",
        default="2026-04-29",
        help="ingest_date YAML field (when saving into repo)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw_root = args.notebook_root / "raw-input"
    written: list[Path] = []

    with args.transcript.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("role") != "user":
                continue
            parts = obj.get("message", {}).get("content", [])
            full_text = "".join(
                p.get("text", "")
                for p in parts
                if isinstance(p, dict) and p.get("type") == "text"
            )
            if "conflictsforum.substack.com/p/" not in full_text:
                continue

            body = extract_operator_paste(full_text)
            urls = RE_URL.findall(full_text)
            if not urls:
                continue
            source_url = urls[0]
            slug = slug_from_url(source_url)

            pub_date = pub_date_from_body(body, slug)
            if not pub_date:
                print(
                    f"WARN line {lineno}: no Alastair Crooke / Substack UI date — skip {slug}",
                    file=sys.stderr,
                )
                continue

            out_dir = raw_root / pub_date
            fname = f"substack-crooke-{slug}-{pub_date}.md"
            out_path = out_dir / fname

            fm = f"""---
ingest_date: {args.ingest_date}
pub_date: {pub_date}
thread: crooke
source_url: {source_url}
kind: paste-bundle
note: Verbatim operator paste; backfill from agent transcript (jsonl line {lineno}).
---

# {slug.replace('-', ' ')}

"""
            content = fm + body

            if args.dry_run:
                print(f"would write {out_path} ({len(content)} chars)")
                continue

            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8")
            written.append(out_path)

    if args.dry_run:
        return 0
    for p in written:
        print(p.as_posix())
    print(f"wrote {len(written)} file(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
