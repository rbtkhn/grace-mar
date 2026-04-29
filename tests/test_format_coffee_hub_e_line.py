"""Smoke tests for coffee hub **E** label line."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from cadence_conductor_resolution import format_coffee_hub_e_line  # noqa: E402


def test_format_coffee_hub_e_line_shape() -> None:
    assert format_coffee_hub_e_line("grace-mar") == "**E — Conductor**"
