#!/usr/bin/env python3
"""Review report for self-library.md — surfaces stale, under-scoped,
and operator-book entries to support freshness and retrieval hygiene.

Modes:
  (default)   structured text to stdout
  --write     also writes artifacts/self-library/runtime-summary.md
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LIB = REPO_ROOT / "users" / "grace-mar" / "self-library.md"
ARTIFACT_DIR = REPO_ROOT / "artifacts" / "self-library"
ARTIFACT_PATH = ARTIFACT_DIR / "runtime-summary.md"

STALE_DAYS = 30
PRIORITY_ORDER = ["preferred", "high", "medium", "low", "none"]


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(
        r"-\s+id:\s+(LIB-\d+)(.*?)(?=-\s+id:\s+LIB-|\Z)", content, re.DOTALL
    ):
        lib_id = m.group(1)
        block = m.group(2)
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        scope_m = re.search(r"scope:\s*\[([^\]]*)\]", block)
        status_m = re.search(r"status:\s*[\"']?(\w+)", block)
        priority_m = re.search(r"lookup_priority:\s*[\"']?(\w+)", block)
        lane_m = re.search(r"lane:\s*[\"']?(\w+)", block)
        shelf_m = re.search(r"shelf_intent:\s*[\"']?(\w+)", block)
        subtype_m = re.search(r"operator_subtype:\s*[\"']?(\w+)", block)
        reviewed_m = re.search(r"reviewed_at:\s*[\"']?(\d{4}-\d{2}-\d{2})", block)
        added_m = re.search(r"added_at:\s*[\"']?(\d{4}-\d{2}-\d{2})", block)

        if status_m and status_m.group(1) != "active":
            continue
        if not title_m:
            continue

        scope_raw = scope_m.group(1) if scope_m else ""
        scopes = [s.strip().strip("'\"") for s in scope_raw.split(",") if s.strip()]
        entries.append(
            {
                "id": lib_id,
                "title": title_m.group(1)[:72],
                "scope": scopes,
                "lookup_priority": priority_m.group(1) if priority_m else "low",
                "lane": lane_m.group(1) if lane_m else "canon",
                "shelf_intent": shelf_m.group(1) if shelf_m else "",
                "operator_subtype": subtype_m.group(1) if subtype_m else "",
                "reviewed_at": reviewed_m.group(1) if reviewed_m else "",
                "added_at": added_m.group(1) if added_m else "",
            }
        )
    return entries


def is_stale(entry: dict, today: date) -> bool:
    r = entry.get("reviewed_at", "")
    if not r:
        return True
    try:
        reviewed = date.fromisoformat(r)
    except ValueError:
        return True
    return (today - reviewed).days > STALE_DAYS


def priority_entries(entries: list[dict], level: str) -> list[dict]:
    return [e for e in entries if e["lookup_priority"] == level]


def operator_book_entries(entries: list[dict]) -> list[dict]:
    return [e for e in entries if e["shelf_intent"] == "operator_book"]


def scope_distribution(entries: list[dict], top_n: int = 10) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for e in entries:
        for s in e["scope"]:
            c[s] += 1
    return c.most_common(top_n)


def singleton_scope_entries(entries: list[dict]) -> list[dict]:
    return [e for e in entries if len(e["scope"]) <= 1]


def duplicate_scope_clusters(entries: list[dict]) -> dict[str, list[str]]:
    scope_to_ids: dict[str, list[str]] = {}
    for e in entries:
        key = tuple(sorted(e["scope"]))
        if not key:
            continue
        scope_to_ids.setdefault(str(key), []).append(e["id"])
    return {k: v for k, v in scope_to_ids.items() if len(v) > 1}


def fmt_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "(none)\n"
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    hdr = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |"
    lines = [hdr, sep]
    for row in rows:
        lines.append(
            "| " + " | ".join(cell.ljust(w) for cell, w in zip(row, widths)) + " |"
        )
    return "\n".join(lines) + "\n"


def build_report(entries: list[dict], today: date) -> str:
    out: list[str] = []

    # Preferred entries
    pref = priority_entries(entries, "preferred")
    out.append("## Preferred entries\n")
    out.append(
        fmt_table(
            ["ID", "Title", "Shelf", "Subtype", "Reviewed"],
            [
                [e["id"], e["title"], e["shelf_intent"], e["operator_subtype"], e["reviewed_at"] or "—"]
                for e in pref
            ],
        )
    )

    # High-priority entries
    high = priority_entries(entries, "high")
    out.append("\n## High-priority entries\n")
    out.append(
        fmt_table(
            ["ID", "Title", "Shelf", "Subtype", "Reviewed"],
            [
                [e["id"], e["title"], e["shelf_intent"], e["operator_subtype"], e["reviewed_at"] or "—"]
                for e in high
            ],
        )
    )

    # Operator books by subtype
    ob = operator_book_entries(entries)
    subtypes_found = sorted({e["operator_subtype"] for e in ob if e["operator_subtype"]})
    out.append("\n## Operator analytical entries by subtype\n")
    for st in subtypes_found:
        out.append(f"### {st}\n")
        subset = [e for e in ob if e["operator_subtype"] == st]
        out.append(
            fmt_table(
                ["ID", "Title", "Priority", "Reviewed"],
                [
                    [e["id"], e["title"], e["lookup_priority"], e["reviewed_at"] or "—"]
                    for e in subset
                ],
            )
        )
    untyped = [e for e in ob if not e["operator_subtype"]]
    if untyped:
        out.append("### (no subtype)\n")
        out.append(
            fmt_table(
                ["ID", "Title", "Priority"],
                [[e["id"], e["title"], e["lookup_priority"]] for e in untyped],
            )
        )

    # Scope distribution
    dist = scope_distribution(entries)
    out.append("\n## Scope distribution (top 10)\n")
    out.append(
        fmt_table(["Tag", "Count"], [[tag, str(count)] for tag, count in dist])
    )

    # Entries needing review
    stale = [e for e in entries if e["lookup_priority"] in ("preferred", "high", "medium") and is_stale(e, today)]
    out.append(f"\n## Entries needing review (stale or missing reviewed_at, cutoff {STALE_DAYS}d)\n")
    out.append(
        fmt_table(
            ["ID", "Title", "Priority", "Reviewed"],
            [
                [e["id"], e["title"], e["lookup_priority"], e["reviewed_at"] or "—"]
                for e in stale
            ],
        )
    )

    # Singleton scope
    singles = singleton_scope_entries(entries)
    if singles:
        out.append(f"\n## Entries with empty or singleton scope ({len(singles)})\n")
        out.append(
            fmt_table(
                ["ID", "Title", "Scope"],
                [[e["id"], e["title"], ", ".join(e["scope"]) or "(empty)"] for e in singles],
            )
        )

    # Duplicate scope clusters
    dupes = duplicate_scope_clusters(entries)
    if dupes:
        out.append(f"\n## Duplicate-scope clusters ({len(dupes)})\n")
        for scope_key, ids in dupes.items():
            out.append(f"- {', '.join(ids)} → scope: {scope_key}\n")
        out.append("")

    return "\n".join(out)


def build_artifact(entries: list[dict], today: date) -> str:
    lines: list[str] = [
        "# SELF-LIBRARY runtime summary",
        "",
        f"Generated: {today.isoformat()}",
        f"Active entries: {len(entries)}",
        "",
        "---",
        "",
    ]
    lines.append(build_report(entries, today))
    lines.append(
        "\n---\n\n*Rebuildable artifact. Source: `scripts/library_review_report.py --write`.*\n"
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-library review report")
    parser.add_argument(
        "--lib",
        type=Path,
        default=DEFAULT_LIB,
        help="Path to self-library.md",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write runtime-summary.md to artifacts/self-library/",
    )
    args = parser.parse_args()

    entries = load_entries(args.lib)
    if not entries:
        print("No active entries found.")
        return 1

    today = date.today()
    report = build_report(entries, today)
    print(report)

    if args.write:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        artifact = build_artifact(entries, today)
        ARTIFACT_PATH.write_text(artifact, encoding="utf-8")
        print(f"\nArtifact written: {ARTIFACT_PATH.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
