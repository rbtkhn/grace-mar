"""Cached JSON loads for seed-phase / review validators (orjson + path-keyed LRU).

Import when run as ``python3 scripts/<tool>.py`` (``scripts/`` on sys.path):
``from cache import load_json_file, load_schema, clear_cache``.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import orjson

REPO_ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=None)
def _cached_json(path_key: str) -> object:
    return orjson.loads(Path(path_key).read_bytes())


def load_json_file(path: Path) -> object:
    """Load JSON from *path*; cached by resolved path (CLI one-shot safe)."""
    return _cached_json(str(path.resolve()))


def load_schema(rel_to_repo_root: str) -> object:
    """Load a repo-relative schema path (e.g. values from ``SCHEMA_BY_FILE``)."""
    return load_json_file(REPO_ROOT / rel_to_repo_root)


def clear_cache() -> None:
    _cached_json.cache_clear()
