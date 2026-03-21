"""Tests for recursion_gate_territory.normalize_territory_cli."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from recursion_gate_territory import (  # noqa: E402
    normalize_territory_cli,
    territory_cli_argparse_choices,
)


def test_normalize_maps_aliases_to_work_politics() -> None:
    assert normalize_territory_cli("wap") == "work-politics"
    assert normalize_territory_cli("WAP") == "work-politics"
    assert normalize_territory_cli("wp") == "work-politics"
    assert normalize_territory_cli("work-politics") == "work-politics"


def test_normalize_leaves_companion_and_all() -> None:
    assert normalize_territory_cli("companion") == "companion"
    assert normalize_territory_cli("all") == "all"


def test_argparse_choices_include_aliases() -> None:
    assert "work-politics" in territory_cli_argparse_choices()
    assert "wap" in territory_cli_argparse_choices()
