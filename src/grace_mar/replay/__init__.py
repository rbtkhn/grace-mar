"""Harness replay synthesis: load audit JSONL, correlate, report, heuristic provenance."""

from grace_mar.replay.loaders import (
    AuditPaths,
    load_compute_ledger,
    load_fork_lineage,
    load_fork_manifest_raw,
    load_harness_events,
    load_merge_receipts,
    load_pipeline_events,
    read_jsonl,
)
from grace_mar.replay.report import build_report
from grace_mar.replay.synthesis import (
    build_replay_events,
    classify_pipeline_row_provenance,
    infer_answer_provenance,
    replay_provenance_summary,
    write_replay_artifacts,
)

__all__ = [
    "AuditPaths",
    "build_replay_events",
    "build_report",
    "classify_pipeline_row_provenance",
    "infer_answer_provenance",
    "load_compute_ledger",
    "load_fork_lineage",
    "load_fork_manifest_raw",
    "load_harness_events",
    "load_merge_receipts",
    "load_pipeline_events",
    "read_jsonl",
    "replay_provenance_summary",
    "write_replay_artifacts",
]
