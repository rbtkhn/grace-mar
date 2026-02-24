# Business Roadmap — Strategy, Monetization, Go-to-Market

**Purpose:** Capture business priorities, monetization paths, and strategic roadmap items. Complements the product/feature [Design Roadmap](DESIGN-ROADMAP.md).

**Status:** Living document. Items are strategic-stage unless noted otherwise.

---

## 1. Positioning

**Category:** Identity infrastructure for the agent web — not second-brain tool, AI clone, or child-specific tutor.

**Execution sequence (next 18 months):**
- Primary wedge: hosted family product (homeschool/microschool)
- Secondary: 1-2 scoped integration pilots
- Deferred: certification/compliance program as standalone revenue

**Dual positioning:**
- **Supplemental** — Works alongside Alpha (and similar AI schools). Alpha teaches; Grace-Mar records. Record feeds Incept for personalization.
- **Low-cost alternative** — Open-source. Families outside $40K–$75K tuition run Grace-Mar + Khan/IXL + lightweight structure.

See [Design Notes](DESIGN-NOTES.md) for full white-paper narrative and differentiation table.

---

## 2. Monetization Angles

| Path | Value | Use Case | Monetization |
|------|-------|----------|--------------|
| **Supplemental** | Add Record layer to Alpha | Alpha parent wants portable, evidence-grounded Record | Integration license; subscription for Record hosting + Alpha-compatible export |
| **Low-cost alternative** | Same architecture at $0 software | Family wants fork, cannot afford $40K+/year | Open core free; optional hosted service, support, premium export |
| **B2B (AI schools)** | Identity substrate for platforms | School integrates Record as identity layer | Platform license, API fees, white-label |
| **Infrastructure** | Open schema, protocol, trust primitives | Others build Grace-Mar-compatible systems | Reference implementation, certification, ecosystem revenue share |
| **Hybrid** | Open core + hosted + enterprise | Mixed adoption | Open core; hosted for non-technical; enterprise licensing for integrators |

---

## 3. Priority Roadmap Items

| Priority | Item |
|----------|------|
| 1 | Export format optimized for motivation/engagement (interests, curiosity, personality) — input for tutors, platforms, parents |
| 2 | Homeschool-focused documentation: "Using Grace-Mar without a school" |
| 3 | Elevate "we did X" as first-class ritual in UX/docs — recognition, celebration, accountability loop |
| 4 | Session continuity + PENDING-REVIEW as lightweight accountability for homeschool |
| 5 | Alpha/Incept integration path — Record as identity feed |

**Design target:** Homeschool is the primary gap (Alpha homeschool = 1x). Grace-Mar + Khan/IXL + lightweight structure = low-cost alternative. Record feeds motivation; "we did X" provides ritual.

---

## 4. Key Metrics (Proposal-Ready)

| Metric | Target | How to Verify |
|--------|--------|---------------|
| Record completeness | IX-A, IX-B, IX-C populated | Dashboard, growth script |
| Pipeline health | Candidates processed, not stale | PENDING-REVIEW queue |
| Knowledge boundary | No undocumented references | Counterfactual harness |
| Export adoption | Integrations using identity export | OpenClaw, other agents |
| Trust signal | User approval rate, rejection reasons | Pipeline analytics |
| Gate integrity | Merge receipt coverage; auditable apply events | MERGE-RECEIPTS + PIPELINE-EVENTS |
| Retention quality | Week-4 and month-3 paid cohort retention | Product analytics |

---

## 5. Child Safety & Privacy (Compliance)

Not essential to system operation; required for go-to-market in child/minor segments.

| Area | Consideration |
|------|---------------|
| **Email (Grace-Mar address)** | PII; parent creates/manages; COPPA applies if linked to child identity |
| **X (Twitter)** | Platform ToS; COPPA for minors; parent-managed accounts still subject to regulatory scrutiny; posting in fork's voice = higher risk |
| **YouTube (OAuth, history)** | Parent OAuth; only recommended videos recorded; no full history sync (see YOUTUBE-PLAYLIST-DESIGN) |
| **Third-party integrations** | Any service holding child PII requires parent consent and platform compliance |

**Principle:** Parent controls linkage. No autonomous child-facing accounts without explicit setup and consent.

---

## 6. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Agent web adoption slower than expected | Grace-Mar works as standalone Record + Voice; identity value persists regardless |
| Competitor copies schema | First-mover, evidence-grounding depth, governance maturity; open protocol grows ecosystem |
| Trust incidents (agent misuse) | Document security posture; treat agent as adversary; gate is non-negotiable |
| User fatigue (approval burden) | Staging automation reduces capture friction; approval remains lightweight |

---

## 7. Related Docs

| Document | Relevance |
|----------|-----------|
| [White Paper](WHITE-PAPER.md) | Full narrative, differentiation, trust primitive |
| [Business Prospectus](BUSINESS-PROSPECTUS.md) | Investor/partner summary |
| [Design Roadmap](DESIGN-ROADMAP.md) | Product/feature design (email, newsletters, X, integrations) |
| [Design Notes](DESIGN-NOTES.md) | White paper input, positioning, agent-web insights |
| [Competitive Analysis](COMPETITIVE-ANALYSIS.md) | Market landscape |
| [Differentiation](DIFFERENTIATION.md) | Competitive moats |
| [Market Research Alpha/Khan](MARKET-RESEARCH-ALPHA-KHAN.md) | Alpha alternatives, cost comparison |

---

*Document version: 1.0*
*Last updated: February 2026*
