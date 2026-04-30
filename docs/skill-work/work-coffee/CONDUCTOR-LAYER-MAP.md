# Conductor Layer Map

**Status:** WORK / operator doctrine — **not** Record, **not** gate authority. Links companion docs without replacing them.

---

## 1. Purpose

The **five conductors** mechanism is a **stance-selection** and **attention-routing** device for Grace-Mar work. It helps the operator decide **how** to approach a piece of work **before** acting. It is **not** an autonomous agent system, **not** a dashboard family, and **not** a Record authority surface.

---

## 2. Core Principle

The conductors are **modes of attention**, not actors with independent authority. They may shape rehearsal, synthesis, draft preparation, review posture, and **coding-agent proposal design**, but they **do not** promote candidates, write durable Record state, bypass recursion-gate, or override the operator.

---

## 3. The Five Conductors

| Conductor | Slug | Mode | Primary Function | Typical Use |
|-----------|------|------|------------------|-------------|
| Toscanini | `toscanini` | Precision | Verify seams, strip unsupported rhetoric, enforce discipline | Citation checks, boundary audits, unsupported claim cleanup |
| Furtwängler | `furtwangler` | Flow | Preserve unresolved tension and organic emergence | Conflicting experts, watch markers, unresolved strategic tension |
| Bernstein | `bernstein` | Vitality | Make stakes vivid and publicly intelligible | Reflection paragraphs, public-facing synthesis, persuasion |
| Karajan | `karajan` | Elegance | Shape long arc, balance, polish, total effect | Monthly synthesis, balance checks, architectural polish |
| Kleiber | `kleiber` | Selectivity | Narrow ruthlessly and refuse excess | PR triage, next-action choice, anti-sprawl decisions |

Use the ASCII slug **`furtwangler`** for durable logs unless the repo already uses a different canonical slug. Display name may remain **Furtwängler**.

---

## 4. Layer Map

| Layer | File | Role | Authority |
|-------|------|------|-----------|
| **Synthesis theory** | [SYNTHESIS-OPERATING-MODEL.md](../work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md) | Defines the operator-as-conductor model and polyphonic synthesis principle | Theory / doctrine only |
| **Strategy ritual** | [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) | Applies the five movements to strategy-notebook coffee cadence | WORK-layer ritual |
| **Generic conductor pass** | [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md) | Defines the portable cross-lane conductor pass shape | WORK-layer pass shape |
| **Cursor conductor skill** | [`.cursor/skills/conductor/SKILL.md`](../../../.cursor/skills/conductor/SKILL.md) | Operational router for selecting conductor stance and action menu | Runtime/operator skill |
| **Coffee hub skill** | [`.cursor/skills/coffee/SKILL.md`](../../../.cursor/skills/coffee/SKILL.md) | Main coffee hub; may route to conductor pass but has its own A–E menu | Runtime/operator skill |
| **Compiled-view recipe** | [expert-polyphony-synthesis-five-conductors.md](../work-strategy/strategy-notebook/compiled-views/recipes/expert-polyphony-synthesis-five-conductors.md) | Derived Symphony Snapshot output recipe | Derived view recipe only |
| **Coding proposal lenses** | [conductor-proposal-lenses.md](../work-dev/conductor-proposal-lenses.md) | Translates conductor modes into coding-agent proposal shapes | Prompt convention only |
| **Derived metrics (offline)** | [conductor-observability.md](conductor-observability.md) | Heuristic scoring + replay harness for Conductor action MCQ text — rebuildable JSON, not Record | Derived WORK observability only |

Clarifications:

- No single layer replaces the others.
- The layer map exists to prevent accidental conflation.
- The strategy-notebook ritual remains the most concrete **notebook-specific** implementation.
- The generic conductor pass is the reusable **cross-lane** abstraction.
- The Cursor skill is **operational routing**, not doctrine.
- The coffee hub has its **own** menu and may route **into** conductor work.
- The compiled-view recipe is **downstream output shaping**, not the mechanism itself.
- The coding proposal lenses are **prompt conventions**, not code authority.

