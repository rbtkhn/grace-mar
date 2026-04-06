#!/usr/bin/env python3
"""
Print or validate work-dev agent-surface checklists and capability contracts.

Three axes (ecosystem framing): runtime placement, orchestration, interface.
Grace-Mar block: Record authority, staging, gate, continuity.

Usage:
  python scripts/work_dev/agent_surface_checklist.py
  python scripts/work_dev/agent_surface_checklist.py --validate path/to/eval.yaml
  python scripts/work_dev/agent_surface_checklist.py --validate-contracts
  python scripts/work_dev/agent_surface_checklist.py --validate-contracts path/to/contract.yaml
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
CONTRACTS_DIR = (
    REPO_ROOT / "docs" / "skill-work" / "work-dev" / "control-plane"
)

REQUIRED_TOP = ("version", "runtime", "orchestration", "interface", "grace_mar")
REQUIRED_GRACE = (
    "record_authority",
    "staging_surface",
    "merge_requires_companion_gate",
    "continuity_contract",
)

ALLOWED_AGENT_SPECIES = frozenset(
    {
        "coding_harness",
        "dark_factory",
        "auto_research",
        "workflow_orchestration",
    }
)

# ── Capability-contract validation ──────────────────────────────────────

CONTRACT_REQUIRED_TOP = (
    "version",
    "contract_id",
    "integration_name",
    "schema",
    "auth",
    "failure_policy",
    "cost",
    "governance",
)

CONTRACT_REQUIRED_SCHEMA = ("description",)
CONTRACT_REQUIRED_AUTH = ("mode",)
CONTRACT_REQUIRED_FAILURE = ("escalation",)
CONTRACT_REQUIRED_COST = ("hint",)
CONTRACT_REQUIRED_GOVERNANCE = (
    "review_requirement",
    "receipt_shape",
    "record_authority",
    "merge_allowed",
)

ALLOWED_AUTH_MODES = frozenset(
    {"none", "api_key", "oauth", "signed_role", "companion_gate"}
)
ALLOWED_COST_HINTS = frozenset(
    {"free", "negligible", "per_call", "metered", "unknown"}
)
ALLOWED_REVIEW_REQUIREMENTS = frozenset(
    {"none", "post_hoc", "pre_approval", "companion_gate"}
)
ALLOWED_ESCALATIONS = frozenset(
    {"abort", "log_and_continue", "alert_operator", "queue_for_review"}
)
ALLOWED_CONTRACT_STATUSES = frozenset(
    {"active", "planned", "deprecated", "experimental"}
)


def _check_enum(section: str, key: str, value: str, allowed: frozenset[str]) -> str | None:
    v = str(value).strip()
    if not v:
        return None
    if v not in allowed:
        return f"{section}.{key} must be one of {sorted(allowed)}, got {v!r}"
    return None


def _check_mapping(data: dict, section: str, required: tuple[str, ...]) -> list[str]:
    block = data.get(section)
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"{section} must be a mapping"]
    return [f"missing {section}.{k}" for k in required if k not in block]


def validate_contract(data: dict) -> list[str]:
    """Validate a capability contract YAML against the template schema."""
    errors: list[str] = []
    for key in CONTRACT_REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    cid = data.get("contract_id")
    if isinstance(cid, str) and not cid.strip():
        errors.append("contract_id must not be empty")

    errors.extend(_check_mapping(data, "schema", CONTRACT_REQUIRED_SCHEMA))
    errors.extend(_check_mapping(data, "auth", CONTRACT_REQUIRED_AUTH))
    errors.extend(_check_mapping(data, "failure_policy", CONTRACT_REQUIRED_FAILURE))
    errors.extend(_check_mapping(data, "cost", CONTRACT_REQUIRED_COST))
    errors.extend(_check_mapping(data, "governance", CONTRACT_REQUIRED_GOVERNANCE))

    auth = data.get("auth") or {}
    if isinstance(auth, dict):
        e = _check_enum("auth", "mode", auth.get("mode", ""), ALLOWED_AUTH_MODES)
        if e:
            errors.append(e)

    cost = data.get("cost") or {}
    if isinstance(cost, dict):
        e = _check_enum("cost", "hint", cost.get("hint", ""), ALLOWED_COST_HINTS)
        if e:
            errors.append(e)

    gov = data.get("governance") or {}
    if isinstance(gov, dict):
        e = _check_enum("governance", "review_requirement", gov.get("review_requirement", ""), ALLOWED_REVIEW_REQUIREMENTS)
        if e:
            errors.append(e)

    fp = data.get("failure_policy") or {}
    if isinstance(fp, dict):
        e = _check_enum("failure_policy", "escalation", fp.get("escalation", ""), ALLOWED_ESCALATIONS)
        if e:
            errors.append(e)

    dec = data.get("decision") or {}
    if isinstance(dec, dict):
        e = _check_enum("decision", "status", dec.get("status", ""), ALLOWED_CONTRACT_STATUSES)
        if e:
            errors.append(e)

    return errors


def _discover_contracts(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(directory.glob("capability-contract-*.yaml"))


def run_validate_contracts(targets: list[Path] | None) -> int:
    """Validate one or more capability contracts. Returns 0 if all pass."""
    try:
        import yaml
    except ImportError:
        print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
        return 2

    if targets:
        files = targets
    else:
        files = _discover_contracts(CONTRACTS_DIR)
        files = [f for f in files if f.name != "capability-contract-template.yaml"]
        if not files:
            print("no capability contracts found in control-plane/", file=sys.stderr)
            return 2

    total_errors = 0
    for p in files:
        rel = p.relative_to(REPO_ROOT) if p.is_relative_to(REPO_ROOT) else p
        if not p.is_file():
            print(f"SKIP  {rel}  (not a file)", file=sys.stderr)
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            print(f"FAIL  {rel}  root must be a mapping", file=sys.stderr)
            total_errors += 1
            continue
        errs = validate_contract(data)
        if errs:
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"  - {e}")
            total_errors += len(errs)
        else:
            print(f"ok    {rel}")

    if total_errors:
        print(f"\n{total_errors} error(s) across {len(files)} contract(s)", file=sys.stderr)
        return 1
    print(f"\nall {len(files)} contract(s) valid")
    return 0


# ── Agent-surface checklist validation (original) ──────────────────────

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
    ap = argparse.ArgumentParser(
        description="Agent surface checklist + capability contract validator.",
    )
    ap.add_argument("--validate", type=Path, metavar="YAML", help="Validate a filled agent-surface checklist")
    ap.add_argument(
        "--validate-contracts",
        nargs="*",
        type=Path,
        metavar="YAML",
        default=None,
        help="Validate capability contracts (auto-discovers in control-plane/ if no paths given)",
    )
    args = ap.parse_args()

    if args.validate_contracts is not None:
        targets = args.validate_contracts if args.validate_contracts else None
        return run_validate_contracts(targets)

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
