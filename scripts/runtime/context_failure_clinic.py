#!/usr/bin/env python3
"""
Grace-Mar Context Failure Diagnostics Clinic.

This script performs local, heuristic checks for context/retrieval/routing failures.
It does not call an LLM, mutate Record surfaces, approve candidates, or merge anything.

It is intentionally conservative: it flags likely risks for review rather than trying
to resolve them automatically.
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
_SCHEMA_REL = Path("schemas/context-failure-report.v1.schema.json")

CATEGORIES = [
    "surface_confusion",
    "stale_context",
    "missing_evidence",
    "compression_loss",
    "lane_misrouting",
    "authority_drift",
    "synthesis_overreach",
]

GOVERNANCE_NOTE = (
    "This report is a derived diagnostic artifact. It does not alter canonical "
    "Record surfaces, approve candidates, merge candidates, or resolve context "
    "failures automatically. Recommended actions require operator review."
)


@dataclass(frozen=True)
class Finding:
    level: str
    category: str
    message: str
    matched_terms: list[str]


@dataclass(frozen=True)
class RecommendedAction:
    priority: str
    category: str
    action: str


@dataclass(frozen=True)
class ContextFailureReport:
    schema_version: str
    input_path: str
    overall_risk: str
    category_scores: dict[str, int]
    findings: list[Finding]
    recommended_actions: list[RecommendedAction]
    governance_note: str


def read_input(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    if not path.is_file():
        raise SystemExit(f"Input path is not a file: {path}")
    return path.read_text(encoding="utf-8")


def find_terms(text: str, terms: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return sorted({term for term in terms if term.lower() in lowered})


def regex_matches(text: str, patterns: Iterable[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            matches.append(pattern)
    return matches


def add_score(scores: dict[str, int], category: str, amount: int) -> None:
    scores[category] = min(10, scores.get(category, 0) + amount)


def diagnose_surface_confusion(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    canonical_terms = find_terms(
        text,
        [
            "canonical",
            "record",
            "durable truth",
            "source of truth",
            "approved memory",
            "permanent memory",
        ],
    )
    derived_terms = find_terms(
        text,
        [
            "runtime",
            "prepared context",
            "derived artifact",
            "dashboard",
            "work lane",
            "notebook",
            "candidate",
            "draft",
        ],
    )
    risky_phrases = regex_matches(
        text,
        [
            r"runtime .* (is|as) .* canonical",
            r"derived .* (is|as) .* record",
            r"draft .* (is|as) .* approved",
            r"candidate .* (is|as) .* canonical",
            r"work[- ]lane .* (is|as) .* record",
        ],
    )
    if canonical_terms and derived_terms:
        add_score(scores, "surface_confusion", 3)
        findings.append(
            Finding(
                "warn",
                "surface_confusion",
                "Input mixes canonical/Record language with runtime/work/derived language; confirm surface boundaries.",
                canonical_terms + derived_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "medium",
                "surface_confusion",
                "Add or verify a surface classification block: canonical, staged candidate, work-lane artifact, prepared context, or runtime-only.",
            )
        )
    if risky_phrases:
        add_score(scores, "surface_confusion", 7)
        findings.append(
            Finding(
                "risk",
                "surface_confusion",
                "Input contains language that may confuse derived/runtime material with canonical Record status.",
                risky_phrases,
            )
        )
        actions.append(
            RecommendedAction(
                "high",
                "surface_confusion",
                "Route this item through review before any durable-state use; explicitly restate that derived/runtime material is not canonical.",
            )
        )


def diagnose_stale_context(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    date_like = regex_matches(
        text,
        [
            r"\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b",
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? [0-9]{1,2}, 20[0-9]{2}\b",
            r"\bQ[1-4] 20[0-9]{2}\b",
        ],
    )
    freshness_terms = find_terms(
        text,
        [
            "stale",
            "current as of",
            "last updated",
            "refresh",
            "freshness",
            "recency",
            "superseded",
        ],
    )
    if date_like and not freshness_terms:
        add_score(scores, "stale_context", 4)
        findings.append(
            Finding(
                "warn",
                "stale_context",
                "Input contains date-like references without visible freshness or supersession handling.",
                date_like,
            )
        )
        actions.append(
            RecommendedAction(
                "medium",
                "stale_context",
                "Add a freshness note: source date, last-checked date, and whether newer evidence may supersede the claim.",
            )
        )
    if find_terms(text, ["obsolete", "deprecated", "superseded"]) and not find_terms(text, ["replacement", "current"]):
        add_score(scores, "stale_context", 5)
        findings.append(
            Finding(
                "risk",
                "stale_context",
                "Input flags obsolete/deprecated material without naming the replacement authority.",
                find_terms(text, ["obsolete", "deprecated", "superseded"]),
            )
        )
        actions.append(
            RecommendedAction(
                "high",
                "stale_context",
                "Identify the replacement file, authority surface, or current workflow before reusing this context.",
            )
        )


def diagnose_missing_evidence(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    claim_terms = find_terms(
        text,
        [
            "therefore",
            "proves",
            "demonstrates",
            "shows that",
            "confirms",
            "clearly",
            "must mean",
            "we know",
        ],
    )
    evidence_terms = find_terms(
        text,
        [
            "source:",
            "sources:",
            "evidence:",
            "receipt:",
            "input:",
            "citation",
            "warrant",
            "provenance",
            "raw-input",
            "file:",
        ],
    )
    if claim_terms and not evidence_terms:
        add_score(scores, "missing_evidence", 6)
        findings.append(
            Finding(
                "risk",
                "missing_evidence",
                "Input makes strong interpretive claims without visible source, receipt, input path, warrant, or provenance marker.",
                claim_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "high",
                "missing_evidence",
                "Add evidence anchors before routing this into a candidate, notebook synthesis, or durable review process.",
            )
        )
    if not evidence_terms:
        add_score(scores, "missing_evidence", 2)
        findings.append(
            Finding(
                "info",
                "missing_evidence",
                "No explicit evidence/provenance marker was found.",
                [],
            )
        )


def diagnose_compression_loss(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    compression_terms = find_terms(
        text,
        [
            "summary",
            "summarized",
            "compressed",
            "condensed",
            "brief",
            "digest",
            "reduced",
        ],
    )
    anchor_terms = find_terms(
        text,
        [
            "anchor",
            "quote",
            "verbatim",
            "source line",
            "receipt",
            "restore",
            "dropped",
            "omitted",
        ],
    )
    if compression_terms and not anchor_terms:
        add_score(scores, "compression_loss", 5)
        findings.append(
            Finding(
                "warn",
                "compression_loss",
                "Input appears compressed or summarized without anchor, quote, restore, or dropped-content notes.",
                compression_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "medium",
                "compression_loss",
                "Add a compression receipt identifying preserved anchors, dropped sections, and restore instructions.",
            )
        )
    if find_terms(text, ["unabridged", "complete"]) and compression_terms:
        add_score(scores, "compression_loss", 4)
        findings.append(
            Finding(
                "warn",
                "compression_loss",
                "Input mixes completeness language with compression language; confirm whether the artifact is complete or condensed.",
                compression_terms,
            )
        )


def diagnose_lane_misrouting(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    lane_terms = find_terms(
        text,
        [
            "work-strategy",
            "work-dev",
            "work-politics",
            "history-notebook",
            "strategy-notebook",
            "expert thread",
            "state thread",
            "recursion-gate",
            "approval inbox",
        ],
    )
    ambiguity_terms = find_terms(
        text,
        [
            "not sure where",
            "wrong lane",
            "route",
            "routing",
            "misrouted",
            "should this go",
        ],
    )
    if len(lane_terms) >= 2 and ambiguity_terms:
        add_score(scores, "lane_misrouting", 6)
        findings.append(
            Finding(
                "risk",
                "lane_misrouting",
                "Input mentions multiple lanes/surfaces and routing ambiguity.",
                lane_terms + ambiguity_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "high",
                "lane_misrouting",
                "Classify the target lane before synthesis: work-dev, work-strategy, history-notebook, strategy-notebook, review/gate, or Record.",
            )
        )
    elif len(lane_terms) >= 3:
        add_score(scores, "lane_misrouting", 3)
        findings.append(
            Finding(
                "warn",
                "lane_misrouting",
                "Input references several lanes/surfaces; confirm the intended destination.",
                lane_terms,
            )
        )


def diagnose_authority_drift(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    unsafe_terms = find_terms(
        text,
        [
            "auto-approve",
            "auto approve",
            "self-approve",
            "merge directly",
            "merge without review",
            "overwrite record",
            "update canonical",
            "promote to record",
            "approved automatically",
        ],
    )
    if unsafe_terms:
        add_score(scores, "authority_drift", 9)
        findings.append(
            Finding(
                "risk",
                "authority_drift",
                "Input contains language suggesting approval, merge, or canonical update authority.",
                unsafe_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "high",
                "authority_drift",
                "Replace authority-drift language with staged-candidate language and require review before durable adoption.",
            )
        )
    if (
        find_terms(text, ["candidate", "proposal"])
        and find_terms(text, ["approved", "canonical"])
        and not find_terms(text, ["reviewed", "operator"])
    ):
        add_score(scores, "authority_drift", 5)
        findings.append(
            Finding(
                "warn",
                "authority_drift",
                "Candidate/proposal language appears near approved/canonical language without visible review authority.",
                find_terms(text, ["candidate", "proposal", "approved", "canonical"]),
            )
        )


def diagnose_synthesis_overreach(
    text: str,
    scores: dict[str, int],
    findings: list[Finding],
    actions: list[RecommendedAction],
) -> None:
    overreach_terms = find_terms(
        text,
        [
            "definitively",
            "certainly",
            "undeniably",
            "proves",
            "no alternative",
            "only explanation",
            "must mean",
            "settled",
        ],
    )
    uncertainty_terms = find_terms(
        text,
        [
            "uncertain",
            "confidence",
            "alternative",
            "could",
            "may",
            "possibly",
            "disconfirm",
            "ambiguity",
            "partial",
        ],
    )
    if overreach_terms and not uncertainty_terms:
        add_score(scores, "synthesis_overreach", 6)
        findings.append(
            Finding(
                "risk",
                "synthesis_overreach",
                "Input uses high-certainty synthesis language without visible uncertainty or alternative-hypothesis handling.",
                overreach_terms,
            )
        )
        actions.append(
            RecommendedAction(
                "medium",
                "synthesis_overreach",
                "Add confidence level, alternative interpretations, and evidence that would disconfirm the synthesis.",
            )
        )


def compute_overall_risk(scores: dict[str, int]) -> str:
    max_score = max(scores.values()) if scores else 0
    total = sum(scores.values())
    if max_score >= 8 or total >= 24:
        return "high"
    if max_score >= 5 or total >= 12:
        return "medium"
    return "low"


def dedupe_actions(actions: list[RecommendedAction]) -> list[RecommendedAction]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[RecommendedAction] = []
    for action in actions:
        key = (action.priority, action.category, action.action)
        if key not in seen:
            deduped.append(action)
            seen.add(key)
    return deduped


def evaluate_context(path: Path) -> ContextFailureReport:
    text = read_input(path)
    scores = {category: 0 for category in CATEGORIES}
    findings: list[Finding] = []
    actions: list[RecommendedAction] = []
    diagnose_surface_confusion(text, scores, findings, actions)
    diagnose_stale_context(text, scores, findings, actions)
    diagnose_missing_evidence(text, scores, findings, actions)
    diagnose_compression_loss(text, scores, findings, actions)
    diagnose_lane_misrouting(text, scores, findings, actions)
    diagnose_authority_drift(text, scores, findings, actions)
    diagnose_synthesis_overreach(text, scores, findings, actions)
    if not findings:
        findings.append(
            Finding(
                "info",
                "missing_evidence",
                "No obvious context-failure signatures were detected by local heuristics.",
                [],
            )
        )
    risk = compute_overall_risk(scores)
    if not actions and risk != "low":
        actions.append(
            RecommendedAction(
                "medium",
                "missing_evidence",
                "Review the item manually before using it in durable or candidate-generating workflows.",
            )
        )
    return ContextFailureReport(
        schema_version="context-failure-report.v1",
        input_path=str(path.resolve()),
        overall_risk=risk,
        category_scores=scores,
        findings=findings,
        recommended_actions=dedupe_actions(actions),
        governance_note=GOVERNANCE_NOTE,
    )


def report_to_jsonable(report: ContextFailureReport) -> dict:
    return {
        "schema_version": report.schema_version,
        "input_path": report.input_path,
        "overall_risk": report.overall_risk,
        "category_scores": report.category_scores,
        "findings": [asdict(item) for item in report.findings],
        "recommended_actions": [asdict(item) for item in report.recommended_actions],
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


def report_to_markdown(report: ContextFailureReport) -> str:
    lines = [
        "# Context Failure Diagnostics Report",
        "",
        f"- Input: `{report.input_path}`",
        f"- Overall risk: `{report.overall_risk}`",
        "",
        "## Category Scores",
        "",
        "| Category | Score |",
        "|---|---:|",
    ]
    for category in CATEGORIES:
        lines.append(f"| `{category}` | {report.category_scores[category]}/10 |")
    lines.extend(["", "## Findings", ""])
    for finding in report.findings:
        matched = ", ".join(f"`{term}`" for term in finding.matched_terms) if finding.matched_terms else "_none_"
        lines.append(f"- **{finding.level.upper()}** `{finding.category}` — {finding.message} Matched: {matched}")
    lines.extend(["", "## Recommended Actions", ""])
    if report.recommended_actions:
        for action in report.recommended_actions:
            lines.append(f"- **{action.priority.upper()}** `{action.category}` — {action.action}")
    else:
        lines.append("No recommended actions.")
    lines.extend(["", "## Governance Note", "", report.governance_note, ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose Grace-Mar context/retrieval/routing failures.")
    parser.add_argument("--input", required=True, type=Path, help="Path to context output or artifact to diagnose.")
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

    report = evaluate_context(args.input)
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

    risk_findings = [finding for finding in report.findings if finding.level == "risk"]
    if risk_findings:
        print(f"Completed with {len(risk_findings)} risk finding(s). Overall risk: {report.overall_risk}")
    else:
        print(f"Completed with no risk findings. Overall risk: {report.overall_risk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
