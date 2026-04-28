#!/usr/bin/env python3
"""
Local repo-scoped read-only directory index — metadata-only Markdown packet + MCP receipt.

Does not execute MCP servers, use credentials, invoke network/shell, or read users/grace-mar/.
See docs/mcp/mcp-local-index-adapter.md.

  python3 scripts/mcp_local_index.py \\
    --input examples/mcp-local-index-request.example.json \\
    --output artifacts/mcp-local-index/index-mcp-docs.md
"""

from __future__ import annotations

import argparse
import copy
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
from mcp_local_path_policy import (  # noqa: E402
    basename_blocked,
    posix_under_repo,
    rel_under_allowed_root,
    rel_under_blocked_root,
    resolve_target_under_allowlist,
    validate_allowlist_schema,
)
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

REQUEST_SCHEMA_PATH = REPO_ROOT / "schemas" / "mcp-local-index-request.v1.json"
DEFAULT_ALLOWLIST = REPO_ROOT / "config" / "mcp-local-read-allowlist.yaml"
DEFAULT_POLICY = REPO_ROOT / "config" / "mcp-risk-policy.yaml"
DEFAULT_CAPABILITY_ID = "filesystem_readonly"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

BANNER = (
    "LOCAL READ-ONLY DIRECTORY INDEX · WORK ARTIFACT · NO NETWORK · NO CREDENTIALS · NOT APPROVED INTEGRATION"
)


def load_request(path: Path) -> dict[str, Any]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("request root must be an object")
    return doc


def resolve_packet_destination(repo_root: Path, output: Path | None) -> Path:
    bucket = (repo_root / "artifacts" / "mcp-local-index").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        return bucket / "local-index-packet.md"
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


def line_count_if_allowed(path: Path, max_bytes: int, want: bool) -> str:
    if not want:
        return ""
    try:
        st = path.stat()
    except OSError:
        return ""
    if st.st_size > max_bytes:
        return "_(over max_file_bytes)_"
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    text = raw.decode("utf-8", errors="replace")
    return str(len(text.splitlines()))


def sha256_if_allowed(path: Path, max_bytes: int, want: bool) -> str:
    if not want:
        return ""
    try:
        st = path.stat()
    except OSError:
        return ""
    if st.st_size > max_bytes:
        return "_(over max_file_bytes)_"
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    return hashlib.sha256(raw).hexdigest()


