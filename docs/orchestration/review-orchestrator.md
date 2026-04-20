# Review orchestrator (bounded review prep)

The **review orchestrator** is a **read-only** helper that runs a small, explicit **multi-pass** workflow over a proposed change and emits a single **Markdown review packet** for the operator. It **parallelizes review structure, not authority**: it does **not** replace companion gate review, does **not** merge into the Record, and does **not** auto-approve candidates.

**Canonical gate truth** remains [`users/<id>/recursion-gate.md`](../../users/grace-mar/recursion-gate.md). For a read-only gate backlog pass, use [`.cursor/skills/gate-review-pass/SKILL.md`](../../.cursor/skills/gate-review-pass/SKILL.md). For a **non-mutating** counterfactual preview of likely Record/downstream effects before approving a high-impact candidate, see the [Shadow Merge Simulator](shadow-merge-simulator.md). For an advisory **surface placement** check (claimed vs content signals), see the [Surface Misclassification Detector](surface-misclassification-detector.md).

## What it does

Four passes plus synthesis (see script output):

1. **Evidence pass** — observation count, `source_refs`, recency, **evidence sufficiency** (reuses [PR 1 uncertainty envelope](../abstention-policy.md)).
2. **Contradiction pass** — `contradiction_refs` on observations, or gate conflict / constitution / duplicate hints for candidate mode.
3. **Boundary pass** — pre-gate: work-layer vs Record-target heuristics; candidate mode: `boundary_review`, `profile_target`, `territory`, `risk_tier` from [`scripts/recursion_gate_review.py`](../../scripts/recursion_gate_review.py) parsing.
4. **Promotion-risk pass** — fabricated-history risk, promotion recommendation, envelope reasons, scope/prematurity.
5. **Synthesis** — recommended action (`allow` | `allow_with_review` | `hold` | `block`) aligned with the envelope (advisory).
6. **Operator questions** — concrete follow-ups.

## Task anchor (required)

Every invocation must include **`--task-anchor`** with a short description of the operator’s original question or constraint for this review. The packet includes a **`## Task Anchor`** section (task, optional constraint, and **active scope**) so long reviews do not silently drift from intent.

- **`--constraint-anchor`** — optional extra boundary (e.g. abstention, “do not broaden”).
- **`--active-scope`** — optional human-readable scope string. If omitted, scope is **derived** from lane, observation ids, or candidate id (see script).

Optional **`--receipt-out PATH`** writes a **JSON sidecar** for audit (not canonical Record truth): `run_id`, `built`, `mode`, `target`, `anchor`, **`phase_anchor_checks`** (per-pass drift strings, PR 2), **`phase_sequence`** (six named phases with `phase_id`, `title`, `status`, `summary`, `halt_recommended`, `halt_reason`), and `non_canonical: true`. Phases match the Markdown sections in order: retrieval (Evidence) → invalidators (Contradiction) → boundary → promotion risk → synthesis → operator questions.

## Modes

| Mode | Input | Use when |
|------|--------|----------|
| `pre_gate` | `--lane` + one or more `--id` (runtime observation ids), or `--mixed-lane` | Deciding whether to **stage** from runtime / prepared context / memory-brief line of thought |
| `candidate_review` | `--candidate CANDIDATE-NNNN` | **Post-staging** hygiene on an existing pending block |

Candidate mode scores **gate-text-derived** synthetic text through the same PR 1 envelope (clearly labeled in the packet); it does not require ledger rows for the candidate body.

## Examples

**Pre-gate (observation-driven):**

```bash
python3 scripts/runtime/review_orchestrator.py \
  --mode pre_gate \
  --lane work-strategy \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --id obs_20260413T191455Z_e5f6g7h8 \
  --task-anchor "Decide whether these observations justify staging a gate candidate."
```

**Candidate-driven:**

```bash
python3 scripts/runtime/review_orchestrator.py \
  --mode candidate_review \
  --candidate CANDIDATE-0042 \
  --user grace-mar \
  --task-anchor "Hygiene review on pending CANDIDATE-0042 before companion approve."
```

**Write to optional artifact path:**

```bash
python3 scripts/runtime/review_orchestrator.py \
  --mode candidate_review \
  --candidate CANDIDATE-0042 \
  --user grace-mar \
  --task-anchor "Hygiene review before approve." \
  --output artifacts/review-packets/CANDIDATE-0042.md
```

**Optional JSON receipt (non-canonical):**

```bash
python3 scripts/runtime/review_orchestrator.py \
  --mode pre_gate \
  --lane work-strategy \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --task-anchor "Assess ledger observations for promotion." \
  --receipt-out artifacts/review-packets/example-anchor-receipt.json \
  -o artifacts/review-packets/review-packet.md
```

**Tests / alternate repo root:**

```bash
python3 scripts/runtime/review_orchestrator.py \
  --mode candidate_review \
  --candidate CANDIDATE-9001 \
  --user testuser \
  --repo-root /path/to/fixture/repo \
  --task-anchor "Fixture run for tests."
```

## Policy mode envelope

Every packet includes a **Policy mode envelope** section (from `--policy-mode` or `GRACE_MAR_POLICY_MODE`, default `operator_only`) so promotion advice is read next to declared governance posture — see [policy-modes.md](../policy-modes.md).

## Optional: budgeted context hint

Pass `--context-mode compact|medium|deep` to append a **Suggested budgeted context** section with a copy-paste command for [`build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py). This does **not** run the script; it links review prep to explicit context budgeting ([context-budgeting.md](../runtime/context-budgeting.md)). The suggested command includes `--policy-mode` matching the active envelope when possible.

## Relation to other docs

- **PR 1 abstention / uncertainty:** [abstention-policy.md](../abstention-policy.md) — envelope rules.
- **Runtime vs Record:** [memory-retrieval.md](../runtime/memory-retrieval.md).
- **Context budgeting:** [context-budgeting.md](../runtime/context-budgeting.md).
- **Narrative walkthrough (memory brief → gate):** [memory-brief-to-gate-demo.md](memory-brief-to-gate-demo.md).

## What not to use it for

- Replacing companion judgment or the **approve → `process_approved_candidates.py`** pipeline.
- Autonomous mutation of `self.md`, EVIDENCE, or gate files.
- A general-purpose multi-agent “team” — this is a **structured checklist** in Markdown form.

## See also

- [`scripts/runtime/review_orchestrator.py`](../../scripts/runtime/review_orchestrator.py) (source)
- [`scripts/runtime/score_evidence_sufficiency.py`](../../scripts/runtime/score_evidence_sufficiency.py)
