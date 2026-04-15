# Skills membrane — cross-module flow map

**Purpose:** Define how information may cross between Record skill modules (THINK, WRITE) and adjacent work territories (work-strategy) without collapsing boundaries. This doc adds the **cross-module flow map** that [skills-modularity.md](skills-modularity.md) does not provide; it complements (does not restate) the formal module boundaries in skills-modularity §3 and the data flow diagram in §5.

---

## Core rule

**Modules may exchange typed seams, not shared truth surfaces.**

A crossing is valid when:

1. The **source** keeps ownership of its own truth surface.
2. The **destination** reinterprets the incoming material in its own lane terms.
3. Any **SELF-facing** change still goes through RECURSION-GATE and companion approval.

If a move transfers ownership without reinterpretation, it is a membrane violation.

---

## Vocabulary note

This doc defines **cross-module seams** — flows between Record skill modules and work territories (THINK → WRITE, work-strategy → THINK, etc.).

The strategy lane also uses **strategy-internal crossing tokens** (`seam:ritter+davis`, `membrane:single`, `crosses:`) documented in [strategy-commentator-threads.md § Crossing filters](skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md). Those are **within-strategy** hygiene for expert-lane crossings, not cross-module flows. Both levels are valid; they operate at different scopes.

---

## Allowed flows

| Flow | What crosses | Friction |
|------|-------------|----------|
| **THINK → WRITE** | Topic familiarity, reasoning depth, vocabulary range, contrast ability | Easy |
| **THINK → work-strategy** | Lenses the fork can use, comprehension improvements, transferable distinctions | Easy |
| **work-strategy → WRITE** | Knots, inbox lines, active watches, decision framing, strategy synthesis | Easy |
| **work-strategy → THINK** | Repeated demonstrated synthesis patterns, observed reasoning gains | Narrow |
| **WRITE → THINK** | Evidence that the fork can explain, compress, contrast, or adapt across surfaces | Narrow |
| **WRITE → work-strategy** | Discovered ambiguity, weak thesis, unsupported claim, unclear stakes | Narrow |
| **any → SELF** | Only through RECURSION-GATE and companion approval | Hardest |

### What does not cross

| Flow | Excluded |
|------|----------|
| THINK → WRITE | Identity truth, public-copy preferences, direct Voice rewrites |
| THINK → work-strategy | Record truth, direct knot edits by implication, SELF claims |
| work-strategy → WRITE | Record truth, automatic capability claims |
| work-strategy → THINK | Raw knot prose copied verbatim, automatic level upgrades |
| WRITE → THINK | Operator taste rules, public-surface defaults, direct identity claims |
| WRITE → work-strategy | Prose preferences as strategy truth |

---

## Disallowed flows

- **THINK, WRITE, work-strategy → SELF (automatic)** — No automatic merge into SELF from any module or territory. SELF remains gated.
- **WRITE doctrine → Companion WRITE capability** — Operator preferences in `docs/skill-write/` do not automatically become Record capability claims in `users/[id]/skill-write.md`.
- **work-strategy → Record truth** — No direct writes from work territory into Record skill containers without an explicit staged update step.

---

## Asymmetry rule

The membrane is intentionally asymmetric:

| Direction | Friction |
|-----------|----------|
| THINK → work-strategy | Easy |
| THINK → WRITE | Easy |
| work-strategy → WRITE | Easy |
| work-strategy → THINK | Narrower |
| WRITE → THINK | Narrower |
| any lane → SELF | Hardest |

This reflects the architecture: capability can inform execution; execution can produce evidence; but identity requires separate approval.

---

## Strongest rule

**Crossing the membrane should change the type of the object.**

- A THINK item crossing into work-strategy becomes **strategy context**.
- A work-strategy item crossing into WRITE becomes **draft input**.
- A WRITE sample crossing into THINK becomes **evidence of capability**.
- Nothing crosses into SELF automatically.

---

## Decision test

Before allowing a cross-lane move, ask:

1. Is this crossing **context**, **evidence**, or **ownership**?
2. Has the destination **rewritten** the material in its own lane terms?
3. Would this change **identity-facing Record truth**?
4. If yes, has it gone through **gate / approval**?

If the move transfers ownership without reinterpretation, it is probably a membrane violation.

---

## Future schema adoption

When THINK and WRITE claims accumulate, the following seam fields are candidates for schema adoption:

| Field | Purpose |
|-------|---------|
| `applied_in` | Where the capability was exercised (downstream lane) |
| `inputs_from` | Upstream context consumed by this claim |
| `candidate_for` | Possible gated promotion target |
| `seam_note` | Short explanation of what crossed and what did not |

Not adding them now — schemas were just built, zero claims exist. Strategy knots already have a **Lineage** section (Inbox, Expert threads, History resonance, Civilizational bridge) that covers the `inputs_from` role for that surface. WRITE claims already have `target_surface` and `sample_ref`.

---

## Cross-references

| Topic | Where |
|-------|-------|
| Formal module boundaries, data flow | [skills-modularity.md](skills-modularity.md) §3, §5 |
| THINK is not SELF / WORK / EVIDENCE | [think-purpose-and-boundary.md](skill-think/think-purpose-and-boundary.md) |
| Strategy-internal crossing filters | [strategy-commentator-threads.md](skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md) § Crossing filters |
| Gate as membrane (Record boundary) | [conceptual-framework.md](conceptual-framework.md) |
| WRITE two-layer split (doctrine vs Record) | [skill-write/README.md](skill-write/README.md) |
