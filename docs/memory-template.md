# MEMORY–TEMPLATE v2.0

Self-memory · Short / medium / long horizons · Not part of the Record

Status: ACTIVE  
Version: 2.0  
Last Update: March 2026

**Governed by**: [GRACE-MAR-CORE v2.0](grace-mar-core.md)

---

## I. PURPOSE

The MEMORY module (**self-memory**, file `memory.md`) holds **continuity context** at **three horizons** — short, medium, and long — used to prime the Voice and improve continuity. Content is **mostly chronological**: within each horizon, entries read as a **time-ordered prose thread** (what happened lately, what is open now). That is a **slim** chronology — not **multicategory** structured evidence (no READ-/ACT- sections, no artifact spine). MEMORY is **not part of the Record**. It refines; it does not override SELF.

**“Ephemeral” in governance docs** means **outside the gated Record** and **intended to be rotated or pruned** — **not** a synonym for “short-term only.” All three horizons (including **long**) are still MEMORY, not SELF; **long** is for **meta** (pointers, habits, where truth lives), not for smuggling durable identity or facts without the gate.

**Horizon ≠ authority.** Long-term here means **how you run sessions** (pointers, habits, rotation policy), **not** a second copy of durable identity or facts. Those belong in **SELF**, **EVIDENCE** (`self-archive.md`), and the **gate**.

**Contrast with self-archive (EVIDENCE).** Canonical **self-archive.md** is **also chronological** (dated entries, list ordering, ACT/READ progression within each log) but **far more expansive**: **multicategory** (separate sections and id families for reading, writing, creation, activity, media, § VIII) and **multimodal** (artifact paths, YAML, gated approved blocks) — all **durable Record** once merged. **MEMORY** is deliberately **narrow**: mostly prose across three horizons for session continuity and meta pointers — chronology without that **category spine** or multimodal evidence shape. It does not substitute for evidence, artifacts, or the activity log.

### MEMORY is

- **Short-term** — session / day: tone, immediate thread, calibrations, resistance for *this* stretch
- **Medium-term** — days to a few weeks: open loops, sprint-level notes, hypotheses **explicitly labeled** as such
- **Long-term (still non-Record)** — months: **meta only** — rotation habits, pointers to where durable truth lives (`self.md`, `self-work.md`), standing *process* preferences — not stable facts

### MEMORY is NOT

- A shadow Record — no durable facts, identity claims, or knowledge (use IX-A/B/C + gate)
- A staging area for the pipeline — that is RECURSION-GATE
- A substitute for SELF — SELF is authoritative; MEMORY defers

---

## II. HIERARCHY

**SELF is authoritative.** When MEMORY conflicts with SELF, follow SELF.

**Promotion rule:** If a line **survives weeks** or **repeats across sessions** and sounds like Record content, **stage a candidate** (LEARN / CUR / PER / self-identity per protocol) — do **not** “upgrade” it to long-term MEMORY instead of the gate.

---

## III. CONTENT SCOPE

| Horizon | Allowed | Avoid |
|---------|---------|--------|
| **Short-term** | Tone, recent thread topics, session calibrations, resistance notes | Facts that belong in IX-A; interests that belong in IX-B |
| **Medium-term** | Open loops, “mid-project” reminders, operator coordination cues | Copy-pasting SELF; internals as if public truth |
| **Long-term** | “Last rotated” policy, links to canonical files, session *process* | Knowledge claims, personality claims, user quotes |

MEMORY must NOT contain (any horizon):

- Facts or knowledge claims that belong in **SELF**
- Identity or personality claims that belong in **SELF** or **self-identity.md**
- User quotes or verbatim content intended as Record
- Anything that would require the gated pipeline if it were true in-character

---

## IV. LIFESPAN & DECAY

| Horizon | Suggested span | Action |
|---------|----------------|--------|
| **Short** | Hours–2 days | Clear or trim at session end / daily |
| **Medium** | Days–few weeks | Weekly prune; promote to gate if it’s really Record |
| **Long** | Until you revise | Quarterly review; must stay meta/pointers only |

Document policy in the file header / **Long-term** block. Optional: `expires: YYYY-MM-DD` on bullets (operator honor system).

The Voice loads horizons in order (**short → medium → long**) with **per-section line caps** in code to limit prompt size.

---

## V. WRITE RULES

- The analyst does NOT write to MEMORY. Analysts stage to RECURSION-GATE only.
- MEMORY may be written by: operator (manual), future session summarizer, or user.
- Nothing in MEMORY may become a claim in SELF or EVIDENCE without going through the gated pipeline.

---

## VI. TEMPLATE STRUCTURE (three horizons)

Use these **exact** top-level headers so the bot can bucket content: `## Short-term`, `## Medium-term`, `## Long-term`.

Legacy files that only use `## Tone`, `## Recent Topics`, etc. (no horizon headers) still work: the whole file is treated as one block (backward compatible).

```markdown
# MEMORY — Ephemeral Session Context

> Not part of the Record. SELF is authoritative.

Last rotated: YYYY-MM-DD

## Short-term

(session / day — tone, thread, calibrations, resistance)

## Medium-term

(days–weeks — open loops, labeled hypotheses)

## Long-term

(meta — rotation policy, pointers to self.md / self-work.md; no durable facts)
```

Optional: keep **## Resistance Notes** under **Short-term** or as its own `##` subsection under Short-term (subsections stay inside Short-term).

---

## VII. LEGACY (v1.0) — single block

If you omit horizon headers, you may keep the older shape (`## Tone`, `## Recent Topics`, `## Calibrations`, `## Resistance Notes`). The loader will pass the filtered file through as before.
