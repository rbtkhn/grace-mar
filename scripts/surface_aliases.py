"""
Surface name migration helpers: canonical Record terms vs friendlier display labels.

- Canonical file: users/<id>/self-library.md
- Formal surface: SELF-LIBRARY (identity vs reference boundary unchanged)
- Display label: "Library" for customer-facing copy and optional export metadata
"""

from __future__ import annotations

# Map incoming legacy or alias strings to a single internal enum-like key.
SURFACE_ALIASES: dict[str, str] = {
    "SELF-LIBRARY": "LIBRARY",
    "SELF_LIBRARY": "LIBRARY",
    "LIBRARY": "LIBRARY",
}


def normalize_surface_token(name: str) -> str:
    key = name.strip().upper().replace("-", "_").replace(" ", "_")
    return SURFACE_ALIASES.get(key, key)


def library_export_labels() -> dict[str, str]:
    return {
        "canonical_surface": "SELF-LIBRARY",
        "display_name": "Library",
        "on_disk_file": "self-library.md",
    }
