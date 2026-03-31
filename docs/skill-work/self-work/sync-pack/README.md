# Sync pack (optional template module)

**Purpose:** Reusable manual sync pattern for companion instances.

Use this pack when an instance needs to mirror selected updates from source WORK territories into instance-local mirror docs.

This pack is optional and review-first.

**Canonical public upstream:** [companion-self](https://github.com/rbtkhn/companion-self) (instances should sync from upstream repo + pinned ref when needed).

**Canonical template copy:** [sync-pack README on `main`](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/self-work/sync-pack/README.md) — source of truth for pack text in the template repo.

**Diff discipline:** When this pack or an instance mirror changes, run `python3 scripts/template_diff.py --use-manifest` from a repository that ships the script (for example [grace-mar](https://github.com/rbtkhn/grace-mar)), or follow your instance’s documented diff workflow.

---

## What this includes

- `SYNC-CONTRACT.template.md` - territory-level sync rules and relevance criteria
- `SYNC-LOG.template.md` - append-only sync check ledger
- `SYNC-DAILY.template.md` - optional single-page daily sync surface (training mode)
- `ENABLE-SYNC-PACK.md` - step-by-step enablement runbook
- `INITIAL-GOOD-MORNING.md` — legacy filename; template sequence for first **coffee** / startup sync routine (legacy **hey** wording may still appear in older copies)

Default initial **coffee** (startup) order:
1) template alignment (optional),
2) work-dev sync (optional, if established) + next-step suggestions,
3) work-business sync (optional, if established) + next-step suggestions.

**Closeout** trio (same contracts; legacy filenames on disk):
- [Startup / coffee rhythm spec](../../../good-morning-brief-spec.md)
- [Closeout template](../../../good-night-template.md)
- [Closeout spec](../../../good-night-brief-spec.md)

---

## Deterministic upgrade path (instance-side)

Reference instances (for example [grace-mar](https://github.com/rbtkhn/grace-mar)) ship `scripts/upgrade-from-template.py`. From the **instance** repository root, with a checkout of companion-self at `companion-self/` (or a path your script expects):

```bash
python3 scripts/upgrade-from-template.py --dry-run
python3 scripts/upgrade-from-template.py
```

That refreshes sync-pack files from the pinned template tree and updates `template-source.json` when the script is present. If your instance has no such script, merge manually per [how-instances-consume-upgrades.md](../../../../how-instances-consume-upgrades.md).

---

## Core invariants

- Manual and review-first (no automatic write-through)
- No direct Record writes during sync
- If identity implications are discovered, stage via gate (`recursion-gate.md`)
- Human approval remains required for consequential/public changes
