# Shadow Merge Simulator

**Script:** [`scripts/runtime/shadow_merge_simulator.py`](../../scripts/runtime/shadow_merge_simulator.py)

## Invocation contract

| Field | Value |
|-------|--------|
| **Surface type** | Workflow / operator tooling (read-only) |
| **Primary purpose** | Preview likely consequences of approving a proposed canonical change **without** mutating the Record |
| **When to use** | A candidate, draft, or proposal is plausible enough to merit **consequence review** before approval |
| **Inputs** | `--candidate CANDIDATE-NNNN`, or `--proposal-file` (JSON aligned with [`schema-registry/recursion-gate-candidate.schema.json`](../../schema-registry/recursion-gate-candidate.schema.json)), or direct proposal (`--target-surface` + `--proposal-summary` + `--proposed-change`) |
| **Outputs** | A Markdown **Shadow Merge Report** under `artifacts/shadow-merges/` (default) or `--output` |
| **Mutation scope** | Writes **only** the report file (and stderr log line). No gate merge, no Record writes. |
| **Canonical Record access** | Read-only (`users/<id>/recursion-gate.md`, optional runtime observation ledger for envelope signals) |
| **Typical next step** | Operator review, then gate decision or surface reclassification |
| **Do not use for** | Approval, merge, or silent promotion of runtime material into canonical Record |

## Purpose

The simulator writes a **Shadow Merge Report** (Markdown) that previews **likely** consequences if a RECURSION-GATE candidate were approved: which **canonical surfaces** would move, **keyword best-fit** vs **resolved target**, what **downstream artifacts** might need attention, and **governance risks** (classification, narrative). It answers: *“What world am I creating if I approve this?”* — not *“Should I approve?”*

## Non-goals

- **Not** a merge tool. It does not run `process_approved_candidates.py`, edit `users/<id>/self.md`, `self-archive.md`, `self-skills.md`, SELF-LIBRARY files, `recursion-gate.md`, or `bot/prompt.py`.
- **Not** an approval mechanism. Output is **operator-readable simulation** only.
- **Not** line-perfect diffs across the repo (v1 uses heuristics).

## Why it exists

Grace-Mar treats durable memory changes as **governed state transitions** ([`docs/runtime-vs-record.md`](../runtime-vs-record.md)). The simulator adds **counterfactual review** before final gate decisions — especially for high-impact surfaces, uncertain claims, or ontology-sensitive proposals.

A plausible proposal can still be risky if it touches the **wrong surface**, hardens weak material into **durable doctrine**, distorts **downstream retrieval** and prompt behavior, or **compresses ambiguity** too early.

## CLI

**Candidate mode** (preferred; uses the canonical gate queue):

```bash
python scripts/runtime/shadow_merge_simulator.py \
  -u grace-mar \
  --candidate CANDIDATE-0042 \
  -o artifacts/shadow-merges/CANDIDATE-0042.md
```

Default output when `-o` is omitted: `artifacts/shadow-merges/<candidate-id>.md` (under the repo root).

**Proposal JSON file** (no gate lookup; schema-aligned payload):

```bash
python scripts/runtime/shadow_merge_simulator.py \
  --proposal-file path/to/candidate-payload.json \
  -o artifacts/shadow-merges/preview.md
```

**Direct proposal mode** (no gate lookup — for drafts or hypotheticals):

```bash
python scripts/runtime/shadow_merge_simulator.py \
  --target-surface SKILLS \
  --proposal-summary "Refine skill-strategy notebook writing boundary" \
  --proposed-change "Skill-strategy should write compact notebook-linked summaries and avoid raw prose dumps into strategy-notebook." \
  -o artifacts/shadow-merges/skill-strategy-preview.md
```

Optional **`--repo-root`** is intended for tests; default resolution follows the live repo layout.

When a staged candidate or JSON payload includes **`source_observation_ids`**, the simulator may load those observations (see `GRACE_MAR_RUNTIME_LEDGER_ROOT` in runtime docs) and attach **uncertainty envelope** signals — **advisory only**, same spirit as [`review-orchestrator.md`](review-orchestrator.md).

## Output location

Reports are usually written under [`artifacts/shadow-merges/`](../../artifacts/shadow-merges/README.md). Default policy: gitignore `*.md` there; only the folder README (and `.gitkeep`) need to track in git.

## Related

- [Review orchestrator](review-orchestrator.md) — multi-pass review packet (read-only).
- [Runtime vs Record](../runtime-vs-record.md) — canonical surfaces vs derived/runtime.
- [Gate board](../gate-board.md) — derived gate snapshot (not authoritative).

### Operator habit

For **high-impact** candidates, consider generating a shadow merge report **before** approval so consequence review is routine, not exceptional.

## Boundary reminder

The simulator is valuable because Grace-Mar distinguishes **runtime assistance** from **governed truth**. It is a **counterfactual preview** tool, not a hidden approval engine.
