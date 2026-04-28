#!/usr/bin/env python3
"""
Run governed MCP tooling against committed examples; write aggregated Markdown report.

No live MCP servers. Uses subprocess with shell=False only. Does not write canonical Record paths under `users/`.
See docs/mcp/mcp-governance-runbook.md.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO_ROOT / "artifacts" / "mcp-governance-demo-report.md"


def _posix(base: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _run_step(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        shell=False,
        capture_output=True,
        text=True,
    )


def _parse_artifact_paths(stdout: str, stderr: str) -> list[str]:
    found: list[str] = []
    for block in (stdout, stderr):
        for line in block.splitlines():
            s = line.strip()
            if s.startswith("artifacts/"):
                found.append(s)
    # De-dupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for p in found:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _tail(text: str, max_chars: int = 800) -> str:
    t = text.strip()
    if len(t) <= max_chars:
        return t
    return t[-max_chars:]


@dataclass
class StepResult:
    name: str
    kind: Literal["required", "optional"]
    cmd_display: str
    returncode: int | None
    status: Literal["PASS", "FAIL", "SKIP_ABSENT"]
    notes: str = ""
    artifacts: list[str] = field(default_factory=list)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run MCP governance demo checks (local scripts only).")
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: infer from script location).",
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    demo = root / "artifacts" / "mcp-governance-demo"
    report_out = root / "artifacts" / "mcp-governance-demo-report.md"
    demo.mkdir(parents=True, exist_ok=True)

    py = sys.executable

    def script(name: str) -> str:
        return str((root / "scripts" / name).resolve())

    def posix_rel(p: Path) -> str:
        return _posix(root, p)

    results: list[StepResult] = []

    def run_required(name: str, cmd: list[str], known_artifacts: list[str]) -> None:
        display = " ".join(cmd[2:]) if len(cmd) > 2 else " ".join(cmd)
        cp = _run_step(cmd, root)
        arts = list(dict.fromkeys(known_artifacts + _parse_artifact_paths(cp.stdout, cp.stderr)))
        ok = cp.returncode == 0
        note = ""
        if not ok:
            note = _tail((cp.stderr or "") + "\n" + (cp.stdout or ""))
        results.append(
            StepResult(
                name=name,
                kind="required",
                cmd_display=display,
                returncode=cp.returncode,
                status="PASS" if ok else "FAIL",
                notes=note,
                artifacts=arts,
            )
        )

    def run_optional(name: str, input_rel: Path, cmd: list[str], known_artifacts: list[str]) -> None:
        inp = (root / input_rel).resolve()
        display = " ".join(cmd[2:])
        if not inp.is_file():
            results.append(
                StepResult(
                    name=name,
                    kind="optional",
                    cmd_display=display,
                    returncode=None,
                    status="SKIP_ABSENT",
                    notes=f"missing input {input_rel.as_posix()}",
                    artifacts=[],
                )
            )
            return
        cp = _run_step(cmd, root)
        arts = list(dict.fromkeys(known_artifacts + _parse_artifact_paths(cp.stdout, cp.stderr)))
        ok = cp.returncode == 0
        note = ""
        if not ok:
            note = _tail((cp.stderr or "") + "\n" + (cp.stdout or ""))
        results.append(
            StepResult(
                name=name,
                kind="optional",
                cmd_display=display,
                returncode=cp.returncode,
                status="PASS" if ok else "FAIL",
                notes=note,
                artifacts=arts,
            )
        )

    cap_md = demo / "capability-report.md"
    auth_md = demo / "authority-report.md"
    risk_md = demo / "risk-report.md"
    risk_js = demo / "risk-report.json"
    man_md = root / "artifacts/mcp-admission/governance-demo-manifest.md"
    mock_md = root / "artifacts/mcp-mock-runs/governance-demo-mock.md"
    lr_md = root / "artifacts/mcp-local-read/governance-demo-read.md"
    li_md = root / "artifacts/mcp-local-index/governance-demo-index.md"
    ev_md = root / "artifacts/evidence-stubs/governance-demo-stub.md"
    pi_md = root / "artifacts/patch-intake/governance-demo-intake.md"

    run_required(
        "mcp_capability_audit",
        [
            py,
            script("mcp_capability_audit.py"),
            "-o",
            str(cap_md),
        ],
        [posix_rel(cap_md)],
    )
    run_required(
        "mcp_authority_check",
        [
            py,
            script("mcp_authority_check.py"),
            "-o",
            str(auth_md),
        ],
        [posix_rel(auth_md)],
    )
    run_required(
        "mcp_risk_scan",
        [
            py,
            script("mcp_risk_scan.py"),
            "--markdown",
            str(risk_md),
            "--json",
            str(risk_js),
        ],
        [posix_rel(risk_md), posix_rel(risk_js)],
    )
    run_required(
        "mcp_manifest_admission",
        [
            py,
            script("mcp_manifest_admission.py"),
            "--input",
            str(root / "examples" / "mcp-server-manifest.example.yaml"),
            "--output",
            str(man_md),
        ],
        [posix_rel(man_md)],
    )
    run_required(
        "mcp_mock_harness",
        [
            py,
            script("mcp_mock_harness.py"),
            "--input",
            str(root / "examples" / "mcp-mock-run.shell-blocked.example.json"),
            "--output",
            str(mock_md),
        ],
        [posix_rel(mock_md)],
    )
    run_required(
        "mcp_local_readonly",
        [
            py,
            script("mcp_local_readonly.py"),
            "--input",
            str(root / "examples" / "mcp-local-read-request.example.json"),
            "--output",
            str(lr_md),
        ],
        [posix_rel(lr_md)],
    )
    run_required(
        "mcp_local_index",
        [
            py,
            script("mcp_local_index.py"),
            "--input",
            str(root / "examples" / "mcp-local-index-request.example.json"),
            "--output",
            str(li_md),
        ],
        [posix_rel(li_md)],
    )

    run_optional(
        "research_to_evidence_stub",
        Path("examples/research-evidence-input.example.json"),
        [
            py,
            script("research_to_evidence_stub.py"),
            "--input",
            str(root / "examples" / "research-evidence-input.example.json"),
            "--output",
            str(ev_md),
        ],
        [posix_rel(ev_md)],
    )
    run_optional(
        "coding_agent_patch_intake",
        Path("examples/coding-agent-patch-intake.example.json"),
        [
            py,
            script("coding_agent_patch_intake.py"),
            "--input",
            str(root / "examples" / "coding-agent-patch-intake.example.json"),
            "--output",
            str(pi_md),
        ],
        [posix_rel(pi_md)],
    )

    receipt_paths = sorted({p for r in results for p in r.artifacts if "mcp-receipts/" in p})

    lines: list[str] = [
        "# MCP governance demo report",
        "",
        f"**Generated (UTC):** `{ts}`",
        "",
        "**Orchestrator:** `scripts/run_mcp_governance_checks.py`",
        "",
        "## Command results",
        "",
        "| Step | Kind | Exit | Status | Command |",
        "|------|------|------|--------|---------|",
    ]
    for r in results:
        rc = "" if r.returncode is None else str(r.returncode)
        lines.append(
            f"| `{r.name}` | {r.kind} | {rc} | **{r.status}** | `{r.cmd_display}` |",
        )

    lines.extend(["", "## Notes (failures only)", ""])
    any_notes = False
    for r in results:
        if r.status == "FAIL" and r.notes:
            any_notes = True
            lines.extend([f"### `{r.name}`", "", "```text", r.notes, "```", ""])
    if not any_notes:
        lines.append("_None._")
        lines.append("")

    lines.extend(
        [
            "## Artifacts referenced",
            "",
        ]
    )
    all_art = sorted({p for r in results for p in r.artifacts})
    for p in all_art:
        lines.append(f"- `{p}`")
    if not all_art:
        lines.append("_None._")
    lines.append("")

    lines.extend(
        [
            "## Receipt JSON paths (from stdout/stderr)",
            "",
        ]
    )
    if receipt_paths:
        for p in receipt_paths:
            lines.append(f"- `{p}`")
    else:
        lines.append("_None detected in captured output (receipts may still exist under `artifacts/mcp-receipts/`)._")
    lines.append("")

    lines.extend(
        [
            "## Boundaries confirmed (design)",
            "",
            "- **Live MCP execution:** none — only local Python scripts.",
            "- **Credentials:** none added by this orchestrator.",
            "- **Network:** none — subprocesses run repo tooling on local files.",
            "- **Shell:** `subprocess.run(..., shell=False)` only; no shell DSL.",
            "- **Canonical Record mutation:** none — orchestrator does not write companion identity files or gate surfaces.",
            "- **Companion users/ tree write:** none (orchestrator emits only `artifacts/` outputs).",
            "",
            "## Summary",
            "",
        ]
    )

    required_failed = any(r.kind == "required" and r.status == "FAIL" for r in results)
    optional_failed = any(r.kind == "optional" and r.status == "FAIL" for r in results)
    if required_failed:
        summary = "**FAIL** — one or more required steps returned non-zero."
        code = 1
    elif optional_failed:
        summary = "**FAIL** — an optional step ran but failed."
        code = 1
    else:
        summary = "**PASS** — all required steps succeeded; optional steps skipped or passed."
        code = 0

    lines.append(summary)
    lines.append("")

    report_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.write_text("\n".join(lines), encoding="utf-8")
    print(_posix(root, report_out.resolve()))

    return code


if __name__ == "__main__":
    sys.exit(main())
