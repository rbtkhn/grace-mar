# Template sync status (grace-mar)

Living document for **alignment** between this **instance** and the [companion-self](https://github.com/rbtkhn/companion-self) template. Policy remains in AGENTS.md, GRACE-MAR-CORE, and companion-approved merges.

---

## Contract target

- **Target template version:** see root [`instance-contract.json`](../instance-contract.json) (`templateVersionTarget`).
- **Target companion-self commit:** see root [`instance-contract.json`](../instance-contract.json) (`templateCommitTarget`).
- **Canonical upgrade procedure:** [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).
- **Template release metadata:** companion-self [`template-version.json`](https://github.com/rbtkhn/companion-self/blob/main/template-version.json) (`compatibilityContract`).

---

## Applied provenance

- **Last applied companion-self commit:** see root [`template-source.json`](../template-source.json) (`companionSelfCommit`).
- **Last applied template version:** see root [`template-source.json`](../template-source.json) (`templateVersion`).
- **Last applied sync timestamp:** see root [`template-source.json`](../template-source.json) (`syncedAt`).
- **Historical baseline note:** [TEMPLATE-BASELINE](skill-work/work-companion-self/TEMPLATE-BASELINE.md) remains useful as a historical governance reference, but it is no longer the primary machine pin once [`instance-contract.json`](../instance-contract.json) and [`template-source.json`](../template-source.json) are kept current.

**Reading rule:** `instance-contract.json` describes the **target** state grace-mar wants to align to. `template-source.json` records the **applied** state that has actually been merged. They may differ temporarily during intentional catch-up work.

---

## Authority model

| Layer | Primary surface | Role |
|------|------------------|------|
| **Doctrine** | [merging-from-companion-self.md](merging-from-companion-self.md), [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md) | Policy: what may sync, what must never sync, and how selective merge works |
| **Contract** | [instance-contract.json](../instance-contract.json) | Target version / commit grace-mar is aiming to match |
| **Applied provenance** | [template-source.json](../template-source.json) | Last actual upstream commit merged, by whom, and on which paths |
| **Audit** | [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md), `scripts/template_diff.py` | Drift visibility and next merge slices |

---

## Identity Fork Protocol (explicit rule)

- **Grace-mar** hosts the **full IFP specification** ([identity-fork-protocol.md](identity-fork-protocol.md), reference implementation).
- **Companion-self** hosts a **short-form summary** that points here for the full spec. Do **not** replace grace-mar’s IFP with the template file; port **portable** wording from template into grace-mar only when it improves clarity without dropping reference-implementation sections.

---

## Aligned (2026-03-27 pass)

- Portable **change-review doctrine** pulled from template: [change-review.md](change-review.md), [change-review-lifecycle.md](change-review-lifecycle.md), [change-types.md](change-types.md), [contradiction-policy.md](contradiction-policy.md), [concept.md](concept.md) (same paths as companion-self).
- [change-review-validation.md](change-review-validation.md) — template body + **grace-mar** gate → review-queue bridge preserved.
- [contradiction-resolution.md](contradiction-resolution.md) — template principle + **grace-mar** `conflict_check` implementation section.
- [layer-map.json](layer-map.json) — `forbiddenCrossings` aligned with template (`users/**/Record/**` included).
- Instance paths under `users/grace-mar/` follow canonical layout ([canonical-paths.md](canonical-paths.md)).
- Gated pipeline and `recursion-gate.md` as default staging (see [identity-fork-protocol.md](identity-fork-protocol.md) §4).
- Change-review scaffold and validators (`change_review_queue.json`, `change_event_log.json`) per template naming.

---

## Diverged but approved

- **[identity-fork-protocol.md](identity-fork-protocol.md)** — grace-mar full spec vs companion-self short form (see above).
- **[CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md)** — grace-mar **reference extension** (~760+ lines); companion-self ~240-line portable baseline. Opening **Template alignment** paragraph documents the split.
- **[approval-inbox-spec.md](approval-inbox-spec.md)** — **Portable baseline** link + grace-mar extended UX/API spec.
- **Historical seed narrative** vs Seed Phase v2 numbered stages — [companion-self-seed-phase-v2-mapping.md](companion-self-seed-phase-v2-mapping.md).
- **Operator tooling** (harness, work-jiang, operator cadence / `operator_daily_warmup`) — instance-specific; not required to match template minimal student app.
- **`docs/skill-work/work-*`** — large **instance-only** trees (work-build-ai legacy, generated dashboards, etc.); entrypoint READMEs carry **template mirror** links for diff hygiene.

---

## Sync classes

| Class | Meaning | Typical examples |
|------|---------|------------------|
| **Canonical template surfaces** | Portable template material that grace-mar normally wants close to upstream | `schema-registry/`, `users/_template/`, change-review doctrine docs, template validators |
| **Mirrored-but-adapted** | Same conceptual surface, but grace-mar keeps additional reference-implementation detail | `identity-fork-protocol.md`, contradiction docs, architecture/concept expansions, local schema mirrors |
| **Instance-only** | Never part of template parity | `users/grace-mar/`, deployment/runtime config, local operator tooling, most `docs/skill-work/work-*` trees |

This classification is the default answer when a diff appears: first decide the class, then decide whether anything should merge.

---

## Pending migration

- Push **enriched** `users/_template/review-queue/README.md` to upstream companion-self if you want the template scaffold to match grace-mar validator doctrine (optional PR).
- Re-run **`template_diff.py --use-manifest`** after the next companion-self `main` pull; add `--include-skill-work` only when you want the broader WORK-tree audit. Update [audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md).
- Promote the refreshed target/applied pin model into operator habit: update [`instance-contract.json`](../instance-contract.json) when the intended target changes; update [`template-source.json`](../template-source.json) when a merge actually lands.

---

## Last audit date

- **2026-04-06** — Steward template/boundary pass: integrity PASS; §3 sync log updated to match `template-source.json` applied commit `f16104b` (seed-phase pytest scaffold); companion-self HEAD ahead of pinned commit. No new downstream merges this pass.
- **2026-03-27** — Doctrine sync: change-review cluster, validation, contradiction-resolution merge, layer-map, skill-work README pointers, TEMPLATE-BASELINE pin, audit report regeneration.
- **Reference audit:** [audit-grace-mar-vs-companion-self-template.md](audit-grace-mar-vs-companion-self-template.md).

---

## See also

- [gate-vs-change-review.md](gate-vs-change-review.md)
- [grace-mar vs companion-self](grace-mar-vs-companion-self.md)
