"""
Record surface registry: internal machine keys, on-disk stems, display labels, legacy aliases.

- Canonical EVIDENCE body: users/<id>/self-archive.md (not self-evidence.md; pointer optional).
- SELF-KNOWLEDGE (IX-A/B/C) primarily lives in self.md — self_knowledge is a logical export bucket.
- Display names (Library, Skills, Evidence, Memory) are for customer-facing copy; see README + docs/glossary.md.
- Self-memory on disk: **self-memory.md**; legacy **memory.md** remains readable via `legacy_file_stems`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

# Map incoming legacy or alias strings to a single internal enum-like token (legacy API).
SURFACE_ALIASES: dict[str, str] = {
    "SELF-LIBRARY": "LIBRARY",
    "SELF_LIBRARY": "LIBRARY",
    "LIBRARY": "LIBRARY",
}


@dataclass(frozen=True)
class SurfaceDef:
    canonical_key: str
    canonical_file_stem: str | None  # None = logical-only (no dedicated .md)
    display_name: str
    legacy_keys: tuple[str, ...] = ()
    legacy_file_stems: tuple[str, ...] = ()


# Keyed by canonical_key for stable lookup.
SURFACES: Dict[str, SurfaceDef] = {
    "self": SurfaceDef(
        canonical_key="self",
        canonical_file_stem="self",
        display_name="Self",
    ),
    "self_knowledge": SurfaceDef(
        canonical_key="self_knowledge",
        canonical_file_stem=None,
        display_name="Self-Knowledge",
        legacy_keys=("knowledge",),
    ),
    "self_library": SurfaceDef(
        canonical_key="self_library",
        canonical_file_stem="self-library",
        display_name="Library",
        legacy_keys=("library",),
        legacy_file_stems=("library",),
    ),
    "self_skills": SurfaceDef(
        canonical_key="self_skills",
        canonical_file_stem="self-skills",
        display_name="Skills",
        legacy_keys=("skills",),
        legacy_file_stems=("skills",),
    ),
    "self_evidence": SurfaceDef(
        canonical_key="self_evidence",
        canonical_file_stem="self-archive",
        display_name="Evidence",
        legacy_keys=("evidence",),
        # body is self-archive.md; self-evidence.md is optional pointer (handled in repo_io resolve)
        legacy_file_stems=(),
    ),
    "self_memory": SurfaceDef(
        canonical_key="self_memory",
        canonical_file_stem="self-memory",
        display_name="Memory",
        legacy_keys=("memory",),
        legacy_file_stems=("memory",),
    ),
}


def get_surface_by_key(key: str) -> Optional[SurfaceDef]:
    k = (key or "").strip().lower().replace("-", "_")
    if k in SURFACES:
        return SURFACES[k]
    for surface in SURFACES.values():
        if k == surface.canonical_key or k in tuple(x.lower() for x in surface.legacy_keys):
            return surface
    return None


def get_surface_by_file_stem(stem: str) -> Optional[SurfaceDef]:
    s = (stem or "").strip().lower()
    if not s:
        return None
    for surface in SURFACES.values():
        if surface.canonical_file_stem and s == surface.canonical_file_stem.lower():
            return surface
        if s in tuple(x.lower() for x in surface.legacy_file_stems):
            return surface
    return None


def display_name_for(key: str) -> str:
    surface = get_surface_by_key(key)
    return surface.display_name if surface else key


def canonical_key_for(key: str) -> str:
    surface = get_surface_by_key(key)
    return surface.canonical_key if surface else key


def canonical_file_stem_for(stem_or_key: str) -> str | None:
    surface = get_surface_by_key(stem_or_key) or get_surface_by_file_stem(stem_or_key)
    return surface.canonical_file_stem if surface else None


def normalize_surface_token(name: str) -> str:
    """Legacy token normalizer for SELF-LIBRARY display family (returns LIBRARY)."""
    key = name.strip().upper().replace("-", "_").replace(" ", "_")
    return SURFACE_ALIASES.get(key, key)


def library_export_labels() -> dict[str, str]:
    """Backward-compatible export metadata for SELF-LIBRARY / Library."""
    lib = SURFACES["self_library"]
    assert lib.canonical_file_stem is not None
    return {
        "canonical_surface": "SELF-LIBRARY",
        "display_name": lib.display_name,
        "on_disk_file": f"{lib.canonical_file_stem}.md",
    }


def surface_export_labels(canonical_key: str) -> dict[str, str] | None:
    """Export metadata for any surface with an on-disk file."""
    s = get_surface_by_key(canonical_key)
    if not s or not s.canonical_file_stem:
        return None
    formal = canonical_key.upper().replace("_", "-")
    return {
        "canonical_surface": formal,
        "display_name": s.display_name,
        "on_disk_file": f"{s.canonical_file_stem}.md",
    }
