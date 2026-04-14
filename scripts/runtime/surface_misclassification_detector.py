#!/usr/bin/env python3
"""
Surface Misclassification Detector — advisory ontology check for gate proposals.

Reads pending candidates from users/<id>/recursion-gate.md (or JSON / direct args).
Does not rewrite targets, mutate Record surfaces, or change gate state.

See docs/orchestration/surface-misclassification-detector.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CLASSIFICATION_DIR = REPO_ROOT / "artifacts" / "classification-reports"
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = Path(__file__).resolve().parent
for _p in (_SCRIPTS, _RUNTIME):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from recursion_gate_review import (
    _extract_block,
    _extract_scalar,
    parse_review_candidates,
)

DEFAULT_USER = "grace-mar"
CANONICAL_SURFACES = ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE")

SURFACE_SIGNALS = {
    "SELF": frozenset({
        "identity", "self-knowledge", "voice", "personality", "preference",
        "temperament", "curiosity", "values", "ix-a", "ix-b", "ix-c",
    }),
    "SELF-LIBRARY": frozenset({
        "library", "reference", "corpus", "shelf", "domain", "civilization",
        "civilizational", "civ-mem", "source", "tradition", "archive", "reading",
        "roman", "imperial", "encyclopedia", "return-to", "lib-",
    }),
    "SKILLS": frozenset({
        "skill", "capability", "workflow", "operator", "doctrine", "write",
        "think", "procedure", "competence", "ability", "reliable",
    }),
    "EVIDENCE": frozenset({
        "evidence", "artifact", "receipt", "activity", "event", "observation",
        "log", "submission", "trace", "happened", "read-",
    }),
    "WORK_LAYER": frozenset({
        "draft", "explore", "hypothesis", "maybe", "plan", "todo",
        "checkpoint", "handoff", "in-progress", "next step",
    }),
}

SURFACE_EXPLANATIONS = {
    "SELF": "identity and self-knowledge",
    "SELF-LIBRARY": "governed reference and return-to sources",
    "SKILLS": "capability and reliable procedural reach",
    "EVIDENCE": "activity, artifacts, and receipts",
    "WORK_LAYER": "planning, execution, and exploratory work that should not yet redefine the Record",
}


@dataclass
class Proposal:
    proposal_id: str
    candidate_type: str | None = None
    target_surface: str | None = None
    target_path: str | None = None
    proposal_summary: str | None = None
    proposed_change: str | None = None
    source_observation_ids: list[str] = field(default_factory=list)
    supporting_evidence_refs: list[str] = field(default_factory=list)
    contradiction_refs: list[str] = field(default_factory=list)
    confidence: float | None = None
    why_now: str | None = None
    status: str | None = None
    source_file: str | None = None


def now_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_surface(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    aliases = {
        "SELF_LIBRARY": "SELF-LIBRARY",
        "SELF-LIBRARY": "SELF-LIBRARY",
        "SELF": "SELF",
        "SKILLS": "SKILLS",
        "EVIDENCE": "EVIDENCE",
        "WORK_LAYER": "WORK_LAYER",
        "WORK-LAYER": "WORK_LAYER",
        "OTHER": "OTHER",
    }
    return aliases.get(value, value)


def _extract_yaml_string_list(yaml_body: str, key: str) -> list[str]:
    prefix = f"{key}:"
    lines = yaml_body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith(prefix):
            i += 1
            while i < len(lines):
                ln = lines[i]
                if not ln.strip():
                    i += 1
                    continue
                m = re.match(r"^\s+-\s+(.+)$", ln)
                if m:
                    val = m.group(1).strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    out.append(val)
                    i += 1
                    continue
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s", ln):
                    break
                i += 1
            break
        i += 1
    return out


def _extract_source_observation_ids(yaml_body: str) -> list[str]:
    return _extract_yaml_string_list(yaml_body, "source_observation_ids")


def _find_gate_row(user_id: str, candidate_id: str, *, repo_root: Path | None) -> dict | None:
    for row in parse_review_candidates(user_id=user_id, repo_root=repo_root):
        if row["id"] == candidate_id:
            return row
    return None


def proposal_from_gate_row(
    row: dict,
    raw_block: str,
    *,
    user_id: str,
    repo_root: Path | None,
) -> Proposal:
    root = repo_root.resolve() if repo_root else REPO_ROOT
    gate_rel = (root / "users" / user_id / "recursion-gate.md").relative_to(root)
    yaml_target = _extract_scalar(raw_block, "target_surface")
    proposal_summary = (
        _extract_scalar(raw_block, "proposal_summary").strip() or (row.get("summary") or "").strip()
    )
    proposed_change = _extract_block(raw_block, "proposed_change").strip() or (
        (row.get("suggested_entry") or "")[:4000]
    )
    ctype = _extract_scalar(raw_block, "candidate_type") or row.get("proposal_class")
    conf_raw = _extract_scalar(raw_block, "confidence")
    conf: float | None = None
    if conf_raw and conf_raw.lower() != "null":
        try:
            conf = float(conf_raw)
        except ValueError:
            conf = None
    return Proposal(
        proposal_id=row["id"],
        candidate_type=str(ctype).strip() if ctype else None,
        target_surface=normalize_surface(yaml_target) if yaml_target else None,
        target_path=_extract_scalar(raw_block, "target_path") or None,
        proposal_summary=proposal_summary or None,
        proposed_change=proposed_change or None,
        source_observation_ids=_extract_source_observation_ids(raw_block),
        supporting_evidence_refs=_extract_yaml_string_list(raw_block, "supporting_evidence_refs"),
        contradiction_refs=_extract_yaml_string_list(raw_block, "contradiction_refs"),
        confidence=conf,
        why_now=_extract_scalar(raw_block, "why_now") or None,
        status=_extract_scalar(raw_block, "status") or None,
        source_file=str(gate_rel),
    )


def proposal_from_json_payload(payload: dict[str, Any]) -> Proposal:
    why = payload.get("why_now")
    conf = payload.get("confidence")
    cfloat: float | None = None
    if isinstance(conf, (int, float)):
        cfloat = float(conf)
    tp = payload.get("target_path")
    tpath = str(tp).strip() if tp not in (None, "") else None
    return Proposal(
        proposal_id=str(payload.get("gate_candidate_id") or payload.get("candidate_id") or "FILE-PROPOSAL"),
        candidate_type=str(payload.get("candidate_type") or "").strip() or None,
        target_surface=normalize_surface(str(payload.get("target_surface") or "") or None),
        target_path=tpath,
        proposal_summary=str(payload.get("proposal_summary") or payload.get("summary") or ""),
        proposed_change=str(payload.get("proposed_change") or ""),
        source_observation_ids=[str(x) for x in (payload.get("source_observation_ids") or [])],
        supporting_evidence_refs=[str(x) for x in (payload.get("supporting_evidence_refs") or [])],
        contradiction_refs=[str(x) for x in (payload.get("contradiction_refs") or [])],
        confidence=cfloat,
        why_now=str(why).strip() if why is not None else None,
        status=str(payload.get("status") or "").strip() or None,
        source_file=None,
    )


def score_surface_signals(proposal: Proposal) -> dict[str, int]:
    text_parts = [
        proposal.proposal_summary or "",
        proposal.proposed_change or "",
        proposal.why_now or "",
        " ".join(proposal.supporting_evidence_refs),
        " ".join(proposal.contradiction_refs),
        proposal.target_path or "",
    ]
    text = " ".join(text_parts).lower()
    scores: dict[str, int] = {key: 0 for key in SURFACE_SIGNALS}
    for surface, keywords in SURFACE_SIGNALS.items():
        for kw in keywords:
            if kw in text:
                scores[surface] += 1
    ctype = (proposal.candidate_type or "").lower()
    if "skill" in ctype:
        scores["SKILLS"] += 2
    if "evidence" in ctype or "read" in ctype:
        scores["EVIDENCE"] += 2
    if "identity" in ctype:
        scores["SELF"] += 2
    if "library" in ctype or "reference" in ctype:
        scores["SELF-LIBRARY"] += 2
    if len(proposal.supporting_evidence_refs) == 0 and len(proposal.source_observation_ids) > 0:
        scores["WORK_LAYER"] += 2
    if proposal.contradiction_refs:
        scores["WORK_LAYER"] += 1
    decl = normalize_surface(proposal.target_surface)
    if decl in ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE"):
        scores[decl] += 1
    return scores


def best_fit_surface(scores: dict[str, int]) -> str:
    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[0][0]


def classification_risk(
    proposal: Proposal, predicted: str, scores: dict[str, int]
) -> tuple[str, str]:
    declared = normalize_surface(proposal.target_surface)
    work_score = scores.get("WORK_LAYER", 0)
    pred_score = scores.get(predicted, 0)
    if predicted == "WORK_LAYER":
        return "high", (
            "content appears exploratory, contradictory, or under-evidenced enough to remain in work territory"
        )
    if declared and declared != predicted and declared in ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE"):
        if work_score >= pred_score or len(proposal.contradiction_refs) > 0 or len(
            proposal.supporting_evidence_refs
        ) == 0:
            return "high", (
                "declared surface diverges from dominant content signals and support looks premature or unstable"
            )
        return "medium", "declared surface diverges from dominant content signals"
    if len(proposal.contradiction_refs) >= 2:
        return "medium", "proposal may be surface-correct but remains unstable due to unresolved contradiction pressure"
    return "low", "declared surface broadly matches the observed content signals"


def recommendation(proposal: Proposal, predicted: str, risk: str) -> str:
    declared = normalize_surface(proposal.target_surface)
    if predicted == "WORK_LAYER":
        return "suggest_alternative_surface"
    if declared and declared != predicted and declared in CANONICAL_SURFACES:
        return "review_surface_choice"
    if risk == "low":
        return "keep_current_surface"
    return "review_surface_choice"


def defensibility_requirements(proposal: Proposal, predicted: str) -> list[str]:
    reqs: list[str] = []
    declared = normalize_surface(proposal.target_surface)
    if predicted == "WORK_LAYER":
        reqs.append("stronger evidence and fewer unresolved contradictions before canonical promotion")
    if declared == "SELF":
        reqs.append("clear identity-facing evidence rather than primarily reference or workflow framing")
    if declared == "SELF-LIBRARY":
        reqs.append("clear governed reference / return-to source logic rather than identity or capability claims")
    if declared == "SKILLS":
        reqs.append("evidence that the proposal describes reliable capability, not a one-off artifact or event")
    if declared == "EVIDENCE":
        reqs.append("evidence that the proposal is about activity or receipts, not durable doctrine or capability")
    if len(proposal.supporting_evidence_refs) == 0:
        reqs.append("explicit evidence references")
    if proposal.contradiction_refs:
        reqs.append("resolution or narrowing of contradiction refs")
    if not reqs:
        reqs.append(
            "operator confirmation that the surface placement improves clarity rather than distorting ontology"
        )
    return reqs


def build_report(
    proposal: Proposal,
    *,
    boundary_review: dict[str, Any] | None = None,
) -> str:
    scores = score_surface_signals(proposal)
    predicted = best_fit_surface(scores)
    risk, reason = classification_risk(proposal, predicted, scores)
    declared = normalize_surface(proposal.target_surface) or "unknown"
    rec = recommendation(proposal, predicted, risk)
    alt_surface = predicted if predicted != declared else "none"
    lines = [
        "# Classification Risk Report",
        "",
        f"Built: {now_z()}",
        f"Proposal: {proposal.proposal_id}",
        f"Claimed Target Surface: {declared}",
        f"Predicted Best-Fit Surface: {predicted}",
        f"Risk: {risk}",
        f"Recommendation: {rec}",
        "",
        "**Boundary:**",
        "This report is **advisory only**.",
        "It does not update SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or `recursion-gate.md`.",
        "",
        "## Proposed change",
        proposal.proposal_summary or "(no summary provided)",
        "",
    ]
    if proposal.proposed_change:
        lines.extend([proposal.proposed_change, ""])
    lines.extend(["## Why the current classification may be wrong", f"- {reason}", ""])
    if boundary_review and boundary_review.get("misfiled_warning"):
        lines.append(f"- **Gate boundary_review:** {boundary_review['misfiled_warning']}")
        lines.append("")
    lines.extend([
        "## Best-fit alternative",
        f"- {alt_surface}",
        "",
        "## Signals considered",
        f"- Score map: {scores}",
        f"- Candidate type: {proposal.candidate_type or 'n/a'}",
        f"- Supporting evidence refs: {len(proposal.supporting_evidence_refs)}",
        f"- Contradiction refs: {len(proposal.contradiction_refs)}",
        f"- Source observations: {len(proposal.source_observation_ids)}",
        f"- Target path: {proposal.target_path or 'n/a'}",
        f"- Source file: {proposal.source_file or 'unknown'}",
        "",
        "## Surface meanings in play",
        f"- SELF → {SURFACE_EXPLANATIONS['SELF']}",
        f"- SELF-LIBRARY → {SURFACE_EXPLANATIONS['SELF-LIBRARY']}",
        f"- SKILLS → {SURFACE_EXPLANATIONS['SKILLS']}",
        f"- EVIDENCE → {SURFACE_EXPLANATIONS['EVIDENCE']}",
        f"- WORK_LAYER → {SURFACE_EXPLANATIONS['WORK_LAYER']}",
        "",
        "## What would make the current classification more defensible?",
    ])
    for item in defensibility_requirements(proposal, predicted):
        lines.append(f"- {item}")
    lines.extend(["", "## Operator question"])
    if predicted == "WORK_LAYER":
        lines.append(
            "Is this actually ready for any canonical surface, or should it remain an exploratory work artifact for now?"
        )
    elif declared != predicted and declared in CANONICAL_SURFACES + ("WORK_LAYER",):
        lines.append(f"Is this really a {declared} change, or is it more truthfully a {predicted} change?")
    else:
        lines.append(
            "Does this placement clarify the ontology, or does it still blur identity, reference, capability, and evidence?"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Advisory surface misclassification check for Grace-Mar gate proposals (read-only)."
    )
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    ap.add_argument("--repo-root", type=Path, default=None, help="Repository root (tests)")
    ap.add_argument("--candidate", default=None, help="CANDIDATE-NNNN in pending gate section")
    ap.add_argument("--proposal-file", type=Path, default=None, help="JSON (schema-aligned gate candidate payload)")
    ap.add_argument("--target-surface", default=None, help="Direct mode: SELF | SELF-LIBRARY | SKILLS | EVIDENCE")
    ap.add_argument("--proposal-summary", default=None)
    ap.add_argument("--proposed-change", default=None)
    ap.add_argument(
        "-o", "--output", type=Path, default=None,
        help=f"Output Markdown (default: {DEFAULT_CLASSIFICATION_DIR}/<id>.md)",
    )
    args = ap.parse_args()
    repo_root = args.repo_root.resolve() if args.repo_root else None
    has_direct = (
        bool(args.target_surface and str(args.target_surface).strip())
        and args.proposal_summary is not None
        and args.proposed_change is not None
    )
    direct_any = (
        bool(args.target_surface and str(args.target_surface).strip())
        or args.proposal_summary is not None
        or args.proposed_change is not None
    )
    if direct_any and not has_direct:
        print(
            "error: direct mode requires --target-surface, --proposal-summary, and --proposed-change together",
            file=sys.stderr,
        )
        return 2
    modes = sum(
        1 for x in (
            bool(args.candidate and str(args.candidate).strip()),
            bool(args.proposal_file),
            has_direct,
        ) if x
    )
    if modes != 1:
        print(
            "error: specify exactly one of: --candidate, --proposal-file, or "
            "(--target-surface + --proposal-summary + --proposed-change)",
            file=sys.stderr,
        )
        return 2
    row = None
    boundary_review = None
    if args.candidate:
        cid = args.candidate.strip()
        row = _find_gate_row(args.user, cid, repo_root=repo_root)
        if row is None:
            print(f"error: candidate not found in active gate section: {cid}", file=sys.stderr)
            return 2
        raw_block = row.get("raw_block") or ""
        proposal = proposal_from_gate_row(row, raw_block, user_id=args.user, repo_root=repo_root)
        boundary_review = row.get("boundary_review")
    elif args.proposal_file:
        path = args.proposal_file
        if not path.is_absolute():
            path = (repo_root if repo_root else REPO_ROOT) / path
        if not path.is_file():
            print(f"error: proposal file not found: {path}", file=sys.stderr)
            return 2
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(payload, dict):
            print("error: proposal JSON must be an object", file=sys.stderr)
            return 2
        proposal = proposal_from_json_payload(payload)
        try:
            proposal.source_file = str(path.relative_to(REPO_ROOT))
        except ValueError:
            proposal.source_file = str(path)
    else:
        proposal = Proposal(
            proposal_id="DIRECT-PROPOSAL",
            target_surface=normalize_surface(args.target_surface),
            proposal_summary=(args.proposal_summary or "").strip(),
            proposed_change=(args.proposed_change or "").strip(),
            status="analysis_only",
            source_file="direct-args",
        )
    if not (proposal.proposal_summary or "").strip() and not (proposal.proposed_change or "").strip():
        print("error: proposal has no proposal_summary or proposed_change content", file=sys.stderr)
        return 2
    report = build_report(proposal, boundary_review=boundary_review)
    out = args.output
    if out is None:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", proposal.proposal_id).strip("-") or "classification-report"
        DEFAULT_CLASSIFICATION_DIR.mkdir(parents=True, exist_ok=True)
        out = DEFAULT_CLASSIFICATION_DIR / f"{safe}.md"
    else:
        out = Path(out)
        if not out.is_absolute():
            out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
