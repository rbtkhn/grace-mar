"""
Shared workflow depth routing contract (WORK / runtime only — not Record truth).

See docs/runtime/workflow-depth-contract.md
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

# Canonical operator-facing depth presets (aligned with CLI).
DEPTH_CHOICES: tuple[str, ...] = ("shallow", "normal", "deep", "exhaustive", "auto")
DepthPreset = Literal["shallow", "normal", "deep", "exhaustive", "auto"]
BudgetClass = Literal["compact", "medium", "deep"]


def fixed_depth_to_budget_and_max_obs(depth: DepthPreset) -> tuple[BudgetClass, int]:
    """Map a fixed depth preset to lane budget class and default max observation candidates."""
    if depth == "shallow":
        return "compact", 30
    if depth == "normal":
        return "medium", 30
    if depth == "deep":
        return "deep", 30
    if depth == "exhaustive":
        return "deep", 48
    raise ValueError(f"fixed_depth_to_budget_and_max_obs expects fixed preset, got {depth!r}")


def workflow_depth_root(repo_root: Path) -> Path:
    raw = os.environ.get("GRACE_MAR_WORKFLOW_DEPTH_HOME", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (repo_root / "runtime" / "workflow-depth").resolve()


def append_workflow_depth_receipt(repo_root: Path, record: dict[str, Any]) -> Path:
    """Append one JSON object as a line to workflow-depth index (append-only)."""
    wd = workflow_depth_root(repo_root)
    wd.mkdir(parents=True, exist_ok=True)
    idx = wd / "index.jsonl"
    with idx.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return idx


@dataclass
class WorkflowDepthDecision:
    """Routing decision for receipts and cross-script parity."""

    initial_depth: str
    final_depth: str
    budget_class: str
    lane: str
    task_anchor: str
    constraint: str | None = None
    operator_override: bool = False
    escalated: bool = False
    escalation_reason: str = ""
    halt_reason: str = ""
    rationale: str = ""
    source_workflow: str = "prepared_context"
    estimated_load: str | float | None = None
    retrieval_miss_count: int | None = None

def decision_from_fixed(
    *,
    preset: DepthPreset,
    lane: str,
    task_anchor: str,
    constraint: str | None,
    operator_override: bool = False,
    source_workflow: str = "prepared_context",
) -> WorkflowDepthDecision:
    bc, _max_obs = fixed_depth_to_budget_and_max_obs(preset)
    return WorkflowDepthDecision(
        initial_depth=preset,
        final_depth=preset,
        budget_class=bc,
        lane=lane,
        task_anchor=task_anchor,
        constraint=constraint,
        operator_override=operator_override,
        escalated=False,
        source_workflow=source_workflow,
    )


def decision_from_auto_resolved(
    *,
    resolved_budget_class: BudgetClass,
    stop_reason: str,
    lane: str,
    task_anchor: str,
    constraint: str | None,
    guard_veto: bool = False,
    veto_reason: str = "",
    operator_override: bool = False,
    source_workflow: str = "prepared_context",
) -> WorkflowDepthDecision:
    """After auto_decide_format: record initial=auto, final=resolved pack depth."""
    escalated = auto_escalation_detected(stop_reason, resolved_budget_class)
    halt_reason = veto_reason if guard_veto else ""
    rationale = f"auto stop_reason={stop_reason}"
    return WorkflowDepthDecision(
        initial_depth="auto",
        final_depth=resolved_budget_class,
        budget_class=resolved_budget_class,
        lane=lane,
        task_anchor=task_anchor,
        constraint=constraint,
        operator_override=operator_override,
        escalated=escalated,
        escalation_reason=stop_reason if escalated else "",
        halt_reason=halt_reason,
        rationale=rationale,
        source_workflow=source_workflow,
    )


def auto_escalation_detected(stop_reason: str, resolved_mode: str) -> bool:
    """Heuristic: auto path chose medium after compact dry-pack."""
    if resolved_mode != "medium":
        return False
    return stop_reason in (
        "no_ranked_hits_escalate",
        "high_contradiction_density",
        "low_utilization_escalate",
    )


def build_workflow_depth_receipt_record(
    *,
    schema_version: str,
    status: str,
    timestamp: str,
    boundary_notes: list[str],
    output_markdown: str,
    scores: dict[str, Any],
    run_id: str,
    workflow_depth_label: str,
    effective_mode: str,
    max_observations: int,
    phases: list[dict[str, Any]],
    stop_reason: str,
    task_anchor: str,
    constraint_anchor: str | None,
    lane: str,
    decision: WorkflowDepthDecision | None,
    compact_dry_scores: dict[str, Any] | None = None,
    guard_receipt_extras: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Single builder for append-only workflow-depth receipts (extends legacy keys).
    """
    rec: dict[str, Any] = {
        "schemaVersion": schema_version,
        "status": status,
        "timestamp": timestamp,
        "boundary_notes": list(boundary_notes),
        "run_id": run_id,
        "task_anchor": task_anchor,
        "constraint_anchor": constraint_anchor,
        "lane": lane,
        "workflow_depth": workflow_depth_label,
        "effective_mode": effective_mode,
        "max_observations": max_observations,
        "stop_reason": stop_reason,
        "output_markdown": output_markdown,
        "scores": scores,
        "phases": phases,
    }
    if compact_dry_scores is not None:
        rec["compact_dry_scores"] = compact_dry_scores
    if guard_receipt_extras:
        rec.update(guard_receipt_extras)
    if decision:
        rec["initialDepth"] = decision.initial_depth
        rec["finalDepth"] = decision.final_depth
        rec["budgetClass"] = decision.budget_class
        rec["escalated"] = decision.escalated
        rec["escalationReason"] = decision.escalation_reason
        rec["haltReason"] = decision.halt_reason
        rec["rationale"] = decision.rationale
        rec["operatorOverride"] = decision.operator_override
        rec["sourceWorkflow"] = decision.source_workflow
        if decision.estimated_load is not None:
            rec["estimatedLoad"] = decision.estimated_load
        if decision.retrieval_miss_count is not None:
            rec["retrievalMissCount"] = decision.retrieval_miss_count
    return rec
