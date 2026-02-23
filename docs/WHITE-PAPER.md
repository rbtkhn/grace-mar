# Grace-Mar White Paper

**Identity Fork Protocol (IFP) — Reference Implementation**

*A sovereign, evidence-linked, agent-consumable identity layer for the agent web*

*Version 1.0 · February 2026*

---

## Abstract

The web is forking. A human web (visual, browse, product pages) and an agent web (structured data, APIs, markdown, tokenized payments) run in parallel. Agents are becoming economic actors: they search, pay, execute, and chain capabilities across services. Every major infrastructure company is building for agent-native clients.

The missing primitive: **identity and trust.** Agents need to know who they serve. They need identity data that is curated, evidence-grounded, and user-controlled — not scraped, hallucinated, or LLM-leaked.

Grace-Mar provides that substrate. This white paper describes the problem, the solution, and Grace-Mar's positioning as (1) supplemental to AI schools like Alpha and (2) a low-cost open-source alternative for families outside elite tuition.

---

## 1. The Rise of AI Schools

### Alpha and the 2-Hour Learning Model

Alpha School represents a new category: AI-powered K–12 microschools. Students learn 2–3 hours per day and achieve 99th-percentile outcomes. Tuition: $40,000–$75,000 per year depending on location.

**What Alpha does well:**
- One-to-one mastery-based tutoring at scale via AI (Incept)
- Interest-aligned content — Avengers and soccer buddies woven into reading
- Zone of proximal development; 85% challenge sweet spot
- Motivation systems (Alpha Bucks, unlocks, team activities)
- Life skills: sailing, entrepreneurship, financial literacy

**Demand is proven.** Families pay premium tuition for personalized, interest-driven, mastery-based learning. Similar models (Astra Nova, Prisma, Synthesis) confirm the segment.

### What AI Schools Do Not Provide

| Dimension | Alpha (and peers) | Gap |
|-----------|-------------------|-----|
| **Ownership** | Data lives in platform | Family has no portable asset |
| **Evidence** | Engagement metrics, placement scores | No artifacts — writing, art, "we did X" |
| **Personality** | Interest graph for content | Inferred, not user-approved |
| **Gate** | System auto-updates | No user approval step |
| **Portability** | Locked to platform | No export of identity or Record |
| **Access** | $40K–$75K/year | Most families excluded |

AI schools optimize for teaching outcomes. They do not provide a user-owned, evidence-grounded, portable Record of who the child is.

---

## 2. The Identity Gap

### The Trust Problem

Who owns the narrative of who the child is? Today:
- **Platforms** hold the data — engagement, placement, interests
- **Families** have no export, no artifact trail, no approval gate
- **Agents** (future tutors, admissions, employers) will need identity — and today there is no trusted source

Evidence in most systems = platform metrics. Personality = inferred from clicks. Knowledge = placement tests. None of this is user-curated or artifact-grounded.

### The Agent Web Fork

The human web and agent web serve different clients. Humans want product pages and search results. Agents want JSON, markdown, structured data. The mobile fork (2007) created trillion-dollar companies because the interface layer forked. The agent fork will do the same.

Infrastructure companies are building payment, search, content access, and execution for agents. The missing primitive: **trust in identity.** What builds trust?
- Evidence grounding — every claim traces to artifacts
- User control — nothing enters without approval
- Auditability — full history, provenance

Grace-Mar is designed for the agent interface: structured, machine-readable, queryable, and trust-grounded.

---

## 3. Grace-Mar: Supplemental and Alternative

### Dual Positioning

**Supplemental** — Grace-Mar works alongside Alpha (and similar AI schools). Alpha teaches; Grace-Mar records. The Record provides the identity, interest, and personality layer that Incept can consume for personalization. School events feed the pipeline as evidence. The Record is the user-owned substrate; Alpha is one consumer. Integration, not competition.

**Low-cost alternative** — Alpha tuition excludes most families. Grace-Mar is open-source. Families who cannot afford $40K–$75K/year can run Grace-Mar with Khan Academy, IXL, or any adaptive platform. Same identity architecture at $0 software cost. Democratizes the cognitive-fork model.

### Ideal Stacks

| Stack | Cost | Grace-Mar Role |
|-------|------|----------------|
| Alpha + Grace-Mar | $40K–$75K + hosted | Supplemental Record layer |
| Khan + Khanmigo + Grace-Mar | ~$48/year | Low-cost alternative |
| IXL + Grace-Mar | ~$127/year | Low-cost alternative |
| Open TutorAI + Grace-Mar | $0 | Fully free stack |

