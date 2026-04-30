# Daily Ops Card (Cici)

Use this as the final required output of **`coffee`** (legacy **`hey`** still accepted).

Keep it short, concrete, and runnable.

---

Date: **2026-04-30**

## 1) Top sync action
- territory: work-cici — work-dev + work-politics **mirrors**
- action: Run forced relevance scans because both mirror sync logs are still at 2026-04-12.
- done when: Both mirror `SYNC-LOG.md` files have 2026-04-30 rows and `SYNC-DAILY.md` is refreshed from `stale sync state: yes` to the scan result.

## 2) Top execution action
- lane: work-cici mirror hygiene
- action: Pick the smallest Cici-readable mirror copy set after the forced scan; avoid deep CI or campaign-only churn unless it affects her current workflow.
- done when: `SYNC-DAILY.md` lists scored candidate updates and one combined next action that no longer references the 04-11/04-12 batch.

## 3) Top gate action
- candidate or review action: none by default
- approval needed from: Cici/her repo only if scan output implies identity or Voice changes; otherwise operator WORK-only review
- done when: No `self.md`, `self-archive.md`, or `recursion-gate.md` edits are made from this lane without the proper repo gate.

## 4) Stop condition (avoid over-maintenance)
- stop after: the two sync-log rows plus one refreshed snapshot
- defer remaining maintenance to: WORK-LEDGER watches unless an active Cici session requires it

## 5) Timeboxed plan
- `0-30 min`: scan work-dev/work-politics parent lanes for Cici-relevant deltas since 2026-04-12
- `30-60 min`: append dated sync-log rows with selected copy candidates
- `60-90 min`: refresh `SYNC-DAILY.md` and this card; stop before broad mirror rewrites

## 6) Risk and escalation
- biggest risk today: stale mirror recommendations being treated as current coffee guidance
- escalation trigger: scan finds identity/Voice implications, secrets, or cross-repo copy pressure
- who to escalate to: operator; Cici/her repo gate for any durable identity change

