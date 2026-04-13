#!/usr/bin/env python3
"""
Fetch expanded runtime observation payloads for explicit IDs only.

Use after lane-search / lane-timeline filtering — not an implicit search.
See docs/runtime/observation-expansion.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

from observation_store import by_id  # noqa: E402

# Bounded expansion (richer than search; not a shadow Record).
EXPAND_KEYS = (
    "obs_id",
    "timestamp",
    "lane",
    "source_kind",
    "title",
    "summary",
    "source_path",
    "source_refs",
    "tags",
    "confidence",
    "contradiction_refs",
    "notes",
)


def expanded_row(raw: dict) -> dict:
    out: dict = {}
    for k in EXPAND_KEYS:
        out[k] = raw.get(k)
    return out


def render_markdown(rows: list[dict]) -> str:
    parts = ["# Expanded runtime observations", "", "_Runtime memory — not canonical Record truth._", ""]
    for row in rows:
        oid = row.get("obs_id", "?")
        parts.append(f"## {oid} — {row.get('title', '')}")
        parts.append(f"- Timestamp: {row.get('timestamp')}")
        parts.append(f"- Lane: {row.get('lane')}")
        parts.append(f"- Type: {row.get('source_kind')}")
        parts.append(f"- Confidence: {row.get('confidence')}")
        parts.append(f"- Source path: {row.get('source_path')}")
        parts.append("")
        parts.append(f"Summary: {row.get('summary', '')}")
        parts.append("")
        refs = row.get("source_refs") or []
        if refs:
            parts.append("Source refs:")
            for ref in refs:
                parts.append(f"- {ref}")
            parts.append("")
        tags = row.get("tags") or []
        if tags:
            parts.append("Tags: " + ", ".join(str(t) for t in tags))
            parts.append("")
        crefs = row.get("contradiction_refs") or []
        if crefs:
            parts.append("Contradiction refs:")
            for c in crefs:
                parts.append(f"- {c}")
            parts.append("")
        if row.get("notes"):
            parts.append("Notes:")
            parts.append(str(row["notes"]))
            parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Expand selected runtime observations by explicit ID (read-only)."
    )
    parser.add_argument(
        "--id",
        action="append",
        dest="ids",
        default=[],
        metavar="OBS_ID",
        help="Observation ID (repeatable)",
    )
    parser.add_argument(
        "obs_ids_pos",
        nargs="*",
        help="Optional positional IDs (same as --id)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read additional IDs from stdin (one per line)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON array (default unless --markdown)")
    parser.add_argument("--markdown", action="store_true", help="Emit Markdown document")
    parser.add_argument("--output", "-o", type=Path, help="Write to file instead of stdout")
    args = parser.parse_args()

    ids: list[str] = list(args.ids)
    ids.extend(args.obs_ids_pos)
    if args.stdin:
        for line in sys.stdin:
            s = line.strip()
            if s:
                ids.append(s)

    if not ids:
        print("error: no observation IDs (use --id or positional args)", file=sys.stderr)
        return 2

    if args.json and args.markdown:
        print("error: use only one of --json and --markdown", file=sys.stderr)
        return 2

    missing: list[str] = []
    expanded: list[dict] = []
    for oid in ids:
        raw = by_id(oid)
        if raw is None:
            missing.append(oid)
        else:
            expanded.append(expanded_row(raw))

    if missing:
        print(f"error: missing observation id(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    expanded.sort(key=lambda r: r.get("timestamp") or "")

    use_md = args.markdown
    if use_md:
        content = render_markdown(expanded)
    else:
        content = json.dumps(expanded, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
