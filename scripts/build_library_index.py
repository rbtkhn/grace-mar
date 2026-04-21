#!/usr/bin/env python3
"""
Emit artifacts/library-index.md — derived operator dashboard from SELF-LIBRARY entries in self-library.md.

Does not modify users/*/self-library.md or any Record file.
"""

from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
import sys

if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from operator_dashboard_common import REPO_ROOT, load_self_library_entries  # noqa: E402

# Dashboard layout (plain Markdown; no schema changes)
COMPACT_LANE_PREVIEW = 10
START_HERE_CAP = 20
RECENT_TOUCHED_CAP = 20
SCOPE_TAG_TOP = 28
READ_GAP_CAP = 25


def _git_last_commit_iso_for_file(repo_root: Path, rel_path: str) -> str | None:
    """ISO-8601 timestamp of the last commit touching rel_path, or None."""
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", rel_path],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0:
            return None
        s = (r.stdout or "").strip()
        return s or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _generated_at_stamp(repo_root: Path, user_id: str) -> str:
    """Stable for a given git commit: last commit time on self-library.md, else UTC now."""
    rel = f"users/{user_id}/self-library.md"
    iso = _git_last_commit_iso_for_file(repo_root, rel)
    if iso:
        try:
            normalized = iso.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalized)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return iso
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git_last_commit_ts(repo_root: Path, rel_path: str) -> str | None:
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0:
            return None
        s = (r.stdout or "").strip()
        return s or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _url_to_repo_path(url: str) -> str | None:
    if "github.com" in url and "/blob/" in url:
        parts = url.split("/blob/")
        if len(parts) < 2:
            return None
        rest = parts[1].split("/", 1)
        if len(rest) < 2:
            return None
        return rest[1]
    return None


def _lookup_priority_rank(entry: dict[str, Any]) -> int:
    lp = str(entry.get("lookup_priority") or "").strip().lower()
    order = {"preferred": 0, "high": 1, "medium": 2, "low": 3}
    return order.get(lp, 9)


def _entry_id(entry: dict[str, Any]) -> str:
    return str(entry.get("id") or "")


def _sort_key_priority_id(entry: dict[str, Any]) -> tuple[int, str]:
    return (_lookup_priority_rank(entry), _entry_id(entry))


def _is_operator_analytical(entry: dict[str, Any]) -> bool:
    if str(entry.get("shelf_intent") or "").strip().lower() == "operator_book":
        return True
    scope = entry.get("scope")
    if not isinstance(scope, list):
        return False
    return any(isinstance(t, str) and t.strip() == "operator_analytical" for t in scope)


def _format_entry_bullet(e: dict[str, Any], *, title_max: int = 80, show_lookup: bool = True) -> str:
    eid = e.get("id", "")
    title = str(e.get("title", ""))[:title_max]
    lp_raw = str(e.get("lookup_priority") or "").strip()
    lp = lp_raw.lower()
    # Surface non-default priorities only (skip medium, empty, none, etc.)
    show_lp = show_lookup and lp in ("preferred", "high", "low")
    if show_lp:
        return f"- **{eid}** — {title} (`lookup_priority`: {lp_raw})\n"
    return f"- **{eid}** — {title}\n"


