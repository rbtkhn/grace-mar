# Coffee–dream pair (runtime hints)

**Status:** WORK (operator cadence). **Not** Record, not SELF, not a merge substitute.

**What it is:** A **small bridge** between `coffee` (work-cadence events) and `dream` (`last-dream.json`):

- **Dream** can attach **`last_coffee_echo`** to the handoff — a one-line, bounded description of the most recent `coffee` session, derived from the same **24h rollup** as `coffee_rollup_24h` in [`scripts/dream_coffee_rollup.py`](../../scripts/dream_coffee_rollup.py).
- **Morning coffee** (`operator_daily_warmup.py` via `operator_coffee.py`) can show a **quiet** one- or two-line readout when the dream run had nothing to flag, and still show a **fuller** "night handoff" when there are **signals** (digest, followups, integrity/governance issues). Use **`--verbose-dream`** for the long form.

**What it is not:** Canonical memory, evidence, or policy. If something must be true for the project, it belongs in the gate / Record path—not in this handoff.

See also: [work-dream history](../work-dream/work-dream-history.md) (chronology of last-dream + warmup), [menu-reference — signing-off](menu-reference.md#signing-off-intent) (closeout and dream adjacency).
