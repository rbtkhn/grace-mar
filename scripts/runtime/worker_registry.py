"""
Load and validate config/runtime_workers/registry.yaml (WORK only).

Does not execute entrypoints — validates repo-relative paths exist.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_REGISTRY_REL = Path("config/runtime_workers/registry.yaml")


def registry_path(repo_root: Path | None = None) -> Path:
    root = repo_root.resolve() if repo_root else REPO_ROOT
    return (root / _REGISTRY_REL).resolve()


def load_registry(repo_root: Path | None = None) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as e:  # pragma: no cover
        raise SystemExit("PyYAML is required to load the worker registry") from e

    path = registry_path(repo_root)
    if not path.is_file():
        raise FileNotFoundError(f"worker registry missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("registry root must be a mapping")
    return data


def validate_entrypoints(repo_root: Path, registry: dict[str, Any]) -> None:
    root = repo_root.resolve()
    for section in ("shared_workers", "routed_workers"):
        block = registry.get(section)
        if not isinstance(block, dict):
            raise ValueError(f"registry.{section} must be a mapping")
        for wid, meta in block.items():
            if not isinstance(meta, dict):
                raise ValueError(f"registry.{section}.{wid} must be a mapping")
            ep = meta.get("entrypoint")
            if not ep or not isinstance(ep, str):
                raise ValueError(f"registry.{section}.{wid} missing entrypoint string")
            p = (root / ep.strip()).resolve()
            if not p.is_file():
                raise FileNotFoundError(f"registry entrypoint not found: {ep}")


def get_shared_workers(registry: dict[str, Any]) -> dict[str, Any]:
    sw = registry.get("shared_workers")
    if not isinstance(sw, dict):
        raise ValueError("registry.shared_workers must be a mapping")
    return sw


def get_routed_workers(registry: dict[str, Any]) -> dict[str, Any]:
    rw = registry.get("routed_workers")
    if not isinstance(rw, dict):
        raise ValueError("registry.routed_workers must be a mapping")
    return rw


def get_shared_worker_defs(registry: dict[str, Any]) -> dict[str, Any]:
    """Alias for :func:`get_shared_workers` (plan / doc naming)."""
    return get_shared_workers(registry)


def get_routed_worker_def(name: str, registry: dict[str, Any]) -> dict[str, Any]:
    """Return one routed worker block by registry key, or raise ``KeyError``."""
    rw = get_routed_workers(registry)
    if name not in rw:
        raise KeyError(f"unknown routed worker: {name!r}")
    return rw[name]
