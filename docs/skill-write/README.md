# skill-write — doctrine hub

**Purpose:** Operator- and agent-facing documentation for **WRITE** — **your writing preferences**, craft rules, and boundaries — **without** duplicating [skills-modularity.md](../skills-modularity.md) (formal module spec) in full. **Not** companion-indexed in SELF-LIBRARY unless you add that later — see [Visibility (recorded)](write-operator-preferences.md#visibility-recorded).

**Primary job:** Calibrate **system outputs** (e.g. `tri-mind` passes, strategy ingests, analysis threads) into **operator publishing surfaces** — especially **Locals** ([VivaBarnesLaw](https://vivabarneslaw.beta.locals.com/), **Duran** on Locals), **X**, and **YouTube comments** (especially **Predictive History**). **Recorded pipeline:** **Locals first**; **X / PH** as follow-on trims unless you direct otherwise. **Scope:** all **public operator** writing is covered here **unless** you exclude something by name (see [write-operator-preferences.md](write-operator-preferences.md)).

## Two layers (do not conflate)

| Layer | Location | Role |
|-------|----------|------|
| **Companion WRITE (Record)** | `users/[id]/skill-write.md` (and related evidence) | What the fork **demonstrates** — samples, YAML, capability trajectory; feeds **Voice** / linguistic layer per skills-modularity §4. |
| **skill-write doctrine (this hub)** | `docs/skill-write/*.md` | **Operator preferences** and **drafting craft** — how agent-assisted drafts are shaped for **Locals / X / YouTube comments** (above), plus ledes, closers, density; update when your taste changes. |

**Territory:** **self-skill-write** in the Record still means **capability-facing** production evidence. **Identity-facing** truth stays **SELF**. This hub holds **how you want prose shaped** when collaborating with agents, alongside pointers into `.cursor/rules/` where those rules are also enforced in Cursor.

**Evolving rules (recorded):** When doctrine changes, update **`docs/skill-write/`** and affected **`.cursor/rules/`** **in lockstep** — see [write-operator-preferences.md](write-operator-preferences.md) (*Changing rules*).

## Contents

| Doc | Role |
|-----|------|
| [write-operator-preferences.md](write-operator-preferences.md) | **SSOT for operator writing preferences** — living list; start here (includes **tri-mind → public copy** handoff and **Chat delivery** — full echo in Cursor thread) |
| [write-no-abstract-stacked-closers.md](write-no-abstract-stacked-closers.md) | Craft: avoid bloaty abstract stacked closers in short public copy |
| [write-memorable-closer.md](write-memorable-closer.md) | Craft: end on one strong sentence that encapsulates the core argument |
| [write-no-rhetorical-question-closer.md](write-no-rhetorical-question-closer.md) | Craft: do not end on a rhetorical question (prefer declarative closer) |
| *(sections in [write-operator-preferences.md](write-operator-preferences.md))* | Exposition vs. instructions; dispreferred pundit phrases (e.g. “has any bite,” “when the stakes spike”) |
| [write-shipping-checklist.md](write-shipping-checklist.md) | **Global** pre-flight checklist for all public operator surfaces |
| [write-exercises.md](write-exercises.md) | Test types, prompts, scaffolding for public-copy drills |

## Claims and observability

| Artifact | Role |
|----------|------|
| [`artifacts/skill-write/write-claims.json`](../../artifacts/skill-write/write-claims.json) | Operator WRITE capability claims (not companion Record) |
| [`schemas/skill_write/write_claims.schema.json`](../../schemas/skill_write/write_claims.schema.json) | JSON Schema for write claims |
| [`scripts/validate_write_claims.py`](../../scripts/validate_write_claims.py) | Validator with advisory warnings |
| [`scripts/build_write_observability.py`](../../scripts/build_write_observability.py) | Observability builder (surface-aware metrics) |

## Pipelines and formal spec

- [skills-modularity.md](../skills-modularity.md) — WRITE module, Voice as f(skill-write)
- [skills-template.md](../skills-template.md) — skill file shape
- Instance WRITE evidence: `users/[id]/skill-write.md` (or split per template); see [canonical-paths.md](../canonical-paths.md)
- Topic-first ledes (Cursor): [.cursor/rules/drafting-topic-lede.mdc](../../.cursor/rules/drafting-topic-lede.mdc)
