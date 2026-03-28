"""Surface alias normalization (SELF-LIBRARY / Library display migration)."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_normalize_surface_token_library_variants() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from surface_aliases import normalize_surface_token

    assert normalize_surface_token("SELF-LIBRARY") == "LIBRARY"
    assert normalize_surface_token("SELF_LIBRARY") == "LIBRARY"
    assert normalize_surface_token("LIBRARY") == "LIBRARY"
    assert normalize_surface_token("Library") == "LIBRARY"
    assert normalize_surface_token("self library") == "LIBRARY"
    assert normalize_surface_token("Self-Library") == "LIBRARY"
    assert normalize_surface_token("library") == "LIBRARY"


def test_normalize_surface_unknown_passthrough() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from surface_aliases import normalize_surface_token

    assert normalize_surface_token("OTHER_SURFACE") == "OTHER_SURFACE"


def test_get_surface_by_key_and_legacy() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from surface_aliases import SURFACES, get_surface_by_key

    assert get_surface_by_key("self_skills") is SURFACES["self_skills"]
    assert get_surface_by_key("skills") is SURFACES["self_skills"]
    assert get_surface_by_key("self-evidence") is SURFACES["self_evidence"]
    assert get_surface_by_key("evidence") is SURFACES["self_evidence"]
    assert get_surface_by_key("knowledge") is SURFACES["self_knowledge"]
    assert get_surface_by_key("unknown_xyz") is None


def test_get_surface_by_file_stem() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from surface_aliases import get_surface_by_file_stem

    assert get_surface_by_file_stem("self-archive") is not None
    assert get_surface_by_file_stem("self-archive").canonical_key == "self_evidence"
    assert get_surface_by_file_stem("skills") is not None
    assert get_surface_by_file_stem("skills").canonical_key == "self_skills"
    assert get_surface_by_file_stem("self-skills") is not None
    assert get_surface_by_file_stem("self-skills").canonical_key == "self_skills"


def test_display_and_canonical_helpers() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from surface_aliases import (
        canonical_file_stem_for,
        canonical_key_for,
        display_name_for,
        library_export_labels,
    )

    assert display_name_for("self_skills") == "Skills"
    assert display_name_for("skills") == "Skills"
    assert canonical_key_for("skills") == "self_skills"
    assert canonical_file_stem_for("self_skills") == "self-skills"
    assert canonical_file_stem_for("skills") == "self-skills"
    assert canonical_file_stem_for("self_knowledge") is None

    lib = library_export_labels()
    assert lib["display_name"] == "Library"
    assert lib["on_disk_file"] == "self-library.md"
    assert lib["canonical_surface"] == "SELF-LIBRARY"
