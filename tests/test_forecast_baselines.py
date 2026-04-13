"""Smoke tests for forecast baseline metrics (no pandas required for pure functions)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from run_forecast_baselines import mae, mape, rmse  # noqa: E402


def test_mae_simple() -> None:
    assert mae([10.0, 20.0], [12.0, 18.0]) == 2.0


def test_rmse_simple() -> None:
    assert rmse([3.0, 4.0], [1.0, 2.0]) == pytest.approx(2.0)


def test_mape_skips_zero_actual() -> None:
    assert mape([0.0, 100.0], [10.0, 90.0]) == pytest.approx(10.0)


def test_import_observability_script() -> None:
    import build_forecast_observability_report  # noqa: F401
