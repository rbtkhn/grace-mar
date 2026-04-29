#!/usr/bin/env python3
"""
Turn validated coding-agent patch intake JSON into a governed Markdown packet + MCP receipt.

Does not apply patches, merge PRs, or edit canonical Record files. See
docs/mcp/coding-agent-patch-intake.md.

  python3 scripts/coding_agent_patch_intake.py \\
    --input examples/coding-agent-patch-intake.example.json \\
    --output artifacts/patch-intake/example-packet.md
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
    bindings_lane_map,
    build_receipt,
    capability_by_id,
    load_yaml,
    validate_json_schema,
    validate_mcp_receipt,
)

INTAKE_SCHEMA_PATH = REPO_ROOT / "schemas" / "coding-agent-patch-intake.v1.json"
DEFAULT_CAPABILITY_ID = "coding_agent_patch_intake"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

# Phrases suggesting canonical approval / merge authority (subset aligned with research stub adapter).
CANONICAL_APPROVAL_DENYLIST = (
    "canonical record approval",
    "merged into evidence",
    "approved as canonical record",
    "approved record update",
    "quick path to self-archive",
    "written to self-archive without companion approval",
)

MERGE_AUTHORITY_DENYLIST = (
    "direct merge",
    "merge approved",
    "merged to main",
    "merge to main",
    "merge without review",
    "approved merge",
    "merge into main",
    "ship to production without gate",
)

# Canonical Record paths under grace-mar instance (normalized posix, lower).
RECORD_CRITICAL_PATHS = frozenset(
    {
        "users/grace-mar/self.md",
        "users/grace-mar/self-archive.md",
        "users/grace-mar/recursion-gate.md",
        "users/grace-mar/evidence.md",
    }
)

HIGH_EXACT_PATHS = frozenset(
    {
        "config/authority-map.json",
        "config/mcp-capabilities.yaml",
        "config/mcp-authority-bindings.yaml",
        "scripts/process_approved_candidates.py",
        "scripts/check_record_write_policy.py",
    }
)


def _posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path.as_posix()
    return rel.as_posix()


def normalize_path(path_raw: str) -> str:
    """Repo-relative POSIX path for classification."""
    s = path_raw.strip().replace("\\", "/")
    while s.startswith("./"):
        s = s[2:]
    parts = [p for p in s.split("/") if p]
    return "/".join(parts)


def validate_repo_relative_path(path_raw: str) -> str:
    """Return normalized path or raise ValueError."""
    s = path_raw.strip()
    if not s:
        raise ValueError("empty path")
    if "\\" in s:
        s = s.replace("\\", "/")
    if s.startswith("/"):
        raise ValueError("absolute paths are not allowed")
    if len(s) >= 2 and s[1] == ":":
        raise ValueError("absolute paths are not allowed")
    if ":" in s:
        raise ValueError("paths may not contain ':'")
    norm = normalize_path(s)
    parts = norm.split("/")
    if not parts:
        raise ValueError("empty path")
    if ".." in parts:
        raise ValueError("paths may not contain '..'")
    return norm


def path_exposes_secrets(norm_lower: str, basename: str) -> bool:
    """True if path looks like secret material (reject intake)."""
    parts = norm_lower.split("/")
    if ".env" in parts or norm_lower.endswith("/.env") or basename == ".env":
        return True
    if "secrets" in parts:
        return True
    if basename in ("id_rsa", "id_ed25519", "id_ecdsa"):
        return True
    if basename.endswith(".pem"):
        return True
    return False


def classify_risk(norm: str) -> str:
    """Return CRITICAL | HIGH | MEDIUM | LOW."""
    n = norm.lower()
    parts = n.split("/")
    basename = parts[-1] if parts else ""

    # CRITICAL — Record-shaped + env + secrets dir + key material (overlap with validate)
    if n in RECORD_CRITICAL_PATHS:
        return "CRITICAL"
    if ".env" in parts or n.endswith("/.env") or basename == ".env":
        return "CRITICAL"
    if "secrets" in parts:
        return "CRITICAL"
    if basename in ("id_rsa", "id_ed25519", "id_ecdsa") or basename.endswith(".pem"):
        return "CRITICAL"

    if n in HIGH_EXACT_PATHS or n.startswith("schemas/"):
        return "HIGH"

    if (
        n.startswith("scripts/")
        or n.startswith("docs/mcp/")
        or n.startswith("artifacts/evidence-stubs/")
        or n.startswith("tests/")
        or n.startswith("examples/")
    ):
        return "MEDIUM"

    if (
        n == "readme.md"
        or n.startswith("docs/")
        or n.startswith("artifacts/patch-intake/")
    ):
        return "LOW"

    return "LOW"


def is_record_critical_path(norm: str) -> bool:
    return norm.lower() in RECORD_CRITICAL_PATHS


def has_any_critical_risk(norm_paths: list[str]) -> bool:
    return any(classify_risk(p) == "CRITICAL" for p in norm_paths)


def has_record_critical_path(norm_paths: list[str]) -> bool:
    return any(is_record_critical_path(p) for p in norm_paths)


def gather_strings_for_scan(doc: dict[str, Any]) -> list[str]:
    chunks: list[str] = []
    chunks.append(doc["task"]["title"])
    chunks.append(doc["task"]["operator_intent"])
    chunks.append(doc["task"]["claimed_summary"])
    chunks.append(doc["repo"]["name"])
    chunks.append(doc["repo"]["base_ref"])
    if doc["repo"].get("head_ref"):
        chunks.append(doc["repo"]["head_ref"])
    if doc["repo"].get("commit"):
        chunks.append(doc["repo"]["commit"])
    chunks.append(doc["agent"]["name"])
    for r in doc.get("risks") or []:
        chunks.append(r)
    rr = doc["review_request"]
    chunks.append(rr["desired_action"])
    for cl in doc["tests"]["claimed"]:
        chunks.append(cl)
    for rr_item in doc["tests"]["reported_results"]:
        chunks.append(rr_item)
    if doc["tests"].get("not_run_reason"):
        chunks.append(doc["tests"]["not_run_reason"])
    return chunks


def denylist_scan(chunks: list[str], phrases: tuple[str, ...]) -> None:
    blob = "\n".join(chunks).lower()
    for phrase in phrases:
        if phrase in blob:
            raise ValueError(f"input contains disallowed phrase: {phrase!r}")


def validate_paths_and_classify(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate each path; return rows with path, norm, change_type, surface_hint, risk."""
    rows: list[dict[str, Any]] = []
    for ft in doc["files_touched"]:
        raw = ft["path"]
        norm = validate_repo_relative_path(raw)
        bn = norm.split("/")[-1].lower()
        if path_exposes_secrets(norm.lower(), bn):
            raise ValueError(f"path appears to expose secrets or forbidden env material: {raw!r}")
        risk = classify_risk(norm)
        rows.append(
            {
                "path": raw,
                "norm": norm,
                "change_type": ft["change_type"],
                "surface_hint": ft.get("surface_hint"),
                "risk": risk,
            }
        )
    return rows


