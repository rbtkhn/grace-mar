"""Worker registry and router (deterministic)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME = REPO_ROOT / "scripts" / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from worker_registry import (  # noqa: E402
    get_routed_worker_def,
    get_shared_worker_defs,
    load_registry,
    validate_entrypoints,
)
from worker_router import (  # noqa: E402
    TASK_TYPE_TO_ROUTED,
    UnknownTaskTypeError,
    resolve_routing,
)


def test_registry_loads_shared_and_routed_sections() -> None:
    reg = load_registry(REPO_ROOT)
    assert "shared_workers" in reg and isinstance(reg["shared_workers"], dict)
    assert "routed_workers" in reg and isinstance(reg["routed_workers"], dict)
    assert "provenance_checker" in reg["shared_workers"]
    assert "strategy_worker" in reg["routed_workers"]


def test_validate_entrypoints_succeeds() -> None:
    reg = load_registry(REPO_ROOT)
    validate_entrypoints(REPO_ROOT, reg)


def test_plan_named_helpers_match_blocks() -> None:
    reg = load_registry(REPO_ROOT)
    assert get_shared_worker_defs(reg) == reg["shared_workers"]
    assert get_routed_worker_def("strategy_worker", reg)["entrypoint"].endswith(
        "review_orchestrator.py"
    )


def test_router_strategy_resolves_expected_routed_and_shared() -> None:
    reg = load_registry(REPO_ROOT)
    rr = resolve_routing("strategy", REPO_ROOT, reg)
    assert rr.task_type == "strategy"
    assert rr.routed_worker_id == "strategy_worker"
    assert "provenance_checker" in rr.shared_worker_ids
    assert "strategy_worker" in rr.entrypoints
    assert rr.entrypoints["strategy_worker"].endswith("review_orchestrator.py")


def test_unknown_task_type_raises() -> None:
    reg = load_registry(REPO_ROOT)
    with pytest.raises(UnknownTaskTypeError):
        resolve_routing("not_a_type", REPO_ROOT, reg)
