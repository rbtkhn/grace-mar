#!/usr/bin/env python3
"""
MCP mock execution harness — fixture JSON → Markdown packet + MCP receipt (no live MCP).

Does not execute MCP servers, use credentials, invoke network/shell, or enable integrations.
See docs/mcp/mcp-mock-execution-harness.md.

  python3 scripts/mcp_mock_harness.py \\
    --input examples/mcp-mock-run.github-readonly.example.json \\
    --output artifacts/mcp-mock-runs/github-readonly-demo.md
"""

from __future__ import annotations

import argparse
import copy
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
    bindings_lane_map,
    build_receipt,
    capability_by_id,
    load_yaml,
    validate_json_schema,
    validate_mcp_receipt,
)
from mcp_risk_scan import evaluate_capability  # noqa: E402

MOCK_RUN_SCHEMA_PATH = REPO_ROOT / "schemas" / "mcp-mock-run.v1.json"
DEFAULT_POLICY = REPO_ROOT / "config" / "mcp-risk-policy.yaml"
DEFAULT_CAPABILITY_ID = "mcp_mock_harness"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

_NETWORK_RANK: dict[str, int] = {"none": 0, "read": 1, "full": 2}
_CRED_RANK: dict[str, int] = {"none": 0, "optional": 1, "required": 2}

_SHELL_NEEDLES = (
    "shell_execute",
    "shell ",
    "subprocess",
    "/bin/bash",
    "/bin/sh",
    "powershell",
    "cmd.exe",
    "interactive_terminal",
)
_COMMAND_NEEDLES = ("execute_command", "run_command")

BANNER = "MOCK MCP RUN · WORK ARTIFACT · NO LIVE SERVER · NOT APPROVED INTEGRATION"


def _lte_rank(value: str, cap_max: str, ranks: dict[str, int]) -> bool:
    return ranks.get(value, -1) <= ranks.get(cap_max, -1)