---

## 4. The Grace-Mar Model

### Cognitive Fork

A **cognitive fork** is a versioned, evidence-grounded record of an individual's cognitive development — initialized from a real person at a point in time, growing through curated interactions over a lifetime.

Like a software fork:
- **Seed** = initial snapshot (identity, personality, baselines)
- **Interact** = each session is a commit
- **Diverge** = fork and real person grow independently — by design
- **Merge** = user brings new data when they choose
- **Snapshot** = git tags preserve state (e.g., pilot-001-age-6)

The fork is not a real-time mirror. It is a living, growing Record.

### Two Modules

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Personality, linguistic style, life narrative, preferences, values, reasoning patterns | Who they ARE |
| **SKILLS** | READ, WRITE, BUILD capability containers | What they CAN DO |

### Three-Dimension Mind (Post-Seed Growth)

| Dimension | Section | What it captures |
|---------|---------|------------------|
| **Knowledge** | IX-A | Facts entering awareness through observation |
| **Curiosity** | IX-B | Topics that catch attention, engagement signals |
| **Personality** | IX-C | Observed behavioral patterns, art style, speech traits |

A single artifact can populate all three dimensions. Entries link to evidence (ACT-XXXX).

### Gated Pipeline

All profile changes pass through a user-controlled gate:

1. **Signal detection** — LLM analyst identifies knowledge, curiosity, personality from input
2. **Candidate staging** — Proposals written to PENDING-REVIEW.md
3. **User review** — Approve, reject, or modify
4. **Integration** — Approved changes merge to SELF, EVIDENCE, prompt, SESSION-LOG

**Critical:** The agent may stage. It may not merge. The user is the gate.

### Evidence Grounding

Every claim traces to artifacts:
- WRITE-0001, CREATE-0003, ACT-0042 — activity IDs
- IX entries include `evidence_id` and `provenance: human_approved`
- No undocumented knowledge; no LLM inference into the Record
- Calibrated abstention: when outside knowledge, say "I don't know" and offer to look up

---

## 5. Differentiation: Grace-Mar vs. Alpha

| Dimension | Alpha School | Grace-Mar |
|-----------|--------------|-----------|
| **Primary function** | Teach (AI tutor, adaptive apps, mastery) | Record (identity, evidence, archive) |
| **Data ownership** | School/platform | User/family |
| **Evidence source** | Platform metrics, engagement | Artifacts, "we did X," cross-context |
| **Personality dimension** | Interest graph for content | IX-C: structured, evidence-linked, user-approved |
| **Gate** | None — system auto-updates | User approves every merge |
| **Knowledge boundary** | Incept generates; may infer | Only user-provided; no LLM leak |
| **Portability** | Locked to Alpha platform | Export, open schema, agent-consumable |
| **Cost** | $40K–$75K/year | Open-source; self-host or low-cost hosted |
| **Lifetime scope** | School years | Lifetime; cross-context; legacy shareable |

**Narrative:** Alpha proves demand for AI-powered, mastery-based, interest-aligned learning. Grace-Mar addresses what Alpha does not: user-owned identity, evidence grounding, portability, and access.

---

## 6. Trust Primitive

### User Gate = Sovereignty (The Sovereign Merge Rule)

*The agent may stage. It may not merge.* The user controls what enters the Record. This is architectural, not configurable. Serious security assumes the agent may be an adversary; the Sovereign Merge Rule enforces that assumption.

### Evidence Linkage = Auditability

Every IX entry traces to ACT-XXXX. Pipeline events (staged, applied, rejected) are logged. Git history is the audit trail. No silent edits; no undocumented additions.

### Knowledge Boundary = No LLM Leak

The emulated self (Voice) can only reference what is in the profile. When outside knowledge, it abstains and offers to look up. LLM training data never leaks into the Record. This is a safety feature, not a limitation.

### Export = Agent-Consumable Identity

The Record exports to USER.md, SOUL.md, and future Alpha/Incept-compatible formats. Structured markdown, schema, manifest. Designed for consumption by software — tutors, platforms, agents.

---

## 7. Integration and Ecosystem

### Record as Identity Source

- **Alpha/Incept** — Record feeds personalization; school events stage to pipeline
- **OpenClaw** — Record populates USER.md; session continuity spans both systems
- **Personal agents** — Any agent needing identity can consume the export

