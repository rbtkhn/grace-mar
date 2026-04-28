"""
MCP execution receipt validation — shared by mcp_receipt.py and mcp_receipt_audit.py.

Authority is derived from config/mcp-authority-bindings.yaml (same SSOT as PR2).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CAPABILITIES_PATH = REPO_ROOT / "config" / "mcp-capabilities.yaml"
BINDINGS_PATH = REPO_ROOT / "config" / "mcp-authority-bindings.yaml"
RECEIPT_SCHEMA_PATH = REPO_ROOT / "schemas" / "mcp-execution-receipt.v1.json"

_NETWORK_RANK: dict[str, int] = {"none": 0, "read": 1, "full": 2}
_CRED_RANK: dict[str, int] = {"none": 0, "optional": 1, "required": 2}


def load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required (pip install -r requirements-dev.txt)") from e
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_json_schema(instance: Any, schema_path: Path = RECEIPT_SCHEMA_PATH) -> None:
    try:
        import jsonschema
    except ImportError as e:
        raise RuntimeError("jsonschema required (pip install -r requirements-dev.txt)") from e
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)


def capability_by_id(caps_doc: dict[str, Any], cid: str) -> dict[str, Any] | None:
    for cap in caps_doc.get("capabilities") or []:
        if cap.get("id") == cid:
            return cap
    return None


def bindings_lane_map(bind_doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """output_lane -> binding row; raises ValueError on duplicate lanes."""
    out: dict[str, dict[str, Any]] = {}
    for row in bind_doc.get("bindings") or []:
        lane = row["output_lane"]
        if lane in out:
            raise ValueError(f"duplicate binding for output_lane '{lane}'")
        out[lane] = row
    return out


def authority_from_binding(binding: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_surface": binding["authority_surface"],
        "authority_class": binding["authority_class"],
        "gate_required_for_record_change": binding["gate_required_for_record_change"],
    }


def _lte_rank(value: str, cap_max: str, ranks: dict[str, int]) -> bool:
    return ranks.get(value, -1) <= ranks.get(cap_max, -1)


def warnings_for_receipt(
    receipt: dict[str, Any],
    cap: dict[str, Any],
) -> list[str]:
    """Non-fatal advisory lines for audit report."""
    warns: list[str] = []
    if receipt.get("governance", {}).get("durable_state_write_attempted") and not cap.get(
        "durable_state_write"
    ):
        warns.append(
            "durable_state_write_attempted is true but capability registry has durable_state_write false "
            "(possible policy breach — intentional audit trail)"
        )
    return warns


def validate_mcp_receipt_business(
    receipt: dict[str, Any],
    caps_doc: dict[str, Any],
    bind_doc: dict[str, Any],
) -> list[str]:
    """Return sorted violation strings; empty means business rules pass."""
    violations: list[str] = []

    cid = receipt.get("capability", {}).get("id")
    cap = capability_by_id(caps_doc, cid) if cid else None
    if cap is None:
        return sorted([f"unknown capability id '{cid}'"])

    rcap = receipt["capability"]
    if rcap.get("output_lane") != cap["output_lane"]:
        violations.append(
            f"capability.output_lane '{rcap.get('output_lane')}' != registry '{cap['output_lane']}'"
        )
    if rcap.get("category") != cap["category"]:
        violations.append(
            f"capability.category '{rcap.get('category')}' != registry '{cap['category']}'"
        )

    lane = cap["output_lane"]
    try:
        lane_map = bindings_lane_map(bind_doc)
    except ValueError as e:
        violations.append(str(e))
        return sorted(violations)

    bind = lane_map.get(lane)
    if bind is None:
        violations.append(f"no binding row for output_lane '{lane}'")
        return sorted(violations)

    auth = receipt["authority"]
    expected = authority_from_binding(bind)
    for k, v in expected.items():
        if auth.get(k) != v:
            violations.append(
                f"authority.{k} '{auth.get(k)}' != binding for lane '{lane}' (expected {v})"
            )

    acc = receipt["access"]
    if not cap.get("writes"):
        if acc.get("resources_written"):
            violations.append(
                "access.resources_written must be empty when registry writes: []"
            )

    gov = receipt["governance"]
    if gov.get("canonical_record_touched") and not gov.get("requires_gate_review"):
        violations.append(
            "governance.canonical_record_touched requires requires_gate_review true"
        )

    if gov.get("durable_state_write_attempted"):
        acls = auth.get("authority_class")
        if acls not in ("review_required", "human_only"):
            violations.append(
                "durable_state_write_attempted requires authority_class review_required or human_only"
            )
        if not auth.get("gate_required_for_record_change"):
            violations.append(
                "durable_state_write_attempted requires gate_required_for_record_change true"
            )

    res = receipt["result"]
    if res.get("status") == "success" and gov.get("prohibited_action_attempted"):
        violations.append("result.status success is invalid when prohibited_action_attempted is true")

    if res.get("status") == "success" and lane == "prohibited":
        violations.append("result.status success is invalid for output_lane prohibited")

    cred_rec = acc.get("credential_use")
    cred_cap = cap.get("credential_requirements")
    if cred_cap is not None and cred_rec is not None:
        if not _lte_rank(cred_rec, cred_cap, _CRED_RANK):
            violations.append(
                f"access.credential_use '{cred_rec}' exceeds capability credential_requirements '{cred_cap}'"
            )

    net_rec = acc.get("network_access")
    net_cap = cap.get("network_access")
    if net_rec is not None and net_cap is not None:
        if not _lte_rank(net_rec, net_cap, _NETWORK_RANK):
            violations.append(
                f"access.network_access '{net_rec}' exceeds capability network_access '{net_cap}'"
            )

    if lane == "candidate_proposal" and not gov.get("requires_human_review"):
        violations.append("candidate_proposal receipts must set requires_human_review true")

    if lane == "evidence_stub" and not gov.get("requires_gate_review"):
        violations.append("evidence_stub receipts must set requires_gate_review true")

    return sorted(violations)


def validate_mcp_receipt(
    receipt: dict[str, Any],
    caps_doc: dict[str, Any],
    bind_doc: dict[str, Any],
    *,
    schema_path: Path = RECEIPT_SCHEMA_PATH,
) -> tuple[list[str], list[str]]:
    """
    Full validation: JSON Schema then business rules.
    Returns (violations, warnings). violations non-empty means invalid receipt.
    """
    try:
        validate_json_schema(receipt, schema_path)
    except Exception as e:
        return ([f"schema: {e}"], [])

    biz = validate_mcp_receipt_business(receipt, caps_doc, bind_doc)
    cap = capability_by_id(caps_doc, receipt.get("capability", {}).get("id") or "")
    warns: list[str] = []
    if cap:
        warns = warnings_for_receipt(receipt, cap)
    return (biz, sorted(warns))


def canonical_json_for_hash(obj: dict[str, Any]) -> str:
    """Stable JSON for hashing; integrity.receipt_hash omitted."""
    copy = json.loads(json.dumps(obj))
    integrity = copy.get("integrity")
    if isinstance(integrity, dict):
        integrity.pop("receipt_hash", None)
    return json.dumps(copy, sort_keys=True, separators=(",", ":"))


def receipt_sha256_hex(obj: dict[str, Any]) -> str:
    payload = canonical_json_for_hash(obj).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
