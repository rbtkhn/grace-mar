# Sync pack (optional template module)

**Purpose:** Reusable manual sync pattern for companion instances.

Use this pack when an instance needs to mirror selected updates from source WORK territories into instance-local mirror docs.

This pack is optional and review-first.

**Canonical public upstream:** [companion-self](https://github.com/rbtkhn/companion-self) (instances should sync from upstream repo + pinned ref when needed).

---

## What this includes

- `SYNC-CONTRACT.template.md` - territory-level sync rules and relevance criteria
- `SYNC-LOG.template.md` - append-only sync check ledger
- `SYNC-DAILY.template.md` - optional single-page daily sync surface (training mode)
- `ENABLE-SYNC-PACK.md` - step-by-step enablement runbook
- `INITIAL-GOOD-MORNING.md` - template sequence for first daily sync routine

Default initial good-morning order:
1) template alignment (optional),
2) work-dev sync (optional, if established) + next-step suggestions,
3) work-business sync (optional, if established) + next-step suggestions.

Companion closeout pair:
- [Good Morning Brief Spec](../../../good-morning-brief-spec.md)
- [Good Night Template](../../../good-night-template.md)
- [Good Night Brief Spec](../../../good-night-brief-spec.md)

---

## Deterministic upgrade path (instance-side)

From `grace-mar` repo root:

```bash
python3 scripts/upgrade-from-template.py --dry-run
python3 scripts/upgrade-from-template.py
```

This updates sync-pack files from local `../companion-self` and refreshes `template-source.json`.

---

## Core invariants

- Manual and review-first (no automatic write-through)
- No direct Record writes during sync
- If identity implications are discovered, stage via gate (`recursion-gate.md`)
- Human approval remains required for consequential/public changes

