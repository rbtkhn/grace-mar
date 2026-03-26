# Alpha School Mastery — adaptation to companion-self / Grace-Mar

**Purpose:** Explain **Alpha School’s mastery philosophy** and how it maps onto this repo’s **self-skill-think**, **self-skill-write**, **WORK** (including work-jiang), **RECURSION-GATE**, and **EVIDENCE** — without claiming Alpha’s outcomes or copying their product.

**Governed by:** benchmarks stay **optional and external** ([alpha-school-reference.md](skill-work/work-alpha-school/alpha-school-reference.md), [alpha-school-benchmarks.yaml](skill-work/work-alpha-school/alpha-school-benchmarks.yaml)). This doc is **design vocabulary**, not verified performance data.

---

## What Alpha School Mastery is

Alpha School (private micro-school network, e.g. Austin and other campuses) uses a **mastery-based, personalized, AI-supported** progression model: roughly **two hours a day** of focused core academics, with the rest of the day for projects, workshops, life skills, and passions (“Time Back”).

**Core contrast with traditional school**

- Traditional systems often advance by **seat time** or **average** performance, which lets **partial understanding** persist (“Swiss cheese” gaps that compound).
- Alpha’s stance: students **advance only after demonstrated mastery** of the concept or skill; **gaps are not left open**; progression is **concept-based and individual**, not only age- or calendar-driven.

This aligns with classic **mastery learning** research (e.g. Bloom on mastery plus strong tutoring lifting most students well above traditional averages). Alpha adds **adaptive tooling** for diagnosis, practice, and pacing.

---

## Documented mechanics (reference summary)

| Mechanic | Role |
|----------|------|
| **~90%+ mastery threshold** | Hard gate to **unlock next material** / earn credit on a lesson or unit — must hit high correctness on assessments before progression. |
| **~80–85% in-lesson success** | During active practice, target success band so work sits in the **zone of proximal development** — hard enough to grow, not so hard as to break flow. |
| **Continuous adaptive assessment** | Ongoing diagnosis of what is known vs not; targeted lessons, repetition, **spaced retrieval**. |
| **Grade-level mastery tests** | Broad checkpoints before full grade advancement. |
| **Spaced repetition** | Retention over time. |
| **Pomodoro-style blocks** | Focus segments inside the **2-hour** academic window. |
| **“Time Back”** | Efficiency in service of **freed time** for deep projects, entrepreneurship, coding, speaking, etc. Motivation and **visible progress** are treated as central. |

External reporting sometimes cites strong **standardized growth** (e.g. NWEA MAP) vs national averages despite less seat time; treat such claims as **external** until you have your own evidence in the Record.

---

## Map to companion-self / Grace-Mar

This codebase is **not** a school stack. The analogy is **adult, self-directed, sovereign** practice:

| Alpha idea | Grace-Mar / companion-self analogue |
|------------|-------------------------------------|
| Mastery before advancing | **RECURSION-GATE** + approval before SELF/EVIDENCE merge; no silent promotion into the Record. |
| 90% gate on “next step” | **Jiang Compression Engine** ([COMPRESSION-ENGINE.md](skill-work/work-jiang/COMPRESSION-ENGINE.md)): operator checklist + one-sentence outcome + linked evidence + next actions before treating work as “closed enough to build on.” |
| 80–85% “in the zone” during practice | Session design in **skill-think** / tutoring flows: short blocks, difficulty just above current edge (see [alpha-school-reference.md](skill-work/work-alpha-school/alpha-school-reference.md), [educational-software-history-insights.md](educational-software-history-insights.md)). |
| Adaptive loop | **Analyst → gate → merge** and **Voice** grounded in profile — feedback is tied to **documented** state, not generic model knowledge. |
| Evidence of what you did | **self-archive.md** (EVIDENCE), **ACT-** / **READ-** spine, artifacts — confidence from **artifacts**, parallel to Alpha’s tests but **governed by the companion** ([conceptual-framework.md](conceptual-framework.md) — evidence-grounding). |
| Two-hour ceiling (screen academics) | **Optional benchmark** in YAML; design constraint for **Record-driven lessons** and operator pacing — not a mandate for every instance. |
| “Time Back” | **Intention** files ([seed-phase-wizard.md](seed-phase-wizard.md), [good-morning-brief.py](../scripts/good-morning-brief.py)), **memory.md** horizons, and explicit **WORK** lanes so durable identity work is not drowned by busywork. |

**Three recursive pillars (informal mapping)**

- **self-skill-think** — Models, pattern recognition, “did I actually understand?” (mastery of *mental* content).
- **self-skill-write** — Articulation and compression; evidence-friendly output.
- **WORK** (e.g. **work-jiang**) — Execution artifacts; **compression** and **next actions** mirror “clear enough to ship the next increment.”

**Seed wizard** `minimal-core.json` field `preferredProgressUnits` (`behavioral-change`, `identity-coherence`, `evidence-quality`) names **units of progress** comparable to Alpha’s mix of mastery scores, behavior, and identity — still **operator seed data** until promoted through the gate.

---

## Tensions (explicit)

- **Structure vs friction** — How much gating **accelerates** vs slows solo, fast work?
- **Unit of progress** — Raw evidence volume vs **behavioral change** (e.g. work-jiang execution) vs **identity coherence** — they can diverge; the Record preserves tensions, not a single score.
- **Gate discipline under speed** — Compression checklist + RECURSION-GATE exist to prevent **Swiss cheese** in the fork; skipping them trades speed for drift risk.

---

## Related docs and tools

- [bloom-mastery-adaptation.md](bloom-mastery-adaptation.md) — **Bloom / 2 Sigma layer:** mastery learning and tutoring analogy mapped to gates, evidence, and compression (Alpha-operational detail stays in *this* doc).
- [work-alpha-school/README.md](skill-work/work-alpha-school/README.md) — benchmarks submodule index.
- [alpha-school-reference.md](skill-work/work-alpha-school/alpha-school-reference.md) — 2-hour block, YAML usage, Record-driven prompts.
- [educational-software-history-insights.md](educational-software-history-insights.md) — Bloom, Alpha, IXL, Khan, session length.
- [users/grace-mar/work-jiang.md](../users/grace-mar/work-jiang.md) — Jiang lane; compressions under `research/external/work-jiang/compressions/`.
- [scripts/jiang-compress.py](../scripts/jiang-compress.py) — compression workflow.
- [identity-fork-protocol.md](identity-fork-protocol.md) — sovereign merge path.
