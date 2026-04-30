# Ubiquitous Language + Tracer-Bullet Plans

**Status:** WORK-layer operating primitive. **Not** Record truth. **Not** a gate path.

## Purpose

Use this primitive when a work-dev slice risks vocabulary drift, hidden scope expansion, or a documented-only idea being mistaken for an implemented capability.

It borrows two useful habits from coding-agent skill practice:

1. **Ubiquitous Language** - agree on the project slice's terms before building.
2. **Tracer-Bullet Plan** - prove the thinnest end-to-end path before expanding.

Together they give an agent and operator a shared map: what the words mean, what the first proof must touch, and what claims are still forbidden.

## Ubiquitous Language

A ubiquitous-language block is a small glossary for one project slice. It should be short enough to read before implementation starts.

Include:

| Field | Purpose |
|-------|---------|
| **Canonical terms** | The exact terms to use in docs, prompts, code comments, and handoffs. |
| **Banned synonyms** | Words that blur boundaries or imply authority the system does not have. |
| **Boundary terms** | Phrases that mark governance, Record, WORK, generated, staged, or implemented status. |
| **Source-of-truth paths** | Files the agent must inspect before making claims. |
| **Do-not-imply phrases** | Claims the work must avoid unless proof exists. |

Good Grace-Mar candidates:

- `work-cici` lanes: Telegram motion, Core safety, Progress proof.
- Grace Gems monthly review: books, shop health, marketing, tax/compliance readiness.
- Derived regeneration: generated artifacts, rebuild receipts, rationale sidecars, non-canonical status.
- Conductor improvements: ritual lens, coding-agent proposal shape, durable close.
- OpenClaw integration: export, stage-only handback, provenance, companion gate.

## Tracer-Bullet Plan

A tracer-bullet plan is the smallest vertical proof path through a feature or workflow. It is not the full roadmap. It is the first live path that shows whether the idea can travel from input to output to receipt without confusing authority or proof status.

Include:

| Field | Purpose |
|-------|---------|
| **Input** | The smallest real or representative event, file, command, post, or user action. |
| **Path** | The exact files, functions, docs, or surfaces the slice touches. |
| **Output** | The smallest useful artifact or visible behavior. |
| **Proof** | A command, inspection receipt, test, screenshot, or manual check that shows the slice works. |
| **Stop criteria** | Conditions that mean do not expand yet. |
| **Expansion path** | The next broader step only after proof exists. |

The tracer bullet should be narrow enough that failure is informative. If it cannot produce proof, keep it as a documented idea rather than upgrading the status language.

## Fit With The Compound Loop

Use this before the existing [Compound Work Loop](compound-loop.md):

1. **Language** - define terms, forbidden claims, and source-of-truth paths.
2. **Tracer bullet** - pick the smallest end-to-end proof wedge.
3. **Plan** - apply normal work-dev planning with governance risks named.
4. **Execute** - implement the narrow slice.
5. **Review** - check proof, authority, and vocabulary drift.
6. **Compound** - capture reusable lessons in WORK-only compound notes if useful.
7. **Gate** - only if a later human/companion review chooses to stage Record-relevant changes.

This primitive does not create a parallel memory system. It makes the next coding-agent session less likely to overclaim, rename concepts casually, or treat draft structure as implemented behavior.

## Default Rule

When the work is ambiguous, use the template first. A ten-minute language-and-tracer pass is cheaper than repairing a week of mismatched terms, inflated claims, or untestable architecture.
