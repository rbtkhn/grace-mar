"""Load runtime observations from index.jsonl (read-only)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

import ledger_paths  # noqa: E402


def iter_observations() -> Iterator[dict]:
    path = ledger_paths.observations_jsonl()
    if not path.is_file():
        return
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def load_all() -> list[dict]:
    return list(iter_observations())


def by_id(obs_id: str) -> dict | None:
    for row in iter_observations():
        if row.get("obs_id") == obs_id:
            return row
    return None
