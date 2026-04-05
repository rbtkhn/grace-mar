# Seed Intent

**Companion-Self template · Seed-phase artifact**

Seed Phase should establish not only **who** the companion is for, but **what** the companion is **for** — explicit operating purpose and limits before activation.

---

## Why this exists

A companion should not be activated from vague personalization alone. **`seed_intent.json`** captures:

- supported workflows  
- unsupported workflows  
- review-required zones  
- human-only judgment zones  
- what counts as **successful activation**  

---

## Artifact

**File:** `seed_intent.json` in the seed-phase bundle (alongside `seed-phase-manifest.json`, `seed_intake.json`, …).

**Schema:** [schema-registry/seed-intent.v1.json](../schema-registry/seed-intent.v1.json)

---

## Relationship to other artifacts

Seed Intent **does not replace** identity, curiosity, pedagogy, or expression artifacts. It **clarifies** the operating purpose and boundaries of the future instance. Intake may still carry constraints and operator workspace intent ([cursor-pack-from-seed.md](cursor-pack-from-seed.md)); Seed Intent is the **normative purpose/limits** slice for governance and readiness review.

See [seed-phase-artifacts.md](seed-phase-artifacts.md) and [seed-phase-readiness.md](seed-phase-readiness.md).
