#!/usr/bin/env python3
"""
Validate Companion-Self change-review artifacts.

Usage:
  python3 scripts/validate-change-review.py users/demo/review-queue
  python3 scripts/validate-change-review.py users/_template/review-queue --allow-empty
  python3 scripts/validate-change-review.py users/<id>/review-queue --allow-missing-decisions
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema-registry"

QUEUE_SCHEMA = SCHEMA_DIR / "change-review-queue.v1.json"
EVENT_LOG_SCHEMA = SCHEMA_DIR / "change-event-log.v1.json"
PROPOSAL_SCHEMA = SCHEMA_DIR / "change-proposal.v1.json"
DECISION_SCHEMA = SCHEMA_DIR / "change-decision.v1.json"
DIFF_SCHEMA = SCHEMA_DIR / "identity-diff.v1.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_schema(path: Path) -> Dict[str, Any]:
    return load_json(path)


def validate_json(instance: Dict[str, Any], schema: Dict[str, Any], path: Path) -> List[str]:
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    messages = []
    for error in errors:
        location = ".".join(str(x) for x in error.path) if error.path else "<root>"
        messages.append(f"{path}: schema error at {location}: {error.message}")
    return messages


def resolve_ref(base_dir: Path, ref: str) -> Path:
    ref_path = Path(ref)
    if ref_path.is_absolute():
        return ref_path
    if ref.startswith("users/") or ref.startswith("schema-registry/") or ref.startswith("docs/") or ref.startswith("scripts/"):
        return ROOT / ref_path
    return (base_dir / ref_path).resolve()


def collect_json_files(directory: Path) -> List[Path]:
    return sorted([p for p in directory.glob("*.json") if p.is_file()])


def validate_queue_structure(
    review_dir: Path,
    allow_empty: bool,
    allow_missing_decisions: bool = False,
) -> List[str]:
    errors: List[str] = []

    required = [
        review_dir / "change_review_queue.json",
        review_dir / "change_event_log.json",
        review_dir / "proposals",
        review_dir / "decisions",
        review_dir / "diffs",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required path: {path}")

    if errors:
        return errors

    queue = load_json(review_dir / "change_review_queue.json")
    event_log = load_json(review_dir / "change_event_log.json")

    errors.extend(validate_json(queue, load_schema(QUEUE_SCHEMA), review_dir / "change_review_queue.json"))
    errors.extend(validate_json(event_log, load_schema(EVENT_LOG_SCHEMA), review_dir / "change_event_log.json"))

    proposal_files = collect_json_files(review_dir / "proposals")
    decision_files = collect_json_files(review_dir / "decisions")
    diff_files = collect_json_files(review_dir / "diffs")

    if not allow_empty:
        if not proposal_files:
            errors.append(f"{review_dir / 'proposals'}: expected at least one proposal JSON file")
        if not decision_files and not allow_missing_decisions:
            errors.append(f"{review_dir / 'decisions'}: expected at least one decision JSON file")
        if not diff_files:
            errors.append(f"{review_dir / 'diffs'}: expected at least one diff JSON file")

    proposals: Dict[str, Dict[str, Any]] = {}
    decisions: Dict[str, Dict[str, Any]] = {}
    diffs: Dict[str, Dict[str, Any]] = {}

    for path in proposal_files:
        data = load_json(path)
        errors.extend(validate_json(data, load_schema(PROPOSAL_SCHEMA), path))
        proposal_id = data.get("proposalId")
        if proposal_id:
            if proposal_id in proposals:
                errors.append(f"Duplicate proposalId found: {proposal_id}")
            proposals[proposal_id] = data

    for path in decision_files:
        data = load_json(path)
        errors.extend(validate_json(data, load_schema(DECISION_SCHEMA), path))
        decision_id = data.get("decisionId")
        if decision_id:
            if decision_id in decisions:
                errors.append(f"Duplicate decisionId found: {decision_id}")
            decisions[decision_id] = data

    for path in diff_files:
        data = load_json(path)
        errors.extend(validate_json(data, load_schema(DIFF_SCHEMA), path))
        diff_id = data.get("diffId")
        if diff_id:
            if diff_id in diffs:
                errors.append(f"Duplicate diffId found: {diff_id}")
            diffs[diff_id] = data

    errors.extend(validate_queue_refs(review_dir, queue, proposals))
    errors.extend(validate_event_log_refs(review_dir, event_log))
    errors.extend(validate_decision_links(decisions, proposals))
    errors.extend(validate_proposal_refs(review_dir, proposals))

    return errors


def validate_queue_refs(review_dir: Path, queue: Dict[str, Any], proposals: Dict[str, Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    queue_ids = [item["proposalId"] for item in queue.get("items", [])]
    known_ids = set(proposals.keys())

    for proposal_id in queue_ids:
        if proposal_id not in known_ids:
            errors.append(
                f"{review_dir / 'change_review_queue.json'}: queue references missing proposalId {proposal_id}"
            )
    return errors


def validate_event_log_refs(review_dir: Path, event_log: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for event in event_log.get("events", []):
        ref = event.get("ref")
        if not ref:
            continue
        path = resolve_ref(review_dir, ref)
        if not path.exists():
            errors.append(
                f"{review_dir / 'change_event_log.json'}: event ref does not exist: {ref}"
            )
    return errors


def validate_decision_links(
    decisions: Dict[str, Dict[str, Any]],
    proposals: Dict[str, Dict[str, Any]],
) -> List[str]:
    errors: List[str] = []
    known_proposals = set(proposals.keys())
    for decision_id, decision in decisions.items():
        proposal_id = decision.get("proposalId")
        if proposal_id not in known_proposals:
            errors.append(
                f"Decision {decision_id} references unknown proposalId {proposal_id}"
            )
    return errors


def strip_fragment(ref: str) -> str:
    return ref.split("#", 1)[0]


def validate_proposal_refs(review_dir: Path, proposals: Dict[str, Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    for proposal_id, proposal in proposals.items():
        for field in ("priorStateRef", "proposedStateRef"):
            ref = proposal.get(field)
            if not ref:
                continue
            ref_path = resolve_ref(review_dir, strip_fragment(ref))
            if not ref_path.exists():
                errors.append(f"Proposal {proposal_id} has missing {field}: {ref}")

        for evidence in proposal.get("supportingEvidence", []):
            ref = evidence.get("ref")
            if not ref:
                continue
            if ref.startswith("demo-session-") or ref.startswith("session-"):
                continue
            ref_path = resolve_ref(review_dir, strip_fragment(ref))
            if not ref_path.exists():
                errors.append(
                    f"Proposal {proposal_id} has supportingEvidence ref that does not exist: {ref}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate change-review artifacts.")
    parser.add_argument("review_dir", help="Path to review-queue directory")
    parser.add_argument("--allow-empty", action="store_true", help="Allow empty template scaffold")
    parser.add_argument(
        "--allow-missing-decisions",
        action="store_true",
        help="Allow no decision files (gate export / pre-review); still require proposals and diffs unless --allow-empty",
    )
    args = parser.parse_args()

    review_dir = (ROOT / args.review_dir).resolve() if not Path(args.review_dir).is_absolute() else Path(args.review_dir)
    if not review_dir.exists():
        print(f"ERROR: review directory does not exist: {review_dir}", file=sys.stderr)
        return 2

    errors = validate_queue_structure(
        review_dir,
        allow_empty=args.allow_empty,
        allow_missing_decisions=args.allow_missing_decisions,
    )

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALIDATION PASSED: {review_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
