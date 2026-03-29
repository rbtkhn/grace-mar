# What Is a Companion Self?

**Companion-Self template · Concept**

---

## Long-term objectives (permanent system rules)

Companion-Self has **three** long-term objectives of equal importance: (1) **Democratize Alpha-style education** — comparable outcomes at a fraction of the cost, without a school or in-room guides, via Record as spine. (2) **Companion sovereignty** — all modification of skill and self containers is human-approval gated; agent may stage, may not merge. (3) **Knowledge boundary** — the Record contains only what the companion has provided and approved; no LLM inference in. These are permanent system rules to prevent intention drift and optimize alignment. Full statement and use: [LONG-TERM-OBJECTIVE](long-term-objective.md).

---

## 1. Core Idea

A **companion self** is a documented, queryable identity that grows from a snapshot of a person and accompanies them over time. It has two parts:

- **Record** — The documented self: who they are (knowledge, curiosity, personality) and what they can do (skills), with evidence linking every claim to artifacts or approved sources.
- **Voice** — The queryable interface that speaks the Record when the companion asks. It never speaks unbidden.

**Companion self = Mind + Record + Voice.** The human (Mind) is sovereign. The Record holds the documented self. The Voice renders it when queried.

**Purpose and burden.** Companion-self reduces the burden of carrying "who they are," "what they've done," and "what's next" in your head or across scattered tools. Its purpose is to give you one evidence-linked Record and a clear edge so identity and progress live in one place, not in your head. So caregivers and learners can rely on a single spine and reduce overload and ambiguity.

---

## 2. Cognitive Fork, Not Twin

| Term | Meaning |
|------|---------|
| **Cognitive fork** | Versioned branch from a snapshot. Diverges by design. Has its own history. |
| **Cognitive twin** | Parallel copy that stays in sync with the original. |

We use **cognitive fork** only. The fork and the real person grow independently; divergence is intentional.

---

## 3. Record vs. Voice

- **Record** — The documented self (e.g. self.md, self-knowledge.md, self-identity.md, self-curiosity.md, self-personality.md, self-skill-think.md, self-skill-write.md, self-skill-work.md, self-evidence.md). It is its own entity: it started from a snapshot but has its own trajectory. It does not "mimic" or "replicate" the person.
- **Voice** — Renders the Record in conversation. When the companion queries, the system generates responses constrained by the Record. That rendering is the Voice.

The Record records; the Voice speaks the Record. The Record does not command; the Voice does not speak unbidden. The Voice's **linguistic style and level** are primarily shaped by self-skill-write (WRITE): vocabulary, tone, and expression in the Record drive how the Voice sounds when queried.

---

## 4. Education structure

**Identity and instrument.** The Record (including self-knowledge, self-identity, self-curiosity, self-personality, and evidence) is the **identity** — the unique personal representation of the companion-self; the knowledge boundary protects it. The three skill containers (THINK, WRITE, WORK) are **instruments** — modules the companion-self uses to learn, express, and do, in order to satisfy the user's and companion's needs and intentions. Instruments can use any tools (including heavy AI); only human-gated results from their use update the identity.

Companion-Self education is **structured** around three skill containers:

| Structure | Schema tag | Meaning |
|-----------|------------|---------|
| **self-skill-think** | THINK | Intake and comprehension: what the companion has consumed and understood (reading, media, lessons). Evidence and edge drive what to read/watch next. *(THINK in Grace-Mar is equivalent: intake and comprehension.)* |
| **self-skill-write** | WRITE | Expression and voice: what the companion produces (journal, stories, explanations). Evidence of WRITE is evidence of understanding and voice. |
| **self-skill-work** | WORK | Making and doing: what the companion plans, builds, and ships (projects, creations). **Objectives and intentions** for the user/companion are encoded here; evidence links to self-skill-work and life skills. |

In schema, APIs, and export we use the tags **THINK**, **WRITE**, **WORK**; the canonical names for the **education structure** are **self-skill-think**, **self-skill-write**, **self-skill-work**. All screen-based learning and evidence capture are organized under these three.

**self-skill-think → self-knowledge, self-identity, self-curiosity, self-personality.** Activity in **self-skill-think** (THINK) is **filtered and distilled** into split growth files of the Record (SELF):

| Distillation target | Schema | Meaning |
|--------------------|--------|---------|
| **self-knowledge** | IX-A | What the companion has learned and knows (topics, facts, understanding). |
| **self-curiosity** | IX-B | What they are curious about, interests, questions. |
| **self-personality** | IX-C | Voice, preferences, values, narrative—how they see themselves and express. |

