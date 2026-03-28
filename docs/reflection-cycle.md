# Reflection & Proposal Cycle

Operator tool: [`scripts/reflection_cycle.py`](../scripts/reflection_cycle.py) (also `grace-mar reflect …`). It **reads** existing fork files (session transcript, pipeline events, merge receipts, gate processed section, self-evidence, etc.), optionally calls an LLM to propose **evidence-grounded** `CANDIDATE-####` blocks, writes artifacts under `users/<id>/reflection-proposals/`, and **optionally** appends pending candidates to [`recursion-gate.md`](../users/grace-mar/recursion-gate.md).

## Setup

```bash
pip install -e ".[reflect]"
export OPENAI_API_KEY=...
# optional:
export GRACE_MAR_REFLECT_MODEL=gpt-4o-mini
```

Dry-run (no API key, stub proposal):

```bash
python scripts/reflection_cycle.py -u grace-mar --dry-run
# or
grace-mar reflect -u grace-mar --dry-run
```

Full run without staging to the gate (artifacts only):

```bash
python scripts/reflection_cycle.py -u grace-mar
```

Append top proposals to the gate (companion reviews as usual):

```bash
python scripts/reflection_cycle.py -u grace-mar --append
```

Use `--append-all` for up to five proposals (default append count is three). Use `--deep` for a 45-day lookback.

## Merge behavior

- Candidates use numeric ids (`CANDIDATE-####`) so [`process_approved_candidates.py`](../scripts/process_approved_candidates.py) and dashboards keep working.
- `mind_category` is always one of `knowledge` / `curiosity` / `personality` for automated merge into `self.md` + evidence.
- Proposals that target **`self-skills.md`** (or legacy `skills.md`), **`intent_snapshot.json`**, or **SELF-LIBRARY** structural edits should say so in `suggested_entry` and be treated as **manual** follow-up (same pattern as other operator milestones).

## Review surfaces

- **Static HTML:** `python scripts/generate_gate_dashboard.py -u grace-mar` — use the **Reflection** filter for `signal_type: reflection-cycle`.
- **Flask:** [`apps/gate-review-app.py`](../apps/gate-review-app.py) — `/?signal=reflection` shows reflection candidates only.

## Pipeline events

Non–dry-run with `--append` emits `reflection_cycle_run` in `pipeline-events.jsonl` (candidate id `none`, merge payload includes `reflection_cycle_id` and `proposals_created`).

## Safety

- `--dry-run` writes `reflection-proposals/REFLECT-*.md` and updates `index.md` only; no gate append, no events.
- High-risk proposals are rate-limited (see [`src/grace_mar/reflection/rate_limit.py`](../src/grace_mar/reflection/rate_limit.py)); use `--force` only when you accept bypassing caps.
