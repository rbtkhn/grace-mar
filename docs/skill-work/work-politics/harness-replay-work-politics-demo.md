# Harness Event Replay — work-politics demonstration

This walks through **Harness Event Replay** on a **real work-politics candidate** already in `users/grace-mar/`. It shows how **audit lane** (`pipeline-events.jsonl`, `harness-events.jsonl`, `merge-receipts.jsonl`) lines up with **gate YAML** (`territory: work-politics`, `channel_key: operator:wap:*`) and **EVIDENCE** (`ACT-*`).

Full spec: [harness-replay-spec.md](../../harness-replay-spec.md) · CLI: [harness-replay.md](../../harness-replay.md).

---

## Command (work-politics example)

Use a candidate that was staged under **work-politics** with a Massie / KY lane `channel_key`:

```bash
python scripts/replay_harness_event.py -u grace-mar \
  --candidate CANDIDATE-0087 \
  --evidence ACT-0048
```

**CANDIDATE-0087** is the **triangulated analytical lenses** methodology milestone (`docs/skill-work/work-politics/analytical-lenses/`). **ACT-0048** is the evidence line tied to that merge.

Optional: append **runtime** context (large; redact before sharing):

```bash
python scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0087 --evidence ACT-0048 --transcript-snippet
```

---

## What you should see (structure)

| Section | work-politics signal |
|--------|------------|
| **recursion-gate.md (YAML)** | `territory: work-politics`, `channel_key: operator:wap:us-ky4-massie`, summary / `profile_target` |
| **pipeline-events.jsonl** | `intent_constitutional_critique` (pre-merge), **`applied`** rows with `channel_key: operator:wap:us-ky4-massie`, `proposal_class`, `surface` |
| **harness-events.jsonl** | `merge_applied` from `process_approved_candidates`, path to `merge-receipts.jsonl` |
| **merge-receipts.jsonl** | **`territory": "wap"`** (short token in JSON), `candidate_ids`, `checksum_before`, timestamps |
| **self-evidence.md** | Hint line for **`ACT-0048`** when `--evidence` is set |

That answers: *“Which harness steps touched this work-politics merge, and what did the gate say?”* — not *“what did the model think?”* (no full prompt in audit by default).

---

## Sample output (abridged, captured 2026-03-20)

Report header and gate excerpt (structure only — run the command above for full output):

```text
# Harness replay report
**User:** grace-mar
**Candidate:** CANDIDATE-0087

## recursion-gate.md (YAML block if present)
  status: approved
  channel_key: operator:wap:us-ky4-massie
  territory: work-politics
  summary: work-politics — triangulated analytical lenses …
  profile_target: IX-A. KNOWLEDGE
```

Pipeline rows include **intent_constitutional_critique** and **`applied`** with work-politics `channel_key` and `ACT-0048`. Harness lists **`merge_applied`** batches; receipts show **`territory": "wap"`** and paired candidate IDs (e.g. with CANDIDATE-0088 in the same batch).

---

## Newer ledger fields (envelope)

Merges **after** the pipeline envelope work add per-line metadata. When present in `pipeline-events.jsonl`, the same CLI shows an **Audit envelope** subsection and supports **`--event-id evt_…`** to jump from a pasted id:

- **`event_id`**, **`fork_id`**, **`envelope_version`**
- **`replay_mode`** (`proposal` / `merge` / `gate`, …)
- **`parent_event_id`** (links **`applied`** to the earlier **`staged`** row when both have ids)
- **`record_refs`** on **`applied`** (repo paths such as `users/grace-mar/self.md#IX-A`, `self-evidence.md`)

**Work-politics** rows are identifiable through **`channel_key`** / **`territory`** in the gate block and pipeline JSON — the envelope adds **stable ids** for tickets and replay.

---

## Related

- [README.md](README.md) — work-politics scope and gate rhythm
- [boundary-review-queue.md](../../boundary-review-queue.md) — where things should go vs replay (why they went there)
- `scripts/replay_harness_event.py` — implementation
