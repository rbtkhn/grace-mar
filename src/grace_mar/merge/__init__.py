"""Surface-aware merge mutators for self.md, self-archive.md (EVIDENCE), and prompt projection."""

from grace_mar.merge.boundary_classifier import (
    build_boundary_classification,
    sync_boundary_classification_artifact,
    write_boundary_classification,
)
from grace_mar.merge.evidence_log import append_act_entry, insert_reading_list_entry, upsert_reading_list_entry
from grace_mar.merge.prompt_sync import insert_prompt_addition, rebuild_observation_sections_from_self
from grace_mar.merge.self_ix import insert_ix_c_entry, insert_ix_b_entry, insert_ix_a_entry

__all__ = [
    "append_act_entry",
    "build_boundary_classification",
    "insert_ix_a_entry",
    "insert_ix_b_entry",
    "insert_ix_c_entry",
    "insert_prompt_addition",
    "insert_reading_list_entry",
    "rebuild_observation_sections_from_self",
    "sync_boundary_classification_artifact",
    "upsert_reading_list_entry",
    "write_boundary_classification",
]
