# work-dream

**Purpose:** Operator-facing doctrine, boundaries, and evolution history for Grace-Mar's `dream` ritual — the end-of-day consolidation pass. The executable trigger surface lives in [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md).

**Not** Record truth. **Not** MEMORY. **Not** a second merge path.

---

## Role

| Role | Description |
|------|-------------|
| **Consolidation architecture** | Defines the shape of end-of-day maintenance: memory normalization, integrity, governance, contradiction digest, artifact drafts. |
| **Night-to-morning handoff** | Documents the `last-dream.json` data contract that bridges dream output to coffee Step 1. |
| **Boundary surface** | Explains what belongs in WORK-only docs/history versus what must escalate to `RECURSION-GATE`. |
| **Choreography with coffee** | Holds the rationale for the dream→coffee pairing: sequence, timing, data flow. |

---

## Relationship to `dream`

- **`dream` skill** = executable ritual contract, trigger behavior, script commands, return shape, guardrails.
- **`work-dream` territory** = prose home for rationale, boundaries, history, and evolution of the ritual.

This split mirrors `work-coffee`:

- the skill should stay optimized for invocation and agent behavior
- the territory should hold the longer-form doctrine and lane-specific history

---

## Gate threshold

`work-dream` is **WORK-only by default**.

Keep changes in docs/history only when they are about:

- maintenance semantics (what dream checks, in what order)
- strict mode behavior and when to use it
- handoff contract shape (`last-dream.json` fields)
- contradiction digest integration
- dream→coffee choreography

Stage to **`users/grace-mar/recursion-gate.md`** only when a `work-dream` insight would change governed behavior, such as:

- durable prompt or policy behavior
- changes to how integrity/governance checks affect the Record
- new artifact types that cross into Record territory

This territory never creates a second merge path. `RECURSION-GATE` remains the membrane.

---

## Script topology

```
auto_dream.py
  ├─ maintain_self_memory()        normalize self-memory.md
  ├─ validate-integrity.py         integrity checks (--json)
  ├─ governance_checker.py         governance scan
  ├─ contradiction_digest.py       derived contradiction digest
  │    └─ write_artifact_drafts()  optional artifact drafts
  ├─ config/context_budgets/dream.json   write-path caps (via context_budget.py)
  ├─ emit_pipeline_event.py        maintenance event
  └─ _write_last_dream_handoff()   writes last-dream.json
operator_daily_warmup.py           reads coffee.json for collapsed Last dream display
audit_context_tax.py               approximate ritual paste line/char counts
```

**Bundle:** `operator_end_of_day.py` runs `auto_dream.py` then `operator_handoff_check.py` — night-side counterpart to `operator_reentry_stack.py`.

**Strict mode:** `--strict` tightens integrity parity, contradiction classification, and failure states. Same ritual, sharper posture. Use at end of week or after unusual maintenance events.

---

## Handoff contract

`last-dream.json` (written to `users/grace-mar/`) contains:

| Field | Type | Purpose |
|-------|------|---------|
| `generated_at` | ISO timestamp | When dream ran |
| `ok` | boolean | Overall pass/fail |
| `integrity_ok` | boolean | Integrity check result |
| `governance_ok` | boolean | Governance check result |
| `self_memory_changed` | boolean | Whether memory was normalized |
| `reviewable_count` | int | Reviewable items in contradiction digest |
| `contradiction_count` | int | Contradictions found |
| `artifact_draft_count` | int | Artifact drafts generated |
| `promotable_draft_count` | int | Drafts ready for promotion |
| `followups` | string[] | Human-readable follow-up items for morning |
| `coffee_rollup_24h` | object | Rolling 24h summary of `coffee` lines from [`work-cadence-events.md`](../work-cadence/work-cadence-events.md) (`count`, `by_mode`, `by_picked`, `picks`, `first_ts`, `last_ts`, `runs`, …) |
| `execution_paths` | object[] | Three deterministic morning paths (`today_field`, `build`, `steward`) with `first_move`, `stop_rule`, `signals_used` |
| `suggested_execution_path_index` | int | 0–2; **Steward (2)** if integrity or governance failed this run, else **Steward** if gate pending > `max_pending_candidates` in `config/fork-config.json`, else **calendar** `(tomorrow_tm_yday - 1) % 3` |
| `execution_path_suggestion_reason` | string | `integrity_or_governance_fail` \| `gate_backlog` \| `calendar_mod3` |
| `tomorrow_inherits` | string | One-line operational hint for morning (not policy or Record) |
| `civmem_echoes` | object[] | Token-overlap hits from in-repo [`docs/civilization-memory/`](../../civilization-memory/README.md) (count capped by `config/context_budgets/dream.json`); each echo includes `analogy_label`, optional `specificity_pass`, `score` |
| `civmem_disclaimer` | string | States analogical / non-Record scope |
| `civmem_index_missing` | boolean | True when the in-repo civ-mem index file is absent |
| `civmem_suppressed_reason` | string | Present when echoes were cleared by budget or checks (e.g. `disabled_by_budget`, `suppressed_integrity_fail`, `suppressed_governance_alert`) |

**Civ-mem query source:** Echoes are computed from the **pre-persist** self-memory snapshot used in the same `auto_dream` run (`memory_result.before`), which can differ from on-disk `self-memory.md` after normalization writes in that run.

**Context budgets:** Write-path caps and suppress rules live in [`config/context_budgets/dream.json`](../../../config/context_budgets/dream.json); display defaults for the collapsed Last dream block live in [`config/context_budgets/coffee.json`](../../../config/context_budgets/coffee.json). See [`config/context_budgets/README.md`](../../../config/context_budgets/README.md).

**Doctrine:** Dream suggestions (paths, civ-mem, rollup) are **operational hints only** — not truth, not priority, not a substitute for gate review, integrity, companion approval, or operator judgment. Cadence artifacts are not a shadow Record.

Clients should **ignore unknown keys** on future dream versions.

Coffee Step 1 (`operator_daily_warmup.py`) reads this file and renders a **collapsed** **"Last dream (night handoff)"** block by default (`--verbose-dream` for full detail; `--show-civ-mem` / `--show-rollup` opt into extra collapsed lines; defaults from `coffee.json`). The file is classified as runtime noise in `operator_handoff_check.py` — it does not need to be committed.

**Strict halt:** When `auto_dream.py --strict` stops early on integrity/governance failure, a new `last-dream.json` may not be written; morning pickup can reflect an older handoff until the next successful run.

---

## Continuity and trail

`work-dream` does **not** replace any existing continuity surface.

- **Raw continuity:** `users/<id>/session-transcript.md`
- **Lane breadcrumbs:** `docs/skill-work/work-dream/work-dream-history.md`
- **Optional continuity memory:** `users/grace-mar/self-memory.md`
- **Governed durable changes:** `users/grace-mar/recursion-gate.md`

---

## Adjacent surfaces

- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md)
- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)
- [docs/skill-work/work-coffee/README.md](../work-coffee/README.md)
- [scripts/auto_dream.py](../../../scripts/auto_dream.py)
- [scripts/operator_end_of_day.py](../../../scripts/operator_end_of_day.py)

---

## Scope boundaries

In scope:

- end-of-day consolidation architecture
- maintenance semantics and strict mode
- contradiction digest integration
- handoff contract design
- dream→coffee choreography
- night-side operator ergonomics

Out of scope:

- morning re-entry or orientation (that's coffee)
- Record merges or prompt edits without the gate
- generic repo hygiene (coffee B / handoff-check)
- work-politics or other territory content
