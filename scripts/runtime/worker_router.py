"""
Explicit task_type → routed worker mapping (no probabilistic routing).

Uses worker_registry.load_registry + validate_entrypoints.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from worker_registry import get_routed_workers, get_shared_workers, load_registry, validate_entrypoints

# task_type (CLI) → routed_workers key in registry.yaml
TASK_TYPE_TO_ROUTED: dict[str, str] = {
    "strategy": "strategy_worker",
    "tacit": "tacit_worker",
    "moonshot": "moonshot_worker",
    "contradiction": "contradiction_worker",
    "research": "research_worker",
}


@dataclass(frozen=True)
class RoutingResult:
    task_type: str
    routed_worker_id: str
    routed_entrypoint: str
    shared_worker_ids: tuple[str, ...]
    entrypoints: dict[str, str]  # worker_id -> repo-relative path


class UnknownTaskTypeError(ValueError):
    """No routed worker for this task_type."""


def resolve_routing(task_type: str, repo_root: Path, registry: dict[str, Any] | None = None) -> RoutingResult:
    tt = (task_type or "").strip().lower()
    if tt not in TASK_TYPE_TO_ROUTED:
        known = ", ".join(sorted(TASK_TYPE_TO_ROUTED))
        raise UnknownTaskTypeError(f"unknown task_type {task_type!r}; expected one of: {known}")

    root = repo_root.resolve()
    reg = registry if registry is not None else load_registry(root)
    validate_entrypoints(root, reg)

    routed_id = TASK_TYPE_TO_ROUTED[tt]
    routed_block = get_routed_workers(reg)
    if routed_id not in routed_block:
        raise KeyError(f"routed worker {routed_id!r} missing from registry")

    shared = get_shared_workers(reg)
    shared_ids = tuple(sorted(shared.keys()))

    entrypoints: dict[str, str] = {}
    for sid in shared_ids:
        entrypoints[sid] = str(shared[sid]["entrypoint"])
    entrypoints[routed_id] = str(routed_block[routed_id]["entrypoint"])

    ep = str(routed_block[routed_id]["entrypoint"])
    return RoutingResult(
        task_type=tt,
        routed_worker_id=routed_id,
        routed_entrypoint=ep,
        shared_worker_ids=shared_ids,
        entrypoints=dict(sorted(entrypoints.items())),
    )


def routing_receipt_payload(
    *,
    run_id: str,
    result: RoutingResult,
    status: str = "resolved",
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "task_type": result.task_type,
        "routed_worker": result.routed_worker_id,
        "shared_workers": list(result.shared_worker_ids),
        "entrypoints": result.entrypoints,
        "status": status,
        "non_canonical": True,
    }
