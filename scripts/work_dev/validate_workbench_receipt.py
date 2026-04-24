#!/usr/bin/env python3
"""
Validate a Workbench Harness receipt JSON (WORKBENCH-RECEIPT-SPEC v0.1).

Usage:
  python3 scripts/work_dev/validate_workbench_receipt.py path/to/receipt.json

Exits 0 on success, 1 on validation failure. Read-only; no gate or Record I/O.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Workflow statuses (see WORKBENCH-RECEIPT-SPEC). Validator enforces this set.
ALLOWED_STATUS = frozenset(
    {
        "draft",
        "runs",
        "inspected",
        "needs_revision",
        "ready_for_review",
        "rejected",
    }
)

REQUIRED_INSPECTION_KEYS = (
    "method",
    "screenshots",
    "observedFailures",
    "acceptanceChecklist",
)


def validate_receipt(data: Any) -> list[str]:
    """Return a list of human-readable errors; empty if valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]

    def req(key: str) -> None:
        if key not in data:
            errors.append(f"missing top-level key: {key!r}")

    for k in (
        "receiptKind",
        "receiptId",
        "createdAt",
        "workbenchRunId",
        "lane",
        "artifactType",
        "artifactCandidateLabel",
        "relatedGateCandidateId",
        "sourcePromptRef",
        "pathsTouched",
        "commandsRun",
        "launchCommand",
        "inspection",
        "revisionSummary",
        "status",
        "recordAuthority",
        "gateEffect",
    ):
        req(k)

    if data.get("receiptKind") != "workbench":
        errors.append(
            f"receiptKind must be 'workbench', got {data.get('receiptKind')!r}"
        )
    if data.get("recordAuthority") != "none":
        errors.append(
            f"recordAuthority must be 'none', got {data.get('recordAuthority')!r}"
        )
    if data.get("gateEffect") != "none":
        errors.append(f"gateEffect must be 'none', got {data.get('gateEffect')!r}")

    st = data.get("status")
    if st not in ALLOWED_STATUS:
        errors.append(
            f"status must be one of {sorted(ALLOWED_STATUS)!r}, got {st!r}"
        )

    cr = data.get("commandsRun")
    if cr is None:
        errors.append("commandsRun is missing (must be a list, possibly empty)")
    elif not isinstance(cr, list):
        errors.append("commandsRun must be a list")
    elif not all(isinstance(x, str) for x in cr):
        errors.append("commandsRun must be a list of strings")

    pt = data.get("pathsTouched")
    if pt is None or not isinstance(pt, list) or not all(
        isinstance(x, str) for x in pt
    ):
        errors.append("pathsTouched must be a list of strings")

    if not isinstance(data.get("launchCommand"), str):
        errors.append("launchCommand must be a string")

    insp = data.get("inspection")
    if insp is None:
        errors.append("inspection is missing")
    elif not isinstance(insp, dict):
        errors.append("inspection must be an object")
    else:
        if "method" not in insp or not isinstance(insp.get("method"), str):
            errors.append("inspection.method must be a non-empty string key present")
        elif not str(insp.get("method", "")).strip():
            errors.append("inspection.method must not be empty")
        for ik in REQUIRED_INSPECTION_KEYS:
            if ik not in insp:
                errors.append(f"inspection missing key: {ik!r}")
        if "screenshots" in insp and (
            not isinstance(insp["screenshots"], list)
            or not all(isinstance(x, str) for x in insp["screenshots"])
        ):
            errors.append("inspection.screenshots must be a list of strings")
        if "observedFailures" in insp and (
            not isinstance(insp["observedFailures"], list)
            or not all(isinstance(x, str) for x in insp["observedFailures"])
        ):
            errors.append("inspection.observedFailures must be a list of strings")
        if "acceptanceChecklist" in insp and (
            not isinstance(insp["acceptanceChecklist"], list)
            or not all(isinstance(x, str) for x in insp["acceptanceChecklist"])
        ):
            errors.append("inspection.acceptanceChecklist must be a list of strings")

    rgid = data.get("relatedGateCandidateId")
    if rgid is not None and not isinstance(rgid, str):
        errors.append("relatedGateCandidateId must be string or null")

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt", type=Path, help="Path to receipt JSON")
    args = p.parse_args()
    path = args.receipt
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 1
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 1
    err = validate_receipt(data)
    if err:
        for line in err:
            print(f"invalid: {line}", file=sys.stderr)
        return 1
    print("ok: workbench receipt is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
