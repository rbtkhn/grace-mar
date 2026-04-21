"""Model tier policy resolver (runtime-only YAML)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Ensure runtime scripts on path
import sys

sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
from model_policy import resolve_model_policy  # noqa: E402


def test_strategy_quick_scan_tier_b() -> None:
    r = resolve_model_policy(
        repo_root=REPO_ROOT,
        task_type="strategy",
        task_subtype="quick_scan",
    )
    assert r["allowed_tier"] == "B"
    assert r["fallback_chain"] == ["B", "A"]
    assert r["requires_human_review"] is False


def test_strategy_contradiction_review_tier_c() -> None:
    r = resolve_model_policy(
        repo_root=REPO_ROOT,
        task_type="strategy",
        task_subtype="contradiction_review",
    )
    assert r["allowed_tier"] == "C"


def test_forbidden_action_merge_record_tier_x() -> None:
    r = resolve_model_policy(
        repo_root=REPO_ROOT,
        task_type="strategy",
        task_subtype=None,
        action="merge_record",
    )
    assert r["allowed_tier"] == "X"
    assert r["fallback_chain"] == []
    assert r["resolved_provider"] is None
    assert r["resolved_model"] is None
    assert r["requires_human_review"] is True


def test_unknown_task_type_tier_a() -> None:
    r = resolve_model_policy(repo_root=REPO_ROOT, task_type=None)
    assert r["allowed_tier"] == "A"