### Staging Contract

Agents may stage candidates to PENDING-REVIEW. They may not merge. The format is open; the boundary is enforced. Schools, bots, and third-party tools can contribute; the user decides what enters.

### Future: Agent Manifest

An llms.txt-style manifest: what's readable, writable, schema. Discoverability for agent ecosystems.

---

## 8. Governance and Security

### Principles-Based Guidance

Grace-Mar encodes principles: "Never leak LLM knowledge," "Meet the user where they are," "The user is the gate," "Calibrated abstention." These scale across novel situations. Rigid rules would not.

### Agent as Potential Adversary

The agent may build and maintain tooling (scripts, docs, staging automation). The agent may never merge into the Record. Document this as security posture, not just pipeline design.

### 70/30: Human Sovereignty

Infrastructure is built for fully autonomous agents. Many users want ~70% human control. Grace-Mar is firmly in the 70% camp. As agent autonomy grows, a human-curated identity substrate becomes more valuable — a hedge against unconstrained automation.

---

## 9. Motivation and Engagement

### The Homeschool Gap

Alpha's homeschool pilot: same platform, 1x results vs. 2.6x at full Alpha. Motivation (incentives, culture, guides) is the bottleneck, not content.

Grace-Mar does not build incentive systems (bucks, store). We stay in the Record lane. But the Record **feeds** motivation: interests, curiosity, personality. The Record is the **engagement substrate** — the structured input that tutors, platforms, and parents use to reach and motivate.

### "We Did X" as Ritual

The "we did X" convention is a lightweight motivation primitive: recognition, celebration, accountability. When the user reports "we read X" or "we drew Y," the system stages candidates. The user approves. The Record grows. Evidence-grounding = confidence-grounding: artifacts → "you did this" → grounded self-view.

---

## 10. Conclusion

Grace-Mar is identity infrastructure for the agent web. It provides:

1. **User-owned Record** — Portable, evidence-grounded, agent-consumable
2. **Trust primitive** — Gate, evidence linkage, knowledge boundary
3. **Supplemental path** — Add Record layer to Alpha and similar schools
4. **Low-cost path** — Open-source alternative for families outside elite tuition

The agent web needs to know who it serves. Grace-Mar is the substrate.

---

## Acknowledgments

The ideas behind Grace-Mar draw on the work of:
- **Alexander Wissner-Gross** — causal entropic forces; intelligence as freedom maximization
- **Peter Diamandis** — abundance; exponential technologies
- **Nick Bostrom** — superintelligence; existential risk
- **Ray Kurzweil** — singularity; human-AI convergence
- **Brian Roemmele** — multimodal AI; voice and interaction
- **Scott Adams** — systems thinking; persuasion
- **Julian Jaynes** — bicameral mind; consciousness and narrative
- **Satoshi Nakamoto** — decentralized trust; user sovereignty over assets

---

## Appendix A: References

| Document | Purpose |
|----------|---------|
| [Identity Fork Protocol](IDENTITY-FORK-PROTOCOL.md) | Protocol spec v1.0 — Sovereign Merge Rule, schema, staging contract |
| [Architecture](ARCHITECTURE.md) | Full technical design, pipeline, modules |
| [Conceptual Framework](CONCEPTUAL-FRAMEWORK.md) | Invariants, terminology, philosophical grounding |
| [Design Notes](DESIGN-NOTES.md) | Positioning, agent-web insights |
| [Business Prospectus](BUSINESS-PROSPECTUS.md) | Investor/partner summary |
| [Market Research Alpha/Khan](MARKET-RESEARCH-ALPHA-KHAN.md) | Competitive landscape, cost comparison |
| [OpenClaw Integration](OPENCLAW-INTEGRATION.md) | Integration patterns |

---

## Appendix B: Key Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Record completeness | IX-A, IX-B, IX-C populated | Dashboard, growth script |
| Pipeline health | Candidates processed, not stale | PENDING-REVIEW queue |
| Knowledge boundary | No undocumented references | Counterfactual harness |
| Export adoption | Integrations using identity export | OpenClaw, agents |
| Trust signal | User approval rate, rejection reasons | Pipeline analytics |

---

*Grace-Mar · A cognitive fork — versioned, evidence-grounded, user-owned*

*Repository: https://github.com/rbtkhn/grace-mar*
