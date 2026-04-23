#!/usr/bin/env python3
"""Watch tool: cross-expert page views grouped by watch tags.

Reads pages from expert thread files (via ``strategy_page_reader``),
groups them by ``watch=`` attributes, and uses the optional connection file
(``knot-connections.yaml`` on disk) tension relations to surface cross-expert
disagreements.

Usage::

    python3 scripts/strategy_watch.py                          # list all watches
    python3 scripts/strategy_watch.py --watch hormuz            # one watch detail
    python3 scripts/strategy_watch.py --watch hormuz --json     # machine-readable
    python3 scripts/strategy_watch.py --tensions-only           # only disagreements

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_page_reader import (
    PageBlock,
    all_watch_ids,
    discover_all_pages,
    pages_for_watch,
)

DEFAULT_NOTEBOOK = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)
DEFAULT_CONNECTIONS = DEFAULT_NOTEBOOK / "knot-connections.yaml"


# ---------------------------------------------------------------------------
# Tension detection
# ---------------------------------------------------------------------------

def _load_tensions(connections_path: Path) -> list[dict]:
    """Load tension relations from the optional connections YAML."""
    if not connections_path.is_file():
        return []
    data = yaml.safe_load(connections_path.read_text(encoding="utf-8"))
    if not data:
        return []
    return [
        c for c in data.get("connections", [])
        if c.get("relation") == "tension"
    ]


def _page_id_to_source_basename(page_id: str, pages: list[PageBlock]) -> str | None:
    """Return basename from **Source page:** or legacy **Source knot:** in page body."""
    for p in pages:
        if p.id == page_id:
            for line in p.content.splitlines():
                if line.startswith("**Source page:**"):
                    return line.split("**Source page:**", 1)[1].strip()
                if line.startswith("**Source knot:**"):
                    return line.split("**Source knot:**", 1)[1].strip()
    return None


def find_tensions_for_watch(
    watch_id: str,
    watch_pages: dict[str, list[PageBlock]],
    tensions: list[dict],
) -> list[dict]:
    """Find tensions relevant to pages in this watch."""
    all_pages_flat = [p for pages in watch_pages.values() for pages in pages for p in [pages]]
    all_pages_flat = []
    for expert_pages in watch_pages.values():
        all_pages_flat.extend(expert_pages)

    relevant: list[dict] = []
    for tension in tensions:
        warrants = tension.get("warrant", [])
        if any(f"shared-watch:{watch_id}" in w for w in warrants):
            relevant.append(tension)
    return relevant


# ---------------------------------------------------------------------------
# Watch listing
# ---------------------------------------------------------------------------

def list_watches(notebook_dir: Path) -> list[dict]:
    """Return summary data for all watches."""
    all_pages = discover_all_pages(notebook_dir)
    watch_data: dict[str, dict] = {}

    for expert_id, pages in all_pages.items():
        for p in pages:
            if not p.watch:
                continue
            entry = watch_data.setdefault(p.watch, {
                "watch": p.watch,
                "page_count": 0,
                "experts": [],
                "dates": [],
            })
            entry["page_count"] += 1
            if expert_id not in entry["experts"]:
                entry["experts"].append(expert_id)
            if p.date and p.date not in entry["dates"]:
                entry["dates"].append(p.date)

    for entry in watch_data.values():
        entry["experts"].sort()
        entry["dates"].sort()

    return sorted(watch_data.values(), key=lambda w: w["watch"])


def watch_detail(
    watch_id: str,
    notebook_dir: Path,
    connections_path: Path,
) -> dict:
    """Build a detailed view of one watch."""
    wp = pages_for_watch(notebook_dir, watch_id)
    tensions = _load_tensions(connections_path)
    relevant_tensions = find_tensions_for_watch(watch_id, wp, tensions)

    expert_summaries: dict[str, list[dict]] = {}
    for expert_id, pages in sorted(wp.items()):
        expert_summaries[expert_id] = [
            {"id": p.id, "date": p.date, "content_preview": p.content[:200]}
            for p in pages
        ]

    return {
        "watch": watch_id,
        "experts": sorted(wp.keys()),
        "pages_by_expert": expert_summaries,
        "tensions": [
            {
                "from": t.get("from", ""),
                "to": t.get("to", ""),
                "reason": t.get("reason", ""),
            }
            for t in relevant_tensions
        ],
    }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_watches_markdown(watches: list[dict]) -> str:
    lines = ["# Strategy watches\n"]
    if not watches:
        lines.append("_(No watches found — pages need `watch=` attributes.)_")
        return "\n".join(lines)

    lines.append(f"| Watch | Pages | Experts | Date range |")
    lines.append(f"|-------|-------|---------|------------|")
    for w in watches:
        dates = w["dates"]
        date_range = f"{dates[0]} → {dates[-1]}" if dates else "—"
        lines.append(
            f"| {w['watch']} | {w['page_count']} | "
            f"{', '.join(w['experts'])} | {date_range} |"
        )
    return "\n".join(lines)


def format_detail_markdown(detail: dict) -> str:
    lines = [f"# Watch: {detail['watch']}\n"]
    lines.append(f"**Experts:** {', '.join(detail['experts'])}\n")

    for expert_id, pages in sorted(detail["pages_by_expert"].items()):
        lines.append(f"## {expert_id}\n")
        for p in pages:
            lines.append(f"### {p['id']} ({p['date']})\n")
            lines.append(p["content_preview"])
            if len(p["content_preview"]) >= 200:
                lines.append("...")
            lines.append("")

    if detail["tensions"]:
        lines.append("## Tensions\n")
        for t in detail["tensions"]:
            from_name = Path(t["from"]).stem if t["from"] else "?"
            to_name = Path(t["to"]).stem if t["to"] else "?"
            lines.append(f"- **{from_name}** ↔ **{to_name}**: {t['reason']}")
        lines.append("")
    else:
        lines.append("_(No tension relations found for this watch.)_\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--watch", help="Show detail for a specific watch")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--tensions-only", action="store_true", help="Only show watches with tensions")
    ap.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK)
    ap.add_argument("--connections", type=Path, default=DEFAULT_CONNECTIONS)
    args = ap.parse_args()

    if args.watch:
        detail = watch_detail(args.watch, args.notebook, args.connections)
        if args.json:
            print(json.dumps(detail, indent=2, ensure_ascii=False))
        else:
            print(format_detail_markdown(detail))
    else:
        watches = list_watches(args.notebook)
        if args.tensions_only:
            tensions = _load_tensions(args.connections)
            tension_watches: set[str] = set()
            for t in tensions:
                for w in t.get("warrant", []):
                    if w.startswith("shared-watch:"):
                        tension_watches.add(w.split(":", 1)[1])
            watches = [w for w in watches if w["watch"] in tension_watches]

        if args.json:
            print(json.dumps(watches, indent=2, ensure_ascii=False))
        else:
            print(format_watches_markdown(watches))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
