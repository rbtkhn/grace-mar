#!/usr/bin/env python3
"""
Read-only audit for agent-like surfaces.

Phase 1 checks a small JSON registry of known surfaces and reports authority,
receipt, and capability-contract gaps without creating or mutating any surface.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "config" / "agent-surfaces.v1.json"

ALLOWED_STATUS = {
    "implemented",
    "partial",
    "documented_only",
    "needs_verification",
    "blocked",
}
ALLOWED_CATEGORY = {
    "external_runtime",
    "external_handback_agent",
    "portable_emulation_runtime",
    "workbench_runner",
    "interface_artifact_generator",
    "read_only_audit",
    "sandbox_adapter",
    "delegation_protocol",
    "auto_research",
}
ALLOWED_CANONICAL_RECORD_ACCESS = {"none", "read-only"}
ALLOWED_GATE_EFFECT = {"none", "stage-only", "advisory-only"}
REQUIRED_FIELDS = [
    "id",
    "name",
    "status",
    "category",
    "reads",
    "writes",
    "canonical_record_access",
    "merge_authority",
    "gate_effect",
    "receipt_required",
    "capability_contract",
    "owner_lane",
    "notes",
]
INTEGRATION_CATEGORIES = {
    "external_runtime",
    "external_handback_agent",
    "portable_emulation_runtime",
    "sandbox_adapter",
    "auto_research",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _issue(
    kind: str,
    message: str,
    *,
    surface_id: str | None = None,
    field: str | None = None,
    other_surface_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"kind": kind, "message": message}
    if surface_id is not None:
        payload["surfaceId"] = surface_id
    if field is not None:
        payload["field"] = field
    if other_surface_id is not None:
        payload["otherSurfaceId"] = other_surface_id
    return payload


def _is_blank(value: Any) -> bool:
    return isinstance(value, str) and value.strip() == ""


def _surface_id(surface: dict[str, Any], index: int) -> str:
    raw = surface.get("id")
    if isinstance(raw, str) and raw.strip():
        return raw
    return f"<surface-{index}>"


def _validate_surface_shape(surface: dict[str, Any], index: int) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    sid = _surface_id(surface, index)

    for field in REQUIRED_FIELDS:
        if field not in surface:
            errors.append(
                _issue("missing_required_field", f"missing required field: {field}", surface_id=sid, field=field)
            )

    for field in [
        "id",
        "name",
        "status",
        "category",
        "canonical_record_access",
        "merge_authority",
        "gate_effect",
        "owner_lane",
        "notes",
    ]:
        if field in surface and _is_blank(surface[field]):
            errors.append(
                _issue("missing_required_field", f"field must not be blank: {field}", surface_id=sid, field=field)
            )

    for field in ["reads", "writes"]:
        if field in surface and not isinstance(surface[field], list):
            errors.append(
                _issue("invalid_field_type", f"{field} must be a list", surface_id=sid, field=field)
            )

    if "receipt_required" in surface and not isinstance(surface["receipt_required"], bool):
        errors.append(
            _issue(
                "invalid_field_type",
                "receipt_required must be a boolean",
                surface_id=sid,
                field="receipt_required",
            )
        )

    if "status" in surface and surface["status"] not in ALLOWED_STATUS:
        errors.append(
            _issue(
                "invalid_status",
                f"invalid status: {surface['status']!r}",
                surface_id=sid,
                field="status",
            )
        )

    if "category" in surface and surface["category"] not in ALLOWED_CATEGORY:
        errors.append(
            _issue(
                "invalid_category",
                f"invalid category: {surface['category']!r}",
                surface_id=sid,
                field="category",
            )
        )

    if (
        "canonical_record_access" in surface
        and surface["canonical_record_access"] not in ALLOWED_CANONICAL_RECORD_ACCESS
    ):
        errors.append(
            _issue(
                "invalid_canonical_record_access",
                f"canonical_record_access must be one of {sorted(ALLOWED_CANONICAL_RECORD_ACCESS)!r}",
                surface_id=sid,
                field="canonical_record_access",
            )
        )

    if "gate_effect" in surface and surface["gate_effect"] not in ALLOWED_GATE_EFFECT:
        errors.append(
            _issue(
                "invalid_gate_effect",
                f"gate_effect must be one of {sorted(ALLOWED_GATE_EFFECT)!r}",
                surface_id=sid,
                field="gate_effect",
            )
        )

    if "merge_authority" in surface and surface["merge_authority"] != "none":
        errors.append(
            _issue(
                "merge_authority_must_be_none",
                "merge_authority must remain 'none' for Phase 1 surfaces",
                surface_id=sid,
                field="merge_authority",
            )
        )

    return errors


def audit_registry(registry_path: Path, repo_root: Path) -> dict[str, Any]:
    data = _load_json(registry_path)
    surfaces_raw = data.get("surfaces")
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not isinstance(surfaces_raw, list):
        errors.append(
            _issue(
                "invalid_registry",
                "registry must contain a top-level 'surfaces' list",
                field="surfaces",
            )
        )
        return {
            "ok": False,
            "registry": registry_path.relative_to(repo_root).as_posix(),
            "errors": errors,
            "warnings": warnings,
            "counts": {
                "surfaces": 0,
                "errors": len(errors),
                "warnings": len(warnings),
            },
            "surfaces": [],
        }

    surfaces: list[dict[str, Any]] = []
    seen_ids: dict[str, int] = {}

    for index, surface in enumerate(surfaces_raw, start=1):
        if not isinstance(surface, dict):
            errors.append(
                _issue(
                    "invalid_surface_entry",
                    "each surface entry must be an object",
                    surface_id=f"<surface-{index}>",
                )
            )
            continue

        surfaces.append(surface)
        sid = _surface_id(surface, index)
        errors.extend(_validate_surface_shape(surface, index))

        if sid in seen_ids:
            errors.append(
                _issue(
                    "duplicate_id",
                    f"duplicate surface id: {sid}",
                    surface_id=sid,
                )
            )
        else:
            seen_ids[sid] = index

        status = surface.get("status")
        category = surface.get("category")

        if status in {"implemented", "partial"} and category != "read_only_audit":
            receipt_exempt = surface.get("receipt_required_exempt") is True
            if not receipt_exempt and surface.get("receipt_required") is not True:
                errors.append(
                    _issue(
                        "missing_receipt_requirement",
                        "implemented/partial non-audit surfaces must declare receipt_required: true or explicit exemption",
                        surface_id=sid,
                        field="receipt_required",
                    )
                )

        if status in {"implemented", "partial"} and category in INTEGRATION_CATEGORIES:
            exempt = surface.get("capability_contract_exempt") is True
            contract = surface.get("capability_contract")
            if not exempt and (not isinstance(contract, str) or contract.strip() == ""):
                errors.append(
                    _issue(
                        "missing_capability_contract",
                        "implemented/partial integration surfaces must declare a capability_contract or explicit exemption",
                        surface_id=sid,
                        field="capability_contract",
                    )
                )
            elif isinstance(contract, str) and contract.strip():
                contract_path = repo_root / contract
                if not contract_path.exists():
                    errors.append(
                        _issue(
                            "missing_capability_contract_file",
                            f"capability_contract path does not exist: {contract}",
                            surface_id=sid,
                            field="capability_contract",
                        )
                    )

    by_category: dict[str, list[dict[str, Any]]] = {}
    for index, surface in enumerate(surfaces, start=1):
        category = surface.get("category")
        if category not in ALLOWED_CATEGORY:
            continue
        by_category.setdefault(category, []).append(surface)

    for category, items in sorted(by_category.items()):
        for idx, left in enumerate(items):
            left_id = _surface_id(left, idx + 1)
            left_writes = {
                item.strip()
                for item in left.get("writes", [])
                if isinstance(item, str) and item.strip()
            }
            if not left_writes:
                continue
            for right_index, right in enumerate(items[idx + 1 :], start=idx + 2):
                right_id = _surface_id(right, right_index)
                right_writes = {
                    item.strip()
                    for item in right.get("writes", [])
                    if isinstance(item, str) and item.strip()
                }
                overlap = sorted(left_writes & right_writes)
                if not overlap:
                    continue
                warnings.append(
                    _issue(
                        "overlapping_writes_same_category",
                        f"surfaces share category {category!r} and overlapping writes: {', '.join(overlap)}",
                        surface_id=left_id,
                        other_surface_id=right_id,
                    )
                )

    surface_rows = sorted(surfaces, key=lambda item: str(item.get("id", "")))
    return {
        "ok": len(errors) == 0,
        "registry": registry_path.relative_to(repo_root).as_posix(),
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "surfaces": len(surface_rows),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "surfaces": surface_rows,
    }


def _render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Agent Sprawl Control Plane audit: {report['counts']['surfaces']} surfaces, "
        f"{report['counts']['errors']} errors, {report['counts']['warnings']} warnings",
        f"Registry: {report['registry']}",
    ]

    if report["errors"]:
        lines.append("")
        lines.append("Errors:")
        for item in report["errors"]:
            detail = item.get("surfaceId", "<registry>")
            field = f" [{item['field']}]" if "field" in item else ""
            lines.append(f"- {detail}{field}: {item['message']}")

    if report["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        for item in report["warnings"]:
            detail = item.get("surfaceId", "<registry>")
            if "otherSurfaceId" in item:
                detail = f"{detail} / {item['otherSurfaceId']}"
            lines.append(f"- {detail}: {item['message']}")

    if not report["errors"] and not report["warnings"]:
        lines.append("")
        lines.append("No control-plane gaps detected.")

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the Phase 1 agent-surface registry.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to agent-surfaces registry JSON")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Repository root for relative paths")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args(argv)

    report = audit_registry(args.config.resolve(), args.repo_root.resolve())

    if args.json:
        sys.stdout.write(json.dumps(report, indent=2) + "\n")
    else:
        sys.stdout.write(_render_text(report))

    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
