#!/usr/bin/env python3
"""
Validate template-instance sync contract vs applied provenance.

This check is intentionally narrower than a full template diff. It verifies that:
  - instance-contract.json defines the current target contract
  - template-source.json defines the last applied template provenance
  - template-source.json points back at the current target contract
  - the local cached template-manifest.json is structurally aligned with the target version

It does NOT require target and applied pins to match. That difference may be intentional
while an instance is catching up. Mismatch is a warning by default and can be promoted to
an error with --require-target-applied-match.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json: {path}: {exc}") from exc


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _matches_path_reference(value: str, path: Path) -> bool:
    candidates = {_rel(path), path.name}
    return value in candidates


def _require_string(obj: dict, key: str, label: str, errors: list[str]) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} missing non-empty string field: {key}")
        return ""
    return value.strip()


def _require_list_of_strings(obj: dict, key: str, label: str, errors: list[str]) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label} missing list[str] field: {key}")
        return []
    return [item.strip() for item in value]


def validate_sync_contract(
    instance_contract_path: Path,
    template_source_path: Path,
    template_manifest_path: Path,
    require_target_applied_match: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        contract = _read_json(instance_contract_path)
    except ValueError as exc:
        return [str(exc)], warnings
    try:
        template_source = _read_json(template_source_path)
    except ValueError as exc:
        return [str(exc)], warnings
    try:
        template_manifest = _read_json(template_manifest_path)
    except ValueError as exc:
        return [str(exc)], warnings

    contract_label = _rel(instance_contract_path)
    source_label = _rel(template_source_path)
    manifest_label = _rel(template_manifest_path)

    contract_schema = _require_string(contract, "schemaVersion", contract_label, errors)
    if contract_schema and contract_schema not in {"1.0.0", "1.1.0"}:
        warnings.append(f"{contract_label} schemaVersion {contract_schema} is unknown to this validator")

    template_repo = _require_string(contract, "templateRepo", contract_label, errors)
    target_version = _require_string(contract, "templateVersionTarget", contract_label, errors)
    target_commit = _require_string(contract, "templateCommitTarget", contract_label, errors)

    sync_arch = contract.get("syncArchitecture")
    if not isinstance(sync_arch, dict):
        errors.append(f"{contract_label} missing object field: syncArchitecture")
        sync_arch = {}
    applied_provenance_path = _require_string(sync_arch, "appliedProvenancePath", f"{contract_label}.syncArchitecture", errors)
    if applied_provenance_path and not _matches_path_reference(applied_provenance_path, template_source_path):
        errors.append(
            f"{contract_label}.syncArchitecture.appliedProvenancePath points to {applied_provenance_path}, "
            f"expected {_rel(template_source_path)} or {template_source_path.name}"
        )

    source_schema = _require_string(template_source, "schemaVersion", source_label, errors)
    if source_schema and source_schema != "1.1.0":
        warnings.append(f"{source_label} schemaVersion is {source_schema}; expected 1.1.0 for applied provenance")
    record_type = _require_string(template_source, "recordType", source_label, errors)
    if record_type and record_type != "templateAppliedProvenance":
        errors.append(f"{source_label} recordType must be templateAppliedProvenance")

    applied_commit = _require_string(template_source, "companionSelfCommit", source_label, errors)
    applied_version = _require_string(template_source, "templateVersion", source_label, errors)
    _require_string(template_source, "syncedAt", source_label, errors)
    _require_string(template_source, "syncedBy", source_label, errors)
    _require_list_of_strings(template_source, "syncedPaths", source_label, errors)

    upstream = template_source.get("templateUpstream")
    if not isinstance(upstream, dict):
        errors.append(f"{source_label} missing object field: templateUpstream")
        upstream = {}
    upstream_repo = _require_string(upstream, "repo", f"{source_label}.templateUpstream", errors)
    if template_repo and upstream_repo and template_repo != upstream_repo:
        errors.append(f"{source_label}.templateUpstream.repo does not match {contract_label}.templateRepo")

    target_ref = template_source.get("targetReference")
    if not isinstance(target_ref, dict):
        errors.append(f"{source_label} missing object field: targetReference")
        target_ref = {}
    target_ref_contract = _require_string(target_ref, "instanceContract", f"{source_label}.targetReference", errors)
    if target_ref_contract and not _matches_path_reference(target_ref_contract, instance_contract_path):
        errors.append(
            f"{source_label}.targetReference.instanceContract points to {target_ref_contract}, "
            f"expected {_rel(instance_contract_path)} or {instance_contract_path.name}"
        )
    target_ref_version = _require_string(target_ref, "templateVersionTarget", f"{source_label}.targetReference", errors)
    target_ref_commit = _require_string(target_ref, "templateCommitTarget", f"{source_label}.targetReference", errors)
    if target_version and target_ref_version and target_version != target_ref_version:
        errors.append(f"{source_label}.targetReference.templateVersionTarget does not match {contract_label}.templateVersionTarget")
    if target_commit and target_ref_commit and target_commit != target_ref_commit:
        errors.append(f"{source_label}.targetReference.templateCommitTarget does not match {contract_label}.templateCommitTarget")

    manifest_version = _require_string(template_manifest, "templateVersion", manifest_label, errors)
    _require_string(template_manifest, "canonicalAsOf", manifest_label, errors)
    paths = template_manifest.get("paths")
    if not isinstance(paths, list) or not paths:
        errors.append(f"{manifest_label} missing non-empty list field: paths")
    if target_version and manifest_version and manifest_version != target_version:
        errors.append(f"{manifest_label}.templateVersion does not match {contract_label}.templateVersionTarget")

    if target_version and applied_version and target_version != applied_version:
        message = (
            f"target/applied templateVersion differ: target={target_version} applied={applied_version} "
            f"({contract_label} vs {source_label})"
        )
        if require_target_applied_match:
            errors.append(message)
        else:
            warnings.append(message)
    if target_commit and applied_commit and target_commit != applied_commit:
        message = (
            f"target/applied companion-self commit differ: target={target_commit} applied={applied_commit} "
            f"({contract_label} vs {source_label})"
        )
        if require_target_applied_match:
            errors.append(message)
        else:
            warnings.append(message)

    aux_events = template_source.get("auxiliarySyncEvents")
    if aux_events is not None:
        if not isinstance(aux_events, list):
            errors.append(f"{source_label}.auxiliarySyncEvents must be a list when present")
        else:
            for idx, event in enumerate(aux_events):
                label = f"{source_label}.auxiliarySyncEvents[{idx}]"
                if not isinstance(event, dict):
                    errors.append(f"{label} must be an object")
                    continue
                _require_string(event, "kind", label, errors)
                _require_string(event, "companionSelfCommit", label, errors)
                _require_string(event, "templateVersion", label, errors)
                _require_string(event, "syncedAt", label, errors)
                _require_string(event, "syncedBy", label, errors)
                _require_list_of_strings(event, "syncedPaths", label, errors)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate template sync contract vs applied provenance.")
    parser.add_argument("--instance-contract", type=Path, default=REPO_ROOT / "instance-contract.json")
    parser.add_argument("--template-source", type=Path, default=REPO_ROOT / "template-source.json")
    parser.add_argument("--template-manifest", type=Path, default=REPO_ROOT / "template-manifest.json")
    parser.add_argument("--require-target-applied-match", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    errors, warnings = validate_sync_contract(
        instance_contract_path=args.instance_contract,
        template_source_path=args.template_source,
        template_manifest_path=args.template_manifest,
        require_target_applied_match=args.require_target_applied_match,
    )
    ok = not errors

    if args.json:
        print(
            json.dumps(
                {
                    "ok": ok,
                    "errors": errors,
                    "warnings": warnings,
                    "instance_contract": _rel(args.instance_contract),
                    "template_source": _rel(args.template_source),
                    "template_manifest": _rel(args.template_manifest),
                    "require_target_applied_match": args.require_target_applied_match,
                },
                indent=2,
            )
        )
        return 0 if ok else 1

    print("=== Template sync contract ===")
    if ok:
        print("  OK: target contract, applied provenance, and local manifest mirror are structurally aligned.")
    else:
        for error in errors:
            print(f"  FAIL: {error}")
    if warnings:
        print()
        print("=== Template sync drift warnings ===")
        for warning in warnings:
            print(f"  WARN: {warning}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
