#!/usr/bin/env python3
"""
Governed Skill Evaluation Clinic.

This script evaluates a Grace-Mar skill file using local rubric checks and emits
a derived report. It does not call an LLM, edit skill files, approve candidates,
or merge anything.

The point is to make improvement candidates reviewable, not automatic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCHEMA_REL = Path("schemas/skill-eval-report.v1.schema.json")

DIMENSIONS = [
    "boundary_safety",
    "evidence_posture",
    "gate_awareness",
    "operator_clarity",
    "failure_mode_awareness",
]

GOVERNANCE_NOTE = (
    "This report is a derived artifact. It does not edit, approve, or merge "
    "canonical skill content. Candidate improvements require human review and "
    "the normal Grace-Mar gate process before any durable adoption."
)


@dataclass(frozen=True)
class Finding:
    level: str
    dimension: str
    message: str


@dataclass(frozen=True)
class CandidateImprovement:
    priority: str
    target_dimension: str
    recommendation: str
    candidate_text: str


@dataclass(frozen=True)
class SkillEvalReport:
    schema_version: str
    skill_path: str
    overall_score: float
    scores: dict[str, float]
    findings: list[Finding]
    candidate_improvements: list[CandidateImprovement]
    governance_note: str


def read_skill(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Skill file not found: {path}")
    if not path.is_file():
        raise SystemExit(f"Skill path is not a file: {path}")
    return path.read_text(encoding="utf-8")


def contains_any(text: str, patterns: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def regex_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def score_boundary_safety(text: str, findings: list[Finding], improvements: list[CandidateImprovement]) -> float:
    score = 20.0
    boundary_terms = [
        "record",
        "runtime",
        "canonical",
        "derived",
        "staged",
        "candidate",
        "work lane",
        "work-lane",
        "surface",
    ]
    if not contains_any(text, boundary_terms):
        score -= 10
        findings.append(
            Finding(
                "risk",
                "boundary_safety",
                "Skill does not visibly define runtime/work/Record or canonical/derived boundaries.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "high",
                "boundary_safety",
                "Add an explicit boundary rule.",
                "Boundary rule: this skill may generate advisory or staged work products, but it may not directly alter canonical Record surfaces or treat runtime context as durable truth.",
            )
        )
    unsafe_mutation_terms = [
        "automatically update the record",
        "auto-merge",
        "merge without review",
        "overwrite canonical",
        "silently update",
    ]
    if contains_any(text, unsafe_mutation_terms):
        score -= 8
        findings.append(
            Finding(
                "risk",
                "boundary_safety",
                "Skill appears to allow unsafe automatic mutation or merge behavior.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "high",
                "boundary_safety",
                "Replace automatic mutation language with staged-candidate language.",
                "Durable changes must be staged as candidates and reviewed before adoption.",
            )
        )
    return max(score, 0.0)


def score_evidence_posture(text: str, findings: list[Finding], improvements: list[CandidateImprovement]) -> float:
    score = 20.0
    evidence_terms = [
        "evidence",
        "source",
        "citation",
        "receipt",
        "warrant",
        "provenance",
        "reference",
        "input",
    ]
    if not contains_any(text, evidence_terms):
        score -= 10
        findings.append(
            Finding(
                "warn",
                "evidence_posture",
                "Skill does not clearly require evidence, sources, receipts, or warrants.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "medium",
                "evidence_posture",
                "Add an evidence posture clause.",
                "Evidence posture: when producing claims that may influence durable state, include source references, input paths, receipts, or explicit uncertainty notes.",
            )
        )
    if contains_any(text, ["assume", "infer"]) and not contains_any(text, ["uncertain", "uncertainty", "confidence"]):
        score -= 4
        findings.append(
            Finding(
                "warn",
                "evidence_posture",
                "Skill uses assumption/inference language without clear uncertainty handling.",
            )
        )
    return max(score, 0.0)


def score_gate_awareness(text: str, findings: list[Finding], improvements: list[CandidateImprovement]) -> float:
    score = 20.0
    gate_terms = [
        "gate",
        "review",
        "approval",
        "approved",
        "candidate",
        "pending-review",
        "recursion-gate",
    ]
    if not contains_any(text, gate_terms):
        score -= 10
        findings.append(
            Finding(
                "risk",
                "gate_awareness",
                "Skill does not visibly mention gate, review, approval, or candidate workflow.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "high",
                "gate_awareness",
                "Add explicit gate-awareness language.",
                "Gate rule: outputs that would change durable state must be routed to review as candidates; this skill cannot approve or merge its own recommendations.",
            )
        )
    unsafe_authority_terms = [
        "approve its own",
        "self-approve",
        "merge its own",
        "no review required",
    ]
    if contains_any(text, unsafe_authority_terms):
        score -= 10
        findings.append(
            Finding(
                "risk",
                "gate_awareness",
                "Skill contains language suggesting self-approval or bypassing review.",
            )
        )
    return max(score, 0.0)


def score_operator_clarity(text: str, findings: list[Finding], improvements: list[CandidateImprovement]) -> float:
    score = 20.0
    has_when = regex_any(text, [r"\bwhen to use\b", r"\buse this\b", r"\btrigger\b"])
    has_output = regex_any(text, [r"\boutput\b", r"\bproduce\b", r"\breturn\b", r"\breport\b"])
    has_steps = regex_any(text, [r"\bstep\b", r"\bworkflow\b", r"\bprocedure\b", r"\bprocess\b"])
    if not has_when:
        score -= 5
        findings.append(
            Finding(
                "warn",
                "operator_clarity",
                "Skill does not clearly say when it should be used.",
            )
        )
    if not has_output:
        score -= 5
        findings.append(
            Finding(
                "warn",
                "operator_clarity",
                "Skill does not clearly define expected outputs.",
            )
        )
    if not has_steps:
        score -= 4
        findings.append(
            Finding(
                "info",
                "operator_clarity",
                "Skill may benefit from a short procedure or workflow section.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "low",
                "operator_clarity",
                "Add a concise workflow section.",
                "Workflow: identify the request class; gather required context; produce advisory output; flag any durable-state implications; route candidates to review.",
            )
        )
    return max(score, 0.0)


def score_failure_mode_awareness(text: str, findings: list[Finding], improvements: list[CandidateImprovement]) -> float:
    score = 20.0
    failure_terms = [
        "failure mode",
        "risk",
        "limitation",
        "do not",
        "must not",
        "avoid",
        "unsafe",
        "misuse",
    ]
    if not contains_any(text, failure_terms):
        score -= 12
        findings.append(
            Finding(
                "warn",
                "failure_mode_awareness",
                "Skill does not clearly list risks, limitations, or failure modes.",
            )
        )
        improvements.append(
            CandidateImprovement(
                "medium",
                "failure_mode_awareness",
                "Add a failure-mode section.",
                "Known failure modes: over-promoting runtime context; collapsing advisory work into canonical memory; omitting evidence; bypassing review; treating candidate text as approved doctrine.",
            )
        )
    must_not_count = len(re.findall(r"\b(must not|do not|never|avoid)\b", text, flags=re.IGNORECASE))
    if must_not_count == 0:
        score -= 4
        findings.append(
            Finding(
                "info",
                "failure_mode_awareness",
                "Skill has no explicit negative constraints.",
            )
        )
    return max(score, 0.0)


def evaluate_skill(path: Path) -> SkillEvalReport:
    text = read_skill(path)
    findings: list[Finding] = []
    improvements: list[CandidateImprovement] = []
    scores = {
        "boundary_safety": score_boundary_safety(text, findings, improvements),
        "evidence_posture": score_evidence_posture(text, findings, improvements),
        "gate_awareness": score_gate_awareness(text, findings, improvements),
        "operator_clarity": score_operator_clarity(text, findings, improvements),
        "failure_mode_awareness": score_failure_mode_awareness(text, findings, improvements),
    }
    overall = round(sum(scores.values()), 2)
    if overall >= 85:
        findings.append(Finding("info", "operator_clarity", "Skill appears strong under the local clinic rubric."))
    elif overall < 60:
        findings.append(Finding("risk", "gate_awareness", "Skill should be reviewed before being used as a durable workflow guide."))
    return SkillEvalReport(
        schema_version="skill-eval-report.v1",
        skill_path=str(path.resolve()),
        overall_score=overall,
        scores=scores,
        findings=findings,
        candidate_improvements=improvements,
        governance_note=GOVERNANCE_NOTE,
    )


def report_to_jsonable(report: SkillEvalReport) -> dict:
    return {
        "schema_version": report.schema_version,
        "skill_path": report.skill_path,
        "overall_score": report.overall_score,
        "scores": report.scores,
        "findings": [asdict(item) for item in report.findings],
        "candidate_improvements": [asdict(item) for item in report.candidate_improvements],
        "governance_note": report.governance_note,
    }


def validate_report_json(repo_root: Path, jsonable: dict) -> None:
    """Raise jsonschema.ValidationError if instance does not match schema."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError as e:
        raise SystemExit("jsonschema is required (pip install jsonschema)") from e

    schema_path = repo_root / _SCHEMA_REL
    if not schema_path.is_file():
        raise SystemExit(f"Schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(jsonable)


def report_to_markdown(report: SkillEvalReport) -> str:
    lines = [
        "# Skill Evaluation Clinic Report",
        "",
        f"- Skill: `{report.skill_path}`",
        f"- Overall score: `{report.overall_score}/100`",
        "",
        "## Scores",
        "",
        "| Dimension | Score |",
        "|---|---:|",
    ]
    for dimension in DIMENSIONS:
        lines.append(f"| `{dimension}` | {report.scores[dimension]}/20 |")
    lines.extend(["", "## Findings", ""])
    if report.findings:
        for finding in report.findings:
            lines.append(f"- **{finding.level.upper()}** `{finding.dimension}` — {finding.message}")
    else:
        lines.append("No findings.")
    lines.extend(["", "## Candidate Improvements", ""])
    if report.candidate_improvements:
        for item in report.candidate_improvements:
            lines.extend(
                [
                    f"### {item.priority.upper()} — `{item.target_dimension}`",
                    "",
                    item.recommendation,
                    "",
                    "Candidate text:",
                    "",
                    "```text",
                    item.candidate_text,
                    "```",
                    "",
                ]
            )
    else:
        lines.append("No candidate improvements generated.")
    lines.extend(["", "## Governance Note", "", report.governance_note, ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a Grace-Mar skill file without mutating it.")
    parser.add_argument("--skill", required=True, type=Path, help="Path to skill Markdown file.")
    parser.add_argument("--out", required=True, type=Path, help="Path to write JSON report.")
    parser.add_argument("--markdown", type=Path, default=None, help="Optional path to write Markdown report.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root for schema validation (default: inferred from script location).",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    report = evaluate_skill(args.skill)
    jsonable = report_to_jsonable(report)

    try:
        validate_report_json(repo_root, jsonable)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Report failed schema validation: {e}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(jsonable, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote JSON report: {args.out}")

    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(report_to_markdown(report), encoding="utf-8")
        print(f"Wrote Markdown report: {args.markdown}")

    risk_count = sum(1 for finding in report.findings if finding.level == "risk")
    if risk_count:
        print(f"Completed with {risk_count} risk finding(s).")
    else:
        print("Completed with no risk findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
