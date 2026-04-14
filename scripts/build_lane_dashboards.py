#!/usr/bin/env python3
"""
Emit artifacts/lane-dashboards/README.md — compose runtime observations + lane JSON artifacts.

Optional: artifacts/work-lanes-dashboard.json from scripts/build_work_lanes_dashboard.py.
Does not mutate Record or runtime ledger.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = _SCRIPTS / "runtime"
for p in (_SCRIPTS, _RUNTIME):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from ledger_paths import observations_jsonl  # noqa: E402


def _load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def render_markdown(
    *,
    by_lane: dict[str, list[dict]],
    work_lanes_doc: dict | None,
    generated_at: str,
    ledger_path: Path,
) -> str:
    lines: list[str] = [
        "<!-- GENERATED — run: python3 scripts/build_lane_dashboards.py -->\n\n",
        "# Lane dashboards (aggregate)\n\n",
        "**Derived operator artifact.** Work territories do not redefine the Record; this file "
        "only surfaces runtime + WORK telemetry for navigation.\n\n",
        f"- **Generated:** {generated_at}\n",
        f"- **Ledger:** `{ledger_path}` "
        f"({'present' if ledger_path.is_file() else 'missing — no runtime observations yet'})\n\n",
    ]
    if work_lanes_doc:
        lines.append("## work-lanes-dashboard.json snapshot\n\n")
        lines.append("From `artifacts/work-lanes-dashboard.json` (run `build_work_lanes_dashboard.py` first). \n\n")
        lines.append("```json\n")
        lines.append(json.dumps(work_lanes_doc, indent=2)[:8000])
        if len(json.dumps(work_lanes_doc)) > 8000:
            lines.append("\n… truncated …\n")
        lines.append("\n```\n\n")
    else:
        lines.append(
            "## work-lanes-dashboard.json\n\n"
            "_Missing — run `python3 scripts/build_work_lanes_dashboard.py` to populate "
            "`artifacts/work-lanes-dashboard.json`._\n\n"
        )

    lines.append("## Runtime observations by lane (recent)\n\n")
    if not by_lane:
        lines.append(
            "_No observations in ledger._ Operator: `python3 scripts/runtime/log_observation.py --help`\n\n"
        )
    else:
        for lane in sorted(by_lane.keys()):
            rows = sorted(
                by_lane[lane],
                key=lambda r: str(r.get("timestamp") or ""),
                reverse=True,
            )[:12]
            lines.append(f"### {lane}\n\n")
            for r in rows:
                oid = r.get("obs_id", "")
                title = str(r.get("title", ""))[:100]
                ts = r.get("timestamp", "")
                sk = r.get("source_kind", "")
                lines.append(f"- `{ts}` **{oid}** ({sk}) — {title}\n")
            lines.append("\n")

    lines.append(
        "## Active lane compression / context memos\n\n"
        "_`artifacts/context/` is gitignored by default — regenerate with "
        "`scripts/compress_active_lane.py`. Listing skipped here._\n\n"
    )
    lines.append(
        "## Per-lane split (future)\n\n"
        "Optional follow-up: `artifacts/lane-dashboards/work-strategy.md` from the same inputs.\n"
    )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build lane-dashboards README under artifacts/.")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    ledger = observations_jsonl()
    rows = _load_jsonl(ledger)
    by_lane: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        lane = str(r.get("lane") or "unknown")
        by_lane[lane].append(r)

    wl_path = root / "artifacts" / "work-lanes-dashboard.json"
    work_lanes: dict | None = None
    if wl_path.is_file():
        try:
            work_lanes = json.loads(wl_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            work_lanes = None

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_markdown(
        by_lane=by_lane,
        work_lanes_doc=work_lanes,
        generated_at=ts,
        ledger_path=ledger,
    )
    out_dir = root / "artifacts" / "lane-dashboards"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "README.md"
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
