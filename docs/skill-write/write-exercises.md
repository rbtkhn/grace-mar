# WRITE — exercises and tests

**Purpose:** Add a lightweight exercise layer to WRITE so public-copy preferences and writing capability are both sharpened through repeated use.

**Fits current doctrine:** The docs in `docs/skill-write/` remain the hub for operator preferences and drafting craft. Companion WRITE in the Record (`users/[id]/skill-write.md`) remains the capability-facing evidence layer. These exercises target the **operator publishing** layer — Locals, X, YouTube comments — not the companion's developmental writing trajectory.

## Principles

- Prefer short, repeatable drills over large writing ceremonies.
- Tests should improve public-copy quality for Locals, X, YouTube comments, and similar surfaces.
- Preference doctrine and capability evidence should not be conflated.
- WRITE may consume THINK and STRATEGY inputs, but owns prose shaping.

---

## Standard test types

### 1. `surface_trim`

Rewrite the same idea for multiple surfaces.

**Goal:** Prove that one argument can be adapted cleanly for Locals, X, and YouTube comments.

**Prompt:**

> Rewrite this draft for three surfaces:
> - Locals
> - X
> - YouTube comment
>
> Keep the same core claim while changing density, pacing, and sentence length.

**Return:**
- one version for each surface
- what changed across surfaces
- what core claim remained constant

### 2. `lede_test`

Produce three different openings.

**Goal:** Strengthen topic-first openings and reduce weak setup.

**Prompt:**

> Write three alternate ledes for this argument:
> - direct / topic-first
> - contrast-driven
> - concrete / stakes-first

**Return:**
- best option
- why it is best
- what problem the weaker options still have

### 3. `closer_test`

Produce three different endings.

**Goal:** Improve memorability and avoid weak abstract stacked closers.

**Prompt:**

> Write three alternate closers:
> - one sharp declarative line
> - one concise synthesis line
> - one emphatic but non-theatrical ending

**Return:**
- best option
- what makes it memorable
- what the weaker options lose

### 4. `density_control`

Rewrite at different densities.

**Goal:** Show control over compression and expansion.

**Prompt:**

> Write this in:
> - 280 characters
> - 2 sentences
> - 120 words
> - 250 words

**Return:**
- all four versions
- what was lost at each compression level
- which density best serves the argument

### 5. `voice_preservation`

Rewrite without losing the operator's recognizable style.

**Goal:** Calibrate agent-assisted writing to operator taste.

**Prompt:**

> Rewrite this draft to improve clarity and force without changing the underlying voice.

**Return:**
- revised draft
- what was changed
- what was intentionally preserved

### 6. `shipping_check`

Run a final pre-flight test.

**Goal:** Reduce bloat, cliché, and weak endings before public posting.

**Prompt:**

> Audit this draft for:
> - weak opening
> - stacked abstract ending
> - rhetorical-question closer
> - unnecessary throat-clearing
> - phrase-level bloat

**Return:**
- flagged issues (if any)
- suggested fix for each
- clean-to-ship judgment

---

## Scaffolding levels

| Level | Meaning |
|-------|---------|
| `full_template` | Full structure and hints provided |
| `hints_only` | Partial guidance; no template |
| `none` | No scaffolding; independent performance |

## Test result values

| Result | Meaning |
|--------|---------|
| `pass` | Meets the test goal cleanly |
| `partial` | Some success, some gaps |
| `fail` | Does not meet the test goal |

---

## Recording results

Add the following optional fields to a claim in [`write-claims.json`](../../artifacts/skill-write/write-claims.json):

| Field | Type | Purpose |
|-------|------|---------|
| `test_type` | string (enum) | Which test was run |
| `test_date` | date string | When |
| `test_result` | `pass` / `partial` / `fail` | Outcome |
| `target_surface` | `locals` / `x` / `youtube_comment` / `general` | Which publishing surface |
| `scaffolding_level` | `full_template` / `hints_only` / `none` | How much support |
| `sample_ref` | string (optional) | Draft or sample id |
| `failure_mode_notes` | string (optional) | What breaks and how to fix it |
| `next_test` | string (optional) | Next intended test type |

See [`write_claims.schema.json`](../../schemas/skill_write/write_claims.schema.json) for the full schema.

---

## Relation to existing craft docs

These exercises complement the existing shipping and craft rules:
- [write-shipping-checklist.md](write-shipping-checklist.md) — pre-flight for all surfaces
- [write-operator-preferences.md](write-operator-preferences.md) — voice, register, canonical inputs
- [write-memorable-closer.md](write-memorable-closer.md) — closer craft
- [write-no-abstract-stacked-closers.md](write-no-abstract-stacked-closers.md) — anti-pattern
- [write-no-rhetorical-question-closer.md](write-no-rhetorical-question-closer.md) — anti-pattern

The `shipping_check` test type specifically exercises the rules from these docs.
