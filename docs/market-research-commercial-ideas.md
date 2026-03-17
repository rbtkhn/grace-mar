# Market Research — Commercial Ideas (2026)

**Purpose:** New commercial angles derived from market research, aligned with Grace-Mar's identity-fork model, Sovereign Merge Rule, and evidence integrity. Complements [Business Roadmap](business-roadmap.md) and [White Paper](white-paper.md).

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

---

## Market snapshot (2025–2026)

| Category | Size / trend | Relevance to Grace-Mar |
|----------|--------------|------------------------|
| **AI persistent memory / identity** | 2026 framed as "year of persistent context"; Mem0, Weaviate, long-context; enterprise wants memory layer | Grace-Mar = *user-approved* persistent identity + evidence, not stateless or RAG-only — differentiator |
| **AI-enabled personality development** | ~$6.76B (2025) → ~$44.73B (2035), 20.8% CAGR; motivation, coaching, soft skills | IX-B/IX-C + evidence + gate = "personality with provenance" |
| **Digital identity as asset** | High-value deals (e.g. creator digital identity ~$975M); avatar, voice, digital twins | Sovereign, evidence-based identity for agents = protocol-layer play |
| **Personalized learning** | ~$6B–$62B depending on scope; 22–26% CAGR | Curriculum + Record + skill gaps = existing wedge; market supports premium for personalization |
| **Homeschool curriculum** | ~$3.24B (2024) → ~$6.76B (2033), ~8% CAGR | Direct fit for homeschool/microschool wedge |
| **AI companion apps** | ~$4.24B (2025) → ~$9.65B (2030); revenue concentrated in social/romantic | Education/family "companion as Record" underdeveloped; trust + evidence = positioning gap |
| **Family legacy / memory** | Heirloom, Aeternum, LifeVaultAI; ~$3–19/mo; storage + stories + time capsules | Grace-Mar = structured *identity* + queryable voice + artifact trail, not just vault — "living legacy" |
| **K-12 edtech procurement** | Federal $ for AI personalization; FERPA/COPPA/1EdTech; human-in-the-loop required | Gate + evidence + portability align with procurement criteria |
| **Sovereign / user-owned identity** | Self.me, Bloock, Dataswift; SSI, portability, privacy-first | Same category; Grace-Mar adds education + Record + agent-consumable export |
| **Evidence-based portfolios** | Seesaw, Otus, Foliotek; ~$40/portfolio/year, $5K+ minimums | Record as *evidence layer* that feeds portfolios = B2B integration angle |

---

## New commercial ideas

### 1. **"Living legacy" SKU (family / adult)**

**Why:** Legacy apps (Heirloom, Aeternum, LifeVaultAI) sell storage + stories + time capsules at $3–19/mo. None offer a *queryable, evidence-grounded identity* that can speak in the person's voice from approved content. Grace-Mar already has the Record, Voice, and gate; the positioning is "your future self (or your family) can ask the Record — and it answers from what you chose to document."

**Idea:** Package the same stack as **Living Legacy**: one-time or subscription for adults/families who want a durable, queryable identity (values, stories, preferences) with explicit control over what goes in. Market as "not a vault, a voice — your words, your gate."

**Fit:** No change to pipeline or governance. Export/PRP + optional hosted miniapp. Revenue: subscription or one-time "legacy build" fee.

**Effort:** Low (positioning + packaging); Medium if new onboarding flow for non-homeschool adults.

---

### 2. **Evidence layer for existing portfolio/LMS products (B2B)**

**Why:** Seesaw, Otus, Foliotek, and similar sell evidence-based learning and portfolios. They hold *artifacts and grades* but rarely a single, user-owned, approval-gated *identity* that travels. Districts want FERPA/COPPA-safe, human-in-the-loop, explainable profile growth.

**Idea:** Offer Grace-Mar (or companion-self) as an **evidence and identity layer** that schools or portfolio vendors integrate: Record receives approved activities; export feeds their LMS/portfolio. Revenue = per-seat or per-school license, or API/export fee. Position as "we don't replace your LMS; we add sovereign, evidence-linked identity that exports to you."

**Fit:** Aligns with K-12 pilot and "supplemental" positioning. Requires clear API/export contract and compliance narrative.

**Effort:** Medium (integration surface, sales narrative); High for first signed school.

---

### 3. **"Personality with provenance" for coaches and creators**

**Why:** AI-enabled personality development is a $6B+ growth market; motivation and coaching are top use cases. Most systems infer personality from behavior. Grace-Mar's IX-B/IX-C are *curated and approved* — personality with provenance.

