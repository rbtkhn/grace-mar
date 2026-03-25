#!/usr/bin/env python3
"""
Aggregate work-dev observability signals into JSON + Markdown artifacts.

Inputs: control-plane YAML, optional pipeline-events.jsonl for a user,
runtime/observability feeds, optional recursion-gate.md pending candidates.
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

from gate_block_parser import mean_pending_provenance_from_path  # noqa: E402

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


def count_jsonl_events(path: Path, *, event_name: str | None = None) -> int:
    """Count JSONL lines; optional filter by object['event']. Malformed lines skipped."""
    if not path.is_file():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event_name is None:
            n += 1
        elif o.get("event") == event_name:
            n += 1
    return n


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
    """Heuristic 0..1 from staged vs invalid_candidate pipeline events."""
    staged = int(events.get("staged", 0))
    invalid = int(events.get("invalid_candidate", 0))
    if staged == 0:
        return 1.0
    return max(0.0, min(1.0, 1.0 - (invalid / max(staged, 1))))


def _candidates_section(gate_text: str) -> str:
    if "## Candidates" not in gate_text or "## Processed" not in gate_text:
        return ""
    start = gate_text.index("## Candidates")
    end = gate_text.index("## Processed", start)
    return gate_text[start:end]


def _pending_yaml_blocks(section: str) -> list[str]:
    blocks: list[str] = []
    for m in re.finditer(r"```yaml\n(.*?)```", section, re.DOTALL | re.IGNORECASE):
        blob = m.group(1)
        if re.search(r"^status:\s*pending\s*$", blob, re.MULTILINE):
            blocks.append(blob)
    return blocks


def _yaml_block_provenance_fraction(blob: str) -> float:
    has_source = bool(re.search(r"^candidate_source:\s*\S", blob, re.MULTILINE))
    has_path = bool(re.search(r"^artifact_path:\s*\S", blob, re.MULTILINE))
    has_sha = bool(re.search(r"^artifact_sha256:\s*\S", blob, re.MULTILINE))
    has_receipt = bool(re.search(r"^continuity_receipt_path:\s*\S", blob, re.MULTILINE))
    has_const = bool(
        re.search(r"^constitution_check_status:\s*\S", blob, re.MULTILINE)
        or re.search(r"^constitution_rule_ids:\s*\S", blob, re.MULTILINE)
    )
    parts = [has_source, has_path, has_sha, has_receipt, has_const]
    return sum(1 for x in parts if x) / len(parts)


def provenance_score_from_recursion_gate(gate_path: Path) -> float | None:
    """Mean provenance completeness over pending ```yaml blocks; None if no pending candidates."""
    if not gate_path.is_file():
        return None
    text = gate_path.read_text(encoding="utf-8")
    section = _candidates_section(text)
    blocks = _pending_yaml_blocks(section)
    if not blocks:
        return None
    return sum(_yaml_block_provenance_fraction(b) for b in blocks) / len(blocks)


def build_dashboard(*, user_id: str, repo_root: Path) -> DashboardSummary:
    cp = repo_root / "docs" / "skill-work" / "work-dev" / "control-plane"
    pe = repo_root / "users" / user_id / "pipeline-events.jsonl"
    obs = repo_root / "runtime" / "observability"
    gate_path = repo_root / "users" / user_id / "recursion-gate.md"

    integ = _count_integration_status(cp)
    pe_counts = _count_pipeline_events(pe)
    lane_n = count_jsonl_events(obs / "lane_scope.jsonl", event_name="lane_violation")
    cont_n = count_jsonl_events(obs / "continuity_blocks.jsonl", event_name="continuity_block")

    gate_score = mean_pending_provenance_from_path(gate_path)
    if gate_score is not None:
        prov = gate_score
        from_gate = True
    else:
        prov = _provenance_score_from_events(pe_counts)
        from_gate = False

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    notes = [
        "Lane / continuity counts come from runtime/observability/*.jsonl when present (local or CI); empty feeds => 0.",
        "Regenerate after editing control-plane YAML.",
    ]
    return DashboardSummary(
        generated_at=ts,
        integration_status_counts=integ,
        pipeline_event_counts=pe_counts,
        provenance_completeness_score=prov,
        provenance_from_gate=from_gate,
        lane_violation_count=lane_n,
        continuity_block_count=cont_n,
        gap_ids_open=_open_gap_ids(cp),
        notes=notes,
    )


def render_markdown(d: DashboardSummary) -> str:
    prov_label = (
        "recursion gate (pending candidates)" if d.provenance_from_gate else "pipeline-events proxy"
    )
    lines = [
        "<!-- GENERATED — run: python scripts/work_dev/build_dashboard.py -->\n\n",
        "# work-dev dashboard\n\n",
        f"- **Generated:** `{d.generated_at}`\n\n",
        "## Reliability\n\n",
        f"- Provenance completeness ({prov_label}): **{d.provenance_completeness_score:.2f}**\n\n",
        "## Boundary health\n\n",
        f"- Open gap IDs: {', '.join(d.gap_ids_open) or '_(none)_'}\n",
        f"- Lane violation count (observability feed): {d.lane_violation_count}\n",
        f"- Continuity block count (observability feed): {d.continuity_block_count}\n\n",
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
