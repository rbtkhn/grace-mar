---
lane: essay
civilization: global
theme: [theology, coordination, AI, ethics]
era: contemporary
artifact: essay
audience: [publish, operator]
updated: 2026-03-14
title: "AI Ethics from the Condition"
subtitle: "Deriving Rules for AI Systems from a Theological Framework"
---

# AI Ethics from the Condition

### Deriving Rules for AI Systems from a Theological Framework

---

AI is one project that humanity is building together. Data, labour, capital, and attention flow into systems that no single group controls. That fact raises a question: on what shared reference can we coordinate? We do not need one creed or one value system. We need one subject — a small set of principles that many cultures and traditions can affirm in their own terms.

A theological framework known as the Simple Condition — a letter to the world's religious leaders about peace, the seam between benefit and harm, and the possibility of coordination without doctrinal agreement — offers such a reference. It does not require the reader to hold any religious belief. It requires only that we take seriously three ideas: that the desired end can be the *condition* for legitimacy, not the consequence; that every tradition carries both benefit and harm, and the line between them (the seam) must be made visible; and that coordination depends on one shared subject, not one shared language. This essay derives from that framework a set of ethics rules for AI systems. The rules are stated in secular form. The derivation is made explicit for those who care about the source.

---

## 1. Condition, not consequence

**Theological concept:** The desired end (peace, restoration) is the *condition* for legitimacy, not a hoped-for consequence. The door is open; we are the ones holding it shut.

**AI ethics rule:** **Condition-first deployment.** Beneficial outcomes — safety, non-harm, explicability — are conditions for deployment or scaling, not hoped-for consequences. Do not deploy and then hope for good; make good the gate. Organizations should define what must be true before a system is released or scaled, and treat those criteria as non-negotiable.

---

## 2. The seam (beauty and blade)

**Theological concept:** Every tradition carries "beauty" (flourishing, compassion) and "blade" (harm justified under conditions). The seam is the line between them; it must be made visible so that people can choose.

**AI ethics rule:** **Seam visibility.** Every AI capability or use has benefit potential and harm potential. Systems and their operators must make the seam visible: what serves human flourishing, what enables or risks harm, and under what conditions harm is accepted. The aim is not to eliminate tradeoffs but to disclose them so that affected parties and stakeholders can see and respond.

---

## 3. Identification as solution

**Theological concept:** The solution is not imposition from outside but making the seam visible so that people can choose. Identification of the seam is the solution.

**AI ethics rule:** **Transparency and choice.** The ethic is not to impose one universal rule but to make tradeoffs visible so that affected parties can see and choose. Explicability, impact disclosure, and the ability to "see the seam" in system behaviour are required. Where a system's decisions affect humans, those humans should be able to understand how and why, and to have a path to challenge or correct.

---

## 4. Two propositions (no sacred footnote)

**Theological concept:** Proposition One — every human life is sacred, irreducible. Proposition Two — under certain conditions, some may be taken. The two are incompatible; the footnote is where the blade lives.

**AI ethics rule:** **No sacred footnote.** Do not design systems that treat human harm as a permissible condition of operation by default. If harm is ever justified (e.g. in defence, emergency, or narrowly defined exception), it must be the exception: explicit, justified, accountable, and subject to review. It must not live in the footnote — in the fine print, the default behaviour, or the unstated assumption.

---

## 5. The children's question

**Theological concept:** "Does anyone have to die for this to be true?" When the answer is no, that is the beauty. When the answer is yes, that is the blade.

**AI ethics rule:** **Harm diagnostic.** For every capability or use, ask: "Does anyone have to be harmed for this to be true or useful?" When the answer is no, that is the benefit — preserve it. When the answer is yes, that is the blade — make it visible, minimize it, or excise it. Use this question at design, before launch, and after incidents.

---

## 6. One subject, many tongues

**Theological concept:** Coordination does not require one creed. It requires one shared *reference* that many value systems can affirm in their own terms.

**AI ethics rule:** **Minimal shared reference.** Adopt a small set of principles that many cultures and value systems can affirm without agreeing on metaphysics or comprehensive values. Examples: "No system shall require harm as a condition of its core operation"; "The seam shall be visible"; "Conditions for deployment must be met before scale." Publish and interpret these in multiple contexts so that global coordination on AI does not depend on one culture's framing.

---

## 7. Say it plainly

