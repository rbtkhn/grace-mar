# work-dream history

Append-only operator trail for consolidation design, ritual changes, and `dream` workflow architecture.

This log is WORK-only. It is not the Record, not MEMORY, and not a substitute for `recursion-gate.md`.

---

## 2026-04-01 — dream architecture refresh

- Promoted `scripts/auto_dream.py` as the primary entrypoint (was `auto-research/swarm/orchestrator.py dream`).
- Added `last-dream.json` handoff: dream writes a compact summary artifact that coffee Step 1 (`operator_daily_warmup.py`) reads and displays as "Last dream (night handoff)."
- Created `scripts/operator_end_of_day.py` — night-side bundle that runs dream + handoff-check in one command, mirroring `operator_reentry_stack.py` for the morning side.
- Added Maintenance mode to AGENTS.md Operating Modes table — dream touches self-memory, runs integrity/governance, emits pipeline events, so it should be visible in the guardrails doc.
- Classified `last-dream.json` as runtime noise in `operator_handoff_check.py`.
- Created this territory (`docs/skill-work/work-dream/`) paralleling `work-coffee` — skill holds the executable contract, territory holds doctrine, boundaries, and history.
- Added cadence choreography table to dream SKILL.md replacing the vague "Canonical pairing" section with actionable sequencing: dream→coffee closeout at night, coffee reads last-dream.json at morning.
