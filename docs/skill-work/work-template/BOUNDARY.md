# WORK boundary contract — copy-paste checklist

**Purpose:** Drop the bullets below (or a shortened subset) into a new `work-<id>/README.md` **Boundary** section. Full pattern library: [README.md](README.md).

---

## What this lane is for

- **Primary objective:** _(one sentence)_  
- **In scope:** _…_  
- **Out of scope:** _…_  

## What this lane may write

- WORK-local markdown, configs, scripts, drafts, ledgers, and operator logs under `docs/skill-work/work-<id>/` (and documented script paths).  
- **Stage** RECURSION-GATE candidates when the lane’s workflow calls for it (per [AGENTS.md](../../AGENTS.md)).  

## What this lane may not write

- **No direct edits** to `users/<id>/self.md`, `self-archive.md`, `bot/prompt.py`, or merge from gate without companion approval and `process_approved_candidates.py`.  
- **No** treating WORK drafts as Record truth or Voice knowledge until gated and merged.  

## Promotion paths

- **To lane ledger / compounding memory:** operator adds to `WORK-LEDGER.md` or lane-specific ledger (e.g. [STRATEGY.md](../work-strategy/STRATEGY.md)) per lane rules — still WORK-only.  
- **To Record / Voice:** only via **RECURSION-GATE** + companion approval + merge script.  

## Governing gate

- **Default:** `users/<id>/recursion-gate.md` with appropriate `territory` / `channel_key` per lane (see lane `LANE-CI.md` or README).  
- **Lane-specific:** _(e.g. work-politics `territory: work-politics`; work-strategy milestones via `emit_work_strategy_gate_paste_snippet.py` — document in lane README.)_  

## Operator standard

Human sign-off before client-facing or public ship from this lane. Lexile / knowledge boundary for Voice-facing outputs: [AGENTS.md](../../AGENTS.md).