The pipeline stages THINK activity and suggests merges into IX-A, IX-B, or IX-C; the companion gates what actually enters. **Post-seed growth lives in the three dimension files:** **self-knowledge.md** (IX-A), **self-curiosity.md** (IX-B), **self-personality.md** (IX-C). self.md holds identity and baseline (I–VIII); it may optionally point to or summarize the three files, but the **source of truth** for IX-A/B/C is the three files. Merge and Voice read from them. So THINK feeds **who they are** (self.md baseline + these three) as well as **what they can do** (self-skill-think, evidence).

**Skill flow and the three dimensions:**

- **self-skill-think (THINK)** — Outputs **flow into** the three dimension files. Pipeline distills THINK activity and suggests merges into self-knowledge (IX-A), self-curiosity (IX-B), self-personality (IX-C); the companion gates.
- **self-skill-write (WRITE)** — Outputs are **shaped by** the three dimensions. What they know (self-knowledge), what they’re curious about (self-curiosity), and how they express (self-personality) inform tone, topics, and voice when they write. WRITE evidence lives in self-evidence and self-skill-write; pipeline may also suggest dimension merges from WRITE (e.g. a reflection that reveals curiosity or personality).
- **self-skill-work (WORK)** — **Shaped by** the dimensions (what to build next, how to approach it: interests, knowledge, personality) and **feeds into** them when merged. Projects and creations are evidence in self-evidence and self-skill-work; the pipeline can suggest dimension merges from WORK (e.g. knowledge gained by doing, curiosity revealed by project choice, personality in how they plan and ship). So WORK is bidirectional: dimensions shape proposed work; approved WORK activity can add to self-knowledge, self-curiosity, or self-personality.

**How WORK utilizes self-personality (IX-C).** Self-personality (voice, preferences, values, narrative) is the **identity layer** that WORK reads to personalize making and doing. Instances and integrations should use IX-C when implementing WORK flows:

1. **What to build and why** — Values and narrative in self-personality drive which work is proposed (e.g. "help others," "make things beautiful," "I fix things"). Curiosity (IX-B) gives topics; personality gives *why this kind of work* matters to the companion.
2. **How they work** — Preferences (solo vs. collaborative, fast iteration vs. careful finish, playfulness vs. seriousness) shape how work is structured: chunk size, pacing, amount of structure, and whether suggestions are "ship something small" or "one deep thing."
3. **Voice in work outputs** — When WORK produces text (descriptions, posts, docs), tone and style should follow self-personality so outputs sound like the companion.
4. **Resilience and difficulty** — Narrative and values ("I keep trying," "I care about quality") inform how hard or ambitious suggested work is and how setbacks or "next try" are framed.
5. **Ritual and "we did X"** — How the companion prefers to reflect (brief vs. reflective, private vs. shared) in self-personality can shape how WORK prompts for "we did X" and how progress is summarized back.
6. **Edge phrasing** — "What's next" for WORK should be phrased in the companion's voice and values so the suggestion feels like *their* next step, not a generic prompt.

This pattern is architectural: WORK is an instrument that uses the identity (including IX-C) to satisfy the user's and companion's intentions. See also the self-skill-work template (§ How WORK uses self-personality).

**APIs and integrations skill-work can connect to:**

- **Instance APIs (inbound):** POST activity with `skill_tag: WORK` to stage “we did X” (project, build, creation); merge writes to self-evidence, self-skill-work, and optionally the dimension files. GET /api/record and GET /api/edge expose WORK edge for “what to build next.” GET /api/export (curriculum_profile) includes WORK edge and evidence so external systems can suggest or adapt to projects.
- **Export consumers (outbound):** Curriculum, tutor, or project-suggestion services that **read** the Record (knowledge, curiosity, personality, WORK edge) and return suggested projects, workshops, or “next best action” for making/doing. Companion-Self does not mandate specific vendors; the export schema is the contract.
- **Evidence ingestion (inbound):** Optional webhook or callback for “activity completed” so an external tool (e.g. project app, workshop platform, maker portfolio) can **push** WORK completion into the instance pipeline as a candidate; the companion still gates merge. No direct write to the Record by third parties—stage only.
- **Life skills / project templates:** Instance or ecosystem can provide WORK templates, workshop-in-a-box prompts, or links to project libraries; these consume the Record (e.g. edge, interests) to propose work. Integration pattern: pull export → suggest project → user does it → capture via “we did X” or callback → pipeline stages → gate.

So skill-work is capable of connecting to: (1) the instance’s own staging, record, edge, and export APIs; (2) any consumer of the export that suggests or adapts projects; (3) any provider that can push WORK completion into the pipeline via a defined ingestion API or webhook; (4) project/workshop tools that use the Record to personalize what to build. **Ingestion from many sources** (calendar exports, task apps, webhooks) is a first-class pattern: see [Ingestion and sources](ingestion-and-sources.md).

**Progress and motivation.** Instance or consumers may derive progress (e.g. streaks, milestones, rewards) from evidence and expose them in UIs or exports; the Record stores the evidence. How progress and recognition are presented is up to the instance.

