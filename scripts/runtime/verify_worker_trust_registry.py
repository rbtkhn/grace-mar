#!/usr/bin/env python3
"""
Validate worker trust registry JSON against schema and repo policy.

Does not execute workers, merge into the Record, approve candidates, or alter gate behavior.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

_DEFAULT_REGISTRY = Path("config/runtime_workers/worker-trust-registry.v1.json")
_DEFAULT_SCHEMA = Path("schemas/worker-trust-registry.v1.schema.json")

# Actions that must never appear in allowed_actions (documentation + enforcement).
FORBIDDEN_ALLOWED_ACTIONS = frozenset(
    {
        "approve_candidate",
        "merge_candidate",
        "edit_record_surface",
        "overwrite_record_surface",
    }
)

_ORCHESTRATOR_IDS = frozenset({"grace_mar_runtime_worker"})


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def validate_schema(instance: dict[str, Any], schema: dict[str, Any]) -> None:
    """Raise jsonschema.ValidationError on failure."""
    from jsonschema import Draft202012Validator

    validator = Draft202012Validator(schema)
    validator.check_schema(schema)
    validator.validate(instance)


def policy_forbidden_actions(instance: dict[str, Any]) -> list[str]:
    """Return human-readable error lines if Policy A fails."""
    errs: list[str] = []
    workers = instance.get("workers")
    if not isinstance(workers, list):
        return ["workers must be a list"]
    for w in workers:
        if not isinstance(w, dict):
            errs.append("each worker must be an object")
            continue
        wid = w.get("id", "?")
        allowed = w.get("allowed_actions")
        if not isinstance(allowed, list):
            errs.append(f"{wid}: allowed_actions must be a list")
            continue
        bad = FORBIDDEN_ALLOWED_ACTIONS.intersection(a for a in allowed if isinstance(a, str))
        if bad:
            errs.append(f"{wid}: forbidden actions in allowed_actions: {sorted(bad)}")
    return errs


def policy_stage_candidate_gate(instance: dict[str, Any]) -> list[str]:
    """Policy B: stage_candidate requires gate_review_required."""
    errs: list[str] = []
    for w in instance.get("workers") or []:
        if not isinstance(w, dict):
            continue
        wid = w.get("id", "?")
        allowed = w.get("allowed_actions")
        if not isinstance(allowed, list):
            continue
        if "stage_candidate" in allowed and not w.get("gate_review_required"):
            errs.append(f"{wid}: stage_candidate requires gate_review_required true")
    return errs


def policy_yaml_parity(repo_root: Path, instance: dict[str, Any]) -> list[str]:
    """Policy C: every registry.yaml worker id appears exactly once in trust registry."""
    errs: list[str] = []
    runtime = repo_root / "scripts" / "runtime"
    if str(runtime) not in sys.path:
        sys.path.insert(0, str(runtime))
    from worker_registry import load_registry

    reg = load_registry(repo_root)
    yaml_ids: list[str] = []
    for section in ("shared_workers", "routed_workers"):
        block = reg.get(section)
        if isinstance(block, dict):
            yaml_ids.extend(sorted(block.keys()))

    trust_ids = [w.get("id") for w in instance.get("workers") or [] if isinstance(w, dict)]
    dup = _duplicate_ids(trust_ids)
    if dup:
        errs.append(f"duplicate worker ids in trust registry: {sorted(dup)}")

    for yid in yaml_ids:
        if trust_ids.count(yid) != 1:
            errs.append(f"yaml worker {yid!r} must appear exactly once in trust registry (got {trust_ids.count(yid)})")

    extras = set(trust_ids) - set(yaml_ids)
    extras -= _ORCHESTRATOR_IDS
    if extras:
        errs.append(f"trust registry ids not in registry.yaml (unexpected): {sorted(extras)}")
    return errs


def _duplicate_ids(ids: list[Any]) -> set[str]:
    from collections import Counter

    c = Counter(i for i in ids if isinstance(i, str))
    return {k for k, v in c.items() if v > 1}


def verify_worker_trust_registry(
    repo_root: Path,
    registry_path: Path | None = None,
    schema_path: Path | None = None,
    *,
    skip_yaml_parity: bool = False,
) -> list[str]:
    """
    Run schema + policy checks. Returns a list of error strings (empty if ok).
    """
    root = repo_root.resolve()
    reg_rel = registry_path or (root / _DEFAULT_REGISTRY)
    sch_rel = schema_path or (root / _DEFAULT_SCHEMA)
    errs: list[str] = []

    if not reg_rel.is_file():
        return [f"missing registry: {reg_rel}"]
    if not sch_rel.is_file():
        return [f"missing schema: {sch_rel}"]

    try:
        from jsonschema import ValidationError
    except ImportError:
        return ["jsonschema is required (pip install jsonschema)"]

    instance = _load_json(reg_rel)
    schema = _load_json(sch_rel)

    try:
        validate_schema(instance, schema)
    except ValidationError as e:
        errs.append(f"schema: {e.message}")
    except Exception as e:  # pragma: no cover
        errs.append(f"schema: {e}")

    errs.extend(policy_forbidden_actions(instance))
    errs.extend(policy_stage_candidate_gate(instance))
    if not skip_yaml_parity:
        errs.extend(policy_yaml_parity(root, instance))
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify worker trust registry JSON.")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--registry", type=Path, default=None, help="Override registry JSON path")
    ap.add_argument("--schema", type=Path, default=None, help="Override schema path")
    ap.add_argument(
        "--skip-yaml-parity",
        action="store_true",
        help="Skip parity check against config/runtime_workers/registry.yaml (tests only)",
    )
    args = ap.parse_args()

    errs = verify_worker_trust_registry(
        args.repo_root,
        args.registry,
        args.schema,
        skip_yaml_parity=args.skip_yaml_parity,
    )
    if errs:
        for line in errs:
            print(line, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
