#!/usr/bin/env python3
"""
Emit a validated MCP governance execution receipt JSON under artifacts/mcp-receipts/.

Does not execute MCP or mutate Record. See docs/mcp/mcp-execution-receipts.md.

  python3 scripts/mcp_receipt.py --capability-id github_readonly \\
    --actor-kind assistant --actor-name chatgpt \\
    --intent "Inspect repo MCP policy files" \\
    --resources-read config/mcp-capabilities.yaml \\
    --status success --summary "Confirmed MCP registry exists."
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_capability_audit import _git_short_hash  # noqa: E402
from mcp_receipt_lib import (  # noqa: E402
    BINDINGS_PATH,
    CAPABILITIES_PATH,
    RECEIPT_SCHEMA_PATH,
    authority_from_binding,
    bindings_lane_map,
    capability_by_id,
    load_yaml,
    receipt_sha256_hex,
    validate_mcp_receipt,
)

DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"


def _parse_artifacts(items: list[str] | None) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if not items:
        return out
    for raw in items:
        if "=" not in raw:
            raise ValueError(f"--artifact expects path=kind, got {raw!r}")
        path, kind = raw.split("=", 1)
        path = path.strip()
        kind = kind.strip()
        if not path or not kind:
            raise ValueError(f"--artifact expects path=kind, got {raw!r}")
        out.append({"path": path, "kind": kind})
    return out


def build_receipt(
    *,
    cap: dict[str, Any],
    binding: dict[str, Any],
    receipt_id: str,
    created_at: str,
    actor_kind: str,
    actor_name: str,
    session_id: str | None,
    declared_intent: str,
    prompt_summary: str | None,
    operator_supplied_refs: list[str],
    network_access: str,
    credential_use: str,
    resources_read: list[str],
    resources_written: list[str],
    status: str,
    summary: str,
    artifacts: list[dict[str, str]],
    governance: dict[str, Any],
    repo_git_ref: str,
    receipt_hash: str | None,
    parent_receipt_id: str | None,
) -> dict[str, Any]:
    authority = authority_from_binding(binding)
    actor: dict[str, Any] = {"kind": actor_kind, "name": actor_name}
    if session_id:
        actor["session_id"] = session_id

    inputs: dict[str, Any] = {"operator_supplied_refs": operator_supplied_refs}
    if prompt_summary:
        inputs["prompt_summary"] = prompt_summary

    integrity: dict[str, Any] = {"repo_git_ref": repo_git_ref}
    if receipt_hash:
        integrity["receipt_hash"] = receipt_hash
    if parent_receipt_id:
        integrity["parent_receipt_id"] = parent_receipt_id

    return {
        "schema_version": 1,
        "receipt_id": receipt_id,
        "created_at_utc": created_at,
        "actor": actor,
        "capability": {
            "id": cap["id"],
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": authority,
        "declared_intent": declared_intent,
        "inputs": inputs,
        "access": {
            "network_access": network_access,
            "credential_use": credential_use,
            "resources_read": resources_read,
            "resources_written": resources_written,
        },
        "result": {"status": status, "summary": summary, "artifacts": artifacts},
        "governance": governance,
        "integrity": integrity,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build and validate MCP execution receipt JSON.")
    ap.add_argument("--capability-id", required=True)
    ap.add_argument("--actor-kind", required=True, choices=["operator", "assistant", "coding_agent", "script"])
    ap.add_argument("--actor-name", required=True)
    ap.add_argument("--session-id", default=None)
    ap.add_argument("--intent", required=True, dest="declared_intent")
    ap.add_argument("--prompt-summary", default=None)
    ap.add_argument(
        "--operator-supplied-ref",
        action="append",
        default=None,
        dest="operator_supplied_refs",
        help="Repeatable path or URI refs.",
    )
    ap.add_argument(
        "--resources-read",
        nargs="*",
        default=[],
        metavar="PATH",
        help="Zero or more paths read (shell-expand multiple tokens after this flag).",
    )
    ap.add_argument(
        "--resources-written",
        nargs="*",
        default=[],
        metavar="PATH",
        help="Zero or more paths written.",
    )
    ap.add_argument("--network-access", default=None, choices=["none", "read", "full"])
    ap.add_argument("--credential-use", default=None, choices=["none", "optional", "required"])
    ap.add_argument(
        "--status",
        required=True,
        choices=["success", "partial", "blocked", "failed"],
    )
    ap.add_argument("--summary", required=True)
    ap.add_argument("--artifact", action="append", default=None, metavar="PATH=KIND")
    ap.add_argument("--canonical-record-touched", action="store_true")
    ap.add_argument("--durable-state-write-attempted", action="store_true")
    ap.add_argument("--requires-human-review", default=None, action=argparse.BooleanOptionalAction)
    ap.add_argument("--requires-gate-review", default=None, action=argparse.BooleanOptionalAction)
    ap.add_argument("--prohibited-action-attempted", action="store_true")
    ap.add_argument("--prohibited-action-note", action="append", default=None)
    ap.add_argument("--parent-receipt-id", default=None)
    ap.add_argument("--receipt-id", default=None, help="Default: random UUID.")
    ap.add_argument("--with-hash", action="store_true", help="Set integrity.receipt_hash (SHA-256 of canonical JSON).")
    ap.add_argument("--capabilities", type=Path, default=CAPABILITIES_PATH)
    ap.add_argument("--bindings", type=Path, default=BINDINGS_PATH)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("-o", "--output", type=Path, default=None, help="Write receipt JSON here.")
    ap.add_argument("--stdout", action="store_true", help="Also print JSON to stdout.")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    caps_doc = load_yaml(args.capabilities.resolve())
    bind_doc = load_yaml(args.bindings.resolve())

    cap = capability_by_id(caps_doc, args.capability_id)
    if cap is None:
        print(f"mcp_receipt: unknown capability id {args.capability_id!r}", file=sys.stderr)
        return 1

    lane = cap["output_lane"]
    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"mcp_receipt: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(lane)
    if binding is None:
        print(f"mcp_receipt: no binding for lane {lane!r}", file=sys.stderr)
        return 1

    net = args.network_access if args.network_access is not None else cap["network_access"]
    cred = args.credential_use if args.credential_use is not None else cap["credential_requirements"]

    reads = list(args.resources_read or [])
    writes = list(args.resources_written or [])

    refs = list(args.operator_supplied_refs) if args.operator_supplied_refs else []

    rh = args.requires_human_review
    if rh is None:
        rh = lane == "candidate_proposal"
    rg = args.requires_gate_review
    if rg is None:
        rg = lane == "evidence_stub"

    gov = {
        "durable_state_write_attempted": args.durable_state_write_attempted,
        "canonical_record_touched": args.canonical_record_touched,
        "requires_human_review": rh,
        "requires_gate_review": rg,
        "prohibited_action_attempted": args.prohibited_action_attempted,
        "prohibited_action_notes": list(args.prohibited_action_note) if args.prohibited_action_note else [],
    }

    rid = args.receipt_id or str(uuid.uuid4())
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        artifacts = _parse_artifacts(args.artifact)
    except ValueError as e:
        print(f"mcp_receipt: {e}", file=sys.stderr)
        return 1

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=rid,
        created_at=ts,
        actor_kind=args.actor_kind,
        actor_name=args.actor_name,
        session_id=args.session_id,
        declared_intent=args.declared_intent,
        prompt_summary=args.prompt_summary,
        operator_supplied_refs=refs,
        network_access=net,
        credential_use=cred,
        resources_read=reads,
        resources_written=writes,
        status=args.status,
        summary=args.summary,
        artifacts=artifacts,
        governance=gov,
        repo_git_ref=_git_short_hash(root),
        receipt_hash=None,
        parent_receipt_id=args.parent_receipt_id,
    )

    if args.with_hash:
        receipt["integrity"]["receipt_hash"] = receipt_sha256_hex(receipt)

    viols, warns = validate_mcp_receipt(receipt, caps_doc, bind_doc, schema_path=RECEIPT_SCHEMA_PATH)
    if warns:
        for w in warns:
            print(f"mcp_receipt: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"mcp_receipt: invalid: {v}", file=sys.stderr)
        return 1

    out_path = args.output
    if out_path is None:
        DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DEFAULT_OUT_DIR / f"{rid}.json"

    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    out_path.write_text(text, encoding="utf-8")

    try:
        rel = out_path.relative_to(root)
    except ValueError:
        rel = out_path
    print(f"Wrote {rel}", file=sys.stderr)
    if args.stdout:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
