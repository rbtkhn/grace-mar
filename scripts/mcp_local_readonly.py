#!/usr/bin/env python3
"""
Local repo-scoped read-only adapter — bounded UTF-8 file read + Markdown packet + MCP receipt.

Does not execute MCP servers, use credentials, invoke network/shell, or read users/grace-mar/.
See docs/mcp/mcp-local-readonly-adapter.md.

  python3 scripts/mcp_local_readonly.py \\
    --input examples/mcp-local-read-request.example.json \\
    --output artifacts/mcp-local-read/read-governed-mcp-layer.md
"""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
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

REQUEST_SCHEMA_PATH = REPO_ROOT / "schemas" / "mcp-local-read-request.v1.json"
DEFAULT_ALLOWLIST = REPO_ROOT / "config" / "mcp-local-read-allowlist.yaml"
DEFAULT_POLICY = REPO_ROOT / "config" / "mcp-risk-policy.yaml"
DEFAULT_CAPABILITY_ID = "filesystem_readonly"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

BANNER = (
    "LOCAL READ-ONLY MCP-SHAPED RUN · WORK ARTIFACT · NO NETWORK · NO CREDENTIALS · NOT APPROVED INTEGRATION"
)


def _posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_request(path: Path) -> dict[str, Any]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("request root must be an object")
    return doc


def apply_defaults(doc: dict[str, Any]) -> None:
    r = doc["request"]
    if "max_excerpt_chars" not in r:
        r["max_excerpt_chars"] = 2000


def validate_allowlist_schema(cfg: dict[str, Any]) -> None:
    for key in ("allowed_roots", "blocked_roots", "blocked_files", "blocked_name_patterns"):
        if key not in cfg:
            raise ValueError(f"allowlist missing {key!r}")
    if "max_file_bytes" not in cfg:
        raise ValueError("allowlist missing max_file_bytes")


def _norm_segments(rel_posix: str) -> list[str]:
    parts = [p for p in rel_posix.replace("\\", "/").split("/") if p]
    if ".." in parts:
        raise ValueError("path must not contain .. segments")
    return parts


def validate_and_resolve_target(repo_root: Path, path_str: str, cfg: dict[str, Any]) -> Path:
    raw = path_str.strip()
    if not raw:
        raise ValueError("path cannot be empty")

    if len(raw) >= 2 and raw[1] == ":":
        raise ValueError("absolute paths not allowed")
    if raw.startswith("/"):
        raise ValueError("absolute paths not allowed")

    norm = raw.replace("\\", "/").strip("/")
    parts = _norm_segments(norm)
    rel_join = "/".join(parts) if parts else ""

    low_rel = rel_join.lower()
    if low_rel.startswith("users/grace-mar/") or low_rel == "users/grace-mar":
        raise ValueError("path cannot reference users/grace-mar")

    candidate = (repo_root / Path(*parts)) if parts else repo_root
    try:
        resolved = candidate.resolve()
    except OSError as e:
        raise ValueError(f"cannot resolve path: {e}") from e

    repo_abs = repo_root.resolve()
    try:
        resolved.relative_to(repo_abs)
    except ValueError as e:
        raise ValueError(f"path escapes repository root: {resolved}") from e

    rel_final = _posix_under_repo(repo_root, resolved)

    blocked_roots = [str(x).replace("\\", "/").strip("/") for x in cfg["blocked_roots"]]
    for br in blocked_roots:
        br_prefix = br + "/" if br else ""
        if rel_final == br or (br_prefix and rel_final.startswith(br_prefix)):
            raise ValueError(f"path is under blocked root {br!r}")

    allowed = [str(x).replace("\\", "/") for x in cfg["allowed_roots"]]
    ok = False
    for root in allowed:
        prefix = root if root.endswith("/") else root + "/"
        if rel_final == root.rstrip("/") or rel_final.startswith(prefix):
            ok = True
            break
    if not ok:
        raise ValueError(f"path not under any allowed_roots (got {rel_final!r})")

    base = resolved.name
    blocked_files = {str(x).lower() for x in cfg["blocked_files"]}
    if base.lower() in blocked_files:
        raise ValueError(f"basename blocked by allowlist: {base!r}")

    for pat in cfg["blocked_name_patterns"]:
        if fnmatch.fnmatch(base.lower(), pat.lower()):
            raise ValueError(f"basename matches blocked_name_patterns: {pat!r}")

    if not resolved.is_file():
        raise ValueError(f"not a regular file: {resolved}")

    return resolved


