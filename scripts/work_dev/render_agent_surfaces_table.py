#!/usr/bin/env python3
"""
Render a human-readable Markdown table from the Agent Surfaces Control Plane JSON registry.
The JSON file remains authoritative; this output is derived and not Record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "config" / "agent-surfaces.v1.json"
DEFAULT_OUTPUT = (
    REPO_ROOT / "artifacts" / "work-dev" / "agent-surfaces" / "agent-surfaces-table.md"
)

EM_DASH = "\u2014"


def _escape_pipes(s: str) -> str:
    return s.replace("|", r"\|")


def _str_cell(value: Any) -> str:
    if value is None:
        return EM_DASH
    if not isinstance(value, str):
        return _escape_pipes(str(value))
    stripped = value.strip()
    if not stripped:
        return EM_DASH
    return _escape_pipes(stripped)


def _list_cell(value: Any) -> str:
    if value is None or not isinstance(value, list):
        return EM_DASH
    if not value:
        return EM_DASH
    parts: list[str] = []
    for item in value:
        if item is None:
            parts.append("")
        else:
            parts.append(str(item).strip())
    joined = " <br> ".join(parts)
    return _escape_pipes(joined) if joined else EM_DASH


def _bool_cell(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return EM_DASH


def _summary_counts(surfaces: list[dict[str, Any]]) -> dict[str, int]:
    total = len(surfaces)
    implemented = sum(1 for s in surfaces if s.get("status") == "implemented")
    partial = sum(1 for s in surfaces if s.get("status") == "partial")
    documented_only = sum(1 for s in surfaces if s.get("status") == "documented_only")
    planned = sum(1 for s in surfaces if s.get("status") == "planned")
    receipts = sum(1 for s in surfaces if s.get("receipt_required") is True)
    with_contract = 0
    for s in surfaces:
        cc = s.get("capability_contract")
        if isinstance(cc, str) and cc.strip():
            with_contract += 1
    merge_non_none = 0
    for s in surfaces:
        ma = s.get("merge_authority")
        if not isinstance(ma, str) or not ma.strip():
            continue
        if ma.strip() != "none":
            merge_non_none += 1
    return {
        "total": total,
        "implemented": implemented,
        "partial": partial,
        "documented_only": documented_only,
        "planned": planned,
        "receipts": receipts,
        "capability_contracts": with_contract,
        "merge_authority": merge_non_none,
    }


def build_markdown(registry: dict[str, Any]) -> str:
    raw = registry.get("surfaces")
    if not isinstance(raw, list):
        raise ValueError("registry must contain a 'surfaces' list")

    surfaces: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, dict):
            surfaces.append(item)
        else:
            raise ValueError("each surface must be a JSON object")

    surfaces.sort(key=lambda s: str(s.get("id", "")))
    sc = _summary_counts(surfaces)

    lines: list[str] = [
        "# Agent Surfaces Table",
        "",
        "Generated from `config/agent-surfaces.v1.json`.",
        "",
        "This table is derived from the machine-readable Agent Sprawl Control Plane registry.",
        "The JSON registry remains authoritative.",
        "This table is not Record, not approval, not a merge path, and grants no authority.",
        "",
        "## Summary",
        "",
        f"- Total surfaces: {sc['total']}",
        f"- Implemented: {sc['implemented']}",
        f"- Partial: {sc['partial']}",
        f"- Documented-only: {sc['documented_only']}",
        f"- Planned: {sc['planned']}",
        f"- Surfaces requiring receipts: {sc['receipts']}",
        f"- Surfaces with capability contracts: {sc['capability_contracts']}",
        f"- Surfaces with merge authority: {sc['merge_authority']}",
        "",
        "## Surfaces",
        "",
    ]

    header = (
        "| ID | Name | Status | Category | Owner lane | Canonical Record access | "
        "Merge authority | Gate effect | Receipt required | Capability contract | "
        "Reads | Writes | Notes |"
    )
    sep = (
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    lines.append(header)
    lines.append(sep)

    for s in surfaces:
        row = (
            f"| {_str_cell(s.get('id'))} | "
            f"{_str_cell(s.get('name'))} | "
            f"{_str_cell(s.get('status'))} | "
            f"{_str_cell(s.get('category'))} | "
            f"{_str_cell(s.get('owner_lane'))} | "
            f"{_str_cell(s.get('canonical_record_access'))} | "
            f"{_str_cell(s.get('merge_authority'))} | "
            f"{_str_cell(s.get('gate_effect'))} | "
            f"{_bool_cell(s.get('receipt_required'))} | "
            f"{_str_cell(s.get('capability_contract'))} | "
            f"{_list_cell(s.get('reads'))} | "
            f"{_list_cell(s.get('writes'))} | "
            f"{_str_cell(s.get('notes'))} |"
        )
        lines.append(row)

    return "\n".join(lines) + "\n"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render agent surfaces registry to a Markdown table (derived; not Record)."
    )
    ap.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to agent-surfaces.v1.json",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write agent-surfaces-table.md",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Compare rendered output to existing file; exit 1 if missing or stale",
    )
    args = ap.parse_args()

    registry_path = args.registry
    if not registry_path.is_absolute():
        registry_path = REPO_ROOT / registry_path
    output_path = args.output
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    try:
        registry = _load_json(registry_path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: could not read registry: {e}", file=sys.stderr)
        return 1

    try:
        expected = build_markdown(registry)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.check:
        if not output_path.is_file():
            print(
                f"check failed: output missing: {output_path}",
                file=sys.stderr,
            )
            return 1
        on_disk = output_path.read_text(encoding="utf-8")
        if on_disk != expected:
            print(
                f"check failed: output stale or hand-edited: {output_path}\n"
                f"  run: python3 scripts/work_dev/render_agent_surfaces_table.py",
                file=sys.stderr,
            )
            return 1
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(expected, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
