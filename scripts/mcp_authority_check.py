#!/usr/bin/env python3
"""
Cross-check MCP capability registry against authority bindings + authority-map.json.

Read-only with respect to Record. Writes artifacts/mcp-authority-report.md by default.

  python3 scripts/mcp_authority_check.py
  python3 scripts/mcp_authority_check.py --strict   # warnings also fail exit code
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_capability_audit import (  # noqa: E402
    _implies_shell_execution_allowed,
    _write_capable,
    validate_document as validate_jsonschema_document,
)

CAPABILITIES_PATH = REPO_ROOT / "config" / "mcp-capabilities.yaml"
CAPABILITY_SCHEMA = REPO_ROOT / "schemas" / "mcp-capability.v1.json"
BINDINGS_PATH = REPO_ROOT / "config" / "mcp-authority-bindings.yaml"
BINDINGS_SCHEMA = REPO_ROOT / "schemas" / "mcp-authority-bindings.v1.json"
AUTHORITY_MAP_PATH = REPO_ROOT / "config" / "authority-map.json"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "mcp-authority-report.md"

GITHUB_REQUIRED_PROHIBITED = ("merge_to_main", "force_push", "bypass_review")


def _safe_rel(path: Path, root: Path) -> Path | str:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _git_short_hash(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.TimeoutError, subprocess.SubprocessError):
        pass
    return "unknown"


def load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required (pip install -r requirements-dev.txt)") from e
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_authority_map(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bindings_by_lane(bindings_doc: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Return map output_lane -> binding row; violations if duplicate lanes."""
    violations: list[str] = []
    out: dict[str, dict[str, Any]] = {}
    for row in bindings_doc["bindings"]:
        lane = row["output_lane"]
        if lane in out:
            violations.append(f"duplicate binding for output_lane '{lane}'")
        out[lane] = row
    return out, sorted(violations)


def validate_bindings_vs_authority_map(
    bindings_doc: dict[str, Any],
    authority_map: dict[str, Any],
) -> list[str]:
    violations: list[str] = []
    surfaces: dict[str, str] = authority_map.get("surfaces") or {}

    for row in bindings_doc["bindings"]:
        lane = row["output_lane"]
        surf = row["authority_surface"]
        cls = row["authority_class"]
        override = bool(row.get("authority_class_override"))
        reason = (row.get("override_reason") or "").strip()

        if surf not in surfaces:
            violations.append(
                f"binding[{lane}]: unknown authority_surface '{surf}' (not in authority-map.json)"
            )
            continue

        expected = surfaces[surf]
        if cls != expected:
            if override:
                if not reason:
                    violations.append(
                        f"binding[{lane}]: authority_class_override requires non-empty override_reason"
                    )
            else:
                violations.append(
                    f"binding[{lane}]: authority_class '{cls}' != authority-map value '{expected}' "
                    f"for surface '{surf}' (set authority_class_override + override_reason if intentional)"
                )

        if override and cls == expected and reason:
            violations.append(
                f"binding[{lane}]: override_reason set but class matches map — drop override fields"
            )

    return sorted(violations)


def validate_capabilities(
    capabilities: list[dict[str, Any]],
    lane_map: dict[str, dict[str, Any]],
) -> tuple[list[str], list[str]]:
    """Return (violations, warnings)."""
    violations: list[str] = []
    warnings: list[str] = []

    lanes_used: set[str] = set()

    for cap in capabilities:
        cid = cap["id"]
        lane = cap["output_lane"]
        lanes_used.add(lane)

        if lane not in lane_map:
            violations.append(
                f"capability[{cid}]: output_lane '{lane}' has no entry in mcp-authority-bindings.yaml"
            )
            continue

        bind = lane_map[lane]
        bcls = bind["authority_class"]

        if _write_capable(cap) and not cap.get("requires_receipt"):
            violations.append(f"capability[{cid}]: writes/durable_state_write require requires_receipt: true")

        if _write_capable(cap) and bcls == "ephemeral_only":
            violations.append(
                f"capability[{cid}]: write-capable output cannot bind to ephemeral_only lane '{lane}'"
            )

        if lane == "candidate_proposal" and bcls != "review_required":
            violations.append(
                f"capability[{cid}]: candidate_proposal lane must bind to review_required (got {bcls})"
            )

        if lane == "runtime_only" and bcls not in ("ephemeral_only", "read_only"):
            violations.append(
                f"capability[{cid}]: runtime_only lane must bind to ephemeral_only or read_only (got {bcls})"
            )

        if cap.get("durable_state_write"):
            if not cap.get("gate_required_for_record_change"):
                violations.append(
                    f"capability[{cid}]: durable_state_write requires gate_required_for_record_change"
                )
            if bcls not in ("review_required", "human_only"):
                violations.append(
                    f"capability[{cid}]: durable_state_write requires review_required or human_only binding "
                    f"(lane {lane} -> {bcls})"
                )

        if _implies_shell_execution_allowed(cap):
            violations.append(
                f"capability[{cid}]: shell/subprocess execution must remain prohibited for governed MCP"
            )

        if cid == "memory_external_prohibited_by_default" and cap.get("writes"):
            violations.append(
                f"capability[{cid}]: external memory writes prohibited — writes array must be empty"
            )

        if cid in ("github_readonly", "github_patch_proposal"):
            joined = " ".join(cap.get("prohibited_actions", [])).lower()
            for token in GITHUB_REQUIRED_PROHIBITED:
                if token.lower() not in joined:
                    violations.append(
                        f"capability[{cid}]: prohibited_actions must include '{token}' "
                        f"(GitHub SCM governance)"
                    )

    unused = set(lane_map.keys()) - lanes_used
    if unused:
        warnings.append(f"bindings defined but unused by capabilities: {sorted(unused)}")

    return sorted(violations), sorted(warnings)