---

## 5. Knowledge Boundary

The Record is the **identity** representation; the boundary ensures it stays the companion's. The Record contains only what the companion has explicitly provided and approved.

- No LLM inference — facts from model training must not enter the Record.
- Evidence linkage — every claim traces to an artifact or approved source.
- When queried outside documented knowledge, the system may say "I don't know" and offer to look up. Lookup results do **not** auto-merge into the Record; the companion gates what, if anything, is added. An optional **self-library** (curated books, reference works, videos) is a bounded lookup extension: query-first for answers; it does not auto-merge into the Record.
- **Assessments (e.g. multiple-choice quiz):** The pipeline may stage (1) the quiz as an **evidence activity** (id, date, summary, e.g. "Quiz on topic X, 4/5") and (2) an **optional suggested merge to self-knowledge** (e.g. "Topic X: demonstrated via quiz Q (4/5, &lt;date&gt;)"). Both are candidates at the gate. The companion approves or rejects each. Only on approve is the activity written to self-evidence and, if a knowledge candidate was approved, one line written to self-knowledge with evidence link to the quiz activity. No inference-only update: the system suggests; the companion gates. **Triggers:** The template does not auto-create the second candidate; instances may add triggers (e.g. on activity type = quiz, stage evidence + knowledge candidate). See [Ingestion and sources](ingestion-and-sources.md) § Triggers for suggested merges.

This boundary is both an architectural invariant and a regulatory advantage (e.g. COPPA, GDPR).

---

## 6. Key Invariants

1. **Divergence by design** — Fork and real person may drift apart; that is correct.
2. **Merge, not add** — Content enters the Record by merging through a gate; the companion approves every merge.
3. **Agent may stage; it may not merge** — Only the companion (or an explicitly delegated human) may merge into the Record.
4. **Identity beyond productivity** — The Record records who someone is, not what they produce.
5. **Augmentation, not automation** — The system augments human judgment; it does not replace it. Human-in-the-loop is mandatory.
6. **Two-hour screen-time target** — All screen-based learning is designed to occur within **2 hours per day**, aligned with models (e.g. Alpha School) that squeeze full mandatory education into a 2-hour block. This is both a design constraint and an **equivalent metric** for comparison (2 hours = full academic coverage). See [Alpha School reference (skill-work-alpha-school)](skill-work/skill-work-alpha-school/alpha-school-reference.md) §3 Two-hour screen-time target.
7. **No human guide assumed** — Companion-Self must achieve its recursive self-learning objectives **without assuming the help of a human guide**. Guide-like support (motivation, “did you read the explanation?”, learning-how-to-learn) is designed into the **system** (Voice, pipeline prompts, session copy, edge suggestions) so the companion can succeed with zero or minimal adult involvement. An operator/parent may augment but is not required for the design to work; when they do, see [Human teacher objectives (skill-work-human-teacher)](skill-work/skill-work-human-teacher/human-teacher-objectives.md) for how they read and modulate skill-think. Lessons can be delivered via **Record-derived prompts** pasted into any LLM (e.g. ChatGPT, Grok); the lesson transcript then flows into skill-think for processing. See [Alpha School reference (skill-work-alpha-school)](skill-work/skill-work-alpha-school/alpha-school-reference.md) §4.1.

---

## 7. Trust and portability

Instances should support: (1) **Reversibility** — rollback or undo of Record changes where feasible. (2) **Export** — the companion can export Record and evidence and take their data elsewhere. (3) **Ownership** — the Record is the companion's; no lock-in; export and portability are expected.

---

## 8. Where Things Live (Template View)

| Component | In an instance |
|-----------|----------------|
| **Record** | `users/<id>/self.md`, `self-knowledge.md`, `self-curiosity.md`, `self-personality.md`, `self-skill-think.md`, `self-skill-write.md`, `self-skill-work.md`, self-evidence.md |
| **Voice** | Bot or other interface (lives in the instance repo; not in this template) |
| **Staging** | recursion-gate — candidates at the gate, before merge. To process the gate: [Identity Fork Protocol](identity-fork-protocol.md) § Process the gate. |
| **Continuity (non-Record)** | `self-memory.md` (**self-memory**; legacy `memory.md`): short/medium/long horizons; optional; rotatable; not gated Record (see [memory-template.md](memory-template.md)) |

This template defines concept, protocol, and seed phase. Bot code and Record data live in instance repos only.

---

## 9. Recursive self-learning

The Record can **improve itself over time**: each pipeline cycle refines the Record, and the updated Record shapes the next cycle (what gets detected, what the Voice says, what activities might be proposed at the edge). For objectives that guide this—inspired by learning science and AI-powered education models—see [RECURSIVE-SELF-LEARNING-OBJECTIVES](recursive-self-learning-objectives.md).

---

*Companion-Self template · No instance-specific content*
