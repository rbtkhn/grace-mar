#!/usr/bin/env python3
"""
Emit artifacts/lane-dashboards/README.md — compose runtime observations + lane JSON artifacts.

Optional: artifacts/work-lanes-dashboard.json from scripts/build_work_lanes_dashboard.py.
Does not mutate Record or runtime ledger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _ledger_path_for_root(root: Path) -> Path:
    return root / "runtime" / "observations" / "index.jsonl"


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


def _parse_lane_from_checkpoint_body(text: str) -> str | None:
    for line in text.splitlines():
        if line.strip().startswith("Lane:"):
            return line.split("Lane:", 1)[1].strip()
    return None


def _scan_handoffs_markdown(
    *,
    root: Path,
    by_lane: dict[str, list[dict]],
    work_lanes_doc: dict | None,
) -> str:
    """Long-horizon checkpoints + handoff packets (runtime-only)."""
    handoffs_root = root / "artifacts" / "handoffs"
    ck_dir = handoffs_root / "checkpoints"
    lanes: set[str] = set(by_lane.keys())
    if work_lanes_doc and isinstance(work_lanes_doc.get("lanes"), dict):
        for _k, blob in work_lanes_doc["lanes"].items():
            if isinstance(blob, dict) and blob.get("lane"):
                lanes.add(str(blob["lane"]))

    latest_cp: dict[str, tuple[Path, float]] = {}
    if ck_dir.is_dir():
        for p in ck_dir.glob("*.md"):
            try:
                body = p.read_text(encoding="utf-8")
                lane = _parse_lane_from_checkpoint_body(body)
                if not lane:
                    continue
                lanes.add(lane)
                try:
                    mtime = p.stat().st_mtime
                except OSError:
                    mtime = 0.0
                prev = latest_cp.get(lane)
                if prev is None or mtime > prev[1]:
                    latest_cp[lane] = (p, mtime)
            except OSError:
                continue

    last_handoff: dict[str, tuple[Path, float]] = {}
    if handoffs_root.is_dir():
        for p in handoffs_root.glob("*.md"):
            try:
                head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:24])
                lane = None
                for line in head.splitlines():
                    if line.strip().startswith("Lane:"):
                        lane = line.split("Lane:", 1)[1].strip()
                        break
                if not lane:
                    continue
                lanes.add(lane)
                try:
                    mtime = p.stat().st_mtime
                except OSError:
                    mtime = 0.0
                prev = last_handoff.get(lane)
                if prev is None or mtime > prev[1]:
                    last_handoff[lane] = (p, mtime)
            except OSError:
                continue

    lines: list[str] = [
        "## Long-horizon checkpoints and handoffs\n\n",
        "**Runtime work layer** — not Record. See `docs/runtime/long-horizon-work.md`. "
        "Heuristics below are **legibility hints** for operators.\n\n",
        "- **Stale (idle):** latest checkpoint file mtime older than **7 days**.\n",
        "- **Stale (drift):** newest runtime observation for the lane is **newer** than the checkpoint "
        "`Built:` timestamp (parsed when present; else file mtime).\n\n",
    ]

    if not lanes:
        lines.append("_No lanes from ledger or checkpoints yet._\n\n")
        return "".join(lines)

    now_ts = datetime.now(timezone.utc).timestamp()
    stale_idle_s = 7 * 24 * 3600

    for lane in sorted(lanes):
        lines.append(f"### {lane}\n\n")
        cp_t = latest_cp.get(lane)
        ho_t = last_handoff.get(lane)
        if cp_t:
            cp_path, cp_mtime = cp_t
            try:
                rel_cp = cp_path.relative_to(root)
            except ValueError:
                rel_cp = cp_path
            lines.append(f"- **Latest checkpoint:** `{rel_cp}`\n")
            built = None
            try:
                for bl in cp_path.read_text(encoding="utf-8").splitlines():
                    if bl.strip().startswith("Built:"):
                        built = bl.split("Built:", 1)[1].strip()
                        break
            except OSError:
                built = None
            idle = (now_ts - cp_mtime) > stale_idle_s
            obs_rows = by_lane.get(lane, [])
            obs_newer = False
            if obs_rows and built:
                newest_obs = max((str(r.get("timestamp") or "") for r in obs_rows), default="")
                if newest_obs and newest_obs > built:
                    obs_newer = True
            elif obs_rows and not built:
                obs_newer = True
            flags = []
            if idle:
                flags.append("stale_idle")
            if obs_newer:
                flags.append("stale_drift")
            if flags:
                lines.append(f"- **Review:** {', '.join(flags)} — consider a fresh `checkpoint_session.py` pass.\n")
            else:
                lines.append("- **Review:** ok (heuristic)\n")
        else:
            lines.append("- **Latest checkpoint:** _none_\n")
            if by_lane.get(lane):
                lines.append(
                    "- **Review:** stale_drift — observations exist without a lane checkpoint; consider `checkpoint_session.py`.\n"
                )
            else:
                lines.append("- **Review:** _n/a_\n")

        if ho_t:
            ho_path, _ = ho_t
            try:
                rel_ho = ho_path.relative_to(root)
            except ValueError:
                rel_ho = ho_path
            lines.append(f"- **Last handoff packet:** `{rel_ho}`\n")
        else:
            lines.append("- **Last handoff packet:** _none_\n")
        lines.append("\n")

    return "".join(lines)


def _scan_budget_builds(root: Path) -> str:
    path = root / "prepared-context" / "last-budget-builds.json"
    lines: list[str] = [
        "## Context efficiency (budgeted builds)\n\n",
        "Per-lane receipts from `build_budgeted_context.py`. Not Record truth — see "
        "[`docs/runtime/context-budgeting.md`](../../docs/runtime/context-budgeting.md).\n\n",
    ]
    if not path.is_file():
        lines.append(
            "_No receipt yet._ Run `python3 scripts/prepared_context/build_budgeted_context.py` after lane work.\n\n"
        )
        return "".join(lines)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        lines.append("_Receipt present but not valid JSON._\n\n")
        return "".join(lines)
    lanes = data.get("lanes") if isinstance(data, dict) else None
    if not lanes:
        lines.append("_Empty receipt._\n\n")
        return "".join(lines)
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    lines.append(f"- **Receipt file:** `{rel}`\n\n")
    for lane in sorted(lanes.keys()):
        blob = lanes[lane]
        if not isinstance(blob, dict):
            continue
        mode = blob.get("mode", "")
        built = blob.get("built", "")
        exc = blob.get("exclusions", False)
        out_p = blob.get("path", "")
        bt = blob.get("budget_target", "")
        lines.append(f"### {lane}\n\n")
        lines.append(f"- **Last build:** `{out_p}`\n")
        pol = blob.get("policy_mode", "")
        lines.append(f"- **Budget class:** `{mode}` — **budget target (chars):** `{bt}`\n")
        if pol:
            lines.append(f"- **Policy mode:** `{pol}`\n")
        lines.append(f"- **Built:** {built}\n")
        lines.append(f"- **Exclusions occurred:** {'yes' if exc else 'no'}\n\n")
    return "".join(lines)


def render_markdown(
    *,
    by_lane: dict[str, list[dict]],
    work_lanes_doc: dict | None,
    generated_at: str,
    ledger_path: Path,
    root: Path,
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

    lines.append(
        _scan_handoffs_markdown(root=root, by_lane=by_lane, work_lanes_doc=work_lanes_doc)
    )

    lines.append(_scan_budget_builds(root))

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
    ledger = _ledger_path_for_root(root)
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
        root=root,
    )
    out_dir = root / "artifacts" / "lane-dashboards"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "README.md"
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
