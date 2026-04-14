#!/usr/bin/env python3
"""
Emit artifacts/library-index.md — derived overview of SELF-LIBRARY entries from self-library.md.

Does not modify users/*/self-library.md or any Record file.
"""

from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
import sys

if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from operator_dashboard_common import REPO_ROOT, load_self_library_entries  # noqa: E402


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


def render_markdown(
    entries: list[dict[str, Any]],
    *,
    user_id: str,
    repo_root: Path,
    generated_at: str,
) -> str:
    lines: list[str] = [
        "<!-- GENERATED — run: python3 scripts/build_library_index.py -->\n\n",
        "# Library index (SELF-LIBRARY)\n\n",
        "**Derived operator artifact.** Not canonical Record truth; regenerate after editing "
        f"[users/{user_id}/self-library.md](users/{user_id}/self-library.md).\n\n",
        f"- **Generated:** {generated_at}\n",
        f"- **Entry count:** {len(entries)}\n\n",
        "## By lane\n\n",
    ]
    by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in entries:
        lane = str(e.get("lane") or "unknown")
        by_lane[lane].append(e)
    for lane in sorted(by_lane.keys()):
        lines.append(f"### {lane}\n\n")
        for e in sorted(by_lane[lane], key=lambda x: str(x.get("id", "")))[:30]:
            eid = e.get("id", "")
            title = str(e.get("title", ""))[:80]
            lines.append(f"- **{eid}** — {title}\n")
        if len(by_lane[lane]) > 30:
            lines.append(f"\n_… {len(by_lane[lane]) - 30} more in this lane._\n")
        lines.append("\n")

    lines.append("## Scope tags (frequency)\n\n")
    tag_n: dict[str, int] = defaultdict(int)
    for e in entries:
        for t in e.get("scope") or []:
            if isinstance(t, str):
                tag_n[t] += 1
    for tag, n in sorted(tag_n.items(), key=lambda x: (-x[1], x[0]))[:40]:
        lines.append(f"- `{tag}`: {n}\n")
    lines.append("\n")

    lines.append("## Possible READ link gap (heuristic)\n\n")
    lines.append(
        "_Entries with `engagement_status: consumed` but no `read_id` — may warrant a READ-* "
        "link or be intentional._\n\n"
    )
    gap = [
        e
        for e in entries
        if str(e.get("engagement_status") or "").lower() == "consumed" and not e.get("read_id")
    ]
    for e in gap[:25]:
        lines.append(f"- **{e.get('id')}** — {e.get('title')}\n")
    if not gap:
        lines.append("_None matching heuristic._\n")
    elif len(gap) > 25:
        lines.append(f"\n_… {len(gap) - 25} more._\n")
    lines.append("\n")

    lines.append("## Recently touched (git mtime on `source: url` path — best effort)\n\n")
    touched: list[tuple[str, str, str]] = []
    for e in entries:
        url = e.get("url")
        if not isinstance(url, str) or not url.strip():
            continue
        rel = _url_to_repo_path(url)
        if not rel:
            continue
        ts = _git_last_commit_ts(repo_root, rel)
        if ts:
            touched.append((ts, str(e.get("id")), str(e.get("title", ""))[:60]))
    for ts, eid, title in sorted(touched, reverse=True)[:15]:
        lines.append(f"- {ts} — **{eid}** — {title}\n")
    if not touched:
        lines.append("_No git timestamps resolved (missing paths or not git repo)._ \n")

    lines.append(
        "\n## Open contradictions / review flags\n\n"
        "_Not computed in v1 — see contradiction policy and manual review._\n"
    )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build library-index.md from self-library.md entries YAML.")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    uid = args.user.strip()
    entries = load_self_library_entries(root, uid)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_markdown(entries, user_id=uid, repo_root=root, generated_at=ts)
    out = root / "artifacts" / "library-index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
