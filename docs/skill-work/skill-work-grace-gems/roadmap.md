# Skill-work-grace-gems — Roadmap

**Status:** Phase 0 (Record context). Phases 1–3 are aspirational; implementation aligns with AGENTS rules (gated pipeline, knowledge boundary, companion sovereignty).

**Business:** [Grace Gems on Etsy](https://www.etsy.com/market/grace_gems) — custom fine jewelry with natural gemstones; solid 14k/18k gold; handmade in Denver. Star Seller; natural/untreated gemstones; emeralds, rubies, sapphires, tanzanite, moonstone, topaz, tourmaline, amethyst, opal, bridal sets.

---

## Phase 0 — Record context (current)

**Scope:** Document Grace Gems in the Record so the Voice can respond when the companion queries about the business. No automation; context only.

| Deliverable | Description |
|-------------|-------------|
| **Business profile** | Optional section in SELF or skill-work: product range, materials, policies (shipping, returns, warranty, layaway). Gated; companion approves what enters. |
| **WORK evidence** | Business milestones ("we completed X order," "we added Y product") staged as CREATE- or ACT- evidence; merged through pipeline. |

---

## Phase 1 — Operator flows (future)

**Scope:** Operator-facing docs and checklists for managing the business (inventory, listings, customer service). Human-led; no automated actions.

| Deliverable | Description |
|-------------|-------------|
| **Operator checklist** | Pre/post routines for orders, listings, customer messages. Reference Etsy dashboard, Grace Gems policies. |
| **Handback for business** | "We did X" for business events (order fulfilled, new listing, customer feedback) → stage → merge into Record. |

---

## Phase 2 — Curriculum / lesson integration (future)

**Scope:** Optional integration with lesson prompts when the companion documents interest in the business (IX-B curiosity, WORK edge).

| Deliverable | Description |
|-------------|-------------|
| **WORK edge** | If companion documents Grace Gems as WORK focus, lesson generator can include business-related planning/creation activities (e.g., "plan 3 steps for a new listing"). |
| **IX-B alignment** | Business curiosity (gemstones, craftsmanship, design) can feed lesson topics when documented. |

---

## Phase 3 — External integration (future)

**Scope:** Optional APIs or scripts for Etsy (listings, orders, inventory). Companion-controlled; gated.

| Deliverable | Description |
|-------------|-------------|
| **Etsy API** | Read-only or controlled write access for listing sync, order status. Requires companion approval and auth. |
| **Handback from Etsy** | Order/listing events → stage as business evidence → companion approves merge. |

---

## Summary

| Phase | Scope | Key deliverables |
|-------|-------|------------------|
| **0 — Record context** | Document business in Record | Business profile in SELF/skill-work; WORK evidence for milestones |
| **1 — Operator flows** | Human-led management | Operator checklist, handback for business events |
| **2 — Curriculum** | Lesson integration | WORK edge, IX-B alignment when documented |
| **3 — External** | Etsy integration | API, handback from Etsy events |

---

## Design guardrails

1. **Knowledge boundary** — Business facts in Record only if companion documents them. No LLM inference.
2. **Gated pipeline** — Business evidence stages; companion approves merge.
3. **Companion sovereignty** — Business decisions remain with the companion. System supports; does not direct.

---

## Related

- **[market-research-and-automation-ideas.md](market-research-and-automation-ideas.md)** — Market research (Etsy jewelry trends, natural vs lab-grown, seller pain points) and prioritized automation ideas (Etsy handback, message draft assist, order summary, listing sync).
