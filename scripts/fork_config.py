"""Load optional operator thresholds from config/fork-config.json (not part of the Record)."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FORK_CONFIG_PATH = REPO_ROOT / "config" / "fork-config.json"


def load_fork_config() -> dict:
    if not FORK_CONFIG_PATH.is_file():
        return {}
    try:
        data = json.loads(FORK_CONFIG_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}
