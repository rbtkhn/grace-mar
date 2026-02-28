# Skill-work-grace-gems

**Objective:** Manage the Grace Gems Etsy business — [etsy.com/market/grace_gems](https://www.etsy.com/market/grace_gems) — custom fine jewelry with natural gemstones.

This submodule supports WORK and the Record by documenting how Grace-Mar relates to the companion's business: inventory, listings, customer service, orders, and operations. The companion is sovereign; the system supports, does not compel.

---

## Purpose

| Role | Description |
|------|-------------|
| **Business context** | Document what Grace Gems does (product range, materials, policies) so the Record can inform Voice responses when the companion queries about the business. |
| **WORK integration** | Making, planning, execution, exchange — gemstones, jewelry creation, orders, customer interaction. Evidence (CREATE-, ACT-) can capture business milestones. |

Grace Gems (GraceGemsUS) sells customized fine jewelry with natural, untreated gemstones; solid 14k/18k gold; handmade in Denver. Products include emeralds, rubies, sapphires, tanzanite, moonstone, topaz, tourmaline, amethyst, opal, bridal sets. Policies: free worldwide shipping, 30-day returns (excl. custom), 1-year repair warranty, layaway. Companion-led; the Record holds business-relevant context when documented.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and principles for skill-work-grace-gems. |
| **[roadmap.md](roadmap.md)** | Phased roadmap for business management (Record context → operator flows → optional integration). |
| **[market-research-and-automation-ideas.md](market-research-and-automation-ideas.md)** | Deep market research (Etsy jewelry, natural vs lab-grown, pain points) and automation integration ideas aligned with Grace-Mar (handback, draft-only message assist, staged candidates). |

---

## Principles

1. **Companion sovereignty** — Business decisions (pricing, inventory, policies) are the companion's. The Record documents; it does not direct.
2. **Knowledge boundary** — Voice responses about the business use only what is documented in the Record (SELF, SKILLS, EVIDENCE). No LLM inference into business facts.
3. **Evidence-grounded** — Business milestones (new products, sales, feedback) enter the Record through the gated pipeline ("we did X" → stage → approve → merge).
4. **Integrate with WORK** — Grace Gems activities (making, planning, exchange) map to WORK container; CREATE- and ACT- evidence can capture business outcomes.

---

## Cross-references

- [Architecture](../../architecture.md) — WORK container, Record structure
- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [SKILLS-MODULARITY](../../skills-modularity.md) — WORK (BUILD) scope
