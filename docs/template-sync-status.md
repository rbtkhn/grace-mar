# Template sync status (grace-mar)

Living document for **alignment** between this **instance** and the [companion-self](https://github.com/rbtkhn/companion-self) template. Policy remains in AGENTS.md, GRACE-MAR-CORE, and companion-approved merges.

---

## Contract target

- **Target template version:** see root [`instance-contract.json`](../instance-contract.json) (`templateVersionTarget`).
- **Canonical upgrade procedure:** [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).
- **Template release metadata:** companion-self [`template-version.json`](https://github.com/rbtkhn/companion-self/blob/main/template-version.json) (`compatibilityContract`).

---

## Aligned

- Instance paths under `users/grace-mar/` follow canonical layout ([canonical-paths.md](canonical-paths.md)).
- Gated pipeline and `recursion-gate.md` as default staging (see [identity-fork-protocol.md](identity-fork-protocol.md) §4).
- Change-review scaffold and validators (`change_review_queue.json`, `change_event_log.json`) per template naming.

*Update this subsection when you complete a merge from companion-self.*

---

## Diverged but approved

- **Historical seed narrative** vs Seed Phase v2 numbered stages — documented in [companion-self-seed-phase-v2-mapping.md](companion-self-seed-phase-v2-mapping.md).
- **Operator tooling** (harness, work-jiang, daily warmup) — instance-specific; not required to match template minimal student app.

*List intentional instance-only differences here so they are not mistaken for drift.*

---

## Pending migration

- Items waiting on a future template merge or schema bump — link PRs or issues when available.
- *None recorded — replace placeholder when needed.*

---

## Last audit date

- **Placeholder:** not yet scheduled for this doc.
- **Reference audit:** [audit-grace-mar-vs-companion-self-template.md](audit-grace-mar-vs-companion-self-template.md) when present.

---

## See also

- [gate-vs-change-review.md](gate-vs-change-review.md)
- [grace-mar vs companion-self](grace-mar-vs-companion-self.md)
