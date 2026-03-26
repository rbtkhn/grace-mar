# Sync pack (optional template module)

**Purpose:** Reusable manual sync pattern for new companion instances.

Use this pack when an instance needs to mirror selected updates from source WORK territories (for example, `work-dev` or `work-politics`) into instance-local mirror docs.

This pack is optional and review-first.

**Canonical public upstream:** [companion-self](https://github.com/rbtkhn/companion-self) (instances should sync from upstream repo + pinned ref when needed).

---

## What this includes

- `SYNC-CONTRACT.template.md` - territory-level sync rules and relevance criteria
- `SYNC-LOG.template.md` - append-only sync check ledger
- `SYNC-DAILY.template.md` - optional single-page daily sync surface (training mode)
- `ENABLE-SYNC-PACK.md` - step-by-step enablement runbook

---

## Core invariants

- Manual and review-first (no automatic write-through)
- No direct Record writes during sync
- If identity implications are discovered, stage via gate (`recursion-gate.md`)
- Human approval remains required for consequential/public changes

---

## Recommended usage

1. Start with contract + log only.
2. Add daily surface only for onboarding/training-heavy instances.
3. Tune relevance criteria per territory and companion maturity.