def read_file_bounded(path: Path, max_bytes: int) -> tuple[bytes, int]:
    st = path.stat()
    if st.st_size > max_bytes:
        raise ValueError(f"file size {st.st_size} exceeds max_file_bytes ({max_bytes})")
    data = path.read_bytes()
    if len(data) > max_bytes:
        raise ValueError(f"read size exceeds max_file_bytes ({max_bytes})")
    return data, st.st_size


def resolve_packet_destination(repo_root: Path, output: Path | None) -> Path:
    bucket = (repo_root / "artifacts" / "mcp-local-read").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        return bucket / "local-read-packet.md"
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
    req: dict[str, Any],
    *,
    target_rel: str,
    byte_size: int,
    line_count: int,
    sha256_hex: str,
    excerpt: str | None,
    excerpt_requested: bool,
    receipt_id: str,
    packet_rel: str,
    receipt_filename: str,
    risk: dict[str, Any] | None,
    binding_txt: str,
) -> str:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "adapter": "mcp_local_readonly.py",
        "schema": "mcp-local-read-request.v1",
        "receipt_id": receipt_id,
        "request_id": req["id"],
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
        "## Request",
        "",
        f"- **id:** `{req['id']}`",
        f"- **declared_intent:** {req['declared_intent']}",
        f"- **path read:** `{target_rel}`",
        "",
        "## File metrics",
        "",
        f"- **Byte size:** {byte_size}",
        f"- **Line count:** {line_count}",
        f"- **SHA256:** `{sha256_hex}`",
        "",
    ]
    if excerpt_requested:
        lines.extend(["## Excerpt", "", "```text", excerpt or "", "```", ""])
    else:
        lines.extend(["## Excerpt", "", "_Not requested (`include_excerpt: false`)._", ""])

    lines.extend(
        [
            "## Authority binding (filesystem_readonly)",
            "",
            binding_txt,
            "",
            "## Risk evaluation (registry capability)",
            "",
        ]
    )
    if risk:
        lines.extend(
            [
                f"- **Score:** {risk['score']}",
                f"- **Risk level:** `{risk['risk_level']}`",
                f"- **Recommendation:** `{risk['recommendation']}`",
                "",
            ]
        )
    else:
        lines.append("_Skipped._\n")

    lines.extend(
        [
            "## Governance notes",
            "",
            "- **Network:** none (local read adapter only).",
            "- **Credentials:** none.",
            "- **Shell:** not invoked.",
            "- **Canonical Record:** not read and not modified (`users/grace-mar/` blocked by allowlist).",
            "- **Integration approval:** this packet does **not** approve general MCP integration.",
            "",
            "## Receipt note",
            "",
            "Receipt **`access.resources_written`** is empty because registry capability **`filesystem_readonly`** has **`writes: []`**; packet paths appear under **`result.artifacts`** only.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Local read-only MCP-shaped adapter — bounded UTF-8 read + packet + receipt.")
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--allowlist", type=Path, default=DEFAULT_ALLOWLIST)
    ap.add_argument("--capabilities", type=Path, default=CAPABILITIES_PATH)
    ap.add_argument("--bindings", type=Path, default=BINDINGS_PATH)
    ap.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    ap.add_argument(
        "--capability-id",
        default=DEFAULT_CAPABILITY_ID,
        help=f"Receipt capability registry id (default {DEFAULT_CAPABILITY_ID!r}).",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    inp = args.input if args.input.is_absolute() else (root / args.input)
    inp = inp.resolve()
    if not inp.is_file():
        print(f"mcp_local_readonly: input request not found: {inp}", file=sys.stderr)
        return 1

    try:
        doc = load_request(inp)
        apply_defaults(doc)
        validate_json_schema(doc, REQUEST_SCHEMA_PATH)
    except Exception as e:
        print(f"mcp_local_readonly: request validation failed: {e}", file=sys.stderr)
        return 1

    try:
        cfg = load_yaml(args.allowlist.resolve())
        validate_allowlist_schema(cfg)
    except Exception as e:
        print(f"mcp_local_readonly: allowlist load failed: {e}", file=sys.stderr)
        return 1

    caps_doc = load_yaml(args.capabilities.resolve())
    bind_doc = load_yaml(args.bindings.resolve())
    policy_doc = load_yaml(args.policy.resolve())

    cap = capability_by_id(caps_doc, args.capability_id)
    if cap is None:
        print(f"mcp_local_readonly: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1

    req = doc["request"]

    try:
        target_abs = validate_and_resolve_target(root, req["path"], cfg)
    except ValueError as e:
        print(f"mcp_local_readonly: path policy: {e}", file=sys.stderr)
        return 1

    max_bytes = int(cfg["max_file_bytes"])
    try:
        raw, byte_size = read_file_bounded(target_abs, max_bytes)
    except ValueError as e:
        print(f"mcp_local_readonly: read: {e}", file=sys.stderr)
        return 1

    sha256_hex = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    line_count = len(text.splitlines())

    max_excerpt = int(req["max_excerpt_chars"])
    excerpt_requested = bool(req["include_excerpt"])
    excerpt: str | None = None
    if excerpt_requested:
        excerpt = text[: max_excerpt if max_excerpt > 0 else 0]

    risk_finding: dict[str, Any] | None = evaluate_capability(copy.deepcopy(cap), policy_doc)

    binding_txt = "_Binding unresolved._"
    try:
        lm = bindings_lane_map(bind_doc)
        lane = cap["output_lane"]
        b = lm.get(lane)
        if b:
            binding_txt = (
                f"- **output_lane:** `{lane}`\n"
                f"- **authority_surface:** `{b['authority_surface']}`\n"
                f"- **authority_class:** `{b['authority_class']}`"
            )
    except ValueError as e:
        binding_txt = f"(bindings parse error: {e})"

    try:
        dest = resolve_packet_destination(root, args.output)
    except ValueError as e:
        print(f"mcp_local_readonly: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    packet_rel = _posix_under_repo(root, dest)
    target_rel = _posix_under_repo(root, target_abs)
    inp_rel = _posix_under_repo(root, inp)

    caps_doc_full = load_yaml(CAPABILITIES_PATH.resolve())

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"mcp_local_readonly: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(cap["output_lane"])
    if binding is None:
        print(f"mcp_local_readonly: missing binding for output_lane {cap['output_lane']!r}", file=sys.stderr)
        return 1

    decl = req["declared_intent"].strip()
    if len(decl) > 400:
        decl = decl[:399] + "…"

    net_a = cap["network_access"]
    cred_a = cap["credential_requirements"]

    gov = {
        "durable_state_write_attempted": False,
        "canonical_record_touched": False,
        "requires_human_review": True,
        "requires_gate_review": True,
        "prohibited_action_attempted": False,
        "prohibited_action_notes": ["local_read_only_adapter_success"],
    }

    summary = "Local read-only MCP-shaped adapter completed bounded UTF-8 read; packet + receipt emitted."
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts_list = [
        {"path": packet_rel, "kind": "markdown_mcp_local_readonly"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="mcp_local_readonly.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[inp_rel],
        network_access=net_a,
        credential_use=cred_a,
        resources_read=[inp_rel, target_rel],
        resources_written=[],
        status="success",
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
            print(f"mcp_local_readonly: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"mcp_local_readonly: receipt invalid: {v}", file=sys.stderr)
        return 1

    md_body = render_markdown(
        req,
        target_rel=target_rel,
        byte_size=byte_size,
        line_count=line_count,
        sha256_hex=sha256_hex,
        excerpt=excerpt,
        excerpt_requested=excerpt_requested,
        receipt_id=receipt_id,
        packet_rel=packet_rel,
        receipt_filename=receipt_filename,
        risk=risk_finding,
        binding_txt=binding_txt,
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
