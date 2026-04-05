# Change Review Validation

Companion-Self template — validation rules for contradiction and change-review artifacts.

---

## Purpose

This document explains how to validate the change-review subsystem artifacts.

**Dependencies:** `validate-change-review.py` uses **`jsonschema`** (same stack as `validate-seed-phase.py`). Install with `pip install -r scripts/requirements-seed-phase.txt` unless your environment already provides `jsonschema`.

Validation exists to ensure that:

- review artifacts conform to their JSON Schemas
- queue and event-log references are coherent
- decisions point to real proposals
- proposals point to real governed-state artifacts where applicable
- the template scaffold remains structurally correct
- the demo remains a working example

---

## Validator

Use:

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-change-review.py users/demo/review-queue
python3 scripts/validate-change-review.py users/_template/review-queue --allow-empty
python3 scripts/validate-change-review.py users/<fork_id>/review-queue --allow-missing-decisions
```

### What the validator checks

#### 1. Required paths exist

The validator expects:

- `change_review_queue.json`
- `change_event_log.json`
- `proposals/`
- `decisions/`
- `diffs/`

#### 2. JSON files validate against schemas

The validator checks:

- `change_review_queue.json` against `schema-registry/change-review-queue.v1.json`
- `change_event_log.json` against `schema-registry/change-event-log.v1.json`
- proposal files against `schema-registry/change-proposal.v1.json`
- decision files against `schema-registry/change-decision.v1.json`
- diff files against `schema-registry/identity-diff.v1.json`

**Queue items** must include `proposalClass`, `targetSurface`, `materiality`, `reviewType`, `riskLevel`, and `requiresReclassification` when present (non-empty queue). **Proposals** must include `targetSurface`, `materiality`, `reviewType`, and `queueSummary` among required fields. Surface tokens use snake_case values such as `self`, `self_library`, `civ_mem`, `work_layer` (see schemas).

#### 3. Queue references are coherent

Each `proposalId` listed in the queue must correspond to an actual proposal JSON file.

#### 4. Event-log references exist

Each event `ref` should point to an existing file when the ref is file-backed (paths relative to the review-queue directory, or repo-root paths such as `users/demo/...`).

#### 5. Decisions point to real proposals

A decision may not reference a nonexistent proposal.

#### 6. Proposal refs are valid

`priorStateRef` and `proposedStateRef` must point to real files once path fragments are stripped.

Evidence refs may use synthetic session handles such as:

- `demo-session-07`
- `session-12`

These are allowed for demo or runtime-generated evidence handles.

### Empty template mode

The `_template` scaffold is intentionally minimal.

Use `--allow-empty` when validating the template review queue so that empty proposal, decision, and diff directories are treated as valid placeholders.

### Pre-decision bundle

Use `--allow-missing-decisions` when:

- `proposals/` and `diffs/` each contain at least one valid JSON file, and
- `decisions/` is still empty (no human decision recorded yet).

Strict mode without flags requires at least one file in all three directories. `--allow-missing-decisions` relaxes only the decision count; proposals and diffs are still required and fully schema-checked. Combine with `--allow-empty` only for the minimal template scaffold case.

### Demo mode

The `users/demo/review-queue/` directory should validate in strict mode without `--allow-empty`.

The demo is intended to remain a living worked example of:

- one proposal
- one decision
- one diff
- one event log
- one queue item

---

## Diff generation

Use:

```bash
python3 scripts/generate-identity-diff.py users/demo/review-queue/diffs/diff-001.json
```

To write a Markdown file:

```bash
python3 scripts/generate-identity-diff.py \
  users/demo/review-queue/diffs/diff-001.json \
  --output users/demo/review-queue/identity_diff.md
```

This generator creates a readable before/after review surface from the structured diff artifact.

---

## Scope of validation

The validator is intentionally conservative in v1.

It validates:

- structure
- schema conformance
- reference integrity

It does not decide:

- whether a proposal should be approved
- whether a contradiction classification is substantively correct
- whether a merged change is educationally optimal

Those remain review and governance questions.

Companion-Self template — Change-review validation v1