def collect_entries(
    repo_root: Path,
    indexed_abs: Path,
    cfg: dict[str, Any],
    *,
    recursive: bool,
    max_depth: int,
    max_entries: int,
    include_file_hashes: bool,
    include_line_counts: bool,
) -> tuple[list[dict[str, Any]], int]:
    """Returns (rows for markdown table, skipped_count)."""
    rows: list[dict[str, Any]] = []
    skipped = 0
    max_bytes = int(cfg["max_file_bytes"])
    emitted = 0

    def consider_emit(ep: Path) -> None:
        nonlocal emitted, skipped
        if emitted >= max_entries:
            return
        if ep.is_symlink():
            skipped += 1
            return
        try:
            rel_final = posix_under_repo(repo_root, ep.resolve())
        except ValueError:
            skipped += 1
            return
        if rel_under_blocked_root(rel_final, cfg):
            skipped += 1
            return
        if basename_blocked(ep.name, cfg):
            skipped += 1
            return
        if not rel_under_allowed_root(rel_final, cfg):
            skipped += 1
            return
        try:
            is_dir = ep.is_dir()
            is_file = ep.is_file()
        except OSError:
            skipped += 1
            return
        if not is_dir and not is_file:
            skipped += 1
            return

        ext = ep.suffix.lower().lstrip(".") if ep.suffix else ""
        size_b = ""
        lines_cell = ""
        hash_cell = ""
        kind = "directory" if is_dir else "file"
        if is_file:
            try:
                sz = ep.stat().st_size
                size_b = str(sz)
            except OSError:
                size_b = "?"
            lines_cell = line_count_if_allowed(ep, max_bytes, include_line_counts)
            hash_cell = sha256_if_allowed(ep, max_bytes, include_file_hashes)

        rows.append(
            {
                "path": rel_final,
                "kind": kind,
                "ext": ext or "—",
                "size": size_b if is_file else "—",
                "lines": lines_cell if is_file else "—",
                "sha256": hash_cell if is_file else "—",
            }
        )
        emitted += 1

    def walk(cur: Path, remaining_depth: int) -> None:
        nonlocal skipped
        if emitted >= max_entries:
            return
        try:
            children = sorted(cur.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return
        for ep in children:
            if emitted >= max_entries:
                return
            if ep.is_symlink():
                skipped += 1
                continue
            try:
                rel_final = posix_under_repo(repo_root, ep.resolve())
            except ValueError:
                skipped += 1
                continue
            if rel_under_blocked_root(rel_final, cfg):
                skipped += 1
                continue
            if basename_blocked(ep.name, cfg):
                skipped += 1
                continue
            if not rel_under_allowed_root(rel_final, cfg):
                skipped += 1
                continue
            try:
                is_dir = ep.is_dir()
                is_file = ep.is_file()
            except OSError:
                skipped += 1
                continue
            if not is_dir and not is_file:
                skipped += 1
                continue

            consider_emit(ep)
            if is_dir and recursive and remaining_depth > 0:
                walk(ep, remaining_depth - 1)

    if not recursive:
        try:
            children = sorted(indexed_abs.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return rows, skipped
        for ep in children:
            if emitted >= max_entries:
                break
            consider_emit(ep)
        return rows, skipped

    walk(indexed_abs, max_depth)
    return rows, skipped


def render_markdown(
    req: dict[str, Any],
    *,
    indexed_rel: str,
    rows: list[dict[str, Any]],
    skipped: int,
    receipt_id: str,
    packet_rel: str,
    receipt_filename: str,
    risk: dict[str, Any] | None,
    binding_txt: str,
    traversal_note: str,
) -> str:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "kind": "local_directory_index",
        "status": "work_artifact",
        "adapter": "mcp_local_index.py",
        "schema": "mcp-local-index-request.v1",
        "receipt_id": receipt_id,
        "request_id": req["id"],
        "generated_at_utc": ts,
    }
    header = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"

    n_files = sum(1 for r in rows if r["kind"] == "file")
    n_dirs = sum(1 for r in rows if r["kind"] == "directory")

    lines_out = [
        header,
        "",
        f"> {BANNER}",
        "",
        f"MCP receipt JSON (repo-relative): `artifacts/mcp-receipts/{receipt_filename}` — packet path: `{packet_rel}`",
        "",
        "## Declared intent",
        "",
        req["declared_intent"].strip(),
        "",
        "## Indexed directory",
        "",
        f"`{indexed_rel}`",
        "",
        "## Traversal",
        "",
        traversal_note,
        "",
        "## Entries",
        "",
        "| Path | Kind | Ext | Size (bytes) | Lines | SHA256 |",
        "|------|------|-----|--------------|-------|--------|",
    ]
    for r in rows:
        lines_out.append(
            f"| `{r['path']}` | {r['kind']} | {r['ext']} | {r['size']} | {r['lines']} | {r['sha256']} |"
        )
    if not rows:
        lines_out.append("_No entries emitted (may be blocked, empty, or capped)._")

    lines_out.extend(
        [
            "",
            "## Counts",
            "",
            f"- **Files:** {n_files}",
            f"- **Directories:** {n_dirs}",
            f"- **Skipped entries:** {skipped}",
            f"- **Total entries emitted:** {len(rows)}",
            "",
            "## Authority binding (filesystem_readonly)",
            "",
            binding_txt,
            "",
            "## Risk evaluation (registry capability)",
            "",
        ]
    )
    if risk:
        lines_out.extend(
            [
                f"- **Score:** {risk['score']}",
                f"- **Risk level:** `{risk['risk_level']}`",
                f"- **Recommendation:** `{risk['recommendation']}`",
                "",
            ]
        )
    else:
        lines_out.append("_Skipped._\n")

    lines_out.extend(
        [
            "## Governance notes",
            "",
            "- **Network:** none.",
            "- **Credentials:** none.",
            "- **Shell:** not invoked.",
            "- **Canonical Record:** not read or modified (`users/grace-mar/` blocked).",
            "- **File contents:** not emitted (metadata only).",
            "- **Integration approval:** this packet does **not** approve general MCP integration.",
            "",
            "## Receipt note",
            "",
            "Receipt **`access.resources_written`** is empty because registry capability **`filesystem_readonly`** has **`writes: []`**; packet paths appear under **`result.artifacts`** only.",
            "",
        ]
    )
    return "\n".join(lines_out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Local read-only directory index — metadata packet + MCP receipt.")
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
        print(f"mcp_local_index: input request not found: {inp}", file=sys.stderr)
        return 1

    try:
        doc = load_request(inp)
        validate_json_schema(doc, REQUEST_SCHEMA_PATH)
    except Exception as e:
        print(f"mcp_local_index: request validation failed: {e}", file=sys.stderr)
        return 1

    try:
        cfg = load_yaml(args.allowlist.resolve())
        validate_allowlist_schema(cfg)
    except Exception as e:
        print(f"mcp_local_index: allowlist load failed: {e}", file=sys.stderr)
        return 1

    caps_doc = load_yaml(args.capabilities.resolve())
    bind_doc = load_yaml(args.bindings.resolve())
    policy_doc = load_yaml(args.policy.resolve())

    cap = capability_by_id(caps_doc, args.capability_id)
    if cap is None:
        print(f"mcp_local_index: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1

    req = doc["request"]

    try:
        indexed_abs = resolve_target_under_allowlist(root, req["path"], cfg, kind="dir")
    except ValueError as e:
        print(f"mcp_local_index: path policy: {e}", file=sys.stderr)
        return 1

    recursive = bool(req["recursive"])
    max_depth = int(req["max_depth"])
    max_entries = int(req["max_entries"])
    include_hashes = bool(req["include_file_hashes"])
    include_lines = bool(req["include_line_counts"])

    rows, skipped = collect_entries(
        root,
        indexed_abs,
        cfg,
        recursive=recursive,
        max_depth=max_depth,
        max_entries=max_entries,
        include_file_hashes=include_hashes,
        include_line_counts=include_lines,
    )

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
        print(f"mcp_local_index: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    packet_rel = posix_under_repo(root, dest)
    indexed_rel = posix_under_repo(root, indexed_abs)
    inp_rel = posix_under_repo(root, inp)

    caps_doc_full = load_yaml(CAPABILITIES_PATH.resolve())

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"mcp_local_index: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(cap["output_lane"])
    if binding is None:
        print(f"mcp_local_index: missing binding for output_lane {cap['output_lane']!r}", file=sys.stderr)
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
        "prohibited_action_notes": ["local_directory_index_adapter_success"],
    }

    summary = "Local read-only directory index emitted metadata-only packet."
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts_list = [
        {"path": packet_rel, "kind": "markdown_mcp_local_index"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="mcp_local_index.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[inp_rel],
        network_access=net_a,
        credential_use=cred_a,
        resources_read=[inp_rel, indexed_rel],
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
            print(f"mcp_local_index: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"mcp_local_index: receipt invalid: {v}", file=sys.stderr)
        return 1

    if recursive:
        trav = (
            f"- **recursive:** true\n"
            f"- **max_depth:** {max_depth} (levels below indexed directory)\n"
            f"- **max_entries:** {max_entries}"
        )
    else:
        trav = (
            f"- **recursive:** false (direct children only; **max_depth** not applied)\n"
            f"- **max_entries:** {max_entries}"
        )

    md_body = render_markdown(
        req,
        indexed_rel=indexed_rel,
        rows=rows,
        skipped=skipped,
        receipt_id=receipt_id,
        packet_rel=packet_rel,
        receipt_filename=receipt_filename,
        risk=risk_finding,
        binding_txt=binding_txt,
        traversal_note=trav,
    )

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(md_body, encoding="utf-8")

    DEFAULT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = (DEFAULT_RECEIPT_DIR / receipt_filename).resolve()
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(posix_under_repo(root, dest))
    print(posix_under_repo(root, receipt_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
