# work-dream history

Append-only operator trail for consolidation design, ritual changes, and `dream` workflow architecture.

This log is WORK-only. It is not the Record, not MEMORY, and not a substitute for `recursion-gate.md`.

---

## 2026-04-02 — 24h coffee rollup, execution paths, civ-mem echoes in `last-dream.json`

- [`scripts/dream_coffee_rollup.py`](../../scripts/dream_coffee_rollup.py) parses [`work-cadence-events.md`](../work-cadence/work-cadence-events.md) for `coffee` lines in a rolling UTC 24h window.
- [`scripts/dream_execution_paths.py`](../../scripts/dream_execution_paths.py) emits three deterministic paths (`today_field`, `build`, `steward`) and `suggested_execution_path_index` from **tomorrow’s** calendar day `(tm_yday - 1) % 3`.
- [`scripts/dream_civmem_echoes.py`](../../scripts/dream_civmem_echoes.py) runs **query-only** `query_inrepo_civmem` over a bounded string from contradiction digest entries (else short-term `self-memory` excerpt). No auto index build; missing index → `followups` line.
- [`scripts/auto_dream.py`](../../scripts/auto_dream.py) merges these into handoff; [`scripts/operator_daily_warmup.py`](../../scripts/operator_daily_warmup.py) prints them under **Last dream (night handoff)**.

## 2026-04-01 — dream architecture refresh

- Promoted `scripts/auto_dream.py` as the primary entrypoint (was `auto-research/swarm/orchestrator.py dream`).
- Added `last-dream.json` handoff: dream writes a compact summary artifact that coffee Step 1 (`operator_daily_warmup.py`) reads and displays as "Last dream (night handoff)."
- Created `scripts/operator_end_of_day.py` — night-side bundle that runs dream + handoff-check in one command, mirroring `operator_reentry_stack.py` for the morning side.
- Added Maintenance mode to AGENTS.md Operating Modes table — dream touches self-memory, runs integrity/governance, emits pipeline events, so it should be visible in the guardrails doc.
- Classified `last-dream.json` as runtime noise in `operator_handoff_check.py`.
- Created this territory (`docs/skill-work/work-dream/`) paralleling `work-coffee` — skill holds the executable contract, territory holds doctrine, boundaries, and history.
- Added cadence choreography table to dream SKILL.md replacing the vague "Canonical pairing" section with actionable sequencing: dream→coffee closeout at night, coffee reads last-dream.json at morning.
