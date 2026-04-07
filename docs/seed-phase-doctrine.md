# Seed Phase Doctrine

**Companion-Self template -- Constitutional principles for identity formation**

---

## Framing sentence

> Companion-Self does not assume identity; it cultivates identity under governance.

---

## The seven principles

### 1. The system begins without entitlement to durable personal truth

A new companion instance has no identity until evidence is gathered and reviewed. The blank state is the correct starting state. Seed phase is not an absence to be filled quickly; it is a constitutional regime that protects the companion from premature definition.

### 2. Early observations are provisional by default

Every observation enters the Seed Registry as `observed` -- the lowest status. It carries no weight in governed state, cannot alter the durable profile, and cannot drive external actions. Provisional is the default; durable must be earned.

### 3. Recurrence matters more than vividness

A single vivid statement is less trustworthy than a pattern observed across sessions, contexts, and time. The promotion threshold engine encodes this: no claim advances on one observation. Recurrence, time stability, and source diversity outweigh intensity.

### 4. Contradictions are preserved, not collapsed

When evidence conflicts -- the companion says they want to be an astronaut and later says veterinarian -- the system records both observations with explicit contradiction refs. It does not silently discard one to make the profile tidy. Tension is signal; resolution is the companion's prerogative.

### 5. Promotion into governed state must be earned

Each seed claim must pass through promotion thresholds before it can enter the governed Record. The thresholds are explicit, configurable, and sensitivity-aware: identity-shaping claims face stricter requirements than casual preferences. This is where ethics become executable.

### 6. The operator retains final authority over durable identity formation

No automated process may promote a claim into governed state without human review. Sensitivity tiers `elevated` and `high` require explicit operator flags or approval. The system assists formation; it does not decide formation.

### 7. The system may assist formation, but may not silently define the companion

The Weak Signal Nursery may influence soft exploration (question suggestions, curiosity prompts, topic ordering) for claims at `recurring` or higher status. But nursery claims may never alter the durable profile, drive external actions, or be presented as known facts about the companion. The line between "watching with interest" and "acting as if known" is a governance boundary.

---

## What seed phase is not

- **Not onboarding.** Onboarding is UX convenience. Seed phase is a governed formation layer.
- **Not a hidden bootstrap period.** Seed phase is a first-class product and doctrine layer with its own schemas, scripts, thresholds, and audit surfaces.
- **Not an early implementation state.** Seed phase is a constitutional regime -- the system operates under specific rules during formation that differ from post-activation governance.
- **Not a data collection sprint.** The goal is not to fill the profile quickly. The goal is to build durable identity from evidence under review.

---

## What problem this solves

Most AI companion systems handle formation badly through **false early certainty**:

```
conversation -> extract preference -> store memory -> act as if known
```

This pattern produces premature identity collapse: the system infers a person from a few interactions and then reinforces the wrong pattern.

Seed phase provides a fundamentally different formation pipeline:

```
signal -> recurrence -> evidence clustering -> candidate identity -> governed promotion
```

The difference is governance at every stage.

---

## Doctrine version

The `seed-phase-manifest.v1.json` schema includes a `doctrine_version` field so each fork declares which doctrine it was formed under. This provides forward-compatible governance: when doctrine evolves, existing forks retain their formation provenance.

---

## Cross-references

- [seed-phase.md](seed-phase.md) -- Pre-activation artifact pipeline
- [seed-registry.md](seed-registry.md) -- Per-claim lifecycle tracking
- [seed-promotion-thresholds.md](seed-promotion-thresholds.md) -- Promotion rules
- [seed-nursery.md](seed-nursery.md) -- Weak Signal Nursery
- [seed-timeline.md](seed-timeline.md) -- Formation chronology
- [seed-phase-readiness.md](seed-phase-readiness.md) -- Activation gate
- [change-review.md](change-review.md) -- Post-activation governed revision
- [conceptual-framework.md](conceptual-framework.md) -- Fork vs twin, identity architecture
- [AGENTS.md](../AGENTS.md) -- Knowledge boundary, gated pipeline
