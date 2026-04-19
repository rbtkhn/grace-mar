"""
Workflow depth control for prepared-context (WORK only, non-canonical).

Maps OpenMythos-inspired ideas to explicit halt/continue heuristics — no ML,
no Record truth. See docs/runtime/context-budgeting.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

DepthMode = Literal["shallow", "normal", "deep", "exhaustive", "auto"]

# Internal budget mode strings matching build_budgeted_context MODES
BudgetMode = Literal["compact", "medium", "deep"]


def depth_to_mode_and_max_obs(depth: DepthMode) -> tuple[BudgetMode, int]:
    """Fixed depth modes: map to lane budget class and max observation candidates."""
    if depth == "shallow":
        return "compact", 30
    if depth == "normal":
        return "medium", 30
    if depth == "deep":
        return "deep", 30
    if depth == "exhaustive":
        return "deep", 48
    raise ValueError(f"depth_to_mode_and_max_obs expects fixed mode, got {depth!r}")


def count_contradiction_refs(rows: list[dict], limit: int = 12) -> int:
    n = 0
    for r in rows[:limit]:
        for c in r.get("contradiction_refs") or []:
            if c:
                n += 1
    return n


def auto_decide_format(
    *,
    query: str,
    pool_rows: list[dict],
    compact_scores: dict[str, Any],
) -> tuple[BudgetMode, str, list[dict[str, str]]]:
    """
    After a compact-format dry run (scores from greedy pack on compact pieces).

    Returns (final_budget_mode, stop_reason, phase_log_entries).

    Heuristics are deterministic and tuned with work-strategy budgets as reference.
    """
    phases: list[dict[str, str]] = []
    q = (query or "").strip()
    total_cand = int(compact_scores.get("total_candidates", 0))
    util = float(compact_scores.get("utilization", 0.0))
    cov = float(compact_scores.get("coverage", 0.0))
    contr_n = count_contradiction_refs(pool_rows)

    phases.append(
        {
            "phase": "phase_2_metrics",
            "halt_continue": "continue",
            "summary": (
                f"compact pack: utilization={util:.3f}, coverage={cov:.3f}, "
                f"candidates={total_cand}, contradiction_ref_lines~={contr_n}"
            ),
        }
    )

    # No matches but query set — need richer excerpts
    if q and total_cand == 0:
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: no ranked hits for non-empty query",
            }
        )
        return "medium", "no_ranked_hits_escalate", phases

    # Contradiction-heavy pool: prefer medium for readable expansion
    if contr_n >= 4 and total_cand > 0:
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: elevated contradiction ref count in pool",
            }
        )
        return "medium", "high_contradiction_density", phases

    # Strong pack already — stop at compact
    if total_cand > 0 and util >= 0.38 and cov >= 0.25:
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "halt",
                "summary": "skip escalation: utilization/coverage sufficient at compact",
            }
        )
        return "compact", "sufficient_signal", phases

    # Weak fill but we have candidates — try medium
    if total_cand >= 4 and util < 0.22:
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: low utilization with material pool",
            }
        )
        return "medium", "low_utilization_escalate", phases

    # Default: compact adequate
    phases.append(
        {
            "phase": "phase_3_escalate",
            "halt_continue": "halt",
            "summary": "keep compact: default path",
        }
    )
    return "compact", "default_compact", phases


@dataclass
class WorkflowDepthRun:
    """Serializable summary for JSON receipt."""

    run_id: str
    timestamp: str
    lane: str
    task_anchor: str
    constraint_anchor: str | None
    workflow_depth: DepthMode | Literal["off"]
    effective_mode: str
    max_observations: int
    phases: list[dict[str, Any]] = field(default_factory=list)
    stop_reason: str = ""
    query: str = ""
    boundary_notes: list[str] = field(
        default_factory=lambda: [
            "non_canonical",
            "runtime_workflow_depth_receipt_not_record_truth",
        ]
    )


def phase_anchor_blurb(phase_id: str, task_anchor: str) -> str:
    """Template line tying a phase to the operator task (no LLM)."""
    short = (task_anchor.strip() or "(no anchor)").replace("\n", " ")[:200]
    return f"{phase_id}: grounded in task anchor — {short}"
