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
