# Seed Phase

**Companion-Self template · Formation protocol (v2 entrypoint)**

---

## Purpose

**Seed phase** is the **structured formation pipeline** that runs **before** a new companion instance is **activated**. It produces **inspectable JSON artifacts**, **confidence signals**, and a **readiness decision**. It is the **only** sanctioned creation path: no copying another repo’s `users/` and no pre-filled live Record.

---

## Why seed phase exists

- **Sovereignty** — The human (and guardian when applicable) explicitly shapes identity, curiosity, pedagogy, expression, and memory rules before automation scales.
- **Evidence-before-merge** — Formation outputs are **separate** from the gated Record merge path; activation is a deliberate handoff.
- **Measurability** — Stages, schemas, and validation make progress visible and CI-checkable.

---

## Stage model

Canonical stages **0–7** are defined in **[seed-phase-stages.md](seed-phase-stages.md)**:

0. Intake  
1. Identity Scaffold  
2. Curiosity Scaffold  
3. Pedagogy Scaffold  
4. Expression Scaffold  
5. Memory Contract  
6. Trial Interactions  
7. Readiness Gate  

---

## Required outputs

The artifact set (file names, roles, layout) is specified in **[seed-phase-artifacts.md](seed-phase-artifacts.md)**. Every artifact has a **JSON Schema** under `schema-registry/` (see [schema-record-api.md](schema-record-api.md)).

---

## Intent as a seed artifact

Seed Phase includes **`seed_intent.json`**: explicit purpose, boundaries, supported and unsupported workflows, and review-sensitive zones for the future instance. It complements intake and identity artifacts; it does not replace them.

See **[seed-phase-intent.md](seed-phase-intent.md)** and **`schema-registry/seed-intent.v1.json`**.

---

## Readiness gate

**Readiness** is a **hard gate**, not advisory. Rules, thresholds, conditional pass, and re-run-after-upgrade behavior are in **[seed-phase-readiness.md](seed-phase-readiness.md)**.

---

## Confidence model

Per-dimension and overall confidence use **0.0–1.0** scores and **low / medium / high** bands. Definitions: **[seed-phase-confidence-model.md](seed-phase-confidence-model.md)**.

---

## Activation rule

An instance is **activated** only when:

1. Required seed artifacts exist and validate (see [seed-phase-validation.md](seed-phase-validation.md)).  
2. `seed_readiness.json` records an allowed decision (`pass` or `conditional_pass` per policy).  
3. `seed_dossier.md` is reviewed and operator (and guardian if applicable) sign off.  

Only **then** may `users/<birth-name>/` be created or promoted with the live pipeline. Merging into SELF / IX / evidence follows the **[identity-fork-protocol.md](identity-fork-protocol.md)** after activation.

---

## Seed Phase Doctrine

Seed phase is a **constitutional regime**, not just an implementation detail. The seven principles of formation governance are codified in **[seed-phase-doctrine.md](seed-phase-doctrine.md)**: provisional by default, recurrence over vividness, contradiction preservation, earned promotion, operator authority, no silent definition.

The `seed-phase-manifest.v1.json` schema includes an optional `doctrine_version` field so each fork declares which doctrine it was formed under.

---

## Seed Registry and per-claim lifecycle

Individual observations are tracked through the **[Seed Registry](seed-registry.md)**: per-claim lifecycle from first observation through recurrence, evidence clustering, and governed promotion. The registry sits between seed-phase artifact validation and post-activation RECURSION-GATE.

Supporting surfaces:
- **[Promotion thresholds](seed-promotion-thresholds.md)** -- pluggable rules for when claims can advance
- **[Weak Signal Nursery](seed-nursery.md)** -- "why is this still a seed?" explanations
- **[Seed Timeline](seed-timeline.md)** -- formation chronology for individual claims

---

## Post-seed governed revision

Seed Phase establishes the initial baseline for a new companion instance before activation.

After activation, materially important change should not be treated as silent memory drift or silent overwrite of governed state. The **[change-review](change-review.md)** pipeline (see also [change-review-lifecycle.md](change-review-lifecycle.md)) is where those revisions become visible and reviewable.

When new evidence materially affects:

- identity
- curiosity
- pedagogy
- expression
- memory governance
- safety or boundary posture
- other durable operating commitments

the instance should route that change through the change-review subsystem.

This preserves:

- prior state visibility
- supporting evidence
- contradiction classification
- confidence delta when available
- explicit decision before governed state is updated

Seed Phase and change review serve different roles:

- **Seed Phase** forms the initial companion.
- **Change review** governs materially important post-seed revision.

The two systems should remain separate.

Why this matters: the repo already treats seed phase as a defined artifact pipeline before activation, so this addition cleanly answers what happens after that baseline exists.

---

## Relationship to template vs instance

| Location | Role |
|----------|------|
| **This template repo** | Defines protocol, schemas, `_template` scaffold, `demo` example, validation scripts. |
| **Instance repo** (e.g. Grace-Mar) | Holds real `users/<id>/`; may run operator wizards; must align with template schema versions when syncing upgrades. |

---

## Implementation references

| Resource | Path |
|----------|------|
| Stage spec | [seed-phase-stages.md](seed-phase-stages.md) |
| Readiness | [seed-phase-readiness.md](seed-phase-readiness.md) |
| Confidence | [seed-phase-confidence-model.md](seed-phase-confidence-model.md) |
| Artifacts | [seed-phase-artifacts.md](seed-phase-artifacts.md) |
| Survey prompts | [seed-phase-survey.md](seed-phase-survey.md) |
| Validation | [seed-phase-validation.md](seed-phase-validation.md) |
| Schemas | `schema-registry/seed-*.v1.json` |
| Validator | `scripts/validate-seed-phase.py` |
| Dossier generator | `scripts/generate-seed-dossier.py` |
| Cursor pack from intake | Optional `cursor_operator_profile` on `seed_intake.json` — [cursor-pack-from-seed.md](cursor-pack-from-seed.md) |
| Template scaffold | `users/_template/seed-phase/` |
| Demo example | `users/demo/seed-phase/` |

---

## Historical note (v1 prose)

Early seed phase focused on surveys and initial SELF/self-evidence capture **inside** the instance. **v2** keeps that *outcome* as a goal of activation but **requires** the artifact pipeline above **before** activation so formation is **visible, versioned, and validatable**.

---

*Companion-Self template · Seed phase v2*
