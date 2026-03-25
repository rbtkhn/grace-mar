#!/usr/bin/env python3
"""
Aggregate work-dev observability signals into JSON + Markdown artifacts.

Inputs: control-plane YAML, optional pipeline-events.jsonl for a user.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from work_dev.dashboard_models import DashboardSummary  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _count_integration_status(control_plane: Path) -> dict[str, int]:
    p = control_plane / "integration_status.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    c: Counter[str] = Counter()
    for it in data.get("items") or []:
        st = str(it.get("status") or "unknown")
        c[st] += 1
    return dict(c)


def _count_pipeline_events(path: Path) -> dict[str, int]:
    if not path.is_file():
        return {}
    c: Counter[str] = Counter()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = o.get("event")
        if isinstance(ev, str):
            c[ev] += 1
    return dict(c)


def _open_gap_ids(control_plane: Path) -> list[str]:
    p = control_plane / "known_gaps.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    out: list[str] = []
    for g in data.get("items") or []:
        if str(g.get("status") or "") == "open":
            gid = g.get("id")
            if isinstance(gid, str):
                out.append(gid)
    return sorted(out)


def _provenance_score_from_events(events: dict[str, int]) -> float:
    """Heuristic 0..1 from staged events (proxy until full gate parse)."""
    staged = int(events.get("staged", 0))
    invalid = int(events.get("invalid_candidate", 0))
    if staged == 0:
        return 1.0
    return max(0.0, min(1.0, 1.0 - (invalid / max(staged, 1))))


def build_dashboard(*, user_id: str, repo_root: Path) -> DashboardSummary:
    cp = repo_root / "docs" / "skill-work" / "work-dev" / "control-plane"
    pe = repo_root / "users" / user_id / "pipeline-events.jsonl"
    integ = _count_integration_status(cp)
    pe_counts = _count_pipeline_events(pe)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return DashboardSummary(
        generated_at=ts,
        integration_status_counts=integ,
        pipeline_event_counts=pe_counts,
        provenance_completeness_score=_provenance_score_from_events(pe_counts),
        lane_violation_count=0,
        continuity_block_count=0,
        gap_ids_open=_open_gap_ids(cp),
        notes=[
            "Lane violations and continuity blocks require CI/runtime feeds; scores are partial.",
            "Regenerate after editing control-plane YAML.",
        ],
    )


def render_markdown(d: DashboardSummary) -> str:
    lines = [
        "<!-- GENERATED — run: python scripts/work_dev/build_dashboard.py -->\n\n",
        "# work-dev dashboard\n\n",
        f"- **Generated:** `{d.generated_at}`\n\n",
        "## Reliability\n\n",
        f"- Provenance score (pipeline proxy): **{d.provenance_completeness_score:.2f}**\n\n",
        "## Boundary health\n\n",
        f"- Open gap IDs: {', '.join(d.gap_ids_open) or '_(none)_'}\n",
        f"- Lane violation count (placeholder): {d.lane_violation_count}\n\n",
        "## Gate throughput (pipeline events)\n\n",
    ]
    for k, v in sorted(d.pipeline_event_counts.items()):
        lines.append(f"- `{k}`: {v}\n")
    if not d.pipeline_event_counts:
        lines.append("- _(no pipeline-events.jsonl or empty)_\n")
    lines.append("\n## Integration status mix\n\n")
    for k, v in sorted(d.integration_status_counts.items()):
        lines.append(f"- `{k}`: {v}\n")
    lines.append("\n## Notes\n\n")
    for n in d.notes:
        lines.append(f"- {n}\n")
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build work-dev dashboard artifacts.")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    d = build_dashboard(user_id=args.user.strip(), repo_root=root)
    art = root / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    (art / "work_dev_dashboard.json").write_text(
        json.dumps(d.to_json_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    (art / "work_dev_dashboard.md").write_text(render_markdown(d), encoding="utf-8")
    gen = root / "docs" / "skill-work" / "work-dev" / "generated"
    gen.mkdir(parents=True, exist_ok=True)
    (gen / "dashboard.md").write_text(render_markdown(d), encoding="utf-8")
    print("build_dashboard: OK -> artifacts/work_dev_dashboard.{json,md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
