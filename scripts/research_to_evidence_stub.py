#!/usr/bin/env python3
"""
Turn validated structured research JSON into a PRE-CANONICAL Markdown stub plus MCP receipt.

Does not browse the web, run MCP servers, or mutate canonical Record. See
docs/mcp/research-to-evidence-stubs.md.

  python3 scripts/research_to_evidence_stub.py \\
    --input examples/research-evidence-input.example.json \\
    --output artifacts/evidence-stubs/example-topic.md
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

from capture_scaffold_common import slugify, today_iso  # noqa: E402
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

RESEARCH_SCHEMA_PATH = REPO_ROOT / "schemas" / "research-evidence-input.v1.json"
DEFAULT_CAPABILITY_ID = "evidence_stub_operator_template"
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"

CANONICAL_APPROVAL_DENYLIST = (
    "canonical record approval",
    "merged into evidence",
    "approved as canonical record",
    "quick path to self-archive",
    "written to self-archive without companion approval",
)


def _posix_under_repo(repo_root: Path, path: Path) -> str:
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path.as_posix()
    return rel.as_posix()


def validate_extra_rules(doc: dict[str, Any]) -> None:
    """Cross-field checks after JSON Schema."""
    src_ids = {s["source_id"] for s in doc["sources"]}
    for i, cl in enumerate(doc["candidate_claims"]):
        for sid in cl["supporting_sources"]:
            if sid not in src_ids:
                raise ValueError(
                    f"candidate_claims[{i}].supporting_sources references unknown source_id {sid!r}"
                )


def denylist_scan(*chunks: str) -> None:
    blob = "\n".join(chunks).lower()
    for phrase in CANONICAL_APPROVAL_DENYLIST:
        if phrase in blob:
            raise ValueError(
                f"input contains disallowed phrase suggesting canonical approval: {phrase!r}"
            )


def resolve_stub_destination(
    repo_root: Path,
    topic: str,
    output: Path | None,
) -> Path:
    bucket = (repo_root / "artifacts" / "evidence-stubs").resolve()
    bucket.mkdir(parents=True, exist_ok=True)
    if output is None:
        slug = slugify(topic)
        return bucket / f"{today_iso()}-{slug}.md"
    candidate = output if output.is_absolute() else (repo_root / output)
    resolved = candidate.resolve()
    try:
        rel_to_repo = resolved.relative_to(repo_root.resolve())
    except ValueError as e:
        raise ValueError(f"output must be under repository root: {resolved}") from e
    try:
        resolved.relative_to(bucket)
    except ValueError as e:
        raise ValueError(
            f"output must be under {bucket} (got {resolved})"
        ) from e
    rp = rel_to_repo.parts
    if len(rp) >= 2 and rp[0].lower() == "users" and rp[1].lower() == "grace-mar":
        raise ValueError("refusing output path under users/grace-mar/")
    for p in resolved.parts:
        if "self-archive" in p.lower():
            raise ValueError("refusing output path touching self-archive")
        if p.lower() == "self.md":
            raise ValueError("refusing output path touching self.md")
    return resolved


def gather_user_strings(doc: dict[str, Any]) -> list[str]:
    chunks = [doc["topic"], doc["operator_intent"]]
    for s in doc["sources"]:
        chunks.append(s["title"])
        chunks.extend(s.get("claims", []))
        if s.get("notes"):
            chunks.append(s["notes"])
        chunks.extend(s.get("short_excerpts", []))
    for c in doc["candidate_claims"]:
        chunks.append(c["claim"])
    chunks.extend(doc.get("risks_or_uncertainties") or [])
    return chunks


def render_markdown(
    doc: dict[str, Any],
    *,
    receipt_id: str,
    receipt_filename: str,
    stub_repo_rel: str,
    capability_id: str,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fm: dict[str, Any] = {
        "adapter": "research_to_evidence_stub.py",
        "schema": "research-evidence-input.v1",
        "topic": doc["topic"],
        "research_kind": doc["research_kind"],
        "mcp_receipt_id": receipt_id,
        "capability_id": capability_id,
        "generated_at_utc": ts,
        "suggested_gate_action": doc["suggested_gate_action"],
    }
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required") from e

    header = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"

    lines = [
        header,
        "",
        "> **PRE-CANONICAL · WORK ARTIFACT · NOT APPROVED RECORD**",
        "",
        f"MCP receipt JSON (repo-relative path): `artifacts/mcp-receipts/{receipt_filename}` — stub path: `{stub_repo_rel}`",
        "",
        "## Topic",
        "",
        doc["topic"],
        "",
        "## Operator intent",
        "",
        doc["operator_intent"],
        "",
        "## Sources",
        "",
        "| ID | Title | Type | Reliability | Locator |",
        "|----|-------|------|-------------|---------|",
    ]
    for s in doc["sources"]:
        loc = s.get("url") or s.get("local_path") or ""
        lines.append(
            f"| `{s['source_id']}` | {s['title']} | {s['source_type']} | {s['reliability']} | {loc} |"
        )
    lines.extend(["", "### Source detail", ""])
    for s in doc["sources"]:
        lines.append(f"#### {s['source_id']} — {s['title']}")
        lines.append("")
        if s.get("accessed_at_utc"):
            lines.append(f"- Accessed (UTC): {s['accessed_at_utc']}")
        lines.append("- Claims:")
        for cl in s["claims"]:
            lines.append(f"  - {cl}")
        lines.append("- Short excerpts:")
        for ex in s["short_excerpts"]:
            lines.append(f"  - {ex}")
        if s.get("notes"):
            lines.append(f"- Notes: {s['notes']}")
        lines.append("")

    lines.extend(["## Candidate claims", ""])
    for cl in doc["candidate_claims"]:
        lines.append(f"- **Claim:** {cl['claim']}")
        lines.append(f"  - Confidence: `{cl['confidence']}`")
        lines.append(f"  - Record action (operator routing hint): `{cl['record_action']}`")
        lines.append(f"  - Supporting sources: {', '.join(f'`{x}`' for x in cl['supporting_sources'])}")
        lines.append("")

    lines.extend(["## Risks / uncertainties", ""])
    for r in doc.get("risks_or_uncertainties") or []:
        lines.append(f"- {r}")
    if not doc.get("risks_or_uncertainties"):
        lines.append("_None listed._")
    lines.extend(
        [
            "",
            "## Governance",
            "",
            "This file is **not** canonical EVIDENCE and **not** an approved Record merge. Promotion follows the normal companion gate / review path (`recursion-gate.md`, `process_approved_candidates.py`).",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Emit pre-canonical evidence stub Markdown + MCP receipt from research JSON."
    )
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--capability-id",
        default=DEFAULT_CAPABILITY_ID,
        help=f"Must resolve to output_lane evidence_stub (default {DEFAULT_CAPABILITY_ID!r}).",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    inp = args.input if args.input.is_absolute() else (root / args.input)
    inp = inp.resolve()
    if not inp.is_file():
        print(f"research_to_evidence_stub: input not found: {inp}", file=sys.stderr)
        return 1

    raw = json.loads(inp.read_text(encoding="utf-8"))
    try:
        validate_json_schema(raw, RESEARCH_SCHEMA_PATH)
        validate_extra_rules(raw)
        denylist_scan(*gather_user_strings(raw))
        preview_md = render_markdown(
            raw,
            receipt_id="preview",
            receipt_filename="preview.json",
            stub_repo_rel="preview.md",
            capability_id=args.capability_id,
        )
        denylist_scan(preview_md)
    except Exception as e:
        print(f"research_to_evidence_stub: validation failed: {e}", file=sys.stderr)
        return 1

    try:
        dest = resolve_stub_destination(root, raw["topic"], args.output)
    except ValueError as e:
        print(f"research_to_evidence_stub: {e}", file=sys.stderr)
        return 1

    receipt_id = str(uuid.uuid4())
    receipt_filename = f"{receipt_id}.json"
    stub_rel = _posix_under_repo(root, dest)

    md_body = render_markdown(
        raw,
        receipt_id=receipt_id,
        receipt_filename=receipt_filename,
        stub_repo_rel=stub_rel,
        capability_id=args.capability_id,
    )
    denylist_scan(md_body)

    caps_doc = load_yaml(CAPABILITIES_PATH.resolve())
    bind_doc = load_yaml(BINDINGS_PATH.resolve())

    cap = capability_by_id(caps_doc, args.capability_id)
    if cap is None:
        print(f"research_to_evidence_stub: unknown capability {args.capability_id!r}", file=sys.stderr)
        return 1
    if cap["output_lane"] != "evidence_stub":
        print(
            "research_to_evidence_stub: capability output_lane must be evidence_stub "
            f"(got {cap['output_lane']!r})",
            file=sys.stderr,
        )
        return 1

    try:
        lm = bindings_lane_map(bind_doc)
    except ValueError as e:
        print(f"research_to_evidence_stub: bindings error: {e}", file=sys.stderr)
        return 1

    binding = lm.get(cap["output_lane"])
    if binding is None:
        print("research_to_evidence_stub: missing binding for evidence_stub lane", file=sys.stderr)
        return 1

    net = cap["network_access"]
    cred = cap["credential_requirements"]
    input_rel = _posix_under_repo(root, inp)

    gov = {
        "durable_state_write_attempted": False,
        "canonical_record_touched": False,
        "requires_human_review": False,
        "requires_gate_review": True,
        "prohibited_action_attempted": False,
        "prohibited_action_notes": [],
    }

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    artifacts = [
        {"path": stub_rel, "kind": "markdown_evidence_stub"},
        {"path": f"artifacts/mcp-receipts/{receipt_filename}", "kind": "mcp_execution_receipt_json"},
    ]

    decl = raw["operator_intent"]
    if len(decl) > 400:
        decl = decl[:399] + "…"

    receipt = build_receipt(
        cap=cap,
        binding=binding,
        receipt_id=receipt_id,
        created_at=ts,
        actor_kind="script",
        actor_name="research_to_evidence_stub.py",
        session_id=None,
        declared_intent=decl,
        prompt_summary=None,
        operator_supplied_refs=[input_rel],
        network_access=net,
        credential_use=cred,
        resources_read=[input_rel],
        resources_written=[stub_rel],
        status="success",
        summary="Generated pre-canonical evidence stub.",
        artifacts=artifacts,
        governance=gov,
        repo_git_ref=_git_short_hash(root),
        receipt_hash=None,
        parent_receipt_id=None,
    )

    viols, warns = validate_mcp_receipt(receipt, caps_doc, bind_doc, schema_path=RECEIPT_SCHEMA_PATH)
    if warns:
        for w in warns:
            print(f"research_to_evidence_stub: warning: {w}", file=sys.stderr)
    if viols:
        for v in viols:
            print(f"research_to_evidence_stub: receipt invalid: {v}", file=sys.stderr)
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
