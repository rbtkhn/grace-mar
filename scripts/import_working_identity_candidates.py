#!/usr/bin/env python3
"""
Import external working-identity candidates into the recursion-gate staging queue.

Reads a JSON file produced by the external-AI extraction prompt pack and converts
each item into a normalized CANDIDATE block in recursion-gate.md. All imported
candidates are non-canonical until reviewed and approved through the gated pipeline.

Usage:

  python3 scripts/import_working_identity_candidates.py -u grace-mar -f extract.json
  python3 scripts/import_working_identity_candidates.py -u grace-mar -f extract.json --source-tool ChatGPT
  python3 scripts/import_working_identity_candidates.py -u grace-mar -f extract.json --dry-run

Outputs:
  - CANDIDATE blocks staged in users/<id>/recursion-gate.md
  - Human-review digest in artifacts/portable-record/import-digest-YYYY-MM-DD.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stage_gate_candidate import (  # noqa: E402
    insert_before_processed,
    next_candidate_id,
)

DEFAULT_USER = "grace-mar"

LAYER_TO_SURFACE: dict[str, str] = {
    "domain_encoding": "SELF-LIBRARY",
    "workflow_calibration": "SKILLS",
    "behavioral_calibration": "SELF",
    "artifact_rationale": "EVIDENCE",
}

LAYER_SECTIONS = list(LAYER_TO_SURFACE.keys())


def normalize_item(
    raw: str | dict[str, Any],
    *,
    layer_type: str,
    source_tool: str,
) -> dict[str, Any]:
    """Normalize a single extraction item (string or object) into a candidate dict."""
    if isinstance(raw, str):
        claim = raw.strip()
        confidence = "medium"
        durability = "recurring"
        examples: list[str] = []
    else:
        claim = str(raw.get("claim", "")).strip()
        confidence = raw.get("confidence", "medium") or "medium"
        durability = raw.get("durability", "recurring") or "recurring"
        examples = raw.get("examples", []) or []
        if isinstance(examples, str):
            examples = [examples]

    if confidence not in ("high", "medium", "low"):
        confidence = "medium"
    if durability not in ("stable", "recurring", "ephemeral"):
        durability = "recurring"

    if not claim:
        return {}

    return {
        "source_type": "external_ai_extract",
        "layer_type": layer_type,
        "claim": claim,
        "confidence": confidence,
        "durability_class": durability,
        "sensitivity_class": "review_required",
        "portability_class": "cross_tool",
        "proposed_target_surface": LAYER_TO_SURFACE[layer_type],
        "source_tool": source_tool,
        "supporting_examples": [str(e) for e in examples if str(e).strip()],
        "review_status": "pending",
    }


def extract_candidates(
    data: dict[str, Any],
    *,
    source_tool: str,
) -> list[dict[str, Any]]:
    """Extract and normalize all candidates from the extraction JSON."""
    candidates: list[dict[str, Any]] = []

    for layer in LAYER_SECTIONS:
        items = data.get(layer, [])
        if not isinstance(items, list):
            continue
        for raw in items:
            c = normalize_item(raw, layer_type=layer, source_tool=source_tool)
            if c:
                candidates.append(c)

    flags = data.get("sensitivity_flags", [])
    if isinstance(flags, list):
        for raw in flags:
            c = normalize_item(raw, layer_type="behavioral_calibration", source_tool=source_tool)
            if c:
                c["sensitivity_class"] = "review_required"
                candidates.append(c)

    return candidates


def _yaml_escape(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _slug(text: str, max_len: int = 50) -> str:
    import re
    one = " ".join(text.splitlines()[:1]).strip() or "imported candidate"
    one = re.sub(r"\s+", " ", one)
    if len(one) > max_len:
        one = one[: max_len - 1].rstrip() + "…"
    return one


def build_wi_block(
    candidate_id: str,
    candidate: dict[str, Any],
    timestamp: str,
) -> str:
    """Build a YAML candidate block for recursion-gate.md."""
    title = _slug(candidate["claim"])
    summary = candidate["claim"][:200]
    examples = candidate.get("supporting_examples", [])

    lines = [
        f"### {candidate_id} ({title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        "channel_key: operator:portable-working-identity",
        "territory: portable-working-identity",
        "proposal_class: PORTABLE_WORKING_IDENTITY",
        "source: operator — scripts/import_working_identity_candidates.py",
        f"source_type: {candidate['source_type']}",
        f"source_tool: {_yaml_escape(candidate.get('source_tool', 'unknown'))}",
        f"layer_type: {candidate['layer_type']}",
        f"mind_category: {_layer_to_mind(candidate['layer_type'])}",
        "signal_type: external_ai_extract",
        "priority_score: 3",
        f"summary: {_yaml_escape(summary)}",
        f"claim: {_yaml_escape(candidate['claim'])}",
        f"confidence: {candidate['confidence']}",
        f"durability_class: {candidate['durability_class']}",
        f"sensitivity_class: {candidate['sensitivity_class']}",
        f"portability_class: {candidate['portability_class']}",
        f"proposed_target_surface: {candidate['proposed_target_surface']}",
        f"review_status: {candidate['review_status']}",
    ]

    if examples:
        lines.append("supporting_examples:")
        for ex in examples[:5]:
            lines.append(f"  - {_yaml_escape(str(ex)[:300])}")

    lines.extend([
        f"profile_target: {candidate['proposed_target_surface']}",
        f"suggested_entry: {_yaml_escape(candidate['claim'][:300])}",
        "```",
        "",
    ])
    return "\n".join(lines)


def _layer_to_mind(layer: str) -> str:
    return {
        "domain_encoding": "knowledge",
        "workflow_calibration": "knowledge",
        "behavioral_calibration": "personality",
        "artifact_rationale": "knowledge",
    }.get(layer, "knowledge")


def build_digest(
    candidates: list[dict[str, Any]],
    candidate_ids: list[str],
    *,
    source_tool: str,
    timestamp: str,
) -> str:
    """Build a human-review markdown digest."""
    lines = [
        "# Working-identity import digest",
        "",
        f"Generated: {timestamp}",
        f"Source tool: {source_tool}",
        f"Candidates staged: {len(candidates)}",
        "",
        "---",
        "",
        "| ID | Layer | Target | Sensitivity | Claim |",
        "|----|-------|--------|-------------|-------|",
    ]
    for cid, c in zip(candidate_ids, candidates):
        claim = c["claim"][:80]
        lines.append(
            f"| {cid} | {c['layer_type']} | {c['proposed_target_surface']} "
            f"| {c['sensitivity_class']} | {claim} |"
        )
    lines.extend([
        "",
        "---",
        "",
        "All candidates are **non-canonical** until reviewed and approved through the gated pipeline.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Import external working-identity candidates into recursion-gate.md"
    )
    ap.add_argument(
        "-u", "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER,
    )
    ap.add_argument(
        "-f", "--file", type=Path, required=True,
        help="Path to the extraction JSON file",
    )
    ap.add_argument(
        "--source-tool", default="unknown",
        help="Name of the AI system that produced the extract (e.g. ChatGPT, Claude)",
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="Print candidate blocks to stdout without staging",
    )
    args = ap.parse_args()

    input_path = args.file
    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    candidates = extract_candidates(data, source_tool=args.source_tool)
    if not candidates:
        print("No candidates found in input file.")
        return 0

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    gate_path = REPO_ROOT / "users" / args.user / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"Error: recursion-gate.md not found: {gate_path}", file=sys.stderr)
        return 1

    gate_content = gate_path.read_text(encoding="utf-8")
    candidate_ids: list[str] = []
    blocks: list[str] = []

    for c in candidates:
        cid = next_candidate_id(gate_content + "\n".join(blocks))
        candidate_ids.append(cid)
        block = build_wi_block(cid, c, timestamp)
        blocks.append(block)

    if args.dry_run:
        print(f"Dry run: {len(candidates)} candidate(s) would be staged.\n")
        for block in blocks:
            print(block)
        return 0

    combined_block = "\n".join(blocks)
    gate_content = insert_before_processed(gate_content, combined_block)
    gate_path.write_text(gate_content, encoding="utf-8")
    print(f"Staged {len(candidates)} candidate(s) in {gate_path.relative_to(REPO_ROOT)}")

    digest_dir = REPO_ROOT / "artifacts" / "portable-record"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest_path = digest_dir / f"import-digest-{date_str}.md"
    digest = build_digest(candidates, candidate_ids, source_tool=args.source_tool, timestamp=timestamp)
    digest_path.write_text(digest, encoding="utf-8")
    print(f"Digest written to {digest_path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
