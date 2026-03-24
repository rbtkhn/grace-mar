# Multi-Agent Collaboration — work-jiang conventions

This document governs how multiple agents (AI or human) work on the Predictive History book project in parallel without stepping on each other.

---

## Task lifecycle

Every unit of work is a **task** tracked in [`tasks.jsonl`](tasks.jsonl). A task moves through these states:

```
available → claimed → submitted → merged
                  ↘ cancelled
```

Each transition is an append to `tasks.jsonl` via `emit_task_event.py`. The current state of any task is the latest event for its `task_id`.

### Commands

```bash
# See all tasks and their status
python3 scripts/work_jiang/emit_task_event.py list
python3 scripts/work_jiang/emit_task_event.py list --status available

# Claim a task
python3 scripts/work_jiang/emit_task_event.py claim draft-ch07 --agent agent-b

# Submit completed work
python3 scripts/work_jiang/emit_task_event.py submit draft-ch07

# Seed tasks from book architecture (idempotent)
python3 scripts/work_jiang/seed_task_manifest.py
```

---

## Agent roles

| Role | Task type | Reads | Produces | Parallelism |
|------|-----------|-------|----------|-------------|
| Research | `chapter_analysis` | Lecture transcript, outline | Analysis memo | Per-chapter, fully parallel |
| Drafter | `chapter_draft` | Transcript, analysis, outline, prev chapter draft | Chapter draft + prediction extractions | Per-chapter; sequential within volume for arc |
| ASR | `transcript_normalize`, `asr_audit` | Raw/curated transcripts | Normalized transcript, proposed replacement rules | Per-lecture, parallel; merge rules sequentially |
| Scorer | `prediction_score` | Chapter draft, prediction registry | Scored predictions | Per-chapter, fully parallel |
| Divergence | `divergence_check` | Chapter draft, divergence registry | Divergence entries | Per-chapter, fully parallel |
| Pedagogy | `pedagogy_analysis` | Lecture transcripts (cross-series) | Pedagogical method notes | Cross-cutting, read-only |

---

## Context packs

Before starting work, assemble the minimal file set:

```bash
python3 scripts/work_jiang/assemble_context_pack.py --task draft-ch07 -o /tmp/ch07-ctx/
python3 scripts/work_jiang/assemble_context_pack.py --chapter ch07 -o /tmp/ch07-ctx/
python3 scripts/work_jiang/assemble_context_pack.py --lecture "secret-history-08-*" -o /tmp/sh08-ctx/
```

The output directory contains only what the agent needs, plus a `CONTEXT-MANIFEST.md` listing what was included and why.

---

## Branch naming

When working on a branch (recommended for any task that modifies shared files):

```
work-jiang/<task_id>
```

Examples: `work-jiang/draft-ch07`, `work-jiang/asr-sh08`, `work-jiang/predictions-ch03`.

---

## Review queue

All agent-produced content goes to [`review-queue/`](review-queue/) before entering canonical locations.

```
review-queue/
  ch07/
    draft.md
    predictions.json
    notes.md
  asr/
    replacements-sh08.txt
```

### Promotion

```bash
# Preview
python3 scripts/work_jiang/promote_from_review_queue.py ch07 --dry-run

# Promote
python3 scripts/work_jiang/promote_from_review_queue.py ch07 --approve

# List pending
python3 scripts/work_jiang/promote_from_review_queue.py --list
```

Promotion moves files to canonical locations, archives the originals, and marks the task as merged.

---

## Shared mutable files

Some files are shared across tasks. Rules for each:

| File | Policy |
|------|--------|
| `asr_transcript_replacements.py` | Propose additions as `review-queue/asr/replacements-<scope>.txt`. Operator merges manually. Never edit directly from a task branch. |
| `prediction-tracking/registry/predictions.jsonl` | Stage via `prediction-tracking/staging/`. Operator appends after review. |
| `divergence-tracking/registry/divergences.jsonl` | Stage via `divergence-tracking/staging/`. Operator appends after review. |
| `metadata/book-architecture.yaml` | Operator-only. Agents do not modify. |
| `tasks.jsonl` | Append-only. Multiple agents can append simultaneously; conflicts are resolved by timestamp (first claim wins). |

---

## What can be direct-merged (no review queue)

- Transcript normalization using **existing** replacement rules (no new rules added)
- Influence-tracking snapshots (append-only JSONL)
- Context packs (ephemeral, not committed)

Everything else goes through review-queue.

---

## Conflict resolution

- **Task claims:** First `claimed` event wins. If two agents claim the same task, the earlier timestamp takes precedence.
- **Competing submissions:** If two agents submit work for the same scope, the operator chooses which to promote.
- **ASR rules:** Proposed rules are reviewed for false-positive risk before merging. The operator is the merge authority.

---

## Post-merge validation

After promoting content, run the consistency validator:

```bash
python3 scripts/work_jiang/validate_book_consistency.py --volume 1
python3 scripts/work_jiang/validate_book_consistency.py --chapter ch07
python3 scripts/work_jiang/validate_book_consistency.py --all
```

This checks prediction ID integrity, cross-references, transcript citations, and task manifest health.

---

## Related

- [`tasks.jsonl`](tasks.jsonl) — task manifest (append-only)
- [`review-queue/README.md`](review-queue/README.md) — staging conventions
- [`metadata/book-architecture.yaml`](metadata/book-architecture.yaml) — chapter definitions (SSOT)
- [`WORKFLOW-transcripts.md`](WORKFLOW-transcripts.md) — transcript pipeline
