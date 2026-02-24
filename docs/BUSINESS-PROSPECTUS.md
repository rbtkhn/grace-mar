# Grace-Mar — Business Prospectus

**Identity Infrastructure for the Agent Web**

*Version 1.1 · February 2026*

---

## Executive Summary

Grace-Mar defines the **Identity Fork Protocol (IFP)** and ships a reference implementation for user-owned, evidence-grounded identity. The protocol contribution is: schema + gate + evidence linkage + export.

**Core doctrine — The Sovereign Merge Rule:** *The agent may stage. It may not merge.* The user (or explicitly delegated human) is the merge authority.

**Business focus (next 18 months):**
- **Primary wedge:** Hosted B2C product for homeschool and microschool families.
- **Secondary wedge:** 1-2 institutional pilots (school/platform integration).
- **Deferred monetization:** Certification only after independent adoption appears.

This sequencing reduces execution risk and creates proof before broad platform claims.

---

## Problem

| Pain Point | Practical Impact |
|------------|------------------|
| **No trusted identity primitive for agents** | Agents personalize from scraped/inferred context with weak provenance |
| **Platform-owned learner data** | Families cannot carry identity context across tools/schools |
| **Evidence is metric-heavy, artifact-light** | Engagement scores exist; artifact-grounded identity often does not |
| **Elite AI school economics are exclusionary** | High personalization quality exists but is inaccessible to most families |

---

## Solution

Grace-Mar provides:
- **Record:** Structured identity (`SELF`, `SKILLS`, `EVIDENCE`)
- **Gate:** Stage/review/merge with human merge authority
- **Evidence grounding:** claims linked to artifacts (`evidence_id`, provenance)
- **Export:** agent-consumable identity surfaces (markdown, manifest, PRP)

This is not a tutoring replacement. It is an identity substrate that tutoring systems can consume.

---

## Strategy and Sequencing

### Phase 1 (0-18 months): Focused Execution

| Priority | Objective | Success Signal |
|----------|-----------|----------------|
| 1 | Launch hosted product for families | Repeatable onboarding and weekly active usage |
| 2 | Prove engagement and retention | Stable cohort retention and healthy pipeline cadence |
| 3 | Run 1-2 integration pilots | Signed pilot scope + measurable integration outcomes |

### Phase 2 (18-36 months): Scale and Standardize

| Priority | Objective | Success Signal |
|----------|-----------|----------------|
| 1 | Expand integration surfaces | Multiple production integrations |
| 2 | Formalize protocol ecosystem | Third-party implementations emerge |
| 3 | Introduce certification | Independent governance process and published criteria |

---

## Go-to-Market (Primary Wedge: Families)

### ICP (Initial Customer Profile)

- Parent/guardian-led homeschool or microschool families
- Already using fragmented tools (Khan/IXL/tutors) and missing continuity
- High willingness to maintain a portable learner record

### Distribution Plan (First 12 Months)

| Channel | Why It Fits | Leading Indicator |
|---------|-------------|-------------------|
| Homeschool communities | High pain for continuity + portfolio evidence | Waitlist conversions |
| Educator creators/newsletters | Trust transfer and low-CAC education funnel | Cost per activated family |
| Parent referrals | Identity record compounds and is shareable | Referral % of new activations |

---

## Monetization

### Near-Term Revenue (0-18 months)

| Priority | Stream | Target | Price (initial) |
|----------|--------|--------|-----------------|
| 1 | Hosted service (B2C) | Families | $8-15/mo or $80-120/yr |
| 2 | Integration pilot fees (B2B light) | Schools/platforms | Pilot-scoped, fixed fee |
| 3 | Premium exports/workflows | Power users | $50-200/yr |

### Later Revenue (post-proof)

| Stream | Trigger to Activate |
|--------|---------------------|
| Platform license | 2+ validated integrations with measurable uplift |
| Certification | Multiple external implementations requesting conformance proof |

---

## Assumptions Model (Transparent, Testable)