---

## 5. Menu Naming Standard

Define the three menu names:

### Coffee Hub Menu

The **A–E** menu used by [`.cursor/skills/coffee/SKILL.md`](../../../.cursor/skills/coffee/SKILL.md) to route the operator among broad coffee-session options (**Steward / Engineer / Historian / Capitalist / Conductor**).

### Master Selection Menu

The **A–E** menu used to select a **conductor stance**: Toscanini, Furtwängler, Bernstein, Karajan, or Kleiber (often printed as the **Conductor MCQ** masters row — see [CONDUCTOR-PASS.md — Conductor MCQ](CONDUCTOR-PASS.md#conductor-mcq)).

### Conductor Action Menu

The **A–C** menu used **after** a conductor stance is selected to choose the **concrete next actions** for this pass ([CONDUCTOR-PASS.md — Conductor action MCQ](CONDUCTOR-PASS.md#conductor-action-mcq)). All three options should be live choices; refusal / park / no-action is inferred from off-menu behavior rather than presented as one of the three.

Rules:

- Never present **two unlabeled** **A–E** menus in the same output.
- When two menus appear near each other, **label** them explicitly using these names (or equivalent explicit headers).
- **Durable logs** and **file metadata** should prefer **conductor slugs**, not menu letters.
- Letters are **UI conveniences** only.
- If a menu **order** changes, the **slug** remains the stable identifier.

---

## 6. Default Routing by Problem Type

| Problem Type | Default Conductor | Why |
|--------------|-------------------|-----|
| Unsupported claim, bad citation, loose seam | Toscanini | Precision and verification are needed first |
| Conflicting expert lines | Furtwängler | The tension should be preserved before synthesis |
| Public-facing paragraph lacks force | Bernstein | Stakes and legibility need amplification |
| Monthly or long-arc synthesis feels uneven | Karajan | Balance and total shape matter most |
| Too many possible next actions | Kleiber | Narrowing is the work |
| PR triage or implementation sequence is bloated | Kleiber | Refuse excess and choose one next move |
| Boundary or authority ambiguity | Toscanini | Enforcement precedes creativity |
| Strategy thread becoming flattened or over-smoothed | Furtwängler | Polyphony should not be prematurely resolved |
| Notebook becoming ornate or bloated | Karajan or Kleiber | Shape or narrow depending on the failure mode |
| Reflection section lacks human energy | Bernstein | The work needs vitality, not more scaffolding |

---

## 7. Logging and Metadata Guidance

Durable logs, receipts, and structured metadata should use conductor **slugs**:

- `toscanini`
- `furtwangler`
- `bernstein`
- `karajan`
- `kleiber`

Avoid storing **`A`**, **`B`**, **`C`**, **`D`**, **`E`** as stable identifiers for conductor stance.

Letters may appear in user-facing menu text, but **not** as the canonical persisted stance key.

---

## 8. Beethoven and Brahms Test Pointers

The **Beethoven test** in [`../work-dev/conductor-proposal-lenses.md`](../work-dev/conductor-proposal-lenses.md) clarifies how the five conductors differ under **crisis**, **propulsion**, and **formal drama** — use it when conductor proposal styles begin to flatten in those dimensions.

The **Brahms test** (same file, distinct appendix) clarifies distinctions in **density**, **continuity**, **warmth**, **overlap**, and **anti-heaviness** — use it when the problem is crowded or inert texture rather than dramatic conflict.

Use **both** when proposals still collapse into the same generic PR shape after stance selection.

---

## 9. Non-Authority Statement

The conductor mechanism is **WORK-layer attention routing** and **prompt discipline**. It does **not** create durable Record truth, approve candidates, write to canonical surfaces, or bypass recursion-gate. Any promotion remains governed by existing Grace-Mar authority paths.

---

## 10. Maintenance Rule

Future conductor-related docs should **link back to this layer map** when they introduce menu choices, conductor slugs, compiled conductor outputs, or coding-agent proposal lenses.