def build_report_md(
    *,
    passes: bool,
    violations: list[str],
    warnings: list[str],
    capabilities: list[dict[str, Any]],
    lane_map: dict[str, dict[str, Any]],
    generated_at: str,
    git_ref: str,
) -> str:
    lines = [
        "# MCP authority binding report",
        "",
        f"- **Generated (UTC):** {generated_at}",
        f"- **Git:** `{git_ref}`",
        f"- **Status:** {'**PASS**' if passes else '**FAIL**'}",
        "",
        "## Summary",
        "",
        f"- Capabilities checked: **{len(capabilities)}**",
        f"- Bindings (lanes): **{len(lane_map)}**",
        f"- Violations: **{len(violations)}**",
        f"- Warnings: **{len(warnings)}**",
        "",
        "## Lane → authority",
        "",
        "| output_lane | authority_surface | authority_class | gate_for_record_change |",
        "|---------------|--------------------|-----------------|-------------------------|",
    ]
    for lane in sorted(lane_map.keys()):
        b = lane_map[lane]
        lines.append(
            f"| `{lane}` | `{b['authority_surface']}` | {b['authority_class']} | "
            f"{b['gate_required_for_record_change']} |"
        )
    lines.extend(["", "## Capabilities by lane", ""])
    by_lane: dict[str, list[str]] = {}
    for c in capabilities:
        by_lane.setdefault(c["output_lane"], []).append(c["id"])
    for lane in sorted(by_lane.keys()):
        ids = ", ".join(f"`{x}`" for x in sorted(by_lane[lane]))
        lines.append(f"- **`{lane}`:** {ids}")
    lines.extend(["", "## Violations", ""])
    if violations:
        for v in violations:
            lines.append(f"- {v}")
    else:
        lines.append("_None._")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("_None._")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP authority binding cross-check.")
    ap.add_argument("--capabilities", type=Path, default=CAPABILITIES_PATH)
    ap.add_argument("--bindings", type=Path, default=BINDINGS_PATH)
    ap.add_argument("--authority-map", type=Path, dest="authority_map", default=AUTHORITY_MAP_PATH)
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--strict", action="store_true", help="Treat warnings as failure (exit 1).")
    args = ap.parse_args()

    caps_path = args.capabilities.resolve()
    bind_path = args.bindings.resolve()
    map_path = args.authority_map.resolve()
    out_path = args.output.resolve()

    try:
        caps_doc = load_yaml(caps_path)
        bind_doc = load_yaml(bind_path)
        validate_jsonschema_document(caps_doc, CAPABILITY_SCHEMA)
        validate_jsonschema_document(bind_doc, BINDINGS_SCHEMA)
        authority_map = load_authority_map(map_path)
    except Exception as e:
        print(f"mcp_authority_check: load/validate failed: {e}", file=sys.stderr)
        return 1

    lane_map, dup_v = bindings_by_lane(bind_doc)
    bind_v = validate_bindings_vs_authority_map(bind_doc, authority_map)
    capabilities = caps_doc["capabilities"]
    cap_v, warns = validate_capabilities(capabilities, lane_map)

    violations = sorted(set(dup_v + bind_v + cap_v))
    passes = len(violations) == 0 and (not args.strict or len(warns) == 0)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = build_report_md(
        passes=passes,
        violations=violations,
        warnings=warns,
        capabilities=capabilities,
        lane_map=lane_map,
        generated_at=ts,
        git_ref=_git_short_hash(REPO_ROOT),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")

    print(
        f"Wrote {_safe_rel(out_path, REPO_ROOT)} — violations={len(violations)} warnings={len(warns)}",
        file=sys.stderr,
    )

    if violations:
        return 1
    if args.strict and warns:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
