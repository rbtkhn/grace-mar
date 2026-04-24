#!/usr/bin/env python3
"""
Validate interface artifact metadata JSON (Interface Artifact Spec v1).

Usage:
  python3 scripts/work_dev/validate_interface_artifact.py path/to/artifact.json

Exits 0 on success, 1 on validation failure. Read-only; no gate or Record I/O.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

ALLOWED_ARTIFACT_KIND = frozenset(
    {
        "markdown-dashboard",
        "html-visualizer",
        "react-prototype",
        "svg-map",
        "cli-view",
        "review-cockpit",
        "comparison-view",
        "other-work-ui",
    }
)

ALLOWED_STATUS = frozenset(
    {
        "draft",
        "inspected",
        "revised",
        "discarded",
        "promoted-to-scripted-dashboard",
        "superseded",
    }
)

ALLOWED_CANONICAL_RECORD_ACCESS = frozenset({"none", "read-only"})


def _is_list_of_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _mutation_scope_allows_record_write(value: str) -> bool:
    lowered = value.strip().lower()
    if not lowered:
        return True
    write_words = ("write", "update", "merge", "approve", "stage")
    if "canonical" in lowered and any(word in lowered for word in write_words):
        return True
    if "record" in lowered and any(word in lowered for word in write_words):
        return True
    return False


def validate_interface_artifact(data: Any) -> list[str]:
    """Return human-readable validation errors; empty if valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]

    required = (
        "artifactId",
        "title",
        "artifactKind",
        "status",
        "sourceInputs",
        "generatedPaths",
        "intendedUse",
        "mutationScope",
        "canonicalRecordAccess",
        "recordAuthority",
        "gateEffect",
        "inspectionStatus",
        "relatedWorkbenchReceipt",
        "typicalNextStep",
    )
    for key in required:
        if key not in data:
            errors.append(f"missing top-level key: {key!r}")

    for key in (
        "artifactId",
        "title",
        "artifactKind",
        "status",
        "intendedUse",
        "mutationScope",
        "canonicalRecordAccess",
        "recordAuthority",
        "gateEffect",
        "inspectionStatus",
        "typicalNextStep",
    ):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append(f"{key} must be a non-empty string")

    artifact_kind = data.get("artifactKind")
    if artifact_kind not in ALLOWED_ARTIFACT_KIND:
        errors.append(
            "artifactKind must be one of "
            f"{sorted(ALLOWED_ARTIFACT_KIND)!r}, got {artifact_kind!r}"
        )

    status = data.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)!r}, got {status!r}")

    canonical_access = data.get("canonicalRecordAccess")
    if canonical_access not in ALLOWED_CANONICAL_RECORD_ACCESS:
        errors.append(
            "canonicalRecordAccess must be one of "
            f"{sorted(ALLOWED_CANONICAL_RECORD_ACCESS)!r}, got {canonical_access!r}"
        )

    if data.get("recordAuthority") != "none":
        errors.append(
            f"recordAuthority must be 'none', got {data.get('recordAuthority')!r}"
        )

    if data.get("gateEffect") != "none":
        errors.append(f"gateEffect must be 'none', got {data.get('gateEffect')!r}")

    mutation_scope = data.get("mutationScope")
    if isinstance(mutation_scope, str) and _mutation_scope_allows_record_write(
        mutation_scope
    ):
        errors.append(
            "mutationScope must not imply canonical or Record writing, "
            f"got {mutation_scope!r}"
        )

    source_inputs = data.get("sourceInputs")
    if not _is_list_of_strings(source_inputs):
        errors.append("sourceInputs must be a list of strings")

    generated_paths = data.get("generatedPaths")
    if not _is_list_of_strings(generated_paths):
        errors.append("generatedPaths must be a list of strings")
    elif not generated_paths:
        errors.append("generatedPaths must be non-empty")

    related_receipt = data.get("relatedWorkbenchReceipt")
    if related_receipt is not None and not isinstance(related_receipt, str):
        errors.append("relatedWorkbenchReceipt must be string or null")

    if "sourceContractRef" in data and data["sourceContractRef"] is not None:
        if not isinstance(data["sourceContractRef"], str) or not data[
            "sourceContractRef"
        ].strip():
            errors.append("sourceContractRef must be a non-empty string when present")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="Path to interface artifact JSON")
    args = parser.parse_args()

    path = args.artifact
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate_interface_artifact(data)
    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    print("ok: interface artifact metadata is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