def _posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_mock_run(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    doc = json.loads(text)
    if not isinstance(doc, dict):
        raise ValueError("mock run root must be an object")
    return doc


def validate_resource_token(s: str, *, ctx: str) -> None:
    """Reject unsafe resources; allow mock:// URIs or repo-relative fixture paths."""
    t = s.strip()
    if not t:
        raise ValueError(f"{ctx}: empty resource token")
    tl = t.lower()
    if "http://" in tl or "https://" in tl:
        raise ValueError(f"{ctx}: http/https URLs not allowed ({t!r})")
    if "users/grace-mar" in tl:
        raise ValueError(f"{ctx}: users/grace-mar paths not allowed ({t!r})")
    if tl.startswith("mock:"):
        norm = t.replace("\\", "/")
        parts = [p for p in norm.split("/") if p]
        if ".." in parts:
            raise ValueError(f"{ctx}: mock URI must not contain .. ({t!r})")
        return
    if len(t) >= 2 and t[1] == ":":
        raise ValueError(f"{ctx}: absolute paths not allowed ({t!r})")
    if t.startswith("/"):
        raise ValueError(f"{ctx}: absolute paths not allowed ({t!r})")
    norm = t.replace("\\", "/")
    parts = [p for p in norm.split("/") if p]
    if ".." in parts:
        raise ValueError(f"{ctx}: paths must not contain .. ({t!r})")


def validate_mock_resources(doc: dict[str, Any]) -> None:
    mq = doc["mock_request"]
    for i, s in enumerate(mq.get("resources_read") or []):
        validate_resource_token(s, ctx=f"mock_request.resources_read[{i}]")
    for i, s in enumerate(mq.get("resources_written") or []):
        validate_resource_token(s, ctx=f"mock_request.resources_written[{i}]")


def shell_tool_needles_hit(tool_name: str) -> bool:
    h = tool_name.lower()
    return any(n in h for n in _SHELL_NEEDLES) or any(n in h for n in _COMMAND_NEEDLES)


def overlay_simulated_capability(sim: dict[str, Any], mock_req: dict[str, Any]) -> dict[str, Any]:
    syn = copy.deepcopy(sim)
    syn["network_access"] = mock_req["network_access"]
    syn["credential_requirements"] = mock_req["credential_use"]
    syn["reads"] = list(mock_req.get("resources_read") or [])
    syn["writes"] = list(mock_req.get("resources_written") or [])
    return syn


def enforce_mock_vs_registry(doc: dict[str, Any], sim: dict[str, Any]) -> list[str]:
    """Return human-readable violation strings; empty means pass."""
    errs: list[str] = []
    mq = doc["mock_request"]
    mr = doc["mock_response"]
    gov = doc["governance_expectations"]
    run = doc["run"]

    if gov.get("durable_state_write_attempted"):
        errs.append("governance_expectations.durable_state_write_attempted must be false for mock harness")
    if gov.get("canonical_record_touched"):
        errs.append("governance_expectations.canonical_record_touched must be false for mock harness")

    reg_writes = sim.get("writes") or []
    if not reg_writes and mq.get("resources_written"):
        errs.append("mock_request.resources_written must be empty when simulated capability registry writes are empty")

    net_m = mq["network_access"]
    net_cap = sim.get("network_access") or "none"
    if not _lte_rank(net_m, net_cap, _NETWORK_RANK):
        errs.append(
            f"mock_request.network_access {net_m!r} exceeds simulated capability network_access {net_cap!r}"
        )

    cred_m = mq["credential_use"]
    cred_cap = sim.get("credential_requirements") or "none"
    if not _lte_rank(cred_m, cred_cap, _CRED_RANK):
        errs.append(
            f"mock_request.credential_use {cred_m!r} exceeds simulated capability credential_requirements {cred_cap!r}"
        )

    lane = sim.get("output_lane")
    if lane == "prohibited" and mr.get("status") == "success":
        errs.append("mock_response.status cannot be success when simulated capability output_lane is prohibited")

    if shell_tool_needles_hit(run["tool_name"]) and mr.get("status") == "success":
        errs.append("shell/command-shaped tool_name cannot use mock_response.status success (blocked posture required)")

    return errs


def prohibited_action_attempted_for_receipt(mock_status: str, shell_hit: bool) -> bool:
    if mock_status in ("blocked", "failed"):
        return True
    if shell_hit and mock_status != "success":
        return True
    return False


def resolve_mock_run_destination(repo_root: Path, output: Path | None) -> Path:
    bucket = (repo_root / "artifacts" / "mcp-mock-runs").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        return bucket / "mock-mcp-run-packet.md"
    candidate = output if output.is_absolute() else (repo_root / output)
    resolved = candidate.resolve()
    try:
        rel_to_repo = resolved.relative_to(repo_root.resolve())
    except ValueError as e:
        raise ValueError(f"output must be under repository root: {resolved}") from e
    try:
        resolved.relative_to(bucket)
    except ValueError as e:
        raise ValueError(f"output must be under {bucket} (got {resolved})") from e
    rp = rel_to_repo.parts
    if len(rp) >= 2 and rp[0].lower() == "users" and rp[1].lower() == "grace-mar":
        raise ValueError("refusing output path under users/grace-mar/")
    return resolved


def render_markdown(
    doc: dict[str, Any],
    *,
    sim: dict[str, Any],
    binding_summary: str,
    risk: dict[str, Any] | None,
    enforcement_ok: bool,
    violation_notes: list[str],
    receipt_id: str,
    packet_rel: str,
    receipt_filename: str,
) -> str:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "adapter": "mcp_mock_harness.py",
        "schema": "mcp-mock-run.v1",
        "receipt_id": receipt_id,
        "mock_run_id": doc["run"]["id"],
        "simulated_capability_id": doc["run"]["capability_id"],
        "generated_at_utc": ts,
    }
    header = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"

    lines = [
        header,
        "",
        f"> {BANNER}",
        "",
        f"MCP receipt JSON (repo-relative): `artifacts/mcp-receipts/{receipt_filename}` — packet path: `{packet_rel}`",
        "",
        "## Run",
        "",
        f"- **run.id:** `{doc['run']['id']}`",
        f"- **Simulated capability_id:** `{doc['run']['capability_id']}`",
        f"- **tool_name:** `{doc['run']['tool_name']}`",
        f"- **declared_intent:** {doc['run']['declared_intent']}",
        "",
        "## Simulated capability (registry)",
        "",
        f"- **Registry id:** `{sim['id']}`",
        f"- **output_lane:** `{sim.get('output_lane')}`",
        f"- **category:** `{sim.get('category')}`",
        "",
        "## Authority binding (simulated lane)",
        "",
        binding_summary,
        "",
        "## Mock request",
        "",
        "```json",
        json.dumps(doc["mock_request"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Mock response",
        "",
        "```json",
        json.dumps(
            {"status": doc["mock_response"]["status"], "summary": doc["mock_response"]["summary"]},
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "### mock_response.data",
        "",
        "```json",
        json.dumps(doc["mock_response"].get("data") or {}, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Governance expectations (fixture)",
        "",
        "```json",
        json.dumps(doc["governance_expectations"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Risk evaluation (policy overlay on simulated capability)",
        "",
    ]
    if risk:
        lines.extend(
            [
                f"- **Score:** {risk['score']}",
                f"- **Risk level:** `{risk['risk_level']}`",
                f"- **Recommendation:** `{risk['recommendation']}`",
                f"- **Hard blockers:** {risk.get('hard_blockers') or []}",
                f"- **Warnings:** {risk.get('warnings') or []}",
                "",
            ]
        )
    else:
        lines.append("_Risk evaluation skipped._\n")

    lines.extend(
        [
            "## Harness enforcement",
            "",
            f"- **Simulated limits satisfied:** {'yes' if enforcement_ok else 'no'}",
        ]
    )
    if violation_notes:
        lines.append("- **Violations:**")
        for v in violation_notes:
            lines.append(f"  - `{v}`")
    lines.extend(
        [
            "",
            "## Governance",
            "",
            "This packet does **not** execute MCP servers, does **not** approve credentials, and does **not** enable live integration.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Mock MCP execution harness — fixture JSON to packet + receipt.")
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--capabilities", type=Path, default=CAPABILITIES_PATH)
    ap.add_argument("--bindings", type=Path, default=BINDINGS_PATH)
    ap.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    ap.add_argument(
        "--capability-id",
        default=DEFAULT_CAPABILITY_ID,
        help=f"Receipt capability registry id (default {DEFAULT_CAPABILITY_ID!r}); output_lane must be work_artifact.",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    inp = args.input if args.input.is_absolute() else (root / args.input)
    inp = inp.resolve()
    if not inp.is_file():
        print(f"mcp_mock_harness: input not found: {inp}", file=sys.stderr)
        return 1

    try:
        doc = load_mock_run(inp)
        validate_json_schema(doc, MOCK_RUN_SCHEMA_PATH)
        validate_mock_resources(doc)
    except Exception as e:
        print(f"mcp_mock_harness: validation failed: {e}", file=sys.stderr)
        return 1

    caps_doc = load_yaml(args.capabilities.resolve())
    policy_doc = load_yaml(args.policy.resolve())
    bind_doc = load_yaml(args.bindings.resolve())

    sim_id = doc["run"]["capability_id"]
    sim = capability_by_id(caps_doc, sim_id)
    if sim is None:
        print(f"mcp_mock_harness: unknown simulated capability_id {sim_id!r}", file=sys.stderr)
        return 1

    violations = enforce_mock_vs_registry(doc, sim)
    if violations:
        for v in violations:
            print(f"mcp_mock_harness: {v}", file=sys.stderr)
        return 1

    syn = overlay_simulated_capability(sim, doc["mock_request"])
    risk_finding: dict[str, Any] | None = evaluate_capability(syn, policy_doc)

    binding_txt_sim = "_Binding unresolved._"
    try:
        lm = bindings_lane_map(bind_doc)
        lane = sim["output_lane"]
        b = lm.get(lane)
        if b:
            binding_txt_sim = (
                f"- **output_lane:** `{lane}`\n"
                f"- **authority_surface:** `{b['authority_surface']}`\n"
                f"- **authority_class:** `{b['authority_class']}`"
            )
    except ValueError as e:
        binding_txt_sim = f"(bindings parse error: {e})"

    try:
        dest = resolve_mock_run_destination(root, args.output)
    except ValueError as e:
        print(f"mcp_mock_harness: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    packet_rel = _posix_under_repo(root, dest)

    caps_doc_full = load_yaml(CAPABILITIES_PATH.resolve())
    adapter_cap = capability_by_id(caps_doc_full, args.capability_id)
    if adapter_cap is None:
        print(f"mcp_mock_harness: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1
    if adapter_cap["output_lane"] != "work_artifact":
        print(
            f"mcp_mock_harness: capability output_lane must be work_artifact (got {adapter_cap['output_lane']!r})",
            file=sys.stderr,
        )
        return 1

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"mcp_mock_harness: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(adapter_cap["output_lane"])
    if binding is None:
        print("mcp_mock_harness: missing binding for work_artifact lane", file=sys.stderr)
        return 1

    inp_rel = _posix_under_repo(root, inp)
    shell_hit = shell_tool_needles_hit(doc["run"]["tool_name"])
    mock_status = doc["mock_response"]["status"]

    decl = doc["run"]["declared_intent"].strip()
    if len(decl) > 400:
        decl = decl[:399] + "…"

    net_a = adapter_cap["network_access"]
    cred_a = adapter_cap["credential_requirements"]

    pa_attempted = prohibited_action_attempted_for_receipt(mock_status, shell_hit)
    notes: list[str] = []
    if mock_status in ("blocked", "failed"):
        notes.append(f"mock_response.status={mock_status}")
    if shell_hit:
        notes.append("shell_command_tool_shape_detected")

    gov = {
        "durable_state_write_attempted": False,
        "canonical_record_touched": False,
        "requires_human_review": True,
        "requires_gate_review": True,
        "prohibited_action_attempted": pa_attempted,
        "prohibited_action_notes": notes or ["mock_harness_fixture_ok"],
    }

    summary = "Generated MCP mock execution harness packet (fixture-only; no live MCP)."
    if mock_status == "blocked":
        summary += " Mock outcome blocked."

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts_list = [
        {"path": packet_rel, "kind": "markdown_mcp_mock_harness"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    receipt = build_receipt(
        cap=adapter_cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="mcp_mock_harness.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[inp_rel],
        network_access=net_a,
        credential_use=cred_a,
        resources_read=[inp_rel],
        resources_written=[packet_rel],
        status=mock_status,
        summary=summary,
        artifacts=artifacts_list,
        governance=gov,
        repo_git_ref=_git_short_hash(root),
        receipt_hash=None,
        parent_receipt_id=None,
    )

    viols, warns = validate_mcp_receipt(receipt, caps_doc_full, bind_doc, schema_path=RECEIPT_SCHEMA_PATH)
    if warns:
        for w in warns:
            print(f"mcp_mock_harness: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"mcp_mock_harness: receipt invalid: {v}", file=sys.stderr)
        return 1

    md_body = render_markdown(
        doc,
        sim=sim,
        binding_summary=binding_txt_sim,
        risk=risk_finding,
        enforcement_ok=True,
        violation_notes=[],
        receipt_id=receipt_id,
        packet_rel=packet_rel,
        receipt_filename=receipt_filename,
    )

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(md_body, encoding="utf-8")

    DEFAULT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = (DEFAULT_RECEIPT_DIR / receipt_filename).resolve()
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(_posix_under_repo(root, dest))
    print(_posix_under_repo(root, receipt_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