def render_markdown(
    entries: list[dict[str, Any]],
    *,
    user_id: str,
    repo_root: Path,
    generated_at: str,
) -> str:
    lines: list[str] = [
        "<!-- GENERATED — run: python3 scripts/build_library_index.py -->\n\n",
        "# Library index — operator dashboard (SELF-LIBRARY)\n\n",
        "**Derived artifact — not canonical.** Regenerate after editing "
        f"[users/{user_id}/self-library.md](users/{user_id}/self-library.md). "
        "Canonical library truth stays in that file and in [docs/library-schema.md](../docs/library-schema.md).\n\n",
    ]

    by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        lane = str(e.get("lane") or "unknown")
        by_lane[lane].append(e)

    n_operator = sum(1 for e in entries if _is_operator_analytical(e))

    # --- At a glance ---
    lines.append("## At a glance\n\n")
    lines.append(f"- **Generated:** {generated_at}\n")
    lines.append(f"- **Entries:** {len(entries)} total")
    if by_lane:
        parts = [f"{lane}: {len(by_lane[lane])}" for lane in sorted(by_lane.keys())]
        lines.append(" · " + " · ".join(parts))
    lines.append("\n")
    lines.append(f"- **Operator-analytical shelf** (tag or `shelf_intent: operator_book`): **{n_operator}** entries\n\n")

    # --- Start here ---
    start_candidates = [e for e in entries if _is_operator_analytical(e)]
    start_candidates.sort(key=_sort_key_priority_id)
    lines.append("## Start here (operator analytical + lookup priority)\n\n")
    lines.append(
        "_High-value WORK lanes: Predictive History, strategy notebook, journals, etc. "
        "Sorted by `lookup_priority` then id._\n\n"
    )
    if not start_candidates:
        lines.append("_None matched `operator_analytical` / `operator_book` heuristics._\n\n")
    else:
        for e in start_candidates[:START_HERE_CAP]:
            lines.append(_format_entry_bullet(e, show_lookup=True))
        if len(start_candidates) > START_HERE_CAP:
            lines.append(
                f"\n_{len(start_candidates) - START_HERE_CAP} more operator-analytical entries — "
                "see **By lane (compact)** and **Appendix**._\n"
            )
        lines.append("\n")

    # --- Recently touched ---
    lines.append("## Recently touched (git, best effort)\n\n")
    lines.append(
        "_Last commit date on repo path from `url` when it points at this repository — "
        "proxy for “hot” docs._\n\n"
    )
    touched_rows: list[tuple[str, str, str]] = []
    for e in entries:
        url = e.get("url")
        if not isinstance(url, str) or not url.strip():
            continue
        rel = _url_to_repo_path(url)
        if not rel:
            continue
        ts = _git_last_commit_ts(repo_root, rel)
        if ts:
            touched_rows.append((ts, str(e.get("id")), str(e.get("title", ""))[:60]))
    touched_rows.sort(reverse=True)
    if not touched_rows:
        lines.append("_No git timestamps resolved (missing `url`, paths, or not a git checkout)._\n\n")
    else:
        for ts, eid, title in touched_rows[:RECENT_TOUCHED_CAP]:
            lines.append(f"- {ts} — **{eid}** — {title}\n")
        if len(touched_rows) > RECENT_TOUCHED_CAP:
            lines.append(f"\n_{len(touched_rows) - RECENT_TOUCHED_CAP} more with resolvable git dates._\n")
        lines.append("\n")

    # --- By lane (compact) ---
    lines.append("## By lane (compact)\n\n")
    lines.append(
        "_Preview only — full sorted lists are in **Appendix: full inventory by lane**._\n\n"
    )
    for lane in sorted(by_lane.keys()):
        bucket = by_lane[lane]
        bucket_sorted = sorted(bucket, key=_sort_key_priority_id)
        n = len(bucket_sorted)
        lines.append(f"### {lane} ({n})\n\n")
        preview = bucket_sorted[:COMPACT_LANE_PREVIEW]
        for e in preview:
            lines.append(_format_entry_bullet(e, title_max=72, show_lookup=True))
        if n > COMPACT_LANE_PREVIEW:
            lines.append(
                f"\n_{n - COMPACT_LANE_PREVIEW} more in **{lane}** — see appendix._\n"
            )
        lines.append("\n")

    # --- Scope tags (top) ---
    lines.append("## Scope tags (top by frequency)\n\n")
    tag_n: dict[str, int] = defaultdict(int)
    for e in entries:
        for t in e.get("scope") or []:
            if isinstance(t, str):
                tag_n[t] += 1
    sorted_tags = sorted(tag_n.items(), key=lambda x: (-x[1], x[0]))
    top_tags = sorted_tags[:SCOPE_TAG_TOP]
    for tag, n in top_tags:
        lines.append(f"- `{tag}`: {n}\n")
    if len(sorted_tags) > SCOPE_TAG_TOP:
        lines.append(
            f"\n_{len(sorted_tags) - SCOPE_TAG_TOP} additional tags — full histogram in git history or YAML._\n"
        )
    lines.append("\n")

    # --- READ gap ---
    lines.append("## Possible READ link gap (heuristic)\n\n")
    lines.append(
        "_`engagement_status: consumed` but no `read_id` — may warrant a READ-* link or be intentional._\n\n"
    )
    gap = [
        e
        for e in entries
        if str(e.get("engagement_status") or "").lower() == "consumed" and not e.get("read_id")
    ]
    for e in gap[:READ_GAP_CAP]:
        lines.append(f"- **{e.get('id')}** — {e.get('title')}\n")
    if not gap:
        lines.append("_None matching heuristic._\n")
    elif len(gap) > READ_GAP_CAP:
        lines.append(f"\n_… {len(gap) - READ_GAP_CAP} more._\n")
    lines.append("\n")

    # --- Contradictions stub ---
    lines.append("## Open contradictions / review flags\n\n")
    lines.append("_Not computed in v1 — see contradiction policy and manual review._\n\n")

    # --- Appendix: full inventory ---
    lines.append("---\n\n")
    lines.append("## Appendix — full inventory by lane\n\n")
    lines.append(
        "_Complete list for completeness checks; the sections above are for daily navigation._\n\n"
    )
    for lane in sorted(by_lane.keys()):
        bucket = sorted(by_lane[lane], key=lambda x: _entry_id(x))
        lines.append(f"### {lane}\n\n")
        for e in bucket:
            eid = e.get("id", "")
            title = str(e.get("title", ""))[:100]
            lines.append(f"- **{eid}** — {title}\n")
        lines.append("\n")

    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build library-index.md from self-library.md entries YAML.")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    uid = args.user.strip()
    entries = load_self_library_entries(root, uid)
    ts = _generated_at_stamp(root, uid)
    md = render_markdown(entries, user_id=uid, repo_root=root, generated_at=ts)
    out = root / "artifacts" / "library-index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
