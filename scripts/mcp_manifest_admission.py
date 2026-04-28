#!/usr/bin/env python3
"""
MCP server manifest admission — classify declared manifests vs Grace-Mar capability registry.

Does not execute MCP servers, use credentials, or enable integrations. See
docs/mcp/mcp-manifest-admission.md.

  python3 scripts/mcp_manifest_admission.py \\
    --input examples/mcp-server-manifest.example.yaml \\
    --output artifacts/mcp-admission/github-readonly-candidate.md
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

DEFAULT_POLICY = REPO_ROOT / "config" / "mcp-risk-policy.yaml"
MANIFEST_SCHEMA_PATH = REPO_ROOT / "schemas" / "mcp-server-manifest.v1.json"
DEFAULT_CAPABILITY_ID = "mcp_manifest_admission"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

NEEDS_MANUAL = "needs_manual_classification"

LANE_RANK: dict[str, int] = {
    "runtime_only": 0,
    "work_artifact": 1,
    "evidence_stub": 2,
    "candidate_proposal": 3,
    "prohibited": 99,
}

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
_MERGE_TOKENS = ("merge_to_main", "force_push", "bypass_review")
_DB_WRITE_NEEDLES = ("insert", "update", "delete", "ddl", "upsert")
_MEMORY_NEEDLES = ("upsert_embedding", "vector", "embedding_store", "thoughts_row")


def _posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as e:
            raise RuntimeError("PyYAML required") from e
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def validate_path_like_string(s: str, *, ctx: str) -> None:
    """Reject absolute paths and .. segments in manifest strings."""
    t = s.strip()
    if not t:
        return
    if len(t) >= 2 and t[1] == ":":
        raise ValueError(f"{ctx}: absolute paths not allowed ({t!r})")
    if t.startswith("/"):
        raise ValueError(f"{ctx}: absolute paths not allowed ({t!r})")
    if ":" in t and not t.startswith(("http://", "https://")):
        if len(t) > 2 and t[1] == ":":
            raise ValueError(f"{ctx}: absolute paths not allowed ({t!r})")
    norm = t.replace("\\", "/")
    parts = [p for p in norm.split("/") if p]
    if ".." in parts:
        raise ValueError(f"{ctx}: paths must not contain .. ({t!r})")


def collect_manifest_strings(doc: dict[str, Any]) -> list[tuple[str, str]]:
    """Return (context, string) pairs to validate as path-like."""

    out: list[tuple[str, str]] = []

    def walk(prefix: str, obj: Any) -> None:
        if isinstance(obj, str):
            out.append((prefix, obj))
        elif isinstance(obj, list):
            for i, x in enumerate(obj):
                walk(f"{prefix}[{i}]", x)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(f"{prefix}.{k}", v)

    walk("manifest", doc)
    return out


def validate_manifest_paths(doc: dict[str, Any]) -> None:
    """Validate strings that look like filesystem paths (contain slashes or ..)."""
    for ctx, s in collect_manifest_strings(doc):
        if "/" in s or "\\" in s or ".." in s:
            validate_path_like_string(s, ctx=ctx)


def caps_by_id(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {c["id"]: c for c in doc["capabilities"]}


def _hay(xs: list[str] | None) -> str:
    return " ".join(xs or []).lower()


def admission_local_blockers(manifest: dict[str, Any]) -> list[str]:
    """Hard admission rules before registry classification."""
    reasons: list[str] = []
    perm = manifest["permissions"]
    ah = _hay(perm.get("allowed_actions"))
    ph = _hay(perm.get("prohibited_actions"))
    rh = _hay(perm.get("reads"))
    wh = _hay(perm.get("writes"))
    blob = ah + " " + rh + " " + wh

    if any(t in ah for t in _MERGE_TOKENS):
        reasons.append("merge_to_main_or_force_or_bypass_in_allowed_actions")

    if any(n in ah for n in _SHELL_NEEDLES) or any(n in ah for n in _COMMAND_NEEDLES):
        reasons.append("shell_or_command_execution_in_allowed_actions")

    if any(n in ah for n in ("credential_exfiltration", "steal_token", "exfiltrate")):
        reasons.append("credential_exfiltration_in_allowed_actions")

    if "users/grace-mar" in blob:
        reasons.append("users_grace_mar_path_in_manifest_permissions")

    if any(x in wh + ah for x in _DB_WRITE_NEEDLES):
        reasons.append("database_mutating_verbs_in_writes_or_allowed")

    if perm.get("durable_state_write"):
        reasons.append("durable_state_write_declared_true")

    mem_surface = ah + wh
    if any(x in mem_surface for x in _MEMORY_NEEDLES) and (
        "upsert_embedding_store" not in ph or "silent_profile_merge" not in ph
    ):
        reasons.append("external_memory_write_without_prohibition_alignment")

    return reasons


def infer_matched_capability_id(manifest: dict[str, Any]) -> tuple[str, str]:
    """
    Return (registry_capability_id, rationale_snippet).
    Uses conservative keyword routing — unmatched → NEEDS_MANUAL.
    """
    srv = manifest["server"]
    perm = manifest["permissions"]
    ah = perm["allowed_actions"]
    ah_h = _hay(ah)
    wh_h = _hay(perm.get("writes"))
    rh_h = _hay(perm.get("reads"))
    net = perm["network_access"]
    desc = (srv.get("description") or "").lower()

    blob = desc + " " + ah_h + " " + rh_h + " " + wh_h

    if any(n in ah_h for n in _SHELL_NEEDLES + _COMMAND_NEEDLES):
        return "shell_execution_prohibited", "shell/command verbs in allowed_actions → prohibition template"

    if any(x in ah_h + wh_h for x in _MEMORY_NEEDLES):
        return "memory_external_prohibited_by_default", "memory/upsert-style verbs → prohibited-memory template"

    scmish = any(k in blob for k in ("github", " git", "repo", "pull request", " scm"))
    if scmish or net in ("read", "full"):
        if not perm["writes"] and net == "read" and ph_complete_github(perm):
            return "github_readonly", "scm read surfaces + network read + no writes + merge prohibitions listed"

        if (
            perm["writes"]
            or any(k in ah_h for k in ("draft", "open_draft_pr", "comment_patch"))
        ) and ph_complete_github(perm):
            if not any(t in ah_h for t in _MERGE_TOKENS):
                return "github_patch_proposal", "scm draft/write-branch posture without merge verbs in allowed"

    if net == "none" and (
        "list_directory" in ah_h
        or "read_file" in ah_h
        or "filesystem" in desc
    ) and not perm["writes"]:
        return "filesystem_readonly", "filesystem read verbs without writes"

    if any(k in ah_h for k in ("fetch_public_url", "summarize_excerpt", "http")) or "web" in desc:
        return "web_research", "web fetch/summarize posture"

    if any(k in ah_h for k in ("select_queries", "explain_plan", "sql_select")) or "database" in desc:
        return "database_readonly", "database read-only posture"

    if any(k in ah_h for k in ("propose_diff_in_worktree", "open_review_packet", "patch_intake")):
        return "coding_agent_patch_intake", "coding-agent patch/review packet verbs"

    return NEEDS_MANUAL, "no confident capability fingerprint"


def ph_complete_github(perm: dict[str, Any]) -> bool:
    ph = _hay(perm.get("prohibited_actions"))
    return all(t in ph for t in ("merge_to_main", "force_push", "bypass_review"))


def requested_lane_blocked(manifest: dict[str, Any], matched_lane: str) -> str | bool:
    """Return False if OK, else blocker description string."""
    op = manifest.get("operator") or {}
    req = op.get("requested_output_lane")
    if not req:
        return False
    if req not in LANE_RANK or matched_lane not in LANE_RANK:
        return "requested_output_lane_invalid"
    if LANE_RANK[str(req)] > LANE_RANK[str(matched_lane)]:
        return "requested_output_lane_exceeds_matched_capability_lane"
    return False


def overlay_manifest_on_capability(
    base: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    """Merge manifest.permissions onto registry capability for risk scoring."""
    syn = copy.deepcopy(base)
    perm = manifest["permissions"]
    syn["allowed_actions"] = list(perm.get("allowed_actions") or [])
    syn["prohibited_actions"] = list(perm.get("prohibited_actions") or [])
    syn["reads"] = list(perm.get("reads") or [])
    syn["writes"] = list(perm.get("writes") or [])

    na = perm["network_access"]
    if na == "unknown":
        syn["network_access"] = "none"
    else:
        syn["network_access"] = na

    cr = perm["credential_requirements"]
    if cr == "unknown":
        syn["credential_requirements"] = "optional"
    else:
        syn["credential_requirements"] = cr

    syn["durable_state_write"] = bool(perm.get("durable_state_write", False))

    loc = manifest["server"].get("local_or_cloud")
    if loc and loc != "unknown":
        syn["local_or_cloud"] = loc

    return syn


def resolve_admission_destination(repo_root: Path, output: Path | None) -> Path:
    bucket = (repo_root / "artifacts" / "mcp-admission").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        return bucket / "manifest-admission.md"
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
    manifest: dict[str, Any],
    *,
    matched_id: str,
    rationale: str,
    admission_status: str,
    local_blockers: list[str],
    lane_blocker: str | bool,
    risk: dict[str, Any] | None,
    binding_summary: str,
    receipt_id: str,
    receipt_filename: str,
    packet_rel: str,
    capability_id: str,
) -> str:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "adapter": "mcp_manifest_admission.py",
        "schema": "mcp-server-manifest.v1",
        "capability_id": capability_id,
        "mcp_receipt_id": receipt_id,
        "matched_capability_id": matched_id,
        "admission_status": admission_status,
        "generated_at_utc": ts,
    }
    header = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"

    lines = [
        header,
        "",
        "> **MCP ADMISSION REVIEW · WORK ARTIFACT · NOT ENABLED · NOT APPROVED INTEGRATION**",
        "",
        f"MCP receipt JSON (repo-relative): `artifacts/mcp-receipts/{receipt_filename}` — packet path: `{packet_rel}`",
        "",
        "## Server",
        "",
        f"- **ID:** `{manifest['server']['id']}`",
        f"- **Name:** {manifest['server']['name']}",
        f"- **Description:** {manifest['server']['description']}",
        f"- **Local/cloud:** `{manifest['server']['local_or_cloud']}`",
        "",
        "## Declared capabilities",
        "",
        f"- **Tools:** {manifest['declared_capabilities'].get('tools')}",
        f"- **Resources:** {manifest['declared_capabilities'].get('resources')}",
        f"- **Prompts:** {manifest['declared_capabilities'].get('prompts')}",
        "",
        "## Permissions (declared)",
        "",
        "```json",
        json.dumps(manifest["permissions"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Classification",
        "",
        f"- **Matched Grace-Mar capability id:** `{matched_id}`",
        f"- **Rationale:** {rationale}",
        "",
        "## Authority binding (matched lane)",
        "",
        binding_summary,
        "",
        "## Risk evaluation (policy overlay)",
        "",
    ]
    if risk:
        lines.extend(
            [
                f"- **Score:** {risk['score']}",
                f"- **Risk level:** `{risk['risk_level']}`",
                f"- **Recommendation:** `{risk['recommendation']}`",
                f"- **Hard blockers (risk scan):** {risk.get('hard_blockers') or []}",
                f"- **Warnings (risk scan):** {risk.get('warnings') or []}",
                "",
            ]
        )
    else:
        lines.extend(["_Risk scan skipped (manual classification path)._", ""])

    lines.extend(["## Admission gates", ""])
    if local_blockers:
        lines.append("- **Local admission blockers:**")
        for b in local_blockers:
            lines.append(f"  - `{b}`")
    else:
        lines.append("- **Local admission blockers:** _none_")
    if lane_blocker and lane_blocker is not True:
        lines.append(f"- **Lane gate:** `{lane_blocker}`")
    lines.extend(
        [
            "",
            "## Operator intent",
            "",
            manifest["operator"]["intended_use"],
            "",
            "## Governance",
            "",
            "This packet does **not** enable MCP servers, does **not** approve credentials, and is **not** live integration approval. Record mutation stays gated per AGENTS.md.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP manifest admission — classify manifests without executing MCP.")
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
        print(f"mcp_manifest_admission: input not found: {inp}", file=sys.stderr)
        return 1

    try:
        manifest = load_manifest(inp)
        validate_json_schema(manifest, MANIFEST_SCHEMA_PATH)
        validate_manifest_paths(manifest)
    except Exception as e:
        print(f"mcp_manifest_admission: validation failed: {e}", file=sys.stderr)
        return 1

    caps_doc = load_yaml(args.capabilities.resolve())
    policy_doc = load_yaml(args.policy.resolve())
    bind_doc = load_yaml(args.bindings.resolve())
    cmap = caps_by_id(caps_doc)

    local_blockers = admission_local_blockers(manifest)
    matched_id, rationale = infer_matched_capability_id(manifest)

    matched_cap = cmap.get(matched_id)
    lane_block: str | bool = False
    if matched_cap:
        lane_block = requested_lane_blocked(manifest, matched_cap["output_lane"])
    elif matched_id != NEEDS_MANUAL:
        lane_block = "matched_capability_missing"

    risk_finding: dict[str, Any] | None = None
    if matched_cap:
        syn = overlay_manifest_on_capability(matched_cap, manifest)
        risk_finding = evaluate_capability(syn, policy_doc)

    binding_txt = "_No matched capability — binding unresolved._"
    if matched_cap:
        try:
            lm = bindings_lane_map(bind_doc)
            lane = matched_cap["output_lane"]
            b = lm.get(lane)
            if b:
                binding_txt = (
                    f"- **output_lane:** `{lane}`\n"
                    f"- **authority_surface:** `{b['authority_surface']}`\n"
                    f"- **authority_class:** `{b['authority_class']}`"
                )
        except ValueError as e:
            binding_txt = f"(bindings parse error: {e})"

    blocked_reasons = list(local_blockers)
    if lane_block and lane_block is not False:
        blocked_reasons.append(str(lane_block))

    if risk_finding and risk_finding.get("hard_blockers"):
        blocked_reasons.extend(f"risk:{x}" for x in risk_finding["hard_blockers"])

    admission_blocked = bool(blocked_reasons) or (matched_id == NEEDS_MANUAL)

    admission_status = "blocked" if admission_blocked else "review_only"

    try:
        dest = resolve_admission_destination(root, args.output)
    except ValueError as e:
        print(f"mcp_manifest_admission: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    packet_rel = _posix_under_repo(root, dest)

    caps_doc_full = load_yaml(CAPABILITIES_PATH.resolve())
    cap = capability_by_id(caps_doc_full, args.capability_id)
    if cap is None:
        print(f"mcp_manifest_admission: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1
    if cap["output_lane"] != "work_artifact":
        print(
            "mcp_manifest_admission: capability output_lane must be work_artifact "
            f"(got {cap['output_lane']!r})",
            file=sys.stderr,
        )
        return 1

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"mcp_manifest_admission: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(cap["output_lane"])
    if binding is None:
        print("mcp_manifest_admission: missing binding for work_artifact lane", file=sys.stderr)
        return 1

    net = cap["network_access"]
    cred = cap["credential_requirements"]
    inp_rel = _posix_under_repo(root, inp)

    gov = {
        "durable_state_write_attempted": False,
        "canonical_record_touched": bool(any("users_grace_mar" in x for x in blocked_reasons)),
        "requires_human_review": True,
        "requires_gate_review": True,
        "prohibited_action_attempted": admission_blocked,
        "prohibited_action_notes": blocked_reasons[:20],
    }

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts_list = [
        {"path": packet_rel, "kind": "markdown_mcp_manifest_admission"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    decl = manifest["operator"]["intended_use"].strip()
    if len(decl) > 400:
        decl = decl[:399] + "…"

    result_status = "blocked" if admission_blocked else "success"
    summary = "Generated MCP manifest admission packet."
    if admission_blocked:
        summary += " Blocked or manual classification required."

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="mcp_manifest_admission.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[inp_rel],
        network_access=net,
        credential_use=cred,
        resources_read=[inp_rel],
        resources_written=[packet_rel],
        status=result_status,
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
            print(f"mcp_manifest_admission: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"mcp_manifest_admission: receipt invalid: {v}", file=sys.stderr)
        return 1

    md_body = render_markdown(
        manifest,
        matched_id=matched_id,
        rationale=rationale,
        admission_status=admission_status,
        local_blockers=local_blockers,
        lane_blocker=lane_block if lane_block else False,
        risk=risk_finding,
        binding_summary=binding_txt,
        receipt_id=receipt_id,
        receipt_filename=receipt_filename,
        packet_rel=packet_rel,
        capability_id=args.capability_id,
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
