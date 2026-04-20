"""Runtime worker overlays — load and apply_overlay_defaults."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME = REPO_ROOT / "scripts" / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from worker_overlays import (  # noqa: E402
    UnknownOverlayError,
    apply_overlay_defaults,
    get_overlay,
    load_overlays,
)


def test_overlays_yaml_contains_four_families() -> None:
    data = load_overlays(REPO_ROOT)
    for name in ("strategy", "moonshot", "research", "tacit"):
        assert name in data and isinstance(data[name], dict)


def test_strategy_overlay_default_task_and_scope() -> None:
    ov = get_overlay("strategy", REPO_ROOT)
    assert ov["default_task_type"] == "strategy"
    assert "strategy-notebook" in ov["default_scope"]
    assert ov["max_files"] == 250


def test_apply_overlay_defaults_fills_nones() -> None:
    ov = get_overlay("strategy", REPO_ROOT)
    s, mf, mc, tt, applied = apply_overlay_defaults(
        overlay=ov,
        scope=None,
        max_files=None,
        max_chars=None,
        task_type=None,
    )
    assert s and "strategy-notebook" in s
    assert mf == 250 and mc == 150_000
    assert tt == "strategy"
    assert set(applied) == {"scope", "max_files", "max_chars", "task_type"}


def test_explicit_args_override_overlay() -> None:
    ov = get_overlay("strategy", REPO_ROOT)
    s, mf, mc, tt, applied = apply_overlay_defaults(
        overlay=ov,
        scope="research",
        max_files=8,
        max_chars=12000,
        task_type="contradiction",
    )
    assert s == "research" and mf == 8 and mc == 12000 and tt == "contradiction"
    assert applied == []


def test_unknown_overlay_raises() -> None:
    with pytest.raises(UnknownOverlayError):
        get_overlay("not_an_overlay", REPO_ROOT)
