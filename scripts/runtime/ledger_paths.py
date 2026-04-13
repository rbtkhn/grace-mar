"""Shared paths for runtime observation tooling."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def ledger_base() -> Path:
    if os.environ.get("GRACE_MAR_RUNTIME_LEDGER_ROOT"):
        return Path(os.environ["GRACE_MAR_RUNTIME_LEDGER_ROOT"]).resolve()
    return REPO_ROOT


def observations_dir() -> Path:
    return ledger_base() / "runtime" / "observations"


def observations_jsonl() -> Path:
    return observations_dir() / "index.jsonl"


def runtime_observation_schema() -> Path:
    return REPO_ROOT / "schema-registry" / "runtime-observation.v1.json"
