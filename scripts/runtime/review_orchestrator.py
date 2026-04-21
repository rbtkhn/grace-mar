#!/usr/bin/env python3
"""
Multi-pass review packet for operator decision (read-only).

Does not write self.md, EVIDENCE, recursion-gate.md, or auto-approve merges.
See docs/orchestration/review-orchestrator.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SRC = REPO_ROOT / "src"
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = Path(__file__).resolve().parent
for _p in (_SRC, _SCRIPTS, _RUNTIME):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from grace_mar.runtime.workflow_depth import DEPTH_CHOICES  # noqa: E402

from observation_store import by_id  # noqa: E402
from uncertainty_envelope import (  # noqa: E402
    compute_envelope,
    synthetic_observation_from_text,
)

try:
    from recursion_gate_review import parse_review_candidates
except ImportError:
    from scripts.recursion_gate_review import parse_review_candidates  # type: ignore

from policy_mode_config import load_defaults, mode_summary_lines, resolve_mode  # noqa: E402


@dataclass
class ReviewAnchor:
    """Operator task grounding for anti-drift (runtime only; not Record)."""

    task_anchor: str
    constraint_anchor: str | None
    active_scope: str


PHASE_ORDER: tuple[str, ...] = (
    "phase_1_retrieval",
    "phase_2_invalidators",
    "phase_3_boundary",
    "phase_4_promotion_risk",
    "phase_5_synthesis",
    "phase_6_operator_questions",
)


@dataclass
class PhaseResult:
    """One named review phase — machine-readable contract + markdown body."""

    phase_id: str
    title: str
    status: str
    summary_lines: list[str]
    halt_recommended: bool
    halt_reason: str
    markdown_body_lines: list[str]
    anchor_check: dict[str, str]


def _halt_from_anchor_check(chk: dict[str, str]) -> tuple[bool, str]:
    if chk.get("scope_drift_risk") == "high":
        return True, chk.get("why_continue_or_halt", "")
    return False, ""


def _render_phase_section(title: str, markdown_body_lines: list[str], anchor_check: dict[str, str]) -> list[str]:
    out = [f"## {title}", ""]
    out.extend(markdown_body_lines)
    out.append("")
    out.extend(_anchor_fidelity_lines(anchor_check))
    return out


def _phase_result_to_receipt_row(pr: PhaseResult) -> dict[str, Any]:
    return {
        "phase_id": pr.phase_id,
        "title": pr.title,
        "status": pr.status,
        "halt_recommended": pr.halt_recommended,
        "halt_reason": pr.halt_reason,
        "summary": pr.summary_lines,
    }


def _run_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h = hashlib.sha256(f"{ts}:{uuid.uuid4().hex}".encode()).hexdigest()[:12]
    return f"ro_{ts}_{h}"


def _build_anchor_receipt_dict(
    *,
    run_id: str,
    built: str,
    mode: str,
    target: str,
    anchor: ReviewAnchor,
    phase_anchor_checks: list[dict[str, str]],
    phase_sequence: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "built": built,
        "mode": mode,
        "target": target,
        "anchor": {
            "task_anchor": anchor.task_anchor,
            "constraint_anchor": anchor.constraint_anchor,
            "active_scope": anchor.active_scope,
        },
        "phase_anchor_checks": phase_anchor_checks,
        "phase_sequence": phase_sequence,
        "non_canonical": True,
    }


def _derive_active_scope(
    *,
    mode: str,
    lane: str,
    ids: list[str],
    candidate_id: str | None,
    user: str,
    mixed_lane: bool,
) -> str:
    if mode == "pre_gate":
        scope = f"pre_gate; lane={lane or '(mixed)'}; obs={','.join(ids)}"
        if mixed_lane:
            scope += "; mixed_lane=true"
        return scope
    return f"candidate_review; candidate={candidate_id}; user={user}"


def _anchor_fidelity_lines(check: dict[str, str]) -> list[str]:
    return [
        "- **Anchor fidelity**",
        f"  - **scope_drift_risk:** `{check['scope_drift_risk']}`",
        f"  - **relation:** {check['anchor_relation']}",
        f"  - **why_continue:** {check['why_continue_or_halt']}",
        "",
    ]


def _anchor_check_evidence(
    observations: list[dict],
    env: dict[str, Any],
    anchor: ReviewAnchor,
) -> dict[str, str]:
    n = len(observations)
    total_refs = sum(len(o.get("source_refs") or []) for o in observations)
    if n == 0:
        return {
            "phase": "evidence_pass",
            "anchor_relation": "No observation rows; nothing to tie to the task anchor.",
            "scope_drift_risk": "high",
            "why_continue_or_halt": "Halt staging until observations exist or scope is corrected.",
        }
    thin = total_refs == 0
    short_summaries = sum(1 for o in observations if len((o.get("summary") or "").strip()) < 16)
    if thin and short_summaries == n:
        return {
            "phase": "evidence_pass",
            "anchor_relation": f"Evidence targets `{anchor.active_scope}` but lacks source_refs and thin text.",
            "scope_drift_risk": "high",
            "why_continue_or_halt": "Strengthen provenance or narrow the task anchor.",
        }
    if thin or short_summaries > 0:
        return {
            "phase": "evidence_pass",
            "anchor_relation": "Observations partially support review; some rows lack refs or substantive summary.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Continue review with boundary pass; add refs if promoting.",
        }
    return {
        "phase": "evidence_pass",
        "anchor_relation": f"Ledger observations with refs align with scoped review `{anchor.active_scope}`.",
        "scope_drift_risk": "low",
        "why_continue_or_halt": "Proceed to contradiction and boundary passes.",
    }


def _anchor_check_contradiction(
    mode: str,
    observations: list[dict],
    candidate_row: dict | None,
    env: dict[str, Any],
    anchor: ReviewAnchor,
) -> dict[str, str]:
    if mode == "pre_gate":
        union = set()
        for o in observations:
            for c in o.get("contradiction_refs") or []:
                if c:
                    union.add(c)
        if env.get("evidence_state") == "conflicted":
            return {
                "phase": "contradiction_pass",
                "anchor_relation": "Envelope conflicted — tension explicit vs anchor.",
                "scope_drift_risk": "medium",
                "why_continue_or_halt": "Resolve contradictions before promotion; still on-task.",
            }
        if union:
            return {
                "phase": "contradiction_pass",
                "anchor_relation": f"Contradiction refs {sorted(union)[:5]} tie to this review target.",
                "scope_drift_risk": "low",
                "why_continue_or_halt": "Continue; contradictions are in scope for the anchor.",
            }
        return {
            "phase": "contradiction_pass",
            "anchor_relation": "No contradiction_refs; envelope-only signals for `" + anchor.active_scope + "`.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Continue; absence of refs is weakly anchored.",
        }
    assert candidate_row is not None
    if candidate_row.get("has_conflict_markers") or env.get("evidence_state") == "conflicted":
        return {
            "phase": "contradiction_pass",
            "anchor_relation": "Gate/candidate markers or envelope flag contest this staging decision.",
            "scope_drift_risk": "low",
            "why_continue_or_halt": "Contradiction signals are specific to this candidate.",
        }
    return {
        "phase": "contradiction_pass",
        "anchor_relation": "No automated conflict markers; synthetic envelope only.",
        "scope_drift_risk": "medium",
        "why_continue_or_halt": "Cross-check gate YAML manually against anchor.",
    }


def _anchor_check_boundary(
    mode: str,
    observations: list[dict],
    candidate_row: dict | None,
    lane: str,
    anchor: ReviewAnchor,
) -> dict[str, str]:
    if mode == "pre_gate" and observations:
        any_refs = any(o.get("source_refs") for o in observations)
        any_mut = any(o.get("record_mutation_candidate") for o in observations)
        if any_refs or any_mut:
            return {
                "phase": "boundary_pass",
                "anchor_relation": f"Boundary signals (refs/mutation) relate to lane `{lane}` and task.",
                "scope_drift_risk": "low",
                "why_continue_or_halt": "Surface targeting remains reviewable vs anchor.",
            }
        return {
            "phase": "boundary_pass",
            "anchor_relation": "Weak boundary signals — generic work-layer note may apply.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Confirm target surface before gate draft.",
        }
    if candidate_row:
        br = candidate_row.get("boundary_review") or {}
        if br.get("target_surface") or br.get("suggested_surface"):
            return {
                "phase": "boundary_pass",
                "anchor_relation": "Candidate carries boundary_review surfaces tied to this CANDIDATE block.",
                "scope_drift_risk": "low",
                "why_continue_or_halt": "Compare profile_target to operator intent.",
            }
        return {
            "phase": "boundary_pass",
            "anchor_relation": "Partial boundary metadata on candidate row.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Fill boundary_review before approve if scope is unclear.",
        }
    return {
        "phase": "boundary_pass",
        "anchor_relation": "No boundary metadata block for this packet shape.",
        "scope_drift_risk": "high",
        "why_continue_or_halt": "Drift risk: clarify Record vs work-layer vs anchor.",
    }


def _anchor_check_promotion_risk(env: dict[str, Any], anchor: ReviewAnchor) -> dict[str, str]:
    reasons = env.get("reasons") or []
    promo = env.get("promotion_recommendation", "")
    if not reasons:
        return {
            "phase": "promotion_risk_pass",
            "anchor_relation": "Envelope reasons empty — weak link to stated task.",
            "scope_drift_risk": "high",
            "why_continue_or_halt": "Re-run envelope inputs or narrow anchor.",
        }
    if promo in ("hold", "block"):
        return {
            "phase": "promotion_risk_pass",
            "anchor_relation": f"Promotion `{promo}` with explicit envelope reasons vs `{anchor.active_scope}`.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Hold/block is on-policy; companion decides merge.",
        }
    return {
        "phase": "promotion_risk_pass",
        "anchor_relation": "Promotion recommendation and reasons are readable for this review.",
        "scope_drift_risk": "low",
        "why_continue_or_halt": "Proceed to synthesis with same anchor.",
    }


def _anchor_check_synthesis(env: dict[str, Any], anchor: ReviewAnchor) -> dict[str, str]:
    promo = env.get("promotion_recommendation", "allow_with_review")
    if promo == "allow_with_review" and len(env.get("reasons") or []) <= 1:
        return {
            "phase": "synthesis",
            "anchor_relation": "Default advisory action; rationale may be thin vs a specific anchor.",
            "scope_drift_risk": "medium",
            "why_continue_or_halt": "Confirm action matches operator task before acting.",
        }
    ta = anchor.task_anchor
    tail = ta[:80] + ("…" if len(ta) > 80 else "")
    return {
        "phase": "synthesis",
        "anchor_relation": f"Synthesis action `{promo}` follows prior passes for `{tail}`.",
        "scope_drift_risk": "low",
        "why_continue_or_halt": "Packet synthesis is aligned with multi-pass inputs.",
    }


def _anchor_check_operator_questions(
    mode: str,
    questions: list[str],
    candidate_id: str | None,
    anchor: ReviewAnchor,
) -> dict[str, str]:
    joined = " ".join(questions).lower()
    if candidate_id and candidate_id.lower() in joined:
        return {
            "phase": "operator_questions",
            "anchor_relation": "Questions reference the pending candidate id — tied to review target.",
            "scope_drift_risk": "low",
            "why_continue_or_halt": "Use answers to complete gate decision under same anchor.",
        }
    if "target surface" in joined or "record" in joined:
        return {
            "phase": "operator_questions",
            "anchor_relation": "Questions probe surface/Record fit vs anchor.",
            "scope_drift_risk": "low",
            "why_continue_or_halt": "Continue companion review with explicit scope.",
        }
    if len(questions) < 2:
        return {
            "phase": "operator_questions",
            "anchor_relation": "Few follow-ups; boilerplate risk vs a rich anchor.",
            "scope_drift_risk": "high",
            "why_continue_or_halt": "Add operator-specific questions if drift feels likely.",
        }
    return {
        "phase": "operator_questions",
        "anchor_relation": "Standard operator question set for this mode.",
        "scope_drift_risk": "medium",
        "why_continue_or_halt": "Answer before merge; gate-review-pass optional second pass.",
    }


def _candidate_synthetic_text(row: dict) -> str:
    parts = [
        (row.get("summary") or "").strip(),
        (row.get("suggested_entry") or "")[:1500],
        (row.get("example_from_exchange") or "")[:800],
    ]
    return "\n\n".join(p for p in parts if p)


def _pre_gate_boundary_notes(observations: list[dict], lane: str) -> list[str]:
    notes: list[str] = []
    work_lanes = ("work-", "strategy", "politics", "jiang", "dev", "xavier")
    looks_work = any(w in (lane or "").lower() for w in work_lanes)
    any_mut = any(o.get("record_mutation_candidate") for o in observations)
    any_refs = any(o.get("source_refs") for o in observations)
    if looks_work and any_mut:
        notes.append(
            "Lane and mutation flags suggest **work-layer** planning; durable Record changes still require "
            "explicit gate YAML targeting SELF / IX / EVIDENCE — not implied by runtime lane alone."
        )
    elif any_mut and not any_refs:
        notes.append(
            "**Record mutation** intent without `source_refs` on observations: strengthen provenance before staging."
        )
    if any_refs:
        notes.append("At least one observation carries **source_refs** — trace before promotion.")
    if not notes:
        notes.append("No strong boundary signal; classify target surface when drafting the gate candidate.")
    return notes


def _contradiction_pass_observations(observations: list[dict], env: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    union: set[str] = set()
    for o in observations:
        for c in o.get("contradiction_refs") or []:
            if c:
                union.add(c)
    if union:
        lines.append(f"Contradiction refs present: {', '.join(sorted(union))}.")
    else:
        lines.append("No `contradiction_refs` on selected observations.")
    if env.get("evidence_state") == "conflicted":
        lines.append("Uncertainty envelope: **conflicted** — do not promote without resolving tensions.")
    else:
        lines.append("Uncertainty envelope: not in **conflicted** evidence state (still review narrative strength).")
    return lines


def _contradiction_pass_candidate(row: dict, env: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if row.get("has_conflict_markers"):
        lines.append("Gate YAML / text flags **conflict or contradiction** markers — manual review.")
    else:
        lines.append("No automated conflict markers on candidate row.")
    cs = row.get("constitution_check_status")
    if cs:
        lines.append(f"Constitution check status: `{cs}`.")
    cr = row.get("constitution_rule_ids")
    if cr:
        lines.append(f"Constitution rule ids: `{cr}`.")
    if row.get("duplicate_hints"):
        lines.append(f"Duplicate hints: {row['duplicate_hints']!r} — resolve before merge.")
    if env.get("evidence_state") == "conflicted":
        lines.append("Synthetic gate-text envelope: **conflicted** — treat narrative as contested.")
    return lines


def _operator_questions(
    mode: str,
    env: dict[str, Any],
    *,
    candidate_id: str | None = None,
) -> list[str]:
    qs: list[str] = []
    promo = env.get("promotion_recommendation", "")
    if promo in ("hold", "block"):
        qs.append("What additional **primary evidence** (companion-sourced or artifact) would justify staging?")
    if env.get("fabricated_history_risk") in ("medium", "high"):
        qs.append("Can every **historical / biographical** claim be tied to an approved Record line or citation?")
    if env.get("evidence_state") == "conflicted":
        qs.append("Which **contradiction ref** should be resolved first, and how?")
    qs.append("Does the **target surface** (SELF vs SELF-LIBRARY vs SKILLS vs EVIDENCE vs work-layer) match intent?")
    if mode == "candidate_review" and candidate_id:
        qs.append(f"Re-read `### {candidate_id}` in recursion-gate.md for edits before approve.")
    if len(qs) < 3:
        qs.append("Would a second operator pass (e.g. gate-review-pass skill) change the call?")
    return qs[:8]


def _run_phase_1_retrieval(
    observations: list[dict],
    env: dict[str, Any],
    anchor: ReviewAnchor,
) -> PhaseResult:
    n = len(observations)
    total_refs = sum(len(o.get("source_refs") or []) for o in observations)
    md_lines: list[str] = [
        f"- **Observation count:** {n}",
        f"- **Supporting refs (source_refs count):** {total_refs}",
    ]
    summary_lines = [
        f"Observation count: {n}",
        f"Supporting refs count: {total_refs}",
    ]
    if observations:
        kinds: dict[str, int] = {}
        for o in observations:
            k = o.get("source_kind") or "?"
            kinds[k] = kinds.get(k, 0) + 1
        md_lines.append(f"- **source_kind mix:** {kinds}")
        summary_lines.append(f"source_kind mix: {kinds}")
        ts = [o.get("timestamp") for o in observations if o.get("timestamp")]
        if ts:
            md_lines.append(f"- **Recency (timestamps):** oldest `{min(ts)}` → newest `{max(ts)}`")
            summary_lines.append(f"Recency: {min(ts)} to {max(ts)}")
    md_lines.append(f"- **Evidence sufficiency (PR 1 envelope):** `{env['evidence_state']}`")
    summary_lines.append(f"Evidence sufficiency: {env['evidence_state']}")
    chk = _anchor_check_evidence(observations, env, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    return PhaseResult(
        phase_id="phase_1_retrieval",
        title="Evidence Pass",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def _run_phase_2_invalidators(
    mode: str,
    observations: list[dict],
    candidate_row: dict | None,
    env: dict[str, Any],
    anchor: ReviewAnchor,
) -> PhaseResult:
    md_lines: list[str] = []
    summary_lines: list[str] = []
    if mode == "pre_gate":
        for x in _contradiction_pass_observations(observations, env):
            md_lines.append(f"- {x}")
        summary_lines.append("Contradiction pass (observation-led)")
    else:
        assert candidate_row is not None
        for x in _contradiction_pass_candidate(candidate_row, env):
            md_lines.append(f"- {x}")
        summary_lines.append("Contradiction pass (candidate-led)")
    chk = _anchor_check_contradiction(mode, observations, candidate_row, env, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    if env.get("evidence_state") == "conflicted":
        summary_lines.append("Envelope evidence_state: conflicted")
    return PhaseResult(
        phase_id="phase_2_invalidators",
        title="Contradiction Pass",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def _run_phase_3_boundary(
    mode: str,
    observations: list[dict],
    candidate_row: dict | None,
    lane_for_boundary: str,
    anchor: ReviewAnchor,
) -> PhaseResult:
    md_lines: list[str] = []
    summary_lines: list[str] = []
    if mode == "pre_gate" and observations:
        lane = observations[0].get("lane") or ""
        for note in _pre_gate_boundary_notes(observations, lane):
            md_lines.append(f"- {note}")
        summary_lines.append(f"Boundary notes for lane: {lane or '(unknown)'}")
    elif candidate_row:
        br = candidate_row.get("boundary_review") or {}
        md_lines.extend(
            [
                f"- **profile_target:** `{candidate_row.get('profile_target', '')}`",
                f"- **mind_category:** `{candidate_row.get('mind_category', '')}`",
                f"- **territory:** `{candidate_row.get('territory', '')}`",
                f"- **proposal_class:** `{candidate_row.get('proposal_class', '')}`",
                (
                    f"- **boundary_review target_surface:** `{br.get('target_surface', '')}` → "
                    f"suggested `{br.get('suggested_surface', '')}` (confidence: {br.get('confidence', '')})"
                ),
            ]
        )
        if br.get("misfiled_warning"):
            md_lines.append(f"- **Misfiled warning:** {br['misfiled_warning']}")
        for h in br.get("hint_reasons") or []:
            md_lines.append(f"- Hint: {h}")
        md_lines.append(f"- **risk_tier:** `{candidate_row.get('risk_tier', '')}`")
        summary_lines.append(f"profile_target: {candidate_row.get('profile_target', '')}")
        summary_lines.append(f"boundary_review target_surface: {br.get('target_surface', '')}")
    else:
        md_lines.append("- (No boundary metadata for this packet.)")
        summary_lines.append("No boundary metadata for this packet shape")
    chk = _anchor_check_boundary(mode, observations, candidate_row, lane_for_boundary, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    return PhaseResult(
        phase_id="phase_3_boundary",
        title="Boundary Pass",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def _run_phase_4_promotion_risk(
    env: dict[str, Any],
    candidate_row: dict | None,
    anchor: ReviewAnchor,
) -> PhaseResult:
    md_lines = [
        f"- **Fabricated-history risk:** `{env['fabricated_history_risk']}`",
        f"- **Promotion recommendation:** `{env.get('promotion_recommendation', '')}`",
        "- **Reasons (envelope):**",
    ]
    for r in env.get("reasons", [])[:14]:
        md_lines.append(f"  - {r}")
    summary_lines = [
        f"Fabricated-history risk: {env['fabricated_history_risk']}",
        f"Promotion recommendation: {env.get('promotion_recommendation', '')}",
        f"Envelope reasons count: {len(env.get('reasons') or [])}",
    ]
    if candidate_row:
        rt = candidate_row.get("risk_tier", "")
        md_lines.append(
            f"- **Scope / prematurity (gate risk_tier):** `{rt}` — defer or escalate when `manual_escalate`."
        )
        summary_lines.append(f"Gate risk_tier: {rt}")
    else:
        md_lines.append(
            "- **Scope / prematurity:** If staging to gate, confirm IX target and provenance before merge."
        )
        summary_lines.append("Scope/prematurity: confirm IX target if staging")
    chk = _anchor_check_promotion_risk(env, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    return PhaseResult(
        phase_id="phase_4_promotion_risk",
        title="Promotion-Risk Pass",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def _run_phase_5_synthesis(env: dict[str, Any], anchor: ReviewAnchor) -> PhaseResult:
    promo = env.get("promotion_recommendation", "allow_with_review")
    md_lines = [
        f"- **Recommended action:** `{promo}`",
        "- **Rationale:** Derived from PR 1 uncertainty envelope "
        "+ contradiction/boundary signals (advisory; companion decides).",
    ]
    summary_lines = [
        f"Recommended action: {promo}",
        "Rationale: envelope + contradiction/boundary signals (advisory)",
    ]
    chk = _anchor_check_synthesis(env, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    return PhaseResult(
        phase_id="phase_5_synthesis",
        title="Synthesis",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def _run_phase_6_operator_questions(
    mode: str,
    env: dict[str, Any],
    candidate_row: dict | None,
    anchor: ReviewAnchor,
) -> PhaseResult:
    cid = candidate_row.get("id") if candidate_row else None
    oqs = _operator_questions(mode, env, candidate_id=cid)
    md_lines = [f"- {q}" for q in oqs]
    summary_lines = [f"Operator questions count: {len(oqs)}"]
    if cid:
        summary_lines.append(f"Candidate id: {cid}")
    chk = _anchor_check_operator_questions(mode, oqs, cid, anchor)
    halt_r, halt_why = _halt_from_anchor_check(chk)
    return PhaseResult(
        phase_id="phase_6_operator_questions",
        title="Operator Questions",
        status="completed",
        summary_lines=summary_lines,
        halt_recommended=halt_r,
        halt_reason=halt_why,
        markdown_body_lines=md_lines,
        anchor_check=chk,
    )


def build_review_packet_markdown(
    *,
    mode: str,
    built_iso: str,
    target_label: str,
    observations: list[dict],
    env: dict[str, Any],
    candidate_row: dict | None,
    gate_text_derived: bool,
    anchor: ReviewAnchor,
) -> tuple[str, list[dict[str, str]], list[PhaseResult]]:
    lane_for_boundary = (observations[0].get("lane") or "") if observations else ""

    lines: list[str] = [
        "# Review Packet",
        "",
        f"Built: {built_iso}",
        f"Mode: {mode}",
        f"Target: {target_label}",
        "",
    ]
    if gate_text_derived:
        lines.extend(
            [
                "_Note: uncertainty scoring for candidate mode uses **gate-text-derived** synthetic observation(s); "
                "ledger-backed observations were not supplied._",
                "",
            ]
        )

    lines.extend(
        [
            "## Task Anchor",
            "",
            f"- **task_anchor:** {anchor.task_anchor}",
            f"- **constraint_anchor:** {anchor.constraint_anchor or '_(none)_'}",
            f"- **active_scope:** `{anchor.active_scope}`",
            "",
            "_Runtime review artifact only — not SELF, EVIDENCE, or gate truth._",
            "",
        ]
    )

    p1 = _run_phase_1_retrieval(observations, env, anchor)
    p2 = _run_phase_2_invalidators(mode, observations, candidate_row, env, anchor)
    p3 = _run_phase_3_boundary(mode, observations, candidate_row, lane_for_boundary, anchor)
    p4 = _run_phase_4_promotion_risk(env, candidate_row, anchor)
    p5 = _run_phase_5_synthesis(env, anchor)
    p6 = _run_phase_6_operator_questions(mode, env, candidate_row, anchor)
    phase_results = [p1, p2, p3, p4, p5, p6]
    phase_checks = [pr.anchor_check for pr in phase_results]

    for pr in phase_results:
        lines.extend(_render_phase_section(pr.title, pr.markdown_body_lines, pr.anchor_check))

    lines.append("---")
    lines.append("_Review orchestrator output is not canonical. Merge only via companion-approved gate pipeline._")
    lines.append("")
    return "\n".join(lines), phase_checks, phase_results


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build a multi-pass Markdown review packet (pre_gate or candidate_review). Read-only."
    )
    p.add_argument("--mode", required=True, choices=("pre_gate", "candidate_review"))
    p.add_argument("--lane", default=None)
    p.add_argument("--mixed-lane", action="store_true")
    p.add_argument("--id", action="append", dest="ids", default=None)
    p.add_argument("--candidate", default=None, help="CANDIDATE-NNNN for candidate_review")
    p.add_argument("--user", "-u", default="grace-mar")
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detected; use for tests)",
    )
    p.add_argument("-o", "--output", type=Path, default=None)
    p.add_argument(
        "--context-mode",
        choices=("compact", "medium", "deep"),
        default=None,
        help="Append a suggested build_budgeted_context.py command using this budget mode (optional)",
    )
    p.add_argument(
        "--workflow-depth",
        "--depth",
        dest="workflow_depth",
        default=None,
        choices=DEPTH_CHOICES,
        metavar="DEPTH",
        help="Optional: suggest build_budgeted_context.py with --workflow-depth instead of --mode (uses --task-anchor)",
    )
    p.add_argument(
        "--policy-mode",
        default=None,
        help="Append Policy mode envelope section (default: GRACE_MAR_POLICY_MODE or operator_only)",
    )
    p.add_argument(
        "--task-anchor",
        default="",
        help="Original operator task (required) — reinjected in packet and optional receipt",
    )
    p.add_argument(
        "--constraint-anchor",
        default="",
        help="Optional constraint (scope, abstention) for this review",
    )
    p.add_argument(
        "--active-scope",
        default="",
        help="Optional explicit scope string; default derived from lane/ids/candidate",
    )
    p.add_argument(
        "--receipt-out",
        type=Path,
        default=None,
        metavar="PATH",
        help="Optional JSON sidecar: anchor + phase_anchor_checks + phase_sequence (non-canonical)",
    )
    args = p.parse_args()
    repo_root = args.repo_root.resolve() if args.repo_root else None

    task_anchor = (args.task_anchor or "").strip()
    if not task_anchor:
        print("error: --task-anchor is required", file=sys.stderr)
        return 2

    if args.workflow_depth and args.context_mode:
        print(
            "notice: --context-mode ignored because --workflow-depth / --depth is set",
            file=sys.stderr,
        )

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = _run_id()
    constraint_s = (args.constraint_anchor or "").strip() or None

    if args.mode == "pre_gate":
        ids = args.ids or []
        if not ids:
            print("error: pre_gate requires at least one --id", file=sys.stderr)
            return 2
        if not args.mixed_lane and not (args.lane and args.lane.strip()):
            print("error: pre_gate requires --lane or --mixed-lane", file=sys.stderr)
            return 2
        lane = (args.lane or "").strip()
        observations: list[dict] = []
        for oid in ids:
            raw = by_id(oid)
            if raw is None:
                print(f"error: missing observation {oid}", file=sys.stderr)
                return 2
            if not args.mixed_lane and raw.get("lane") != lane:
                print(
                    f"error: {oid} lane {raw.get('lane')!r} != {lane!r} (use --mixed-lane)",
                    file=sys.stderr,
                )
                return 2
            observations.append(raw)
        env = compute_envelope(observations)
        target_label = ", ".join(ids)
        lane = (args.lane or "").strip()
        scope_override = (args.active_scope or "").strip()
        active_scope = scope_override or _derive_active_scope(
            mode="pre_gate",
            lane=lane,
            ids=ids,
            candidate_id=None,
            user=args.user,
            mixed_lane=args.mixed_lane,
        )
        anchor = ReviewAnchor(task_anchor, constraint_s, active_scope)
        md, phase_checks, phase_results = build_review_packet_markdown(
            mode="pre_gate",
            built_iso=built,
            target_label=target_label,
            observations=observations,
            env=env,
            candidate_row=None,
            gate_text_derived=False,
            anchor=anchor,
        )
    else:
        cid = (args.candidate or "").strip()
        if not cid or not cid.startswith("CANDIDATE-"):
            print("error: candidate_review requires --candidate CANDIDATE-NNNN", file=sys.stderr)
            return 2
        rows = parse_review_candidates(user_id=args.user, repo_root=repo_root)
        candidate_row = next((r for r in rows if r.get("id") == cid), None)
        if candidate_row is None:
            print(f"error: candidate not found in active gate section: {cid}", file=sys.stderr)
            return 2
        text = _candidate_synthetic_text(candidate_row)
        observations = [synthetic_observation_from_text(text, record_mutation_candidate=True)]
        env = compute_envelope(observations)
        target_label = cid
        scope_override = (args.active_scope or "").strip()
        active_scope = scope_override or _derive_active_scope(
            mode="candidate_review",
            lane="",
            ids=[],
            candidate_id=cid,
            user=args.user,
            mixed_lane=False,
        )
        anchor = ReviewAnchor(task_anchor, constraint_s, active_scope)
        md, phase_checks, phase_results = build_review_packet_markdown(
            mode="candidate_review",
            built_iso=built,
            target_label=target_label,
            observations=observations,
            env=env,
            candidate_row=candidate_row,
            gate_text_derived=True,
            anchor=anchor,
        )

    pdefs = load_defaults()
    pol = resolve_mode(args.policy_mode, pdefs)
    md += "\n## Policy mode envelope\n\n"
    md += f"Active policy mode: **`{pol}`** (declared for this packet; does not replace gate review).\n\n"
    md += "\n".join(mode_summary_lines(pol, pdefs)) + "\n"
    md += "\nSee `docs/policy-modes.md`.\n"

    if args.workflow_depth:
        lane_hint = (args.lane or "").strip() or "work-strategy"
        ca = constraint_s or ""
        ca_line = f"  --constraint-anchor {json.dumps(ca)} \\\n" if ca else ""
        md += (
            "\n## Suggested budgeted context\n\n"
            f"Lane **`{lane_hint}`** — run `build_budgeted_context.py` with **workflow depth `{args.workflow_depth}`** "
            "(does not use `--mode`; see `docs/runtime/workflow-depth.md`). "
            f"Add `--policy-mode {pol}` to match this envelope. **`--task-anchor`** is required and should match your review intent.\n\n"
            "```bash\n"
            f"python3 scripts/prepared_context/build_budgeted_context.py \\\n"
            f"  --lane {lane_hint} \\\n"
            f"  --policy-mode {pol} \\\n"
            f"  --workflow-depth {args.workflow_depth} \\\n"
            f"  --task-anchor {json.dumps(task_anchor)} \\\n"
            f"{ca_line}"
            "  --query \"(add search terms)\" \\\n"
            "  -o prepared-context/budgeted-review-context.md\n"
            "```\n"
        )
    elif args.context_mode:
        lane_hint = (args.lane or "").strip() or "work-strategy"
        md += (
            "\n## Suggested budgeted context\n\n"
            f"Lane **`{lane_hint}`** — run `build_budgeted_context.py` in **`{args.context_mode}`** budget class "
            "to assemble a bounded context block with explicit inclusion/exclusion reporting "
            "(see `docs/runtime/context-budgeting.md`). Add `--policy-mode {pol}` to match this envelope.\n\n"
            "```bash\n"
            f"python3 scripts/prepared_context/build_budgeted_context.py \\\n"
            f"  --lane {lane_hint} \\\n"
            f"  --policy-mode {pol} \\\n"
            f"  --mode {args.context_mode} \\\n"
            "  --query \"(add search terms)\" \\\n"
            "  -o prepared-context/budgeted-review-context.md\n"
            "```\n"
        )

    if args.receipt_out is not None:
        phase_sequence = [_phase_result_to_receipt_row(pr) for pr in phase_results]
        receipt = _build_anchor_receipt_dict(
            run_id=run_id,
            built=built,
            mode=args.mode,
            target=target_label,
            anchor=anchor,
            phase_anchor_checks=phase_checks,
            phase_sequence=phase_sequence,
        )
        outp = args.receipt_out.resolve()
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {outp}", file=sys.stderr)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(md, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(md, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
