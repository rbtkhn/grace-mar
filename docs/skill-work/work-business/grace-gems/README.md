# Grace Gems (work-business)

**Objective:** Manage the Grace Gems Etsy business — [etsy.com/market/grace_gems](https://www.etsy.com/market/grace_gems) — custom fine jewelry with natural gemstones.

This submodule supports WORK and the Record by documenting how Grace-Mar relates to the companion's business: inventory, listings, customer service, orders, and operations. The companion is sovereign; the system supports, does not compel.

---

## Purpose

| Role | Description |
|------|-------------|
| **Business context** | Document what Grace Gems does (product range, materials, policies) so the Record can inform Voice responses when the companion queries about the business. |
| **WORK integration** | Making, planning, execution, exchange — gemstones, jewelry creation, orders, customer interaction. Evidence (CREATE-, ACT-) can capture business milestones. |

Grace Gems (GraceGemsUS) sells customized fine jewelry with natural, untreated gemstones; solid 14k/18k gold; handmade in Denver. Products include emeralds, rubies, sapphires, tanzanite, moonstone, topaz, tourmaline, amethyst, opal, bridal sets. Policies: free worldwide shipping, 30-day returns (excl. custom), 1-year repair warranty, layaway. Companion-led; the Record holds business-relevant context when documented.

**Sovereignty framing:** Grace Gems aligns with companion-owned, local economy principles: natural provenance (untreated gemstones), handmade in Denver, policy-transparent, cash-friendly. The business models authenticity and local production as alternatives to homogenized, programmable commerce.

---

## Business entity (Colorado)

| Field | Value |
|-------|--------|
| **Legal name** | Grace Gems LLC |
| **State** | Colorado |
| **SOS ID** | 20218086367 |
| **Periodic report** | Filed 2025-03-06 (document # 20251272537) |

*Source: Colorado Secretary of State periodic report receipt. For renewal/filing reference only.*

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, and principles for . |
| **[roadmap.md](roadmap.md)** | Phased roadmap for business management (Record context → operator flows → optional integration). |
| **[workflow-reminders.md](workflow-reminders.md)** | Recurring tasks (e.g. annual Colorado SOS periodic report). Operator sets own calendar/reminders. |
| **[market-research-and-automation-ideas.md](market-research-and-automation-ideas.md)** | Deep market research (Etsy jewelry, natural vs lab-grown, pain points) and automation integration ideas aligned with Grace-Mar (handback, draft-only message assist, staged candidates). |
| **[jewelry-industry-research-pre1970.md](jewelry-industry-research-pre1970.md)** | History and science of gems, jewelry crafting, mining, selling — **sources from 1969 or earlier only**. |
| **[agent-encoding.md](agent-encoding.md)** | Phase 1 agent reference: provenance–stone table, terminology glossary, meta-rules, handback semantics, tone guidelines, example drafts (message assist, listing validation). |
| **[message-assist-calibration.md](message-assist-calibration.md)** | Calibration loop: operator feedback when drafts miss the mark; message-assist loads it if present. |
| **[../accounting/1099k-2025-grace-gems-etsy.md](../accounting/1099k-2025-grace-gems-etsy.md)** | 2025 Form 1099-K totals and monthly Box 5 (no TINs) — reconcile to Etsy + bank ledger. |
| *scripts/grace_gems_message_assist.py* | Message assist — draft-only reply for Etsy customer messages. `python3 scripts/grace_gems_message_assist.py -m "message"` |

---

## Principles

1. **Companion sovereignty** — Business decisions (pricing, inventory, policies) are the companion's. The Record documents; it does not direct.
2. **Knowledge boundary** — Voice responses about the business use only what is documented in the Record (SELF, SKILLS, EVIDENCE). No LLM inference into business facts.
3. **Evidence-grounded** — Business milestones (new products, sales, feedback) enter the Record through the gated pipeline ("we did X" → stage → approve → merge).
4. **Integrate with WORK** — Grace Gems activities (making, planning, exchange) map to WORK container; CREATE- and ACT- evidence can capture business outcomes.

---

## Cross-references

- [Architecture](../../../architecture.md) — WORK container, Record structure
- [AGENTS.md](../../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [SKILLS-MODULARITY](../../../skills-modularity.md) — WORK (BUILD) scope