**Idea:** Target coaches, creator-educators, and small teams who want a **portable, evidence-backed profile** of a person's interests, style, and growth (e.g. for handoffs, continuity, or personalized content). Not a replacement for coaching tools; a **profile substrate** that "this person's documented interests and style" can be consumed by other tools. Monetize via hosted Record + export API or white-label.

**Fit:** Extends "identity for the agent web" to professional/creator segment. Same pipeline; different ICP and messaging.

**Effort:** Medium (positioning, landing page, one segment-specific onboarding).

**Implementation:** See [positioning-personality-with-provenance.md](positioning-personality-with-provenance.md) — segment definition, value prop, messaging, landing copy, and next steps.

---

### 4. **Agent-ready identity API (infrastructure)**

**Why:** 2026 emphasis on persistent context and agent memory; digital identity valued as an asset. Agents need identity they can trust (evidence, audit, user control). Today most agent memory is platform-owned or stateless.

**Idea:** Productize **Grace-Mar-compatible identity API**: structured, read-only (or scoped write) access to a user's Record for approved agents. Revenue: per-identity or per-query; or certification fee for "IFP-compliant" consumers. Position as "the identity primitive for the agent web — evidence-grounded, user-approved, portable."

**Fit:** White paper already frames this. Requires stable schema, auth, and rate limits; certification comes after proof (per business roadmap).

**Effort:** High (API product, auth, docs); sequence after 18-month proof.

---

### 5. **Curriculum + Record bundle (homeschool)**

**Why:** Homeschool curriculum market ~$3.24B→$6.76B; personalized learning 22–26% CAGR. Grace-Mar already has curriculum generator, skill gaps, IX-B signals. Competitors sell curriculum or placement; few sell "curriculum that adapts to *your documented* interests and gaps."

**Idea:** **Curriculum that reads the Record**: generate modules/plans from IX-A/B/C and skill gaps; market as "curriculum that knows your kid — because you approved what goes in." Revenue: premium tier (hosted family + curriculum) or one-time curriculum pack. Differentiator: curriculum is driven by the *same* evidence-grounded Record the family owns.

**Fit:** Builds on existing generate_curriculum, load_alpha_school_benchmarks; aligns with "low-cost alternative" and homeschool wedge.

**Effort:** Medium (bundle packaging, UX for "curriculum from Record"); part of roadmap #12.

---

### 6. **Gate-as-a-service for other products**

**Why:** Many products want "human approval before AI writes" but lack a clean primitive. Grace-Mar's recursion-gate + process_approved_candidates is a reusable pattern.

**Idea:** Offer **gate-as-a-service** (or open-source reference + paid hosting): other apps send candidates; Grace-Mar holds the queue and approval UX; on approve, callbacks or webhooks to the client. Revenue: SaaS fee or usage-based. Positions Grace-Mar as infrastructure for "sovereign merge" in any domain, not only identity.

**Fit:** Requires generalizing gate schema and auth so it's not tied to a single Record type; could dilute focus if pursued too early.

**Effort:** Medium–High (multi-tenant gate, API, security); consider only after core wedge is proven.

---

## Suggested prioritization (with current roadmap)

| Priority | Idea | Rationale |
|----------|------|-----------|
| **Now** | Curriculum + Record bundle (#5) | Already building; market size and homeschool wedge clear. |
| **Next** | Living legacy SKU (#1) | Same stack, new packaging; expands TAM without new pipeline. |
| **Pilot** | Evidence layer B2B (#2) | Aligns with K-12 / integration pilots; one deal validates. |
| **Later** | Personality with provenance (#3) | Clear segment; can run as small experiment (landing page, waitlist). |
| **After proof** | Agent identity API (#4), Gate-as-a-service (#6) | Infrastructure plays; sequence per business roadmap. |

---

## Sources (summary)

- AI memory / persistent context: industry framing 2026; Mem0, Weaviate, long-context.
- AI personality development: Market.us report (CAGR 20.8%).
- Digital identity: Khaby Lame–style valuation; sovereign identity (Self.me, Bloock, Dataswift).
- Personalized / homeschool: Research and Markets, Growth Market Reports, Dataintelo.
- AI companion apps: HyperAI, Economic Times, Research and Markets (~$4.24B 2025).
- Family legacy: Heirloom, Aeternum, LifeVaultAI (pricing and features).
- K-12 procurement: EdWeek Market Brief, ClassWorks, 1EdTech; federal AI $ and human-in-the-loop.
- Evidence portfolios: Seesaw, Otus, Foliotek, Citizens (pricing and positioning).

No change to pipeline semantics, Sovereign Merge Rule, or GRACE-MAR-CORE.
