"""
Load audit-lane JSONL and related files with profile-root precedence over runtime-bundle.

Canonical live instance: read from ``users/<id>/*.jsonl`` first. If a file is missing or
empty, fall back to ``users/<id>/runtime-bundle/...`` mirrors (portable export layout).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def resolve_jsonl_path(primary: Path, bundle_fallback: Path) -> Path:
    """Prefer profile root; use runtime-bundle audit mirror when root missing or empty."""
    if _nonempty_file(primary):
        return primary
    if _nonempty_file(bundle_fallback):
        return bundle_fallback
    return primary


def resolve_path(primary: Path, bundle_fallback: Path) -> Path:
    """Prefer profile root file; fallback to bundle path if primary does not exist."""
    if primary.is_file():
        return primary
    if bundle_fallback.is_file():
        return bundle_fallback
    return primary


@dataclass(frozen=True)
class AuditPaths:
    """Resolved paths for one user profile directory."""

    user_dir: Path
    pipeline_events: Path
    harness_events: Path
    merge_receipts: Path
    compute_ledger: Path
    fork_lineage: Path
    fork_manifest: Path

    @classmethod
    def for_profile(cls, user_dir: Path) -> AuditPaths:
        bud = user_dir / "runtime-bundle"
        audit_b = bud / "audit"
        fh = bud / "fork-history"
        return cls(
            user_dir=user_dir,
            pipeline_events=resolve_jsonl_path(
                user_dir / "pipeline-events.jsonl",
                audit_b / "pipeline-events.jsonl",
            ),
            harness_events=resolve_jsonl_path(
                user_dir / "harness-events.jsonl",
                audit_b / "harness-events.jsonl",
            ),
            merge_receipts=resolve_jsonl_path(
                user_dir / "merge-receipts.jsonl",
                audit_b / "merge-receipts.jsonl",
            ),
            compute_ledger=resolve_jsonl_path(
                user_dir / "compute-ledger.jsonl",
                audit_b / "compute-ledger.jsonl",
            ),
            fork_lineage=resolve_jsonl_path(
                user_dir / "fork-lineage.jsonl",
                fh / "fork-lineage.jsonl",
            ),
            fork_manifest=resolve_path(
                user_dir / "fork-manifest.json",
                audit_b / "fork-manifest.json",
            ),
        )


def load_pipeline_events(user_dir: Path) -> list[dict[str, Any]]:
    return read_jsonl(AuditPaths.for_profile(user_dir).pipeline_events)


def load_merge_receipts(user_dir: Path) -> list[dict[str, Any]]:
    return read_jsonl(AuditPaths.for_profile(user_dir).merge_receipts)


def load_compute_ledger(user_dir: Path) -> list[dict[str, Any]]:
    return read_jsonl(AuditPaths.for_profile(user_dir).compute_ledger)


def load_harness_events(user_dir: Path) -> list[dict[str, Any]]:
    return read_jsonl(AuditPaths.for_profile(user_dir).harness_events)


def load_fork_lineage(user_dir: Path) -> list[dict[str, Any]]:
    return read_jsonl(AuditPaths.for_profile(user_dir).fork_lineage)


def load_fork_manifest_raw(user_dir: Path) -> dict[str, Any] | None:
    p = AuditPaths.for_profile(user_dir).fork_manifest
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


__all__ = [
    "AuditPaths",
    "load_compute_ledger",
    "load_fork_lineage",
    "load_fork_manifest_raw",
    "load_harness_events",
    "load_merge_receipts",
    "load_pipeline_events",
    "read_jsonl",
    "resolve_jsonl_path",
    "resolve_path",
]
