#!/usr/bin/env python3
"""Materialize a sandboxed gate-ready candidate without touching live files."""

from __future__ import annotations

import difflib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SELF_PROPOSALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SELF_PROPOSALS_DIR.parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from stage_gate_candidate import insert_before_processed, next_candidate_id


def _yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def _render_literal(value: str, indent: str = "    ") -> list[str]:
    if not value.strip():
        return [f"{indent}(empty)"]
    return [indent + line for line in value.splitlines()]


def _render_source_exchange(exchange: dict[str, str]) -> list[str]:
    lines = ["source_exchange:"]
    for key, value in exchange.items():
        lines.append(f"  {key}: |")
        lines.extend(_render_literal(value))
    return lines


def normalize_candidate_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    candidate = dict(payload["candidate_bundle"])
    territory = candidate.get("territory")
    default_channel = "operator:auto-research:self-proposals"
    if territory == "work-politics":
        default_channel = "operator:auto-research:work-politics"
    candidate.setdefault("channel_key", default_channel)
    candidate.setdefault("proposal_class", "SIMULATION_RESULT")
    candidate.setdefault("new_vs_record", "Auto-research proposal draft; review against current Record before promotion.")
    candidate.setdefault("suggested_followup", "")
    return candidate


def render_candidate_block(
    payload: dict[str, Any],
    *,
    candidate_id: str,
    timestamp: str | None = None,
    status: str = "pending",
    auto_research_metadata: dict[str, Any] | None = None,
) -> str:
    candidate = normalize_candidate_bundle(payload)
    ts = timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"### {candidate_id} ({candidate['title']})",
        "",
        "```yaml",
        f"status: {status}",
        f"timestamp: {ts}",
        f"channel_key: {candidate['channel_key']}",
    ]
    if candidate.get("territory"):
        lines.append(f"territory: {candidate['territory']}")
    if candidate.get("proposal_class"):
        lines.append(f"proposal_class: {candidate['proposal_class']}")
    lines.extend(
        [
            f"source: {candidate['source']}",
            f"new_vs_record: {_yaml_quote(candidate['new_vs_record'])}",
        ]
    )
    lines.extend(_render_source_exchange(candidate["source_exchange"]))
    lines.extend(
        [
            f"mind_category: {candidate['mind_category']}",
            f"signal_type: {candidate['signal_type']}",
            f"priority_score: {candidate['priority_score']}",
            f"summary: {_yaml_quote(candidate['summary'])}",
            f"profile_target: {candidate['profile_target']}",
            f"suggested_entry: {_yaml_quote(candidate['suggested_entry'])}",
            f"prompt_section: {candidate['prompt_section']}",
            f"prompt_addition: {_yaml_quote(candidate['prompt_addition'])}",
        ]
    )
    if candidate.get("suggested_followup"):
        lines.append(f"suggested_followup: {_yaml_quote(candidate['suggested_followup'])}")
    auto_meta = {
        "lane": "self-proposals",
        "hypothesis": payload["hypothesis"],
        "expected_delta": payload["expected_delta"],
    }
    if payload.get("grounding_mode"):
        auto_meta["grounding_mode"] = payload["grounding_mode"]
    if auto_research_metadata:
        auto_meta.update(auto_research_metadata)
    lines.extend(
        [
            "auto_research:",
        ]
    )
    for key, value in auto_meta.items():
        if isinstance(value, (int, float)):
            lines.append(f"  {key}: {value}")
        else:
            lines.append(f"  {key}: {_yaml_quote(str(value))}")
    lines.extend(["```", ""])
    return "\n".join(lines)


def materialize_sandbox(
    sandbox_root: Path,
    payload: dict[str, Any],
    *,
    user_id: str = "grace-mar",
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    users_src = repo_root / "users"
    sandbox_users_dir = sandbox_root / "users"
    sandbox_user_dir = sandbox_users_dir / user_id
    shutil.copytree(users_src / user_id, sandbox_user_dir)

    gate_path = sandbox_user_dir / "recursion-gate.md"
    original_gate = gate_path.read_text(encoding="utf-8")
    candidate_id = next_candidate_id(original_gate)
    candidate_block = render_candidate_block(payload, candidate_id=candidate_id)
    updated_gate = insert_before_processed(original_gate, candidate_block)
    gate_path.write_text(updated_gate, encoding="utf-8")

    diff_lines = list(
        difflib.unified_diff(
            original_gate.splitlines(),
            updated_gate.splitlines(),
            fromfile="before/recursion-gate.md",
            tofile="after/recursion-gate.md",
            lineterm="",
        )
    )
    preview = "\n".join(diff_lines[:80])

    return {
        "sandbox_root": str(sandbox_root),
        "sandbox_users_dir": str(sandbox_users_dir),
        "sandbox_user_dir": str(sandbox_user_dir),
        "candidate_id": candidate_id,
        "candidate_block": candidate_block,
        "diff_preview": preview,
    }
