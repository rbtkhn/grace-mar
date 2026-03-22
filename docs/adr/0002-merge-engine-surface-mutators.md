# ADR 0002 — Surface-aware merge mutators (IX, EVIDENCE, prompt projection)

**Status:** Implemented (phase 1)  
**Date:** 2026-03-22  
**Supersedes:** ad-hoc string patches only in `process_approved_candidates.py`

## Context

Pipeline merges used regex splice for `self.md` IX-A/B/C YAML blocks, ACT fragments in `self-evidence.md`, and line append for `bot/prompt.py`. That is safe but not semantically named, hard to test in isolation, and blocks richer behavior (READ/WRITE routing, optional IX-driven prompt sync).

## Decision

1. **Centralize** merge mutations in **`src/grace_mar/merge/`**:
   - **`self_ix.py`** — insert LEARN/CUR/PER list items into the fenced IX YAML blocks (same on-disk shape as before).
   - **`evidence_log.py`** — insert structured ACT lines before `## VI. ATTESTATION LOG`; optional hooks for READ/WRITE when candidates carry `evidence_record_type`.
   - **`prompt_sync.py`** — preserve `_insert_prompt_addition` behavior; add **opt-in** `prompt_merge_mode: rebuild_ix` to rebuild YOUR KNOWLEDGE / CURIOSITY / PERSONALITY bullet lists from `topic:` / `observation:` lines in `self.md` IX blocks (canonical projection, not unbounded append growth).

2. **`process_approved_candidates.py`** calls these modules so behavior stays **one place** and unit-testable.

3. **Non-goals (phase 1):** Full YAML round-trip for entire `self-evidence.md`; automatic READ list parsing without companion-approved schema; changing default prompt behavior without `rebuild_ix` on the candidate.

## Consequences

- Operators can add `prompt_merge_mode: rebuild_ix` to a candidate when they want the Voice sections to **track** IX list entries (use sparingly — narrative bullets are replaced by IX-derived lines for those sections).
- Future work: typed `ActivityRecord` for READ/WRITE paths and PRP export driven off the same structures.
