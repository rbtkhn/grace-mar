"""
Load config/runtime_workers/overlays.yaml — small mode defaults for the runtime worker.

Overlays are not a second router; task_type still resolves via worker_router.resolve_routing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from worker_router import TASK_TYPE_TO_ROUTED

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_OVERLAYS_REL = Path("config/runtime_workers/overlays.yaml")

# v1 overlay families (must match YAML top-level keys)
OVERLAY_NAMES = frozenset({"strategy", "moonshot", "research", "tacit"})

_EMPHASIS_KEYS = frozenset(
    {
        "emphasize_anchor",
        "emphasize_contradictions",
        "emphasize_mission_context",
        "emphasize_provenance",
        "emphasize_evidence_density",
        "emphasize_candidate_extraction",
        "emphasize_grounding",
    }
)


class UnknownOverlayError(KeyError):
    """Overlay name not in overlays.yaml."""


class OverlayConfigError(ValueError):
    """Invalid overlays.yaml structure or values."""


def overlays_path(repo_root: Path | None = None) -> Path:
    root = repo_root.resolve() if repo_root else REPO_ROOT
    return (root / _OVERLAYS_REL).resolve()


def load_overlays(repo_root: Path | None = None) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as e:  # pragma: no cover
        raise SystemExit("PyYAML is required to load runtime worker overlays") from e

    path = overlays_path(repo_root)
    if not path.is_file():
        raise FileNotFoundError(f"worker overlays missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise OverlayConfigError("overlays root must be a mapping")
    return data


def get_overlay(name: str, repo_root: Path | None = None) -> dict[str, Any]:
    raw = (name or "").strip().lower()
    if raw not in OVERLAY_NAMES:
        raise UnknownOverlayError(
            f"unknown overlay {name!r}; expected one of: {', '.join(sorted(OVERLAY_NAMES))}"
        )
    data = load_overlays(repo_root)
    block = data.get(raw)
    if not isinstance(block, dict):
        raise OverlayConfigError(f"overlay {raw!r} must be a mapping")
    _validate_overlay_block(raw, block)
    return block


def _validate_overlay_block(name: str, block: dict[str, Any]) -> None:
    tt = block.get("default_task_type")
    if tt is not None:
        tts = str(tt).strip().lower()
        if tts not in TASK_TYPE_TO_ROUTED:
            raise OverlayConfigError(
                f"overlay {name}: default_task_type {tts!r} must be one of "
                f"{', '.join(sorted(TASK_TYPE_TO_ROUTED))}"
            )
    for key in ("default_scope",):
        v = block.get(key)
        if v is not None and not isinstance(v, str):
            raise OverlayConfigError(f"overlay {name}: {key} must be a string")
    for key in ("max_files", "max_chars"):
        v = block.get(key)
        if v is not None and not isinstance(v, int):
            raise OverlayConfigError(f"overlay {name}: {key} must be an integer")
    for k, v in block.items():
        if k in _EMPHASIS_KEYS and v is not None and not isinstance(v, bool):
            raise OverlayConfigError(f"overlay {name}: {k} must be a boolean")


def emphasis_flags(overlay: dict[str, Any]) -> dict[str, bool]:
    """Return only emphasis keys that are explicitly true (inspectable, compact)."""
    out: dict[str, bool] = {}
    for k in _EMPHASIS_KEYS:
        if overlay.get(k) is True:
            out[k] = True
    return out


def apply_overlay_defaults(
    *,
    overlay: dict[str, Any] | None,
    scope: str | None,
    max_files: int | None,
    max_chars: int | None,
    task_type: str | None,
) -> tuple[str | None, int | None, int | None, str | None, list[str]]:
    """
    Fill Nones from overlay. Returns (scope, max_files, max_chars, task_type, applied_keys).

    Caller applies precedence: explicit CLI args should be passed as non-None to skip overlay.
    """
    if not overlay:
        return scope, max_files, max_chars, task_type, []

    applied: list[str] = []
    s, mf, mc, tt = scope, max_files, max_chars, task_type

    if s is None and overlay.get("default_scope"):
        s = str(overlay["default_scope"]).strip().lstrip("/")
        applied.append("scope")
    if mf is None and overlay.get("max_files") is not None:
        mf = int(overlay["max_files"])
        applied.append("max_files")
    if mc is None and overlay.get("max_chars") is not None:
        mc = int(overlay["max_chars"])
        applied.append("max_chars")
    if tt is None and overlay.get("default_task_type"):
        tt = str(overlay["default_task_type"]).strip().lower()
        applied.append("task_type")

    return s, mf, mc, tt, applied
