#!/usr/bin/env python3
"""
Counterfactual Fork Simulator — Phase 1.

Read-only/scratch-only governance foresight tool. Reads a proposal-like JSON input,
estimates likely consequences of accepting the proposal, and writes an advisory report
under artifacts/counterfactual-simulations/.

Standard library only. Never mutates canonical Record files or recursion-gate.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_PROPOSAL_KINDS = {
    "record_change",
    "doctrine_change",
    "skill_update",
    "interface_artifact",
    "portable_emulation",
    "strategy_doctrine",
    "other",
}
ALLOWED_DECISIONS = {"accept", "revise", "split", "defer", "reject", "needs_review"}
SCRATCH_DIR = Path("artifacts") / "counterfactual-simulations"
CANONICAL_TERMS = [
    "SELF",
    "SELF-LIBRARY",
    "SKILLS",
    "EVIDENCE",
    "recursion-gate.md",
    "self.md",
    "self-library.md",
    "self-skills.md",
    "skills.md",
    "evidence",
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return slug or "counterfactual-proposal"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _require_string_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return value


def validate_proposal(data: dict[str, Any]) -> dict[str, Any]:
    proposal_id = _require_string(data, "proposal_id")
    proposal_kind = _require_string(data, "proposal_kind")
    if proposal_kind not in ALLOWED_PROPOSAL_KINDS:
        raise ValueError(
            f"proposal_kind must be one of {sorted(ALLOWED_PROPOSAL_KINDS)!r}, got {proposal_kind!r}"
        )
    target_paths = _require_string_list(data, "target_paths")
    target_surfaces = _require_string_list(data, "target_surfaces")
    proposed_change_summary = _require_string(data, "proposed_change_summary")

    proposed_patch_text = data.get("proposed_patch_text", "")
    if proposed_patch_text is None:
        proposed_patch_text = ""
    if not isinstance(proposed_patch_text, str):
        raise ValueError("proposed_patch_text must be a string when present")

    evidence_refs = data.get("evidence_refs", [])
    if evidence_refs is None:
        evidence_refs = []
    if not isinstance(evidence_refs, list) or not all(isinstance(item, str) for item in evidence_refs):
        raise ValueError("evidence_refs must be a list of strings when present")

    operator_question = data.get("operator_question", "")
    if operator_question is None:
        operator_question = ""
    if not isinstance(operator_question, str):
        raise ValueError("operator_question must be a string when present")

    return {
        "proposal_id": proposal_id,
        "proposal_kind": proposal_kind,
        "target_paths": target_paths,
        "target_surfaces": target_surfaces,
        "proposed_change_summary": proposed_change_summary,
        "proposed_patch_text": proposed_patch_text,
        "evidence_refs": evidence_refs,
        "operator_question": operator_question.strip(),
    }


def _contains_non_none_authority(text: str, authority_key: str) -> bool:
    lowered = text.lower()
    key = authority_key.lower()
    start = 0
    while True:
        idx = lowered.find(key, start)
        if idx == -1:
            return False
        snippet = lowered[idx : idx + 80]
        if "none" not in snippet:
            return True
        start = idx + len(key)


def _mentions_protected_write_without_human_review(text: str) -> bool:
    lowered = text.lower()
    if "human review" in lowered:
        return False
    write_words = ("write", "writes", "update", "updates", "modify", "merge", "approve")
    if not any(word in lowered for word in write_words):
        return False
    protected_tokens = [
        "self",
        "self-library",
        "skills",
        "evidence",
        "recursion-gate.md",
        "self.md",
        "self-library.md",
        "self-skills.md",
        "skills.md",
    ]
    return any(token in lowered for token in protected_tokens)


def _interface_artifact_authority_risk(text: str) -> bool:
    lowered = text.lower()
    return any(
        token in lowered
        for token in (
            "recordauthority",
            "gateeffect",
            "mergeauthority",
            "record authority",
            "gate authority",
            "evidence truth",
            "canonical evidence",
        )
    )


def _portable_emulation_merge_risk(text: str) -> bool:
    lowered = text.lower()
    return "mergeauthority" in lowered or "merge authority" in lowered


def analyze_counterfactual(
    proposal: dict[str, Any], repo_root: Path
) -> dict[str, Any]:
    summary = proposal["proposed_change_summary"]
    patch = proposal["proposed_patch_text"]
    combined = " ".join([summary, patch, proposal["operator_question"]]).strip()
    combined_lower = combined.lower()

    affected_paths = _unique(proposal["target_paths"])
    affected_surfaces = _unique(proposal["target_surfaces"])

    possible_contradictions: list[str] = []
    contradiction_keywords = {
        "replace": "Proposal uses replacement language and may conflict with existing active wording or surface ownership.",
        "rename": "Proposal uses rename language and may create path, doc, or cross-link drift if accepted incompletely.",
        "deprecate": "Proposal uses deprecation language and may leave live references split between old and new doctrine.",
        "remove": "Proposal uses removal language and may erase behavior or references other docs/scripts still assume exist.",
        "canonical": "Proposal references canonical state directly; confirm it does not compress WORK analysis into Record truth.",
        "memory": "Proposal references memory surfaces; confirm continuity, runtime memory, and Record are not being conflated.",
        "record": "Proposal references Record surfaces directly; verify the target surface and merge path are explicit.",
        "identity": "Proposal references identity semantics; check for contradiction with active SELF or governed doctrine.",
    }
    for keyword, message in contradiction_keywords.items():
        if keyword in combined_lower:
            possible_contradictions.append(message)

    doctrine_drift_risks: list[str] = []
    authority_risk_found = False
    for key in ("recordAuthority", "gateEffect", "mergeAuthority"):
        if _contains_non_none_authority(combined, key):
            authority_risk_found = True
            doctrine_drift_risks.append(
                f"Proposed text appears to set {key} to a non-'none' value, which would drift from current doctrine boundaries."
            )

    protected_write_risk = _mentions_protected_write_without_human_review(combined)
    if protected_write_risk:
        authority_risk_found = True
        doctrine_drift_risks.append(
            "Proposal appears to write canonical Record or gate surfaces without human review."
        )

    if proposal["proposal_kind"] == "interface_artifact" and _interface_artifact_authority_risk(combined):
        doctrine_drift_risks.append(
            "Interface artifact proposal appears to claim Record, gate, or evidence authority beyond its WORK-only role."
        )

    if proposal["proposal_kind"] == "portable_emulation" and _portable_emulation_merge_risk(combined):
        doctrine_drift_risks.append(
            "Portable emulation proposal appears to imply merge authority, which violates the non-authoritative emulation contract."
        )

    follow_up_required: list[str] = []
    tests_or_audits_to_run: list[str] = []
    warnings: list[str] = [
        "Advisory only: this simulation report is not evidence, not Record, not approval, and not a merge receipt."
    ]

    if not patch.strip():
        warnings.append(
            "No proposed_patch_text was supplied; this is a summary-only simulation and may miss structural or wording-level effects."
        )
    if not affected_surfaces:
        warnings.append("No target_surfaces were supplied; consequence review is incomplete until surfaces are named.")

    for target_path in affected_paths:
        resolved = (repo_root / target_path).resolve()
        if not resolved.exists():
            warnings.append(f"Target path does not exist in current repo state: {target_path}")
        if target_path.startswith("docs/") or target_path.endswith(".md"):
            follow_up_required.append(
                f"Review nearby documentation cross-links and terminology alignment around {target_path}."
            )
        if target_path.startswith("scripts/"):
            follow_up_required.append(
                f"Review doctrine drift and test coverage for script changes under {target_path}."
            )
            tests_or_audits_to_run.append("python3 scripts/audit_doctrine_drift.py")
            tests_or_audits_to_run.append("pytest tests/test_counterfactual_fork_simulator.py")
        if target_path.startswith("schema-registry/"):
            follow_up_required.append(
                f"Validate schema consumers and example payloads for {target_path}."
            )
            tests_or_audits_to_run.append("pytest tests/test_counterfactual_fork_simulator.py")
        if target_path.startswith("docs/portability/emulation/"):
            follow_up_required.append(
                f"Re-check portable emulation authority wording and validation around {target_path}."
            )
            tests_or_audits_to_run.append(
                "pytest tests/test_emulation_contract_schema.py tests/test_emulation_bundle_schema.py"
            )

    if authority_risk_found:
        tests_or_audits_to_run.append("python3 scripts/audit_doctrine_drift.py")

    tests_or_audits_to_run = _unique(tests_or_audits_to_run)
    follow_up_required = _unique(follow_up_required)
    possible_contradictions = _unique(possible_contradictions)
    doctrine_drift_risks = _unique(doctrine_drift_risks)
    warnings = _unique(warnings)

    decision = "accept"
    rationale = "The proposal is narrow, non-authoritative, and does not trigger obvious doctrine or contradiction risks."

    fatal_authority_risk = authority_risk_found or any(
        "merge authority" in risk.lower() or "write canonical" in risk.lower()
        for risk in doctrine_drift_risks
    )
    if not affected_surfaces:
        decision = "needs_review"
        rationale = "Target surfaces are unspecified, so the simulator cannot confidently map the proposal to the right governed boundaries."
    elif fatal_authority_risk:
        decision = "reject"
        rationale = "The proposal appears to claim merge or canonical Record write authority that Grace-Mar doctrine forbids."
    elif doctrine_drift_risks:
        if len(affected_paths) > 3 or len(affected_surfaces) > 1:
            decision = "split"
            rationale = "The proposal mixes multiple paths or surfaces while carrying non-fatal doctrine risk; split it into smaller governed changes."
        else:
            decision = "revise"
            rationale = "The proposal is plausible, but wording or authority signals should be tightened before it proceeds through the normal gate."
    elif len(affected_paths) > 3 or len(affected_surfaces) > 1:
        decision = "defer"
        rationale = "The proposal is broad for a Phase 1 heuristic pass; defer until it is narrowed or broken into smaller pieces."

    report = {
        "type": "counterfactual-simulation-report-v1",
        "proposal_id": proposal["proposal_id"],
        "generated_at": _utc_now_iso(),
        "authority": {
            "recordAuthority": "none",
            "gateEffect": "none",
            "mergeAuthority": "none",
            "simulationOnly": True,
        },
        "input_summary": {
            "proposal_kind": proposal["proposal_kind"],
            "target_paths": affected_paths,
            "target_surfaces": affected_surfaces,
            "proposed_change_summary": summary,
            "evidence_refs": proposal["evidence_refs"],
            "operator_question": proposal["operator_question"],
            "has_patch_text": bool(patch.strip()),
        },
        "affected_paths": affected_paths,
        "affected_surfaces": affected_surfaces,
        "possible_contradictions": possible_contradictions,
        "doctrine_drift_risks": doctrine_drift_risks,
        "follow_up_required": follow_up_required,
        "tests_or_audits_to_run": tests_or_audits_to_run,
        "recommendation": {
            "decision": decision,
            "rationale": rationale,
        },
        "warnings": warnings,
    }
    validate_report(report)
    return report


def validate_report(report: dict[str, Any]) -> None:
    if report.get("type") != "counterfactual-simulation-report-v1":
        raise ValueError("report type must be 'counterfactual-simulation-report-v1'")
    authority = report.get("authority")
    if authority != {
        "recordAuthority": "none",
        "gateEffect": "none",
        "mergeAuthority": "none",
        "simulationOnly": True,
    }:
        raise ValueError("authority block must remain non-authoritative")
    recommendation = report.get("recommendation")
    if not isinstance(recommendation, dict):
        raise ValueError("recommendation must be an object")
    if recommendation.get("decision") not in ALLOWED_DECISIONS:
        raise ValueError(f"recommendation.decision must be one of {sorted(ALLOWED_DECISIONS)!r}")
    if not isinstance(recommendation.get("rationale"), str) or not recommendation["rationale"].strip():
        raise ValueError("recommendation.rationale must be a non-empty string")
    for key in (
        "affected_paths",
        "affected_surfaces",
        "possible_contradictions",
        "doctrine_drift_risks",
        "follow_up_required",
        "tests_or_audits_to_run",
        "warnings",
    ):
        value = report.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{key} must be a list of strings")


def resolve_output_path(repo_root: Path, output: str | None, proposal_id: str) -> Path:
    allowed_root = (repo_root / SCRATCH_DIR).resolve()
    if output:
        path = Path(output)
        if not path.is_absolute():
            path = repo_root / path
    else:
        path = allowed_root / f"{_slugify(proposal_id)}-simulation.json"
    resolved = path.resolve()
    if resolved != allowed_root and allowed_root not in resolved.parents:
        raise ValueError(f"output must stay under {allowed_root}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a scratch-only counterfactual simulation report")
    parser.add_argument("--proposal", required=True, help="Path to proposal JSON")
    parser.add_argument(
        "--output",
        default="",
        help="Optional report path under artifacts/counterfactual-simulations/",
    )
    parser.add_argument(
        "--repo-root",
        default="",
        help="Repo root to read from (default: current working directory)",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd().resolve()
    proposal_path = Path(args.proposal)
    if not proposal_path.is_absolute():
        proposal_path = Path.cwd() / proposal_path
    proposal_path = proposal_path.resolve()

    try:
        proposal = validate_proposal(_load_json(proposal_path))
        report = analyze_counterfactual(proposal, repo_root)
        output_path = resolve_output_path(repo_root, args.output or None, proposal["proposal_id"])
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