def tests_warning_needed(doc: dict[str, Any]) -> bool:
    t = doc["tests"]
    claimed = t.get("claimed") or []
    reported = t.get("reported_results") or []
    if not claimed:
        return False
    if reported:
        return False
    reason = (t.get("not_run_reason") or "").strip()
    return not reason


def render_markdown(
    doc: dict[str, Any],
    *,
    rows: list[dict[str, Any]],
    receipt_id: str,
    receipt_filename: str,
    packet_repo_rel: str,
    capability_id: str,
    intake_status: str,
    tests_warn: bool,
    blocked: bool,
) -> str:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "adapter": "coding_agent_patch_intake.py",
        "schema": "coding-agent-patch-intake.v1",
        "capability_id": capability_id,
        "mcp_receipt_id": receipt_id,
        "generated_at_utc": ts,
        "intake_status": intake_status,
    }
    header = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"

    lines = [
        header,
        "",
        "> **CANDIDATE PROPOSAL · WORK ARTIFACT · NOT MERGED · NOT APPROVED RECORD**",
        "",
        f"MCP receipt JSON (repo-relative): `artifacts/mcp-receipts/{receipt_filename}` — packet path: `{packet_repo_rel}`",
        "",
        "## Agent",
        "",
        f"- **Name:** {doc['agent']['name']}",
        f"- **Kind:** `{doc['agent']['kind']}`",
    ]
    if doc["agent"].get("model"):
        lines.append(f"- **Model:** {doc['agent']['model']}")

    lines.extend(
        [
            "",
            "## Task",
            "",
            f"- **Title:** {doc['task']['title']}",
            "- **Operator intent:**",
            "",
            doc["task"]["operator_intent"],
            "",
            "- **Claimed summary (agent):**",
            "",
            doc["task"]["claimed_summary"],
            "",
            "## Repository",
            "",
            f"- **Name:** {doc['repo']['name']}",
            f"- **Base ref:** `{doc['repo']['base_ref']}`",
        ]
    )
    if doc["repo"].get("head_ref"):
        lines.append(f"- **Head ref:** `{doc['repo']['head_ref']}`")
    if doc["repo"].get("commit"):
        lines.append(f"- **Commit:** `{doc['repo']['commit']}`")

    lines.extend(["", "## Files touched", "", "| Path | Change | Surface hint | Risk |", "|------|--------|----------------|------|"])
    for row in rows:
        raw = row["path"]
        hint = row.get("surface_hint") or ""
        risk = row["risk"]
        ct = row["change_type"]
        lines.append(f"| `{raw}` | `{ct}` | {hint} | **{risk}** |")

    lines.extend(["", "## Tests", "", "**Claimed:**", ""])
    for c in doc["tests"]["claimed"]:
        lines.append(f"- {c}")
    lines.extend(["", "**Reported results:**", ""])
    for r in doc["tests"]["reported_results"]:
        lines.append(f"- {r}")
    if doc["tests"].get("not_run_reason"):
        lines.extend(["", f"**Not run reason:** {doc['tests']['not_run_reason']}"])
    if tests_warn:
        lines.extend(
            [
                "",
                "### Warning",
                "",
                "Tests were claimed but no reported results were supplied and `not_run_reason` is empty. Treat verification as **unknown**.",
            ]
        )

    lines.extend(["", "## Risks (operator / agent)", ""])
    for r in doc.get("risks") or []:
        lines.append(f"- {r}")
    if not doc.get("risks"):
        lines.append("_None listed._")

    rr = doc["review_request"]
    lines.extend(
        [
            "",
            "## Review request",
            "",
            f"- **Desired action:** `{rr['desired_action']}`",
            f"- **Requires human review (input):** `{rr['requires_human_review']}`",
            "",
            "## Governance notes",
            "",
            "This packet is **not** a merge, **not** gate approval, and **not** canonical Record mutation. Promotion follows companion review and [`recursion-gate.md`](../../users/grace-mar/recursion-gate.md) conventions.",
            "",
            "## Recommendation",
            "",
        ]
    )
    if blocked:
        lines.extend(
            [
                "**BLOCKED — DO NOT MERGE AS-IS.** At least one touched path is classified **CRITICAL** (canonical Record surface, secret-like path, or equivalent). Remove or redirect those changes before any staging.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "**Ready for human review** — classify findings above; merge authority stays outside this adapter.",
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def resolve_packet_destination(repo_root: Path, output: Path | None) -> Path:
    bucket = (repo_root / "artifacts" / "patch-intake").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        slug = "patch-intake-packet"
        return bucket / f"{slug}.md"
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
    for p in resolved.parts:
        if "self-archive" in p.lower():
            raise ValueError("refusing output path touching self-archive")
        if p.lower() == "self.md":
            raise ValueError("refusing output path touching self.md")
    return resolved


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Emit governed patch-review Markdown packet + MCP receipt from coding-agent intake JSON."
    )
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--capability-id",
        default=DEFAULT_CAPABILITY_ID,
        help=f"Must resolve to output_lane candidate_proposal (default {DEFAULT_CAPABILITY_ID!r}).",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    inp = args.input if args.input.is_absolute() else (root / args.input)
    inp = inp.resolve()
    if not inp.is_file():
        print(f"coding_agent_patch_intake: input not found: {inp}", file=sys.stderr)
        return 1

    raw: dict[str, Any] = json.loads(inp.read_text(encoding="utf-8"))

    try:
        validate_json_schema(raw, INTAKE_SCHEMA_PATH)
        denylist_scan(gather_strings_for_scan(raw), CANONICAL_APPROVAL_DENYLIST)
        denylist_scan(gather_strings_for_scan(raw), MERGE_AUTHORITY_DENYLIST)
        rows = validate_paths_and_classify(raw)
    except Exception as e:
        print(f"coding_agent_patch_intake: validation failed: {e}", file=sys.stderr)
        return 1

    norms = [r["norm"] for r in rows]
    blocked = has_any_critical_risk(norms)
    record_touch = has_record_critical_path(norms)
    intake_status = "blocked" if blocked else "ready_for_review"

    tests_warn = tests_warning_needed(raw)

    try:
        dest = resolve_packet_destination(root, args.output)
    except ValueError as e:
        print(f"coding_agent_patch_intake: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    packet_rel = _posix_under_repo(root, dest)

    md_body = render_markdown(
        raw,
        rows=rows,
        receipt_id=receipt_id,
        receipt_filename=receipt_filename,
        packet_repo_rel=packet_rel,
        capability_id=args.capability_id,
        intake_status=intake_status,
        tests_warn=tests_warn,
        blocked=blocked,
    )

    caps_doc = load_yaml(CAPABILITIES_PATH.resolve())
    bind_doc = load_yaml(BINDINGS_PATH.resolve())

    cap = capability_by_id(caps_doc, args.capability_id)
    if cap is None:
        print(f"coding_agent_patch_intake: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1
    if cap["output_lane"] != "candidate_proposal":
        print(
            "coding_agent_patch_intake: capability output_lane must be candidate_proposal "
            f"(got {cap['output_lane']!r})",
            file=sys.stderr,
        )
        return 1

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"coding_agent_patch_intake: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(cap["output_lane"])
    if binding is None:
        print(
            "coding_agent_patch_intake: missing binding for candidate_proposal lane",
            file=sys.stderr,
        )
        return 1

    net = cap["network_access"]
    cred = cap["credential_requirements"]
    input_rel = _posix_under_repo(root, inp)

    result_status = "blocked" if blocked else "success"
    summary = "Generated coding-agent patch intake packet."
    if blocked:
        summary = summary + " Blocked: CRITICAL paths listed."

    gov = {
        "durable_state_write_attempted": False,
        "canonical_record_touched": record_touch,
        "requires_human_review": True,
        "requires_gate_review": True,
        "prohibited_action_attempted": False,
        "prohibited_action_notes": [],
    }

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts = [
        {"path": packet_rel, "kind": "markdown_candidate_patch_packet"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    decl = raw["task"]["operator_intent"]
    if len(decl) > 400:
        decl = decl[:399] + "…"

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="coding_agent_patch_intake.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[input_rel],
        network_access=net,
        credential_use=cred,
        resources_read=[input_rel],
        resources_written=[packet_rel],
        status=result_status,
        summary=summary,
        artifacts=artifacts,
        governance=gov,
        repo_git_ref=_git_short_hash(root),
        receipt_hash=None,
        parent_receipt_id=None,
    )

    viols, warns = validate_mcp_receipt(receipt, caps_doc, bind_doc, schema_path=RECEIPT_SCHEMA_PATH)
    if warns:
        for w in warns:
            print(f"coding_agent_patch_intake: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"coding_agent_patch_intake: receipt invalid: {v}", file=sys.stderr)
        return 1

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