### 12-Month Operating Assumptions (working model)

| Variable | Base Assumption | Notes |
|----------|------------------|-------|
| Free-to-paid conversion | 8-12% | To be validated by onboarding tests |
| Monthly paid churn | 2.5-4.0% | Improved by portfolio/export utility |
| ARPU | ~$100/yr | Blended annualized |
| Gross margin | 75-85% | Model + infra costs not yet optimized |
| CAC | $40-90 | Channel-dependent; expected to fall with referrals |

These are planning assumptions, not validated outcomes. Prospectus updates should mark observed values quarterly.

---

## Traction and Proof Plan

### Current Status

| Milestone | Status |
|-----------|--------|
| Protocol + architecture | Implemented |
| Pilot user profile | Active |
| Gate + pipeline | Live in reference implementation |
| Export surfaces | Implemented (`USER.md`, PRP, manifest) |

### Proof Pack to Publish (investor/integration readiness)

| Proof Item | Metric | Cadence |
|------------|--------|---------|
| Pipeline health | staged/approved/rejected/applied rates | Weekly |
| Gate reliability | merge receipt coverage, merge audit completeness | Weekly |
| Retention | cohort week-4 and month-3 retention | Monthly |
| Evidence depth | artifact-linked claim ratio | Monthly |
| Safety boundary | counterfactual harness pass rate | Per release |

---

## Competitive Position and Defensibility

| Dimension | Defensibility Lever |
|-----------|---------------------|
| Evidence grounding | Artifact-linked claims and provenance discipline |
| Governance trust | Human merge authority + auditable receipts/events |
| Portability | Open export formats and integration surfaces |
| Execution moat | Longitudinal evidence corpus + retention flywheel |

Schema can be copied; longitudinal trust and operating discipline are harder to copy.

---

## Compliance and Trust Controls

Grace-Mar targets family and identity contexts; trust controls are product requirements, not legal afterthoughts.

| Control Area | Current Direction |
|--------------|-------------------|
| Consent model | Parent/guardian-managed linkage; explicit approval gate |
| Data minimization | Stage only what is needed; human-approved merges |
| Auditability | Pipeline events, merge receipts, git-backed history |
| Access boundaries | Role-scoped views and explicit sharing intent |
| Deletion/portability | Export-first architecture; deletion workflows to formalize |

---

## Integration Commercialization Plan

### Pilot Package (90 days)

| Component | Definition |
|-----------|------------|
| Scope | Identity read + stage path only (no autonomous merge) |
| Success metrics | activation rate, personalization quality lift, operator burden change |
| Deliverables | integration report, security posture notes, rollout recommendation |

### Target Buyer

- Head of Product / Learning Science / Platform Integrations at AI school or tutoring platform.

---

## Ask

**Raise:** Pre-seed/seed ($500K-$1.5M) for 18-24 months to:
- ship hosted B2C product,
- prove retention and trust metrics,
- complete 1-2 paid integration pilots.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Scope dilution across too many business models | Enforced sequencing: B2C proof first, integration second |
| Competitor feature copying | Compete on trust operations + longitudinal dataset quality |
| Operator fatigue from approval burden | Better triage, batching, and lightweight review UX |
| Compliance burden slows growth | Build control artifacts in parallel with GTM |

---

## Certification Governance (Future)

Certification is intentionally deferred until ecosystem demand exists. When activated:
- criteria published publicly,
- conformance tests reproducible,
- decision rationale documented,
- appeals process and independent reviewers added.

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [Identity Fork Protocol](IDENTITY-FORK-PROTOCOL.md) | Canonical protocol spec |
| [White Paper](WHITE-PAPER.md) | Narrative + technical rationale |
| [Business Roadmap](BUSINESS-ROADMAP.md) | Strategic priorities and metrics |
| [Architecture](ARCHITECTURE.md) | Implementation design |

---

*Grace-Mar · A cognitive fork — versioned, evidence-grounded, user-owned*
