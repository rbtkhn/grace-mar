#!/usr/bin/env python3
"""Run deterministic diagnostics used locally and in CI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SMOKE_OUTPUT_REL = (
    Path("artifacts")
    / "counterfactual-simulations"
    / "deterministic-diagnostics-smoke.json"
)


def _print_section(title: str) -> None:
    print()
    print(f"== {title} ==")


def _command(repo_root: Path, script_rel: str, *args: str) -> list[str]:
    return [sys.executable, str(repo_root / script_rel), *args]


def _run_step(title: str, command: list[str], *, repo_root: Path) -> subprocess.CompletedProcess[str]:
    _print_section(title)
    print(" ".join(command))
    result = subprocess.run(
        command,
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(
            result.stderr,
            end="" if result.stderr.endswith("\n") else "\n",
            file=sys.stderr,
        )
    return result


def run_diagnostics(
    repo_root: Path,
    *,
    keep_smoke_output: bool = False,
) -> int:
    repo_root = repo_root.resolve()
    smoke_output = repo_root / SMOKE_OUTPUT_REL
    smoke_output.parent.mkdir(parents=True, exist_ok=True)

    steps = [
        (
            "Doctrine Drift Radar",
            _command(repo_root, "scripts/audit_doctrine_drift.py"),
        ),
        (
            "Agent Sprawl Control Plane",
            _command(repo_root, "scripts/work_dev/audit_agent_sprawl.py"),
        ),
        (
            "Counterfactual Fork Simulator",
            _command(
                repo_root,
                "scripts/simulate_counterfactual_fork.py",
                "--proposal",
                "examples/diagnostics/counterfactual-proposal.example.json",
                "--output",
                str(SMOKE_OUTPUT_REL),
            ),
        ),
    ]

    for title, command in steps:
        result = _run_step(title, command, repo_root=repo_root)
        if result.returncode != 0:
            print(
                f"deterministic diagnostics failed during: {title}",
                file=sys.stderr,
            )
            return result.returncode

    if smoke_output.exists() and not keep_smoke_output:
        smoke_output.unlink()

    print()
    print("Deterministic diagnostics passed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic diagnostics for doctrine drift, agent sprawl, and counterfactual smoke."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to run diagnostics from",
    )
    parser.add_argument(
        "--keep-smoke-output",
        action="store_true",
        help="Keep the counterfactual smoke output instead of deleting it after a successful run",
    )
    args = parser.parse_args(argv)
    return run_diagnostics(
        args.repo_root,
        keep_smoke_output=args.keep_smoke_output,
    )


if __name__ == "__main__":
    raise SystemExit(main())
