# Template / instance contract

**Companion-Self** (template) and a **live instance** (for example Grace-Mar) share protocol and vocabulary but differ in responsibility. This document states **canonical compatibility rules** so upgrades, audits, and forks stay legible.

---

## Roles

| Dimension | Template (companion-self) | Instance (e.g. grace-mar) | Rule |
|-----------|---------------------------|---------------------------|------|
| **Authority** | Defines concepts, protocols, seed-phase schemas, scaffolds, and validation scripts. | Holds the companion’s Record, Voice, pipeline, and governed files under `users/<id>/`. | The template never contains a real person’s merged Record; the instance never replaces protocol truth silently. |
| **Staging (gate)** | Documents the **gate queue** abstraction (`recursion-gate.json`, `recursion-gate.md`, optional legacy names). | Chooses a concrete file (Grace-Mar: `recursion-gate.md`). | **Same contract:** stage → review → approve → merge; no merge without approval. Filename is **not** the contract. |
| **Material change (post-seed)** | Documents **change-review** (queue, proposals, decisions, diffs) for durable edits that are not simple gate merges. | May maintain `review-queue/` and related artifacts per [change-review](change-review.md). | Gate and change-review are **different** surfaces; see [gate-vs-change-review](gate-vs-change-review.md). |
| **Seed phase** | Canonical JSON Schemas, stages, readiness rules. | Produces `seed-phase/` artifacts and, after activation, lives in instance paths. | Instance follows template schemas unless a documented migration says otherwise. |
| **Upgrades** | Version metadata (see root `template-version.json` and upgrade docs). | Tracks alignment (see instance `instance-contract.json` and `docs/template-sync-status.md` in grace-mar). | Instances merge template changes deliberately; see [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md). |

---

## Invariants

1. **Sovereign merge:** No change to governed Record content without companion-controlled approval (see [Identity Fork Protocol](identity-fork-protocol.md)).
2. **Gate before merge:** Candidates may be staged; merging into SELF / EVIDENCE / prompt follows the instance’s gated pipeline.
3. **Template clarity:** The template may ship demos (`users/demo/`) and `_template` scaffolds; it does not ship production secrets or a live companion identity.
4. **Naming:** Prefer **companion self** (concept) vs **companion-self** (template repo name); see [concept](concept.md) for terminology.
5. **State layers:** The template preserves the distinction between **Evidence**, **Prepared Context**, and **Governed State** ([state-model.md](state-model.md)). Instances may customize staging or evidence tooling but should **not** collapse these layers into one undifferentiated memory surface.
6. **Truth precedence and review:** Instances may extend source systems and tooling, but should **preserve declared truth precedence** and **review rules** when material conflicts arise ([source-of-truth.md](source-of-truth.md), [conflict-resolution-order.md](conflict-resolution-order.md), [change-review.md](change-review.md)).
7. **Authority classes:** Instances may add local surface keys or tooling, but should **preserve explicit authority classes** and **not silently widen** automated write or merge authority ([authority-map.md](authority-map.md)).
8. **Receipts vs Record:** Instances may extend receipt or audit logging, but **must not replace** governed state with receipt objects alone ([action-receipts.md](action-receipts.md)).

---

## Upgrade rule

When the template bumps **seed-phase version**, **schemas**, or **governance docs**, instances should:

1. Read release notes / `template-version.json` (and [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md)).
2. Run validation scripts against their artifact paths.
3. Record intentional divergence in instance docs (for example `docs/template-sync-status.md` in grace-mar) rather than silently drifting.

---

## See also

- [Instance patterns](instance-patterns.md) — reference implementation (Grace-Mar) and staging contract
- [Gate vs change-review](gate-vs-change-review.md) — when to use the gate vs the change-review queue
- [Change review](change-review.md) — post-seed material change pipeline
