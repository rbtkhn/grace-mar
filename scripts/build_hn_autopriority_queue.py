#!/usr/bin/env python3
"""Generate queue ranking for history-notebook chapter drafting priority.

Inputs:
- book-architecture.yaml (chapter roster and status)
- bookshelf-catalog.yaml (HNSRC rows + candidate_hn_chapters)
- AGENTIC-MVP-CONFIG.yaml (weights + thresholds)

Output:
- research/QUEUE-AUTOPRIORITY.md

WORK only; not Record.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
ARCH_PATH = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "book-architecture.yaml"
CATALOG_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
CONFIG_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "AGENTIC-MVP-CONFIG.yaml"
)
OUT_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "QUEUE-AUTOPRIORITY.md"
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def chapter_rows(arch: dict) -> list[dict]:
    chapters = arch.get("chapters") or []
    out: list[dict] = []
    for c in chapters:
        if not isinstance(c, dict) or "id" not in c:
            continue
        out.append(
            {
                "id": str(c["id"]),
                "title": str(c.get("title") or ""),
                "status": str(c.get("status") or "unknown"),
                "volume": str(c.get("volume") or ""),
                "file": str(c.get("file") or "").strip(),
            }
        )
    return out


def anchor_map(catalog: dict) -> tuple[dict[str, list[str]], dict[str, set[str]]]:
    by_hn: dict[str, list[str]] = {}
    authors: dict[str, set[str]] = {}
    for item in catalog.get("items") or []:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("id") or "").strip()
        author = str(item.get("author") or "").strip() or "Unknown"
        for ch in item.get("candidate_hn_chapters") or []:
            if not isinstance(ch, str):
                continue
            hid = ch.strip()
            by_hn.setdefault(hid, []).append(sid)
            authors.setdefault(hid, set()).add(author)
    for hid in by_hn:
        by_hn[hid] = sorted(set(by_hn[hid]))
    return by_hn, authors


def detect_stub_ratio(file_path: Path, markers: list[str]) -> float:
    if not file_path.is_file():
        return 1.0
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    marker_hits = sum(1 for m in markers if m in text)
    # 7 markers in default template; clamp for safety.
    return min(1.0, marker_hits / max(1, len(markers)))


def norm(val: float, hi: float) -> float:
    if hi <= 0:
        return 0.0
    return min(1.0, max(0.0, val / hi))


def build_markdown(
    rows: list[dict],
    ranked: list[dict],
    *,
    top_n: int,
    under_anchored_max: int,
    buy_or_borrow_max: int,
) -> str:
    lines: list[str] = [
        "# Draft queue autopriority (generated)",
        "",
        "**Do not edit by hand.**",
        "Regenerate: `python3 scripts/build_hn_autopriority_queue.py`",
        "",
        "Scoring combines shelf support density, author diversity, readiness gap, and strategic urgency.",
        "",
    ]
    lines.append("## Top queue")
    lines.append("")
    for i, row in enumerate(ranked[:top_n], start=1):
        lines.append(
            f"{i}. `{row['id']}` — {row['title']} "
            f"(score `{row['score']:.3f}`, anchors `{row['anchor_count']}`, "
            f"authors `{row['author_diversity']}`, status `{row['status']}`)"
        )
    lines.append("")

    lines.append("## High-value but under-anchored")
    lines.append("")
    under = [r for r in ranked if r["anchor_count"] <= under_anchored_max]
    if not under:
        lines.append("- *(none)*")
    for row in under[:15]:
        lines.append(
            f"- `{row['id']}` — anchors `{row['anchor_count']}`; "
            f"queue score `{row['score']:.3f}`; status `{row['status']}`"
        )
    lines.append("")

    lines.append("## Buy/borrow candidates")
    lines.append("")
    buy = [r for r in ranked if r["anchor_count"] <= buy_or_borrow_max]
    if not buy:
        lines.append("- *(none)*")
    for row in buy[:15]:
        lines.append(
            f"- `{row['id']}` — only `{row['anchor_count']}` shelf anchor(s); "
            f"consider acquiring 1-2 specialized sources for chapter thesis coverage."
        )
    lines.append("")

    lines.append("## Full roster scores")
    lines.append("")
    lines.append("| Chapter | Score | Anchors | Author diversity | Status | Volume |")
    lines.append("|---|---:|---:|---:|---|---|")
    for row in ranked:
        lines.append(
            f"| `{row['id']}` | {row['score']:.3f} | {row['anchor_count']} | "
            f"{row['author_diversity']} | {row['status']} | {row['volume']} |"
        )
    lines.append("")
    lines.append(f"_Total chapters scored: {len(rows)}_")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--architecture", type=Path, default=ARCH_PATH)
    ap.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    ap.add_argument("--config", type=Path, default=CONFIG_PATH)
    ap.add_argument("--out", type=Path, default=OUT_PATH)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    for p in (args.architecture, args.catalog, args.config):
        if not p.is_file():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 1

    arch = load_yaml(args.architecture)
    catalog = load_yaml(args.catalog)
    config = load_yaml(args.config)

    weights = (config.get("autopriority") or {}).get("weights") or {}
    readiness_cfg = (config.get("autopriority") or {}).get("readiness") or {}
    status_map = readiness_cfg.get("status_to_readiness") or {}
    markers = readiness_cfg.get("stub_markers") or []
    urgency_map = (config.get("autopriority") or {}).get("strategic_urgency_defaults") or {}
    thresholds = (config.get("autopriority") or {}).get("thresholds") or {}
    queue_cfg = (config.get("autopriority") or {}).get("queue") or {}

    rows = chapter_rows(arch)
    if not rows:
        print("ERROR: no chapters found in book-architecture", file=sys.stderr)
        return 1
    by_hn, author_map = anchor_map(catalog)

    # Pre-compute normalizers.
    anchor_counts = [len(by_hn.get(r["id"], [])) for r in rows]
    author_counts = [len(author_map.get(r["id"], set())) for r in rows]
    max_anchors = max(anchor_counts) if anchor_counts else 1
    max_authors = max(author_counts) if author_counts else 1

    ranked: list[dict] = []
    for r in rows:
        hid = r["id"]
        status = r["status"]
        status_readiness = float(status_map.get(status, status_map.get("unknown", 0.6)))
        stub_ratio = detect_stub_ratio(REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / r["file"], markers)
        readiness_gap = max(status_readiness, stub_ratio)
        anchor_count = len(by_hn.get(hid, []))
        author_div = len(author_map.get(hid, set()))
        urgency = float(urgency_map.get(str(r["volume"]), 0.8))

        score = (
            float(weights.get("shelf_anchor_count", 0.4)) * norm(anchor_count, max_anchors)
            + float(weights.get("shelf_author_diversity", 0.2)) * norm(author_div, max_authors)
            + float(weights.get("chapter_readiness_gap", 0.25)) * readiness_gap
            + float(weights.get("strategic_urgency", 0.15)) * urgency
        )
        ranked.append(
            {
                **r,
                "score": score,
                "anchor_count": anchor_count,
                "author_diversity": author_div,
                "readiness_gap": readiness_gap,
            }
        )

    ranked.sort(key=lambda x: (-x["score"], x["id"]))

    content = build_markdown(
        rows,
        ranked,
        top_n=int(queue_cfg.get("top_n", 10)),
        under_anchored_max=int(thresholds.get("under_anchored_max_count", 2)),
        buy_or_borrow_max=int(thresholds.get("buy_or_borrow_max_count", 1)),
    )

    if args.check:
        if not args.out.is_file():
            print(f"CHECK: missing {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_autopriority_queue.py", file=sys.stderr)
            return 1
        old = args.out.read_text(encoding="utf-8")
        if old != content:
            print(f"CHECK: stale {args.out}", file=sys.stderr)
            print("Run: python3 scripts/build_hn_autopriority_queue.py", file=sys.stderr)
            return 1
        print("ok: hn autopriority queue up to date")
        return 0

    args.out.write_text(content, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
