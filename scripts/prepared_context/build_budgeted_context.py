#!/usr/bin/env python3
"""
Assemble a bounded prepared-context Markdown file with explicit budget reporting.

Runtime / WORK scaffolding only — not Record truth. See docs/runtime/context-budgeting.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_RUNTIME = REPO_ROOT / "scripts" / "runtime"
_PREP = Path(__file__).resolve().parent
for _p in (_RUNTIME, _PREP):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from expand_observations import expanded_row  # noqa: E402
from lane_search import filter_rows, rank_hits  # noqa: E402
from observation_store import by_id, load_all  # noqa: E402
from policy_mode_config import (  # noqa: E402
    load_defaults as load_policy_defaults,
    policy_mode_header_lines,
    resolve_mode as resolve_policy_mode,
)
from workflow_depth_control import (  # noqa: E402
    auto_decide_format,
    depth_to_mode_and_max_obs,
    phase_anchor_blurb,
)

DEPTH_CHOICES = ("shallow", "normal", "deep", "exhaustive", "auto")

LANE_DEFAULTS = REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"
MODES = ("compact", "medium", "deep")


@dataclass(order=True)
class RankedPiece:
    sort_key: float
    label: str
    kind: str
    text: str
    meta: dict[str, Any] = field(compare=False)


def _load_budgets(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _budget_for_lane(budgets: dict[str, Any], lane: str, mode: str) -> int:
    row = budgets.get(lane) or budgets.get("default") or {}
    v = row.get(mode)
    if isinstance(v, int) and v > 0:
        return v
    d = budgets.get("default") or {}
    v2 = d.get(mode)
    if isinstance(v2, int) and v2 > 0:
        return v2
    return 2000


def _observation_rank_score(row: dict, base: float) -> float:
    s = base
    if row.get("contradiction_refs"):
        s += 0.6
    if row.get("record_mutation_candidate"):
        s += 0.35
    conf = row.get("confidence")
    if isinstance(conf, (int, float)) and conf >= 0.75:
        s += 0.15
    summ = (row.get("summary") or "") + (row.get("title") or "")
    if len(summ) > 80:
        s += 0.05
    return s


def _format_observation(row: dict, budget_class: str) -> str:
    oid = row.get("obs_id", "?")
    title = (row.get("title") or "").strip()
    summary = (row.get("summary") or "").replace("\n", " ").strip()
    if budget_class == "compact":
        if len(summary) > 160:
            summary = summary[:157] + "…"
        return f"- `{oid}` — {title}: {summary}"
    if budget_class == "medium":
        raw = by_id(str(oid))
        if raw:
            er = expanded_row(raw)
            summ = (er.get("summary") or summary)[:800]
        else:
            summ = summary[:800]
        return f"### {oid}\n**{title}**\n{summ}\n"
    raw = by_id(str(oid))
    if raw:
        er = expanded_row(raw)
        body = json.dumps(er, indent=2)[:3500]
        return f"### Observation `{oid}`\n```json\n{body}\n```\n"
    return f"### {oid}\n{summary}\n"


def _ranked_score_rows(lane: str, query: str, max_candidates: int) -> list[tuple[float, dict]]:
    rows = load_all()
    pool = filter_rows(
        rows,
        lane_eq=lane,
        source_kind=None,
        since=None,
        until=None,
        required_tags=[],
    )
    ranked = rank_hits(
        pool,
        query=query,
        bonus_tags=[],
        require_positive_match=bool(query.strip()),
    )
    return ranked[:max_candidates]


def _ranked_observation_rows(lane: str, query: str, max_candidates: int) -> list[dict]:
    """Top-ranked observation rows for metrics (contradiction density, pool size)."""
    return [row for _, row in _ranked_score_rows(lane, query, max_candidates)]


def _gather_observations(lane: str, query: str, budget_class: str, max_candidates: int) -> list[RankedPiece]:
    out: list[RankedPiece] = []
    for score, row in _ranked_score_rows(lane, query, max_candidates):
        rk = _observation_rank_score(row, score)
        text = _format_observation(row, budget_class)
        oid = str(row.get("obs_id", ""))
        out.append(
            RankedPiece(
                sort_key=-rk,
                label=f"observation `{oid}`",
                kind="runtime_observation",
                text=text,
                meta={"obs_id": oid, "rank": rk},
            )
        )
    return out


def _read_file_piece(path: Path, kind: str, label: str) -> RankedPiece | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    boost = 500.0
    if "checkpoint" in kind or "handoff" in kind:
        boost += min(50.0, path.stat().st_mtime % 1000 / 100.0)
        if "candidate likely" in text.lower():
            boost += 40.0
    short_label = path.name if path.name else label
    return RankedPiece(
        sort_key=-boost,
        label=short_label,
        kind=kind,
        text=f"### {short_label}\n```markdown\n{text.strip()}\n```\n",
        meta={"path": str(path)},
    )


def _greedy_pack(pieces: list[RankedPiece], budget: int) -> tuple[list[RankedPiece], list[RankedPiece]]:
    ordered = sorted(pieces)
    included: list[RankedPiece] = []
    excluded: list[RankedPiece] = []
    used = 0
    header_overhead = 120
    for p in ordered:
        cost = len(p.text) + header_overhead
        if used + cost <= budget:
            included.append(p)
            used += cost
        else:
            excluded.append(p)
    return included, excluded


def _compact_included_observation_rows(included: list[RankedPiece]) -> list[dict]:
    """Full observation dicts for compact pack — used by workflow depth quality guard."""
    out: list[dict] = []
    for p in included:
        if p.kind != "runtime_observation":
            continue
        oid = p.meta.get("obs_id")
        if not oid:
            continue
        raw = by_id(str(oid))
        if raw:
            out.append(raw)
    return out


def compute_benchmark_scores(
    included: list[RankedPiece],
    excluded: list[RankedPiece],
    budget: int,
) -> dict[str, float]:
    """Return deterministic quality metrics for the packing result."""
    total_candidates = len(included) + len(excluded)
    chars_included = sum(len(p.text) for p in included)
    utilization = chars_included / budget if budget > 0 else 0.0
    coverage = len(included) / total_candidates if total_candidates > 0 else 0.0
    ranks = [p.meta.get("rank", 0.0) for p in included if "rank" in p.meta]
    mean_included_rank = sum(ranks) / len(ranks) if ranks else 0.0
    return {
        "utilization": round(utilization, 4),
        "coverage": round(coverage, 4),
        "mean_included_rank": round(mean_included_rank, 4),
        "chars_included": chars_included,
        "total_candidates": total_candidates,
        "included_count": len(included),
        "excluded_count": len(excluded),
    }


def _write_receipt(
    *,
    repo_root: Path,
    lane: str,
    output: Path,
    budget_class: str,
    policy_mode: str,
    budget: int,
    exclusions: bool,
    built: str,
    scores: dict[str, float] | None = None,
) -> None:
    receipt = repo_root / "prepared-context" / "last-budget-builds.json"
    data: dict[str, Any] = {"schemaVersion": "1.0-budget-receipt", "lanes": {}}
    if receipt.is_file():
        try:
            data = json.loads(receipt.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"schemaVersion": "1.0-budget-receipt", "lanes": {}}
    if "lanes" not in data:
        data["lanes"] = {}
    try:
        rel_out = str(output.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        rel_out = str(output)
    lane_data: dict[str, Any] = {
        "path": rel_out,
        "mode": budget_class,
        "policy_mode": policy_mode,
        "budget_target": budget,
        "exclusions": exclusions,
        "built": built,
    }
    if scores:
        lane_data["scores"] = scores
    data["lanes"][lane] = lane_data
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_markdown(
    *,
    lane: str,
    budget_class: str,
    policy_mode: str,
    query: str,
    budget: int,
    included: list[RankedPiece],
    excluded: list[RankedPiece],
    built: str,
    policy_defaults_path: Path | None = None,
    task_anchor: str | None = None,
    constraint_anchor: str | None = None,
    workflow_depth_label: str | None = None,
    effective_mode_note: str | None = None,
) -> str:
    pdefs = load_policy_defaults(policy_defaults_path)
    pol = resolve_policy_mode(policy_mode, pdefs)
    pol_lines = policy_mode_header_lines(pol, pdefs)
    lines: list[str] = [
        "# Budgeted Context",
        "",
        *pol_lines,
        "",
        f"Built: {built}",
        f"Lane: {lane}",
        f"Budget class: {budget_class}",
        f"Budget target: {budget} (character estimate)",
        f"Query: {query or '(none — recency/rank only)'}",
        "",
    ]
    if task_anchor and str(task_anchor).strip():
        lines.extend(
            [
                "## Task anchor",
                "",
                f"- **Task:** {str(task_anchor).strip()}",
            ]
        )
        if constraint_anchor and str(constraint_anchor).strip():
            lines.append(f"- **Constraint:** {str(constraint_anchor).strip()}")
        if workflow_depth_label:
            lines.append(f"- **Workflow depth:** {workflow_depth_label}")
        if effective_mode_note:
            lines.append(f"- **Effective budget mode:** {effective_mode_note}")
        lines.append("")
    lines.extend(
        [
            "## Included",
            "",
        ]
    )
    if not included:
        lines.append("- _(nothing fit — raise mode or narrow inputs)_")
    else:
        kinds: dict[str, int] = {}
        for p in included:
            kinds[p.kind] = kinds.get(p.kind, 0) + 1
        for p in included:
            lines.append(f"- {p.label} ({p.kind})")
        lines.append("")
        lines.append(f"_Counts: {', '.join(f'{k}: {v}' for k, v in sorted(kinds.items()))}_")
    lines.extend(["", "## Excluded"])
    if not excluded:
        lines.append("- _(none — full rank fit within budget)_")
    else:
        lines.append("- Items below were **not** included (budget pressure or lower rank).")
        for p in excluded[:24]:
            lines.append(f"- {p.label} ({p.kind})")
        if len(excluded) > 24:
            lines.append(f"- … and {len(excluded) - 24} more (lower rank)")
    lines.extend(
        [
            "",
            "## Context Block",
            "",
        ]
    )
    for p in included:
        lines.append(p.text)
        lines.append("")
    lines.extend(
        [
            "## Budget Notes",
            "",
            f"- Budget class **{budget_class}** prioritizes recent, high-rank observations and explicit file includes.",
            f"- Policy mode **{pol}** governs staging/abstention posture — see `docs/policy-modes.md`.",
            "- Older or lower-ranked observations may be omitted even when relevant — rerun in **medium** or **deep** if needed.",
            "- Budgeting does **not** replace abstention checks, gate review, or Record merge discipline.",
            "",
            "## Boundary reminder",
            "This file is runtime / WORK scaffolding only.",
            "It does not update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE.",
        ]
    )
    return "\n".join(lines) + "\n"


def _utc_run_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h = hashlib.sha256(f"{ts}:{uuid.uuid4().hex}".encode()).hexdigest()[:12]
    return f"wd_{ts}_{h}"


def _workflow_depth_root(repo_root: Path) -> Path:
    raw = os.environ.get("GRACE_MAR_WORKFLOW_DEPTH_HOME", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (repo_root / "runtime" / "workflow-depth").resolve()


def _append_workflow_depth_receipt(repo_root: Path, record: dict[str, Any]) -> Path:
    wd = _workflow_depth_root(repo_root)
    wd.mkdir(parents=True, exist_ok=True)
    idx = wd / "index.jsonl"
    with idx.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return idx


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build budgeted prepared-context Markdown with inclusion/exclusion report.",
    )
    ap.add_argument("--lane", required=True, help="Work lane (exact string)")
    ap.add_argument(
        "--mode",
        default=None,
        choices=MODES,
        help="Budget class: compact | medium | deep (required unless --workflow-depth / --depth is set)",
    )
    ap.add_argument(
        "--workflow-depth",
        "--depth",
        dest="workflow_depth",
        default=None,
        choices=DEPTH_CHOICES,
        metavar="MODE",
        help=(
            "Adaptive workflow depth (shallow|normal|deep|exhaustive|auto); alias --depth; "
            "requires --task-anchor; ignores --mode"
        ),
    )
    ap.add_argument(
        "--task-anchor",
        default="",
        help="Original operator task (required with --workflow-depth or --depth); reinjected into output and receipts",
    )
    ap.add_argument(
        "--constraint-anchor",
        default="",
        help="Optional constraint line (scope, abstention, format) — WORK only",
    )
    ap.add_argument("--query", "-q", default="", help="Optional search query for ranking observations")
    ap.add_argument("--output", "-o", type=Path, required=True, help="Output Markdown path")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--budgets-file",
        type=Path,
        default=LANE_DEFAULTS,
        help="Path to lane-defaults.json",
    )
    ap.add_argument(
        "--include-memory-brief",
        type=Path,
        default=None,
        help="Optional memory brief .md to include (high priority)",
    )
    ap.add_argument(
        "--include-checkpoint",
        type=Path,
        action="append",
        default=[],
        metavar="PATH",
        help="Checkpoint .md (repeatable)",
    )
    ap.add_argument(
        "--include-handoff",
        type=Path,
        action="append",
        default=[],
        metavar="PATH",
        help="Handoff packet .md (repeatable)",
    )
    ap.add_argument(
        "--include-mission",
        type=Path,
        action="append",
        default=[],
        metavar="PATH",
        help="Mission workspace .md (WORK; same priority as checkpoint; labeled mission_workspace)",
    )
    ap.add_argument(
        "--max-observations",
        type=int,
        default=None,
        metavar="N",
        help="Max observation candidates to rank (default: 30, or depth preset for --workflow-depth / --depth)",
    )
    ap.add_argument(
        "--policy-mode",
        default=None,
        help="Policy envelope (default: GRACE_MAR_POLICY_MODE or operator_only); see docs/policy-modes.md",
    )
    ap.add_argument(
        "--policy-defaults",
        type=Path,
        default=None,
        help="Optional path to policy_modes defaults.json (default: config/policy_modes/defaults.json)",
    )
    ap.add_argument(
        "--score",
        action="store_true",
        default=False,
        help="Print benchmark quality scores (utilization, coverage, mean_included_rank) to stdout as JSON",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    lane = args.lane.strip()
    wf_depth = args.workflow_depth
    task_anchor = (args.task_anchor or "").strip()
    constraint_anchor = (args.constraint_anchor or "").strip()

    if wf_depth and not task_anchor:
        print(
            "error: --task-anchor is required when --workflow-depth or --depth is set",
            file=sys.stderr,
        )
        return 2
    if not wf_depth and args.mode is None:
        print(
            "error: --mode is required when neither --workflow-depth nor --depth is set",
            file=sys.stderr,
        )
        return 2
    if wf_depth and args.mode is not None:
        print(
            "notice: --mode ignored when --workflow-depth or --depth is set",
            file=sys.stderr,
        )

    policy_defaults_path = args.policy_defaults.resolve() if args.policy_defaults else None
    pdefs = load_policy_defaults(policy_defaults_path)
    policy_resolved = resolve_policy_mode(args.policy_mode, pdefs)
    budgets = _load_budgets(args.budgets_file.resolve())

    pieces: list[RankedPiece] = []
    if args.include_memory_brief:
        rp = _read_file_piece(
            args.include_memory_brief.resolve(),
            "memory_brief",
            str(args.include_memory_brief),
        )
        if rp:
            pieces.append(rp)
    for cp in args.include_checkpoint:
        rp = _read_file_piece(cp.resolve(), "checkpoint", str(cp))
        if rp:
            pieces.append(rp)
    for hp in args.include_handoff:
        rp = _read_file_piece(hp.resolve(), "handoff", str(hp))
        if rp:
            pieces.append(rp)
    for mp in args.include_mission:
        rp = _read_file_piece(mp.resolve(), "mission_workspace", str(mp))
        if rp:
            pieces.append(rp)

    run_id = _utc_run_id()
    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    phases_log: list[dict[str, Any]] = []
    stop_reason = ""
    budget_class: str
    max_obs: int
    receipt_extra: dict[str, Any] | None = None

    if not wf_depth:
        budget_class = args.mode.strip()  # type: ignore[union-attr]
        max_obs = args.max_observations if args.max_observations is not None else 30
        pieces.extend(_gather_observations(lane, args.query, budget_class, max_obs))
        budget = _budget_for_lane(budgets, lane, budget_class)
        included, excluded = _greedy_pack(pieces, budget)
        scores = compute_benchmark_scores(included, excluded, budget)
        md = build_markdown(
            lane=lane,
            budget_class=budget_class,
            policy_mode=args.policy_mode or "",
            query=args.query,
            budget=budget,
            included=included,
            excluded=excluded,
            built=built,
            policy_defaults_path=policy_defaults_path,
        )
    elif wf_depth != "auto":
        dm, depth_max_obs = depth_to_mode_and_max_obs(wf_depth)  # type: ignore[arg-type]
        budget_class = dm
        max_obs = args.max_observations if args.max_observations is not None else depth_max_obs
        phases_log.append(
            {
                "phase": "phase_1_retrieval",
                "halt_continue": "continue",
                "summary": phase_anchor_blurb("phase_1_retrieval", task_anchor),
            }
        )
        phases_log.append(
            {
                "phase": "phase_2_metrics",
                "halt_continue": "skip",
                "summary": "fixed workflow depth — auto metrics not used",
            }
        )
        phases_log.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "skip",
                "summary": f"using mapped mode {budget_class} (depth={wf_depth})",
            }
        )
        pieces.extend(_gather_observations(lane, args.query, budget_class, max_obs))
        budget = _budget_for_lane(budgets, lane, budget_class)
        included, excluded = _greedy_pack(pieces, budget)
        scores = compute_benchmark_scores(included, excluded, budget)
        stop_reason = f"fixed_{wf_depth}"
        phases_log.append(
            {
                "phase": "phase_4_pack_emit",
                "halt_continue": "continue",
                "summary": "packed and emitted markdown",
            }
        )
        md = build_markdown(
            lane=lane,
            budget_class=budget_class,
            policy_mode=args.policy_mode or "",
            query=args.query,
            budget=budget,
            included=included,
            excluded=excluded,
            built=built,
            policy_defaults_path=policy_defaults_path,
            task_anchor=task_anchor,
            constraint_anchor=constraint_anchor or None,
            workflow_depth_label=str(wf_depth),
            effective_mode_note=f"{budget_class} (max_obs={max_obs})",
        )
        receipt_extra = {
            "run_id": run_id,
            "workflow_depth": wf_depth,
            "phases": phases_log,
            "stop_reason": stop_reason,
            "task_anchor": task_anchor,
            "constraint_anchor": constraint_anchor or None,
            "lane": lane,
            "effective_mode": budget_class,
            "max_observations": max_obs,
        }
    else:
        # auto
        max_obs = args.max_observations if args.max_observations is not None else 30
        pool_rows = _ranked_observation_rows(lane, args.query, max_obs)
        phases_log.append(
            {
                "phase": "phase_1_retrieval",
                "halt_continue": "continue",
                "summary": phase_anchor_blurb("phase_1_retrieval", task_anchor)
                + f" — ranked {len(pool_rows)} observation row(s)",
            }
        )
        obs_compact = _gather_observations(lane, args.query, "compact", max_obs)
        pieces_auto = pieces + obs_compact
        budget_try = _budget_for_lane(budgets, lane, "compact")
        inc_try, exc_try = _greedy_pack(pieces_auto, budget_try)
        scores_try = compute_benchmark_scores(inc_try, exc_try, budget_try)
        compact_included_rows = _compact_included_observation_rows(inc_try)
        mode_auto, stop_reason, phase_metrics, guard_receipt = auto_decide_format(
            query=args.query,
            pool_rows=pool_rows,
            compact_scores=scores_try,
            task_anchor=task_anchor,
            compact_included_rows=compact_included_rows,
        )
        for p in phase_metrics:
            phases_log.append(dict(p))
        budget_class = mode_auto
        if mode_auto == "compact":
            included, excluded = inc_try, exc_try
            budget = budget_try
            scores = scores_try
        else:
            obs_final = _gather_observations(lane, args.query, mode_auto, max_obs)
            pieces_f = pieces + obs_final
            budget = _budget_for_lane(budgets, lane, budget_class)
            included, excluded = _greedy_pack(pieces_f, budget)
            scores = compute_benchmark_scores(included, excluded, budget)
        phases_log.append(
            {
                "phase": "phase_4_pack_emit",
                "halt_continue": "continue",
                "summary": "final pack at effective mode "
                + f"{budget_class} (stop_reason={stop_reason})",
            }
        )
        md = build_markdown(
            lane=lane,
            budget_class=budget_class,
            policy_mode=args.policy_mode or "",
            query=args.query,
            budget=budget,
            included=included,
            excluded=excluded,
            built=built,
            policy_defaults_path=policy_defaults_path,
            task_anchor=task_anchor,
            constraint_anchor=constraint_anchor or None,
            workflow_depth_label="auto",
            effective_mode_note=f"{budget_class} (auto — {stop_reason})",
        )
        receipt_extra = {
            "run_id": run_id,
            "workflow_depth": "auto",
            "phases": phases_log,
            "stop_reason": stop_reason,
            "task_anchor": task_anchor,
            "constraint_anchor": constraint_anchor or None,
            "lane": lane,
            "effective_mode": budget_class,
            "max_observations": max_obs,
            "compact_dry_scores": scores_try,
            **guard_receipt,
        }

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    _write_receipt(
        repo_root=root,
        lane=lane,
        output=out,
        budget_class=budget_class,
        policy_mode=policy_resolved,
        budget=budget,
        exclusions=bool(excluded),
        built=built,
        scores=scores,
    )
    print(f"wrote {out}", file=sys.stderr)
    print(f"wrote {root / 'prepared-context' / 'last-budget-builds.json'}", file=sys.stderr)
    if wf_depth and receipt_extra:
        rec = {
            "schemaVersion": "1.0-workflow-depth-receipt",
            "status": "ok",
            "timestamp": built,
            "boundary_notes": [
                "non_canonical",
                "runtime_workflow_depth_receipt_not_record_truth",
            ],
            "output_markdown": str(out.resolve().relative_to(root)) if out.resolve().is_relative_to(root) else str(out),
            "scores": scores,
            **receipt_extra,
        }
        idxp = _append_workflow_depth_receipt(root, rec)
        print(f"wrote workflow-depth receipt {idxp}", file=sys.stderr)
    if args.score:
        print(json.dumps({"lane": lane, "mode": budget_class, **scores}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
