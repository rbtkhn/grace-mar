"""Shared helpers: chapter lists across Volume I and nested volume_* YAML blocks."""
from __future__ import annotations

from typing import Any

# Nested book queues in metadata/book-architecture.yaml (not top-level `book`).
VOLUME_BLOCK_KEYS = (
    "volume_2_civilization",
    "volume_4_game_theory",
    "volume_7_essays",
)


def top_level_chapters(arch: dict[str, Any]) -> list[dict[str, Any]]:
    return list((arch.get("book") or {}).get("chapters") or [])


def chapters_for_volume_block(arch: dict[str, Any], block_key: str) -> list[dict[str, Any]]:
    vol = arch.get(block_key) or {}
    return list((vol.get("book") or {}).get("chapters") or [])


def all_volume_block_chapters(arch: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for key in VOLUME_BLOCK_KEYS:
        out.extend(chapters_for_volume_block(arch, key))
    return out


def all_chapters_flat(arch: dict[str, Any]) -> list[dict[str, Any]]:
    """Volume I (top-level `book.chapters`) plus every `volume_*.book.chapters`."""
    return top_level_chapters(arch) + all_volume_block_chapters(arch)


def chapter_by_id(arch: dict[str, Any], chapter_id: str) -> dict[str, Any] | None:
    for c in all_chapters_flat(arch):
        if c.get("id") == chapter_id:
            return c
    return None


def all_chapter_ids(arch: dict[str, Any]) -> set[str]:
    return {c["id"] for c in all_chapters_flat(arch) if c.get("id")}
