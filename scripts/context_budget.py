#!/usr/bin/env python3
"""Operator scaffolding only; not Record truth — load JSON context budgets from config/."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
BUDGETS_DIR = REPO_ROOT / "config" / "context_budgets"


def load_context_budget(name: str) -> dict[str, Any]:
    path = BUDGETS_DIR / f"{name}.json"
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return raw if isinstance(raw, dict) else {}


def get_int(data: dict[str, Any], key: str, default: int) -> int:
    v = data.get(key, default)
    if isinstance(v, bool):
        return default
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, str):
        try:
            return int(v.strip(), 10)
        except ValueError:
            return default
    return default


def get_bool(data: dict[str, Any], key: str, default: bool) -> bool:
    v = data.get(key, default)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in {"true", "yes", "1", "on"}:
            return True
        if s in {"false", "no", "0", "off"}:
            return False
    return default
