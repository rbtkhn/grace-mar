# Provenance-backed gate staging

Runtime observations in `runtime/observations/index.jsonl` are **work memory**, not Record truth. When a companion or operator wants to propose a durable change, they can **stage** a reviewable candidate in `users/<id>/recursion-gate.md` with explicit lineage from selected observations.

This closes the loop: **search → timeline → expansion → staging → Approval Inbox → (optional) merge**.

## What staging answers

For each staged candidate, reviewers should be able to see:

1. **What change is being proposed?** — `proposal_summary`, `proposed_change`, `target_surface`, optional `target_path`.
2. **Which observations support it?** — `source_observation_ids`, `supporting_evidence_refs`, `timeline_anchor`.
3. **What contradictions or uncertainties remain?** — `contradiction_refs` (aggregated from observations; not silently dropped).
4. **Why consider this for the Record (or a work surface) at all?** — `why_now`, `review_notes`, `confidence`.

## Command

```bash
python3 scripts/runtime/stage_candidate_from_observations.py \
  -u grace-mar \
  --lane work-strategy \
  --candidate-type skill_update \
  --target-surface SKILLS \
  --target-path skills-portable/skill-strategy.md \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --id obs_20260413T191455Z_e5f6g7h8 \
  --proposal-summary "Refine skill-strategy notebook writing boundary" \
  --proposed-change "Skill-strategy should write compact notebook-linked summaries and avoid raw prose dumps into strategy-notebook." \
  --why-now "Multiple recent observations converge on cleaner notebook integration as a recurring need."
```

- **`--proposal-summary`** (alias **`--summary`**) — one line for the gate header and YAML `summary`.
- **`--id` / `--obs-id`** — repeat for multiple observations (required: at least one).
- **`--lane`** — required; every selected observation must match this lane unless **`--allow-mixed-lane`**.
- **`--timeline-anchor`** — optional; defaults to the **earliest** selected observation by timestamp.
- **`--confidence`** — optional override; otherwise the mean of numeric `confidence` values on the selected rows.

The script validates a structured payload against [`schema-registry/recursion-gate-candidate.schema.json`](../../schema-registry/recursion-gate-candidate.schema.json) when `jsonschema` is installed (see `requirements-dev.txt`).

## On-disk shape

Staging inserts a standard gate block: **`### CANDIDATE-NNNN`** with fenced **`yaml`**, `status: pending`, and **`proposal_class: RUNTIME_OBSERVATION_PROPOSAL`**. This matches the merge pipeline’s parser; it is **not** a separate `cand_*` prose format.

**Why `CANDIDATE-NNNN` (not timestamped IDs in the schema):** rationale and alternatives are documented in [memory-retrieval.md](memory-retrieval.md) (gate candidate and schema identifiers).

## Merge behavior

Candidates with **`proposal_class: RUNTIME_OBSERVATION_PROPOSAL`** are **not** auto-merged into SELF, EVIDENCE, or `bot/prompt.py`. When approved, `process_approved_candidates.py` moves the block to **Processed** and prints a reminder to **apply the change manually** to the intended surface (SKILLS, SELF-LIBRARY, etc.). See [`process_approved_candidates.py`](../../scripts/process_approved_candidates.py) (same pattern as `META_INFRA` for non-Record infra proposals).

## Non-goals

- Does **not** edit `self.md`, `self-skills.md`, `self-archive.md`, SELF-LIBRARY paths, or `bot/prompt.py`.
- Does **not** approve or merge; companion review and merge tooling still apply.
- Does **not** infer proposals from a search query alone — you pass explicit **`--id`** values.

## See also

- [memory-retrieval.md](memory-retrieval.md) — search, timeline, expansion.
- [observation-expansion.md](observation-expansion.md) — bounded expansion after narrowing.
- [runtime-vs-record.md](../runtime-vs-record.md) — runtime vs governed Record.
- [governance-unbundling.md](../governance-unbundling.md) — staging vs sensemaking vs merge accountability.
