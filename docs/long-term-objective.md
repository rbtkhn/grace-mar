# Long-Term Objectives (Permanent System Rules)

**Companion-Self template · North star**

These objectives are **permanent system rules**. They exist to **prevent intention drift** and **optimize alignment** across concept, protocol, roadmap, and implementation. All design choices, features, and documentation should be evaluated against them. There are **three** long-term objectives of equal importance.

---

## 1. Democratize Alpha-style education

**Democratize Alpha-style education:** deliver the same *kind* of outcomes (mastery-based progress, ~2-hour academic coverage, life skills, motivation, portable identity) at a **fraction of the cost** and **without requiring a physical school or in-room guides**.

- **Equivalence, not replication** — We aim for comparable outcomes (mastery, evidence, “time back,” identity), not Alpha’s delivery (no Timeback clone, no $40K tuition, no guide-in-the-room assumption).
- **Record as the spine** — The Record is the portable identity layer: what they know, what they care about, what they can do. Evidence-gated and exportable so any curriculum or tutor can plug in. That is what scales without the school building.
- **Reduce overload and anxiety** — A single spine and a clear "what's next" (edge) give learners and caregivers one place for identity and progress instead of scattered tools, reducing overload and anxiety.
- **Sovereignty and evidence** — Learning and identity stay under the learner’s (or explicitly delegated human’s) control. Human-approval gate for all modifications to skill and self containers; no silent writes. See [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md), [CONCEPT](concept.md) §6.

**Equity:** Equity is framed as **adequacy** (every learner reaches a sufficient level to participate meaningfully) **plus growth**; the Record supports both. “Top 1%” in the Alpha reference is a **comparison target** for what’s possible, not a requirement for every learner.

**One line:** Make Alpha-style learning and identity available to many more people via Record + pipeline + low-cost tools, without the school or the budget.

---

## 2. Companion sovereignty (human-approval gate)

**All modification of skill and self containers is gated by the companion or an explicitly delegated human.** The agent may stage; it may not merge. No silent writes to the Record; no platform or system merge without human approval.

- This is the **enabler of trust and portability**. Without it, "Record as the spine" and comparable outcomes could drift into platform-controlled profiles or agent-written identity.
- **Single exception:** An explicitly delegated human (e.g. parent/operator on behalf of the companion) may perform the merge; that is still human-approval gated. When a human is in the loop, see [Human teacher objectives (skill-work-human-teacher)](skill-work/skill-work-human-teacher/human-teacher-objectives.md) for teaching/learning objectives and how they read and modulate skill-think.
- See [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md) (Sovereign Merge Rule), [CONCEPT](concept.md) §6 invariants 2–3.

**One line:** The companion (or delegated human) is sovereign over the Record; only they may merge.

---

## 3. Knowledge boundary

**The Record contains only what the companion has explicitly provided and approved.** No LLM inference into the Record; no facts from model training; every claim traces to an artifact or approved source.

- This defines **what the Record is**: the documented self, not a model’s summary or training data. It supports both trust (identity is theirs) and compliance (e.g. COPPA, GDPR).
- The system may say "I don’t know" and offer to look up when queried outside documented knowledge; it does not fill the Record from inference.
- See [CONCEPT](concept.md) §5 Knowledge Boundary, §6 invariant (evidence linkage).

**One line:** The Record is only what the companion has provided and approved; no inference in.

---

## Use

- **Design** — When adding or changing concept, protocol, or schema: does it advance these objectives or at least not dilute them? Human gate and knowledge boundary are non-negotiable.
- **Roadmap** — Initiatives and success criteria should trace to Record-as-spine and comparable outcomes (mastery, evidence, identity); no feature that bypasses the gate or fills the Record from inference.
- **Implementation** — Features and UX should support the 2-hour target, human gate, evidence linkage, and export for curriculum/tutor.
- **Documentation** — New docs and edits should not contradict or obscure these objectives.

If a proposal would drift the system away from any of these objectives, flag it or reject it.

---

## Reference

- [CONCEPT](concept.md) — Core idea, education structure, invariants.
- [SKILL-WORK-ALPHA-SCHOOL: Alpha School reference](skill-work/skill-work-alpha-school/alpha-school-reference.md) — Benchmarks, 2-hour screen-time target, and equivalent metrics (consolidated in the skill-work submodule: skill-work-alpha-school).
