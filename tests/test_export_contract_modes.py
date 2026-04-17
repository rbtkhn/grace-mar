"""Validate that the export contract is consistent with existing export infrastructure."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

EXPORT_CONTRACT = REPO / "docs" / "portable-record" / "export-contract.md"
EXPORT_CLI = REPO / "scripts" / "export.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_export_contract_exists():
    assert EXPORT_CONTRACT.is_file(), "export-contract.md must exist"


def test_export_contract_references_all_subcommands():
    """The contract doc should mention every unified CLI subcommand."""
    contract = _read(EXPORT_CONTRACT)
    for sub in ("fork", "prp", "identity", "manifest", "bundle"):
        assert sub in contract, f"export-contract.md should reference subcommand '{sub}'"


def test_export_contract_defines_all_classes():
    """Five export classes should be named in the contract."""
    contract = _read(EXPORT_CONTRACT)
    for cls in (
        "Full governed profile",
        "Task-limited profile",
        "Tool bootstrap profile",
        "Demonstrated capability profile",
        "Internal-only",
    ):
        assert cls in contract, f"export-contract.md should define class '{cls}'"


def test_export_contract_references_four_surfaces():
    contract = _read(EXPORT_CONTRACT)
    for surface in ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE"):
        assert surface in contract, f"export-contract.md should reference surface '{surface}'"


def test_export_contract_no_raw_dump_language():
    """The contract must not imply unfiltered exports."""
    contract = _read(EXPORT_CONTRACT)
    for phrase in ("raw dump", "memory dump", "unfiltered export"):
        lower = contract.lower()
        occurrences = lower.count(phrase)
        negated = lower.count(f"not {phrase}") + lower.count(f"not raw memory dump")
        assert occurrences <= negated, (
            f"export-contract.md uses '{phrase}' without negation — "
            "exports must be framed as governed views"
        )


def test_export_cli_references_contract():
    """export.py docstring should point to the export contract doc."""
    cli = _read(EXPORT_CLI)
    assert "export-contract" in cli, "export.py should reference export-contract.md"


def test_runtime_modes_mentioned_in_contract():
    """The contract should mention existing runtime bundle modes."""
    contract = _read(EXPORT_CONTRACT)
    assert "portable_bundle_only" in contract
    assert "adjunct_runtime" in contract
