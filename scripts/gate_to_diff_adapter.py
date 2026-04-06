#!/usr/bin/env python3
"""
Convert recursion-gate.md pending YAML blocks into identity-diff v1 JSON objects.

Instance-specific (grace-mar): bridges the canonical gate staging surface
to the template-portable Record Diff Queue renderer.

Usage:
  python3 scripts/gate_to_diff_adapter.py -u grace-mar
  python3 scripts/gate_to_diff_adapter.py -u grace-mar --output-dir users/grace-mar/review-queue/diffs/
  python3 scripts/gate_to_diff_adapter.py -u grace-mar --stdout
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gate_block_parser import iter_candidate_yaml_blocks, split_gate_sections  # noqa: E402
from repo_io import profile_dir, read_path  # noqa: E402

_CATEGORY_MAP = {
    "knowledge": "identity",
    "curiosity": "curiosity",
    "personality": "expression",
}


def _extract_scalar(yaml_body: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    elif val.startswith("'") and val.endswith("'"):
        val = val[1:-1]
    return val or None


def _extract_block(yaml_body: str, key: str) -> str | None:
    """Extract a multi-line block value (pipe-style or quoted scalar)."""
    m = re.search(rf"^{re.escape(key)}:\s*\|?\s*\n((?:[ \t]+.+\n?)+)", yaml_body, re.MULTILINE)
    if m:
        lines = m.group(1).splitlines()
        stripped = [ln.strip() for ln in lines if ln.strip()]
        return " ".join(stripped) if stripped else None
    return _extract_scalar(yaml_body, key)


def _infer_before_from_self(self_text: str, profile_target: str | None, summary: str | None) -> dict:
    """Best-effort inference of prior state from current SELF."""
    if not profile_target:
        return {"state": "(not yet in Record)"}
    section = profile_target.strip()
    if "IX-A" in section:
        return {"section": "IX-A. KNOWLEDGE", "state": "(no prior entry for this topic)"}
    if "IX-B" in section:
        return {"section": "IX-B. CURIOSITY", "state": "(no prior entry for this topic)"}
    if "IX-C" in section:
        return {"section": "IX-C. PERSONALITY", "state": "(no prior entry for this topic)"}
    return {"section": section, "state": "(no prior entry)"}


def candidate_to_diff(
    candidate_id: str,
    title: str,
    yaml_body: str,
    self_text: str,
) -> dict:
    """Convert a single gate candidate YAML block to an identity-diff v1 JSON object."""
    status = _extract_scalar(yaml_body, "status") or "pending"
    if status != "pending":
        return {}

    mind_cat = (_extract_scalar(yaml_body, "mind_category") or "").lower()
    category = _CATEGORY_MAP.get(mind_cat, "identity")
    profile_target = _extract_scalar(yaml_body, "profile_target")
    summary = _extract_scalar(yaml_body, "summary")
    suggested_entry = _extract_block(yaml_body, "suggested_entry")
    channel_key = _extract_scalar(yaml_body, "channel_key")
    timestamp = _extract_scalar(yaml_body, "timestamp")
    conflicts = _extract_scalar(yaml_body, "conflicts_detected")
    priority = _extract_scalar(yaml_body, "priority_score")

    before = _infer_before_from_self(self_text, profile_target, summary)
    after: dict = {}
    if suggested_entry:
        after["entry"] = suggested_entry
    if profile_target:
        after["target"] = profile_target
    if not after:
        after["summary"] = summary or title or candidate_id

    evidence_refs: list[str] = []
    source = _extract_scalar(yaml_body, "source")
    if source:
        evidence_refs.append(source)
    if channel_key:
        evidence_refs.append(channel_key)
    if not evidence_refs:
        evidence_refs.append(candidate_id)

    conflict_note = ""
    if conflicts and conflicts.lower() not in ("none", "no", "false", "n/a"):
        conflict_note = conflicts

    recommended_action = None
    ready = _extract_scalar(yaml_body, "ready_for_quick_merge")
    if ready and ready.lower() in ("true", "yes"):
        recommended_action = "accept"

    why_it_matters = None
    suggested_followup = _extract_block(yaml_body, "suggested_followup")
    if suggested_followup:
        why_it_matters = suggested_followup

    diff: dict = {
        "schemaVersion": "1.0.0",
        "diffId": f"diff-gate-{candidate_id}",
        "userSlug": "grace-mar",
        "category": category,
        "before": before,
        "after": after,
        "changeSummary": summary or title or f"Gate candidate {candidate_id}",
        "evidenceRefs": evidence_refs,
    }

    confidence_before = 0.5
    if priority:
        try:
            p = int(priority)
            confidence_after = min(0.5 + p * 0.1, 1.0)
        except ValueError:
            confidence_after = 0.6
    else:
        confidence_after = 0.6
    diff["confidenceDelta"] = {"before": confidence_before, "after": confidence_after}

    if conflict_note:
        diff["conflictNote"] = conflict_note
    if recommended_action:
        diff["recommendedAction"] = recommended_action
    if why_it_matters:
        diff["whyItMatters"] = why_it_matters

    return diff


def convert_gate(user_id: str) -> list[dict]:
    """Parse recursion-gate.md and return list of identity-diff v1 JSON objects for pending candidates."""
    gate_path = profile_dir(user_id) / "recursion-gate.md"
    self_path = profile_dir(user_id) / "self.md"
    gate_text = read_path(gate_path)
    self_text = read_path(self_path)

    active, _ = split_gate_sections(gate_text)
    diffs: list[dict] = []
    for candidate_id, title, yaml_body in iter_candidate_yaml_blocks(active):
        status = _extract_scalar(yaml_body, "status")
        if status and status != "pending":
            continue
        d = candidate_to_diff(candidate_id, title, yaml_body, self_text)
        if d:
            diffs.append(d)
    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert recursion-gate pending candidates to identity-diff v1 JSON."
    )
    parser.add_argument("-u", "--user", default="grace-mar", help="User slug (default: grace-mar)")
    parser.add_argument("--output-dir", help="Write individual JSON files to this directory")
    parser.add_argument("--stdout", action="store_true", help="Print JSON array to stdout (default if no --output-dir)")
    args = parser.parse_args()

    diffs = convert_gate(args.user)
    if not diffs:
        print("No pending gate candidates found.", file=sys.stderr)
        return 0

    if args.output_dir:
        out_dir = Path(args.output_dir) if Path(args.output_dir).is_absolute() else ROOT / args.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        for diff in diffs:
            fname = f"{diff['diffId']}.json"
            path = out_dir / fname
            path.write_text(json.dumps(diff, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(diffs)} diff file(s) to {out_dir}", file=sys.stderr)
    else:
        print(json.dumps(diffs, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
