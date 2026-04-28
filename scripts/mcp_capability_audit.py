#!/usr/bin/env python3
"""
Audit MCP capability registry YAML against schemas/mcp-capability.v1.json and emit Markdown.

Read-only with respect to Record: writes only the report path (default artifacts/mcp-capability-report.md).

  python3 scripts/mcp_capability_audit.py
  python3 scripts/mcp_capability_audit.py --strict   # exit 1 if any danger flag
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
DEFAULT_CONFIG = REPO_ROOT / "config" / "mcp-capabilities.yaml"
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "mcp-capability.v1.json"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "mcp-capability-report.md"


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


def _safe_rel(path: Path, root: Path) -> Path | str:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError(
            "PyYAML required (pip install -r requirements-dev.txt)"
        ) from e
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text)


def validate_document(doc: Any, schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as e:
        raise RuntimeError(
            "jsonschema required (pip install -r requirements-dev.txt)"
        ) from e
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=doc, schema=schema)


def _write_capable(cap: dict[str, Any]) -> bool:
    return bool(cap.get("writes")) or bool(cap.get("durable_state_write"))


def _implies_shell_execution_allowed(cap: dict[str, Any]) -> bool:
    """True when configuration implies shell/subprocess execution is in scope (risk)."""
    if cap.get("id") == "shell_execution_prohibited":
        return False
    if cap.get("category") == "shell":
        return True
    hay = " ".join(cap.get("allowed_actions", []) + cap.get("writes", [])).lower()
    needles = (
        "shell",
        "subprocess",
        "terminal",
        "bash",
        "powershell",
        "cmd.exe",
        "/bin/sh",
        "/bin/bash",
    )
    return any(n in hay for n in needles)


def danger_flags(capabilities: list[dict[str, Any]]) -> list[str]:
    """Deterministic sorted danger-flag strings for audit Markdown."""
    flags: list[str] = []
    for cap in capabilities:
        cid = cap["id"]

        # R1 — cloud + credentials + write-capable surface
        if (
            cap.get("local_or_cloud") == "cloud"
            and cap.get("credential_requirements") != "none"
            and _write_capable(cap)
        ):
            flags.append(
                f"R1[{cid}]: cloud deployment + credentials + write-capable "
                "(review exfiltration / lateral movement)"
            )

        # R2 — shell execution exposure
        if _implies_shell_execution_allowed(cap):
            flags.append(
                f"R2[{cid}]: shell/subprocess execution appears permitted "
                "(confirm operator-only harness and no Record writes)"
            )

        # R3 — durable write without gate requirement (contradiction)
        if cap.get("durable_state_write") and not cap.get(
            "gate_required_for_record_change"
        ):
            flags.append(
                f"R3[{cid}]: durable_state_write true but gate_required_for_record_change false"
            )

        # R4 — mutating capability without receipt discipline
        if _write_capable(cap) and not cap.get("requires_receipt"):
            flags.append(
                f"R4[{cid}]: write-capable but requires_receipt false"
            )

    return sorted(flags)


def build_report_markdown(
    *,
    doc: dict[str, Any],
    schema_path: Path,
    config_path: Path,
    flags: list[str],
    generated_at_utc: str | None = None,
    git_ref: str | None = None,
) -> str:
    ts = generated_at_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    gref = git_ref if git_ref is not None else _git_short_hash(REPO_ROOT)
    caps: list[dict[str, Any]] = doc["capabilities"]
    lines: list[str] = [
        "# MCP capability audit report",
        "",
        f"- **Generated (UTC):** {ts}",
        f"- **Git:** `{gref}`",
        f"- **Config:** `{_safe_rel(config_path, REPO_ROOT)}`",
        f"- **Schema:** `{_safe_rel(schema_path, REPO_ROOT)}`",
        f"- **Capabilities:** {len(caps)}",
        "",
        "## Summary",
        "",
        "Planning-only registry classes — not live MCP wiring. Durable Record changes remain gated.",
        "",
        "## Capability classes",
        "",
        "| id | category | local/cloud | trust | network | creds | durable write | gate for Record | receipt | output lane |",
        "|----|----------|-------------|-------|---------|-------|---------------|-----------------|---------|-------------|",
    ]
    for c in sorted(caps, key=lambda x: x["id"]):
        lines.append(
            f"| `{c['id']}` | {c['category']} | {c['local_or_cloud']} | {c['trust_tier']} "
            f"| {c['network_access']} | {c['credential_requirements']} "
            f"| {str(c['durable_state_write']).lower()} "
            f"| {str(c['gate_required_for_record_change']).lower()} "
            f"| {str(c['requires_receipt']).lower()} "
            f"| {c['output_lane']} |"
        )
    lines.extend(["", "## Danger flags", ""])
    if not flags:
        lines.append("*None detected by heuristic rules (R1–R4).*")
    else:
        for f in flags:
            lines.append(f"- **{f}**")
    lines.extend(["", "## Notes", "", doc.get("description", "").strip() or "_(see config description)_", ""])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit MCP capability YAML registry.")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any danger flag is raised (after successful validation).",
    )
    args = ap.parse_args()

    cfg = args.config.resolve()
    sch = args.schema.resolve()
    out = args.output.resolve()

    try:
        doc = load_yaml(cfg)
        validate_document(doc, sch)
    except Exception as e:
        print(f"mcp_capability_audit: validation failed: {e}", file=sys.stderr)
        return 1

    caps = doc["capabilities"]
    flags = danger_flags(caps)
    body = build_report_markdown(
        doc=doc,
        schema_path=sch,
        config_path=cfg,
        flags=flags,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(
        f"Wrote {_safe_rel(out, REPO_ROOT)} ({len(flags)} danger flag(s))",
        file=sys.stderr,
    )
    if args.strict and flags:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
