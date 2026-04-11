# Human Teacher / Learning Objectives (Skill-Work-Human-Teacher)

**Companion-Self template · When a human augments the system**

The template assumes **no human guide**: recursive self-learning objectives are achievable without an in-room adult. When an **operator, parent, caregiver, or teacher** is present, they **augment** the system. This doc consolidates **human teaching and learning objectives** and how they **read and modulate skill-think** (the THINK container: self-skill-think.md).

---

## Audience and contexts

**Designed to teach the human companion.** Skill-work-human-teacher is primarily for **teaching the human in the loop** (operator, parent, caregiver): how to read skill-think and edge, how to run the gate, how to suggest focus and prompt process so the companion’s Record stays coherent and sovereign. The human companion learns to augment the system well.

**Can also be instructed for other contexts.** The same framework can be **instructed** for:

- **Classes and seminars** — A teacher or facilitator can be instructed to use these objectives and read/modulate patterns with a group (e.g. one Record per learner, or a shared edge view for the room).
- **Different ages** — Objectives and phrasing can be adapted by instance or operator for age band (e.g. younger vs older learners); the defaults are generic and extensible.
- **Different languages** — Content and prompts can be localized; the structure (read skill-think, gate, suggest focus) stays the same.

Instances may add instructor briefs, class/seminar variants, or age/language-specific guidance that reference this submodule.

---

## Scope

- **Not required.** The design works with zero or minimal adult involvement; Voice, pipeline, and Record-driven prompts carry the load.
- **When present,** the human supports the same outcomes (mastery at the edge, learning-how-to-learn, motivation, sovereignty) by reading the Record—especially **skill-think**—and shaping what gets proposed and merged.
- **Sovereignty unchanged.** Only the companion (or an explicitly delegated human per [long-term-objective](../../long-term-objective.md)) may merge into the Record. The human teacher does not bypass the gate.

---

## Human teaching / learning objectives

When a human is in the loop, their objectives align with [recursive self-learning objectives](../../recursive-self-learning-objectives.md), from the human’s role:

| Objective | Human’s role |
|-----------|--------------|
| **Activity at the edge** | Use edge (and skill-think) to suggest focus: “What’s next for THINK?” so the companion is challenged but not overwhelmed. |
| **Mastery-based** | Gate with judgment: approve only what reflects real understanding; reject noise or premature claims. |
| **Learning how to learn** | Prompt process: “Did you check your resources? Read the explanation?” so the companion builds meta-learning habits. |
| **Motivation and ownership** | Keep progress visible; use session brief and edge to celebrate “you’re X hours away” or “N items at the gate.” |
| **Character and identity** | Respect SELF and IX-C when suggesting or gating; don’t push content that conflicts with the Record. |

The human does **not** need to deliver curriculum; the system (and Record-derived prompts → LLM) does that. The human **reads** the Record and gate, **shapes** focus and process, and **gates** what enters the Record.

---

## Default human-teacher objectives (for all new users)

When a human teacher is present, the following **generic academic objectives** are suitable as defaults for all new users. Instances may adopt, replace, or extend them (e.g. after seed or by age/context).

| Objective | Description |
|-----------|-------------|
| **Keep learning at the edge** | Use edge and skill-think to suggest focus so the learner is challenged but not overwhelmed (zone of proximal development). |
| **Gate for mastery** | Approve only what reflects real understanding; reject noise or premature claims so the Record stays evidence-based. |
| **Support learning-how-to-learn** | Prompt process: “Did you read the explanation?” “Check your resources.” Build meta-learning habits. |
| **Keep progress visible** | Use session brief and edge to celebrate progress (“you’re X hours away,” “N items at the gate”) so effort maps to growth. |
| **Respect identity** | When suggesting or gating, respect SELF and IX-C; don’t push content that conflicts with the Record. |
| **Support the 2-hour design** | When relevant, help keep screen-based learning within the design (e.g. up to 2 hours per day); protect focus and time back. |

These align with [recursive self-learning objectives](../../recursive-self-learning-objectives.md) and with the human’s read/modulate role above. No curriculum delivery required; the human reads skill-think, shapes focus and gate, and keeps the Record coherent.

---

## Reading skill-think

The human **reads** skill-think (and related state) to know where the companion is and what to do next.

| What to read | Where | Use |
|--------------|--------|-----|
| **THINK capability and evidence** | self-skill-think.md | What has been learned (intake, comprehension); evidence-linked lines. |
| **Edge for THINK** | GET /api/edge (or export) with skill_tag THINK | “What’s next” for intake/comprehension; suggested focus. |
| **Pending THINK candidates** | recursion-gate (candidates with skill_tag THINK) | What’s waiting to be approved and merged into THINK (and possibly IX). |
| **Session brief** | Instance pattern: pending count, recent merges, edge summary | Quick sync before a session or before processing the gate. See [instance-patterns](../../instance-patterns.md) § Session brief. |

Reading skill-think answers: *What have they been learning? What’s at the gate? What should we look at first?*

---

## Shaping / modulating skill-think

The human **modulates** skill-think without writing into the Record directly (unless explicitly delegated to merge):

| How | Effect |
|-----|--------|
| **Run the gate** | Approve or reject candidates. Approved THINK candidates merge into self-skill-think (and possibly IX); rejections stay out. So the human **shapes** what enters THINK by what they approve. |
| **Suggest focus** | Use edge and session brief to say “let’s work on X” or “review these three first.” Shapes what the companion (or system) does next; next activity may become new THINK evidence. |
| **Prompt process** | “Did you read the explanation?” “Check your resources.” Encourages learning-how-to-learn; the resulting behavior may be captured and staged as THINK. |
| **Feed context** | Operator may run seed phase, add “we did X” (with skill_tag THINK), or paste a lesson transcript for staging. Pipeline stages; human gates; merge updates THINK. |

So: **read** skill-think and edge → **shape** focus and gate decisions → THINK (and Record) stay coherent and under companion control.

---

## Integration points

- **Companion app / operator UI:** Show edge and pending gate; optional session brief (pending count, recent activity, suggested next). Human uses these to read and then modulate.
- **Gate workflow:** Process the gate ([identity-fork-protocol](../../identity-fork-protocol.md)); human (or delegated) approves/rejects. THINK candidates merge into self-skill-think and optionally IX.
- **Dual paths (THINK updates):** Operator **direct edit** to `skill-think.md` after reading (no gate) vs **staged THINK candidate** through the gate — both valid; see [think-purpose-and-boundary.md](../../../skill-think/think-purpose-and-boundary.md) and [we-read-think-self-pipeline.md](../../we-read-think-self-pipeline.md).
- **Seed phase:** Operator may assist with surveys and first Record population; after that, ongoing teaching objectives are read/modulate/gate as above.
- **Ingestion:** Caregiver or operator can POST activity (e.g. “we did X” with THINK); pipeline stages; human gates; merge updates skill-think.

---

## Cross-references

- [Recursive self-learning objectives](../../recursive-self-learning-objectives.md) — System objectives; “operator may augment” points here for human role.
- [Concept](../../concept.md) §6–7 — No human guide assumed; operator/parent may augment; invariants.
- [Instance patterns](../../instance-patterns.md) — Session brief (operator tool), analyst and gate.
- [Long-term objective](../../long-term-objective.md) — Delegated human may perform merge; sovereignty.
- [Schema and API](../../schema-record-api.md) — Record schema; self-skill-think.md; edge and gate contract.
