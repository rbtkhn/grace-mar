#!/usr/bin/env python3
"""
Print or validate the work-dev agent-surface checklist (YAML).

Three axes (ecosystem framing): runtime placement, orchestration, interface.
Grace-Mar block: Record authority, staging, gate, continuity.

Usage:
  python scripts/work_dev/agent_surface_checklist.py
  python scripts/work_dev/agent_surface_checklist.py --validate path/to/eval.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_TEMPLATE = (
    REPO_ROOT
    / "docs"
    / "skill-work"
    / "work-dev"
    / "agent-surface-template.yaml"
)

REQUIRED_TOP = ("version", "runtime", "orchestration", "interface", "grace_mar")
REQUIRED_GRACE = (
    "record_authority",
    "staging_surface",
    "merge_requires_companion_gate",
    "continuity_contract",
)

# Four-species taxonomy (production agent patterns); optional field in YAML.
ALLOWED_AGENT_SPECIES = frozenset(
    {
        "coding_harness",
        "dark_factory",
        "auto_research",
        "workflow_orchestration",
    }
)


def validate_doc(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    gm = data.get("grace_mar")
    if isinstance(gm, dict):
        for key in REQUIRED_GRACE:
            if key not in gm:
                errors.append(f"missing grace_mar.{key}")
    elif "grace_mar" in data:
        errors.append("grace_mar must be a mapping")

    raw = data.get("agent_species")
    if raw is not None and str(raw).strip():
        s = str(raw).strip()
        if s not in ALLOWED_AGENT_SPECIES:
            errors.append(
                "agent_species must be one of "
                f"{sorted(ALLOWED_AGENT_SPECIES)} or empty, got {s!r}"
            )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent surface checklist (YAML template + validate).")
    ap.add_argument("--validate", type=Path, metavar="YAML", help="Validate a filled checklist")
    args = ap.parse_args()

    if args.validate is not None:
        try:
            import yaml
        except ImportError:
            print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
            return 2
        p = args.validate.resolve()
        if not p.is_file():
            print(f"error: not a file: {p}", file=sys.stderr)
            return 2
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            print("error: root must be a mapping", file=sys.stderr)
            return 1
        errs = validate_doc(data)
        if errs:
            for e in errs:
                print(e, file=sys.stderr)
            return 1
        print("ok: checklist structure valid")
        return 0

    if not DEFAULT_TEMPLATE.is_file():
        print(f"error: template missing: {DEFAULT_TEMPLATE}", file=sys.stderr)
        return 2
    sys.stdout.write(DEFAULT_TEMPLATE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
