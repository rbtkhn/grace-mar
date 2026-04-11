# Coming from OB1? Start here

Plain-language bridge for people who know **Open Brain (OB1)**-style systems: one place to look, recipes, imports, and a review queue. Grace-Mar keeps the same **governance** ideas (human approval, evidence) but names surfaces differently. Precise doctrine: [glossary.md](glossary.md), [conceptual-framework.md](conceptual-framework.md).

> Grace-Mar is not just a memory layer; it is a **governed companion record**. If you know OB1, the easiest way in is **Library, Skills, Evidence, Workflows, Dashboard, and Approval Inbox** — with durable writes still **gated**.

---

## Translation table

| If you think in… | In Grace-Mar |
|------------------|--------------|
| **Library** | **SELF-LIBRARY** — display label **Library** ([scripts/surface_aliases.py](../scripts/surface_aliases.py)) |
| **Skills** (executable packs) | Two layers: **SKILLS** (Record capability in `self-skills.md`) vs **portable skills** (`skills-portable/`). See [skills-explained.md](skills-explained.md). |
| **Evidence / activity log** | **EVIDENCE** — canonical body on `self-archive.md` |
| **Pending approvals / review queue** | **Approval Inbox** — user-facing name for pending candidates in [`users/grace-mar/recursion-gate.md`](../users/grace-mar/recursion-gate.md) (canonical file name: **recursion-gate**). **Boundary Review** (classification hints) is related but not the whole inbox; see [boundary-review-queue.md](boundary-review-queue.md). |
| **Workflows / recipes** | `docs/skill-work/**`, scripts, bridges — [workflow-catalog.md](workflow-catalog.md) |
| **Imports / capture** | [imports-and-capture.md](imports-and-capture.md) |
| **Dashboard** | [observability.md](observability.md), `runtime/observability/`, family hub / miniapp: [simple-user-interface.md](simple-user-interface.md) |

---

## What will feel familiar

- **Observable state** — pipeline, observability feeds, session tooling ([observability.md](observability.md), [session-observability.md](session-observability.md)).
- **Skills culture** — Cursor **skills**, portable operator assets, plus **SKILLS** as Record capability ([skills-explained.md](skills-explained.md)).
- **Integrations and bridges** — OpenClaw, exports, prepared context ([openclaw-integration.md](openclaw-integration.md), [prepared-context-layer](prepared-context-layer.md) in state model docs).
- **A queue before durable memory** — candidates land in the **Approval Inbox** (`recursion-gate.md`); nothing becomes lasting Record truth without companion approval ([AGENTS.md](../AGENTS.md) § Gated Pipeline).

---

## What is different

- **Four Record surfaces** — SELF, SELF-LIBRARY, SKILLS, EVIDENCE — not a single undifferentiated DB ([README.md](../README.md) Concept).
- **No silent merge into the Record** — staging is not adoption; merge runs only after approval (`process_approved_candidates.py`).
- **Identity vs library** — SELF-KNOWLEDGE (who she is) vs SELF-LIBRARY (reference corpora) — [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).
- **Template state model** — evidence vs prepared context vs governed state complements the four surfaces ([state-model.md](state-model.md)).

---

## Where to start first

1. Skim [README.md](../README.md) — Concept + Gated Pipeline.
2. Open [docs/start-here.md](start-here.md) — **Choose your path** (operator = **C** is the usual OB1-adjacent role).
3. Peek at pending work: [`users/grace-mar/recursion-gate.md`](../users/grace-mar/recursion-gate.md) (**Approval Inbox**).
4. Optional: run a short observability or session script ([observability.md](observability.md)) to see “dashboard-ish” output locally.

---

## How imports and memory work here

Bridges and hooks **ingest**; imports **do not** write directly to durable Record. Typical path: material → **EVIDENCE** / prepared context / transcripts → **candidates** in the Approval Inbox → merge after approval. Full narrative: [imports-and-capture.md](imports-and-capture.md).

---

## What the Approval Inbox does

1. **Signal detection** (bot, operator, tests) proposes structured candidates.  
2. Candidates sit in `recursion-gate.md` until **approved**, **rejected**, or **edited**.  
3. **Merge** runs only on approved rows — Sovereign Merge Rule.

Deeper review semantics (tiers, quick-merge eligibility): [recursion-gate-three-tier.md](recursion-gate-three-tier.md).

---

## See also

- [start-here.md](start-here.md) — audience doors (A–F)
- [gate-vs-change-review.md](gate-vs-change-review.md) — when to escalate beyond the gate
- [feedback-loops.md](feedback-loops.md) — low-friction approval, merge feedback
