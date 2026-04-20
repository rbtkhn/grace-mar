"""
Workflow depth control for prepared-context (WORK only, non-canonical).

Maps OpenMythos-inspired ideas to explicit halt/continue heuristics — no ML,
no Record truth. See docs/runtime/context-budgeting.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

DepthMode = Literal["shallow", "normal", "deep", "exhaustive", "auto"]

# Internal budget mode strings matching build_budgeted_context MODES
BudgetMode = Literal["compact", "medium", "deep"]

# Diminishing-returns guard thresholds (deterministic; tuned for tests)
THRESHOLD_DUPLICATE_EVIDENCE_RATIO = 0.60
THRESHOLD_MARGINAL_SUPPORT_GAIN = 0.15
THRESHOLD_POOL_MIN_FOR_DIMINISHING = 6
THRESHOLD_ANCHOR_DRIFT_RISK = 0.72


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


def _norm_title(s: str) -> str:
    t = (s or "").strip().lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def _token_set(text: str) -> set[str]:
    t = (text or "").lower()
    return {w for w in re.findall(r"[a-z]{3,}", t)}


def _flatten_refs(row: dict) -> set[str]:
    out: set[str] = set()
    for ref in row.get("source_refs") or []:
        if ref:
            out.add(str(ref).strip().lower())
    return out


def _estimate_duplicate_evidence_ratio(selected_rows: list[dict], pool_rows: list[dict]) -> float:
    """Share of pool rows that look like near-duplicates of already-selected evidence."""
    if not pool_rows:
        return 0.0
    sel_titles = {_norm_title(str(r.get("title") or "")) for r in selected_rows}
    sel_titles.discard("")
    sel_refs: set[str] = set()
    for r in selected_rows:
        sel_refs |= _flatten_refs(r)
    dup = 0
    for r in pool_rows:
        nt = _norm_title(str(r.get("title") or ""))
        refs = _flatten_refs(r)
        if nt and nt in sel_titles:
            dup += 1
            continue
        if refs and sel_refs and refs <= sel_refs:
            dup += 1
            continue
        if refs and sel_refs and (refs & sel_refs):
            dup += 1
    return min(1.0, dup / max(1, len(pool_rows)))


def _estimate_marginal_support_gain(selected_rows: list[dict], pool_rows: list[dict]) -> float:
    """Fraction of pool rows whose obs_id is not in the compact-selected set (new support)."""
    if not pool_rows:
        return 1.0
    sel_ids = {str(r.get("obs_id") or "") for r in selected_rows if r.get("obs_id")}
    new_n = sum(1 for r in pool_rows if str(r.get("obs_id") or "") not in sel_ids)
    return new_n / max(1, len(pool_rows))


def _estimate_anchor_drift_risk(task_anchor: str, pool_rows: list[dict]) -> float:
    """1 - Jaccard(anchor tokens, pool title+summary tokens); 0 if no anchor."""
    anchor = (task_anchor or "").strip()
    if not anchor or not pool_rows:
        return 0.0
    a = _token_set(anchor)
    if not a:
        return 0.0
    pool_text_parts: list[str] = []
    for r in pool_rows[:16]:
        pool_text_parts.append(str(r.get("title") or ""))
        pool_text_parts.append(str(r.get("summary") or ""))
    b = _token_set(" ".join(pool_text_parts))
    if not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    jacc = inter / union if union else 0.0
    return max(0.0, min(1.0, 1.0 - jacc))


@dataclass
class GuardSignals:
    duplicate_evidence_ratio: float
    marginal_support_gain: float
    anchor_drift_risk: float
    evidence: dict[str, Any]


def _compute_guard_signals(
    task_anchor: str,
    selected_rows: list[dict],
    pool_rows: list[dict],
    compact_scores: dict[str, Any],
) -> GuardSignals:
    dup = _estimate_duplicate_evidence_ratio(selected_rows, pool_rows)
    marg = _estimate_marginal_support_gain(selected_rows, pool_rows)
    drift = _estimate_anchor_drift_risk(task_anchor, pool_rows)
    sel_ids = {str(r.get("obs_id") or "") for r in selected_rows if r.get("obs_id")}
    new_unique = sum(1 for r in pool_rows if str(r.get("obs_id") or "") not in sel_ids)
    ev: dict[str, Any] = {
        "new_unique_support": new_unique,
        "new_total_items": len(pool_rows),
        "duplicate_evidence_ratio": round(dup, 4),
        "marginal_support_gain": round(marg, 4),
        "anchor_drift_risk": round(drift, 4),
        "chars_included": int(compact_scores.get("chars_included", 0)),
    }
    return GuardSignals(duplicate_evidence_ratio=dup, marginal_support_gain=marg, anchor_drift_risk=drift, evidence=ev)


def _apply_diminishing_returns_guard(sig: GuardSignals, pool_len: int) -> tuple[bool, str, str, float, float]:
    """
    Returns (halt, recommended_stop_reason, signal_key, signal_value, threshold).
    Ordered: duplicate_evidence_bloom, diminishing_returns, anchor_drift_risk.
    """
    if sig.duplicate_evidence_ratio >= THRESHOLD_DUPLICATE_EVIDENCE_RATIO:
        return (
            True,
            "duplicate_evidence_bloom",
            "duplicate_evidence_ratio",
            sig.duplicate_evidence_ratio,
            THRESHOLD_DUPLICATE_EVIDENCE_RATIO,
        )
    if pool_len >= THRESHOLD_POOL_MIN_FOR_DIMINISHING and sig.marginal_support_gain <= THRESHOLD_MARGINAL_SUPPORT_GAIN:
        return (
            True,
            "diminishing_returns",
            "marginal_support_gain",
            sig.marginal_support_gain,
            THRESHOLD_MARGINAL_SUPPORT_GAIN,
        )
    if sig.anchor_drift_risk >= THRESHOLD_ANCHOR_DRIFT_RISK:
        return (
            True,
            "anchor_drift_risk",
            "anchor_drift_risk",
            sig.anchor_drift_risk,
            THRESHOLD_ANCHOR_DRIFT_RISK,
        )
    return False, "", "", 0.0, 0.0


def _quality_guard_phase_dict(
    sig: GuardSignals,
    *,
    halt_escalation: bool,
    veto_reason: str,
    signal_key: str,
    signal_value: float,
    threshold: float,
) -> dict[str, Any]:
    summary = (
        f"veto medium escalation: {veto_reason}" if halt_escalation else "quality guard: no diminishing-returns veto"
    )
    return {
        "phase": "phase_2_quality_guard",
        "halt_continue": "halt" if halt_escalation else "continue",
        "summary": summary,
        "signal": signal_key or "none",
        "signal_value": round(float(signal_value), 4),
        "threshold": round(float(threshold), 4) if threshold else 0.0,
        "evidence": dict(sig.evidence),
        "recommended_stop_reason": veto_reason if halt_escalation else "",
    }


def _guard_receipt_extras(
    sig: GuardSignals,
    halt_escalation: bool,
    veto_reason: str,
    signal_key: str,
    signal_value: float,
    threshold: float,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "stop_signal": signal_key if halt_escalation else "",
        "stop_signal_value": round(float(signal_value), 4) if halt_escalation else 0.0,
        "stop_signal_threshold": round(float(threshold), 4) if halt_escalation else 0.0,
        "guard_summary": dict(sig.evidence),
    }
    if halt_escalation:
        out["guard_veto"] = True
        out["veto_reason"] = veto_reason
    return out


def auto_decide_format(
    *,
    query: str,
    pool_rows: list[dict],
    compact_scores: dict[str, Any],
    task_anchor: str = "",
    compact_included_rows: list[dict] | None = None,
) -> tuple[BudgetMode, str, list[dict[str, Any]], dict[str, Any]]:
    """
    After a compact-format dry run (scores from greedy pack on compact pieces).

    Returns (final_budget_mode, stop_reason, phase_log_entries, guard_receipt_extras).

    guard_receipt_extras has stop_signal, stop_signal_value, stop_signal_threshold, guard_summary
    when a quality guard veto applies (low_utilization_escalation path only); otherwise mostly
    populated with guard_summary metrics for audit.
    """
    selected = list(compact_included_rows or [])
    phases: list[dict[str, Any]] = []
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

    sig = _compute_guard_signals(task_anchor, selected, pool_rows, compact_scores)
    empty_receipt: dict[str, Any] = {
        "stop_signal": "",
        "stop_signal_value": 0.0,
        "stop_signal_threshold": 0.0,
        "guard_summary": dict(sig.evidence),
    }

    # No matches but query set — need richer excerpts
    if q and total_cand == 0:
        phases.append(
            _quality_guard_phase_dict(
                sig,
                halt_escalation=False,
                veto_reason="",
                signal_key="",
                signal_value=0.0,
                threshold=0.0,
            )
        )
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: no ranked hits for non-empty query",
            }
        )
        return "medium", "no_ranked_hits_escalate", phases, empty_receipt

    # Contradiction-heavy pool: prefer medium for readable expansion
    if contr_n >= 4 and total_cand > 0:
        phases.append(
            _quality_guard_phase_dict(
                sig,
                halt_escalation=False,
                veto_reason="",
                signal_key="",
                signal_value=0.0,
                threshold=0.0,
            )
        )
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: elevated contradiction ref count in pool",
            }
        )
        return "medium", "high_contradiction_density", phases, empty_receipt

    # Strong pack already — stop at compact
    if total_cand > 0 and util >= 0.38 and cov >= 0.25:
        phases.append(
            _quality_guard_phase_dict(
                sig,
                halt_escalation=False,
                veto_reason="",
                signal_key="",
                signal_value=0.0,
                threshold=0.0,
            )
        )
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "halt",
                "summary": "skip escalation: utilization/coverage sufficient at compact",
            }
        )
        return "compact", "sufficient_signal", phases, empty_receipt

    # Weak fill but we have candidates — try medium (quality guard may veto)
    if total_cand >= 4 and util < 0.22:
        halt_e, veto_reason, sk, sv, th = _apply_diminishing_returns_guard(sig, len(pool_rows))
        phases.append(
            _quality_guard_phase_dict(
                sig,
                halt_escalation=halt_e,
                veto_reason=veto_reason,
                signal_key=sk,
                signal_value=sv,
                threshold=th,
            )
        )
        gr = _guard_receipt_extras(sig, halt_e, veto_reason, sk, sv, th)
        if halt_e:
            phases.append(
                {
                    "phase": "phase_3_escalate",
                    "halt_continue": "halt",
                    "summary": f"veto medium escalation: {veto_reason}",
                }
            )
            return "compact", veto_reason, phases, gr
        phases.append(
            {
                "phase": "phase_3_escalate",
                "halt_continue": "continue",
                "summary": "escalate to medium: low utilization with material pool",
            }
        )
        return "medium", "low_utilization_escalate", phases, gr

    # Default: compact adequate
    phases.append(
        _quality_guard_phase_dict(
            sig,
            halt_escalation=False,
            veto_reason="",
            signal_key="",
            signal_value=0.0,
            threshold=0.0,
        )
    )
    phases.append(
        {
            "phase": "phase_3_escalate",
            "halt_continue": "halt",
            "summary": "keep compact: default path",
        }
    )
    return "compact", "default_compact", phases, empty_receipt


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
    stop_signal: str = ""
    stop_signal_value: float = 0.0
    stop_signal_threshold: float = 0.0
    guard_summary: dict[str, Any] = field(default_factory=dict)
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