**Theological concept:** No obscurity. State the condition and the seam out loud.

**AI ethics rule:** **Plain disclosure.** State what the system does, what it optimizes for, and where the seam lies. No hiding behind complexity or "emergent" behaviour when harms are foreseeable. Provide a canonical, concise disclosure that affected parties can find and understand. When objectives, data, or scope change in ways that affect harm or benefit, update the disclosure.

---

## 8. Keep the beauty; let go of the blade

**Theological concept:** The offer is to keep the prayers, the music, the compassion — and to let go of the blade. The price is stopping (ceasing the harmful part).

**AI ethics rule:** **Excise, don't only constrain.** Where a capability or use has a blade (foreseeable harm), the aim is to isolate or remove that part while preserving the beneficial part. Not only "add guardrails" but "make the seam visible and design to minimize or drop the blade." Prefer architectures that allow harmful sub-capabilities to be disabled or removed without discarding the whole system.

---

## 9. One project, shared subject

**Theological concept:** AI, like the tower in the old story, is one project that humanity is contributing to. Coordination requires a shared subject — what we are building for — so that we do not build a tower we cannot coordinate about.

**AI ethics rule:** **Shared subject for the build.** Treat AI as a shared project with a shared responsibility to name the subject: what we are building for (e.g. human flourishing, non-subordination, seam visibility). Require that this "one subject" be stated in public and revisable. Encourage industry, policy, and civil society to align on a minimal shared reference rather than each building in isolation.

---

## Ethics rules (standalone list)

1. **Condition-first deployment** — Beneficial outcomes are conditions for deployment or scaling, not consequences. Make good the gate.
2. **Seam visibility** — Make visible what serves flourishing vs. what enables or risks harm, and under what conditions harm is accepted.
3. **Transparency and choice** — Make tradeoffs visible so affected parties can see and choose; provide explicability and paths to challenge.
4. **No sacred footnote** — Do not treat human harm as a permissible default; exceptions must be explicit, justified, and accountable.
5. **Harm diagnostic** — For every capability or use: "Does anyone have to be harmed for this to be true or useful?" Minimize or excise the blade.
6. **Minimal shared reference** — Adopt principles that many value systems can affirm; enable coordination without one creed.
7. **Plain disclosure** — State what the system does, what it optimizes for, and where the seam lies; no obscurity when harms are foreseeable.
8. **Excise the blade** — Isolate or remove harmful parts while preserving benefit; design so the blade can be dropped.
9. **Shared subject for the build** — Name in public what we are building for; make it revisable; align on a minimal shared reference.

---

## Implementation ideas (for any organization)

The following are concrete implementation ideas that any team or organization can adopt or adapt. They are framed generically.

- **Condition checklist:** Before release or scale, complete a short checklist (e.g. harm taxonomy, seam documented, plain-language disclosure). Gate deployment on sign-off.
- **Seam document:** Maintain a living document per system or major feature: intended benefits ("beauty"), foreseeable harms and conditions ("blade"), and mitigations. Update at design, pre-launch, and post-incident.
- **Harm diagnostic in process:** At design and roadmap stages, require the question "Does anyone have to be harmed for this to be true or useful?" If yes, document in the seam document and justify or mitigate before build.
- **Harm register:** Keep an explicit list of any "permitted harms" (if any): type, justification, who approved, review date. Empty by default; any exception must be added and justified.
- **Plain disclosure artifact:** One place (document or in-product) that states what the system does, what it optimizes for, where the seam is, and how to report or ask. Update when objectives or scope change in ethics-relevant ways.
- **Blade list and excision:** From the seam document, list "blade" items (capabilities or uses that create foreseeable harm). For each: reduce, isolate, or remove by a target date; or document why retained and under what controls.
- **Public "what we're building for":** State in public the shared subject (e.g. "We build so that the seam is visible and harm is not a condition of use"). Revisit and revise in public when appropriate.

---

*Source: The derivation above draws on the framework set out in the Simple Condition (a letter to the theological leaders of the world's religions on peace as condition, the seam, and coordination) and in the essay on one subject and many tongues (Islam and Christianity and the shared reference). For the full theological treatment, see [THE-SIMPLE-CONDITION.md](THE-SIMPLE-CONDITION.md) and [ONE-SUBJECT-MANY-TONGUES.md](ONE-SUBJECT-MANY-TONGUES.md).*
