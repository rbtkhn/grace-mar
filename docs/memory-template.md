# MEMORY–TEMPLATE v1.0

Ephemeral Session Context · Not Part of the Record

Status: ACTIVE
Version: 1.0
Last Update: February 2026

**Governed by**: [GRACE-MAR-CORE v2.0](grace-mar-core.md)

---

## I. PURPOSE

The MEMORY module holds **ephemeral session/working context** — tone, recent topics, and calibrations — used to prime the Voice and improve continuity between sessions. MEMORY is **not part of the Record**. It refines; it does not override SELF.

### MEMORY is

- Session-level context (tone, focus, recent topics)
- Calibrations (e.g. "user asked for shorter answers today")
- Optional — the system runs normally if memory.md is absent

### MEMORY is NOT

- A shadow Record — no facts, identity claims, or knowledge
- A staging area for the pipeline — that is PENDING-REVIEW
- A substitute for SELF — SELF is authoritative; MEMORY defers

---

## II. HIERARCHY

**SELF is authoritative.** When MEMORY conflicts with SELF, follow SELF. MEMORY refines tone and focus; it does not override identity, knowledge, or personality.

---

## III. CONTENT SCOPE

MEMORY may contain only:

| Section | Allowed | Example |
|---------|---------|---------|
| **Tone** | Calibrations for current session | `playful`, `calm`, `focused`, `tired` |
| **Recent Topics** | Topics of recent conversation | `frogs`, `solar system`, `art project` |
| **Calibrations** | Session-specific preferences | `shorter answers today`, `more questions than usual` |
| **Resistance Notes** (optional) | Topics to avoid or handle gently | `resistance on school questions`, `deflected when asked about X` |

MEMORY must NOT contain:

- Facts or knowledge claims
- Identity or personality claims
- User quotes or verbatim content
- Anything that would require the gated pipeline if it entered the Record

---

## IV. LIFESPAN

MEMORY is ephemeral. Implement a rotation policy:

- **Daily** — Clear or rotate at start of day
- **Weekly** — Prune entries older than 7 days
- **Session-scoped** — Clear at session end (if used for single-session only)

Document the chosen policy in the MEMORY file header. Include timestamps on entries when helpful.

---

## V. WRITE RULES

- The analyst does NOT write to MEMORY. Analysts stage to PENDING-REVIEW only.
- MEMORY may be written by: operator (manual), future session summarizer, or user.
- Nothing in MEMORY may become a claim in SELF or EVIDENCE without going through the gated pipeline.

---

## VI. TEMPLATE STRUCTURE

```markdown
# MEMORY — Ephemeral Session Context

> Not part of the Record. SELF is authoritative. Rotate: [daily|weekly|session].

Last rotated: YYYY-MM-DD

## Tone

(optional: current tone calibration)

## Recent Topics

(optional: topics from recent conversations)

## Calibrations

(optional: session-specific preferences)

## Resistance Notes

(optional: topics to avoid or handle gently — e.g. "resistance on school questions"; use to avoid retriggering next session)
```
