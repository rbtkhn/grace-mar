#!/usr/bin/env python3
"""Summarize recent strategy runs into a markdown report (WORK only)."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_ROOT = Path(os.environ.get("STRATEGY_RUN_ARTIFACT_ROOT", str(REPO_ROOT))).resolve()
RUNS = ARTIFACT_ROOT / "artifacts" / "strategy-runs"
REPORT = ARTIFACT_ROOT / "artifacts" / "strategy-run-report.md"


def _has_file(path: str | None) -> bool:
    if not path or not isinstance(path, str):
        return False
    p = ARTIFACT_ROOT / path
    return p.is_file()


def _load_states(limit: int | None) -> list[tuple[Path, dict]]:
    if not RUNS.is_dir():
        return []
    rows: list[tuple[Path, dict, float]] = []
    for d in sorted(RUNS.iterdir(), key=lambda p: p.name, reverse=True):
        if not d.is_dir():
            continue
        sp = d / "state.json"
        if not sp.is_file():
            continue
        try:
            st = json.loads(sp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        m = sp.stat().st_mtime
        rows.append((sp, st, m))
    rows.sort(key=lambda x: -x[2])
    if limit is not None:
        rows = rows[:limit]
    return [(a, b) for a, b, _ in rows]


def _blocked_status(st: str) -> str:
    if st == "blocked_for_review":
        return "yes"
    if st == "completed":
        return "no"
    return "—"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Max runs to include (newest by state.json mtime)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=REPORT,
        help="Output markdown path",
    )
    args = ap.parse_args()
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    pairs = _load_states(args.limit)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = [
        "<!-- strategy-run-report: derived; not SSOT; see docs/run-contract.md -->",
        "",
        "# Strategy run report (derived)",
        "",
        f"Generated: `{now}` (UTC). Source: `artifacts/strategy-runs/*/state.json`.",
        "",
        "| run_id | target_date | intent | status | day proposal | page proposal | blocked? |",
        "|--------|-------------|--------|--------|--------------|---------------|----------|",
    ]
    for _sp, st in pairs:
        rid = st.get("run_id", "")
        td = st.get("target_date", "")
        intent = st.get("intent", "")
        status = st.get("status", "")
        po = st.get("proposed_outputs") or {}
        dpath = po.get("day_proposal_path")
        ppath = po.get("page_proposal_path")
        day = "yes" if _has_file(dpath) else "no"
        page = "yes" if _has_file(ppath) else "no"
        blk = _blocked_status(str(status))
        lines.append(
            f"| `{rid}` | {td} | {intent} | {status} | {day} | {page} | {blk} |"
        )
    if not pairs:
        lines.append("| *none* | — | — | — | — | — | — |")
    lines.append("")
    lines.append("Rebuild: `python3 scripts/build_strategy_run_report.py`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        print(out.relative_to(ARTIFACT_ROOT))
    except ValueError:
        print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
