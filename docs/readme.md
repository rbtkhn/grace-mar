# Grace-Mar — Document Map

**Where to go for what.** This folder holds the protocol, governance, and commentary. **Terminology:** [glossary.md](glossary.md). Use the table below to find the right document.

| Need | Document | Role |
|------|----------|------|
| **Protocol (the compact)** | [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md) | Canonical spec: schema, staging contract, evidence, export. Mechanism only. |
| **SELF-KNOWLEDGE vs SELF-LIBRARY** | [BOUNDARY-SELF-KNOWLEDGE-SELF-LIBRARY](boundary-self-knowledge-self-library.md) | Identity-facing vs reference-facing; CIV-MEM as library subdomain; proposal classes. |
| **Boundary Review Queue** | [BOUNDARY-REVIEW-QUEUE](boundary-review-queue.md) | Classify proposals by surface; misfiled hints; inbox; audit trail (phased). |
| **Contradiction timeline** | [CONTRADICTION-TIMELINE](contradiction-timeline.md) | When beliefs/claims changed; evidence (ACT-*); resolved / deferred / open; git + pipeline. |
| **Governance** | [GRACE-MAR-CORE](grace-mar-core.md) | Global governance, prime directive, invariants. |
| **Interpretation & intent** | [CONCEPTUAL-FRAMEWORK](conceptual-framework.md), [DESIGN-NOTES](design-notes.md) | Why we built it this way; design principles; objections answered. Federalist-style commentary. |
| **Narrative & differentiation** | [WHITE-PAPER](white-paper.md) | Full story, positioning, technical model. |
| **Business** | [BUSINESS-PLAN](business-plan.md), [BUSINESS-PROSPECTUS](business-prospectus.md), [BUSINESS-ROADMAP](business-roadmap.md) | Operating plan, market, revenue, roadmap. |
| **Implementation** | [AGENTS](../AGENTS.md), [ARCHITECTURE](architecture.md) | Guardrails for AI and developers; system design. |
| **Trust layers (tools)** | [TRUST-LAYERS](trust-layers.md) | Reliability vs adversarial surfaces; complements knowledge boundary. |
| **Public copy / examples** | [CONTRIBUTING-PUBLIC-COPY](contributing-public-copy.md) | Tone for comparisons; fake tokens in docs. |
| **Naming convention** | [NAMING-CONVENTION](naming-convention.md) | Lowercase/hyphen preference; reserved `AGENTS.md`; Python `snake_case`; OpenClaw export path. |
| **Web app** | [WEB-APP-PLAN](web-app-plan.md) | Grace-mar.com development plan; phases, tech, dependencies. See [DESIGN-ROADMAP](design-roadmap.md) for related features. |
| **Intent schema** | [INTENT-TEMPLATE](intent-template.md) | Machine-readable goal hierarchy, trade-offs, and escalation rules. |
| **Session/development handoff** | [DEVELOPMENT-HANDOFF](development-handoff.md) | Latest engineering state and restart checklist for new agent conversations. |
| **work-jiang session bootstrap** | [WORK-JIANG-BOOTSTRAP](../bootstrap/work-jiang-bootstrap.md) | New agent thread on Jiang research lane: read order, membrane, verify block, warmup when Record/gate touched. |
| **Lanes (north stars + weekly rhythm)** | [lanes/README](lanes/README.md), [WEEKLY-RHYTHM](lanes/WEEKLY-RHYTHM.md) | One screen per lane (Record, WPC, civ-mem, operator); single weekly checklist. |
| **Library ↔ system** | [LIBRARY-INTEGRATION](library-integration.md) | Lookup order (library → CMC → full), scope/priority, shelves, operator script. |
| **Civ-mem encyclopedia (hybrid)** | [civ-mem-encyclopedia-hybrid](civ-mem-encyclopedia-hybrid.md) | Fat `ENCYCLOPEDIA.md` + regen; **owned essays** [civilization-memory/README](civilization-memory/README.md). |
| **K-12 schools (pilot)** | [Rocky Record](rocky-record-service-brief.md), [k12-schools-pilot-playbook](k12-schools-pilot-playbook.md), [k12-schools-colorado](k12-schools-colorado.md), [k12-dpa-placeholders](k12-dpa-placeholders.md), [k12-market-research-2026](k12-market-research-2026.md) | CO offer; DPA stub; research. |
| **Operator onboarding** | [OPERATOR-BRIEF](operator-brief.md), [LETTER-TO-USER](letter-to-user.md), [LETTER-TO-STUDENT](letter-to-student.md) | Age-neutral operator brief; letters to the companion (age-neutral and school-aged variants). [PARENT-BRIEF](parent-brief.md) = parent/guardian variant. |
| **We read / THINK vs IX** | [WE-READ-THINK-SELF-PIPELINE](we-read-think-self-pipeline.md) | After shared reading: log READ + THINK; stage IX separately; optional `intake_evidence_id` on candidates. |
| **Using Grace-Mar without a school** | [USING-GRACE-MAR-WITHOUT-A-SCHOOL](using-grace-mar-without-a-school.md) | Homeschool / standalone: who it's for, core loop, "we did X" + /review, export, optional stack (e.g. Grace-Mar + Khan/IXL). |
| **Audits** | [audit-companion-self](audit-companion-self.md), [AUDIT-GRACE-MAR-VS-COMPANION-SELF-TEMPLATE](audit-grace-mar-vs-companion-self-template.md), [audit-structural-alignment-grace-mar-companion-self](audit-structural-alignment-grace-mar-companion-self.md), [audit-boundary-grace-mar-companion-self](audit-boundary-grace-mar-companion-self.md) | Companion-self concept alignment; instance vs template; structure + formatting; **normative boundaries** (Record · template; what may cross). |
| **work-xavier (advisor module)** | [work-xavier/README](skill-work/work-xavier/README.md) | Operator project lane for advising Xavier; **not** her instance repo. Her Record is **companion-xavier** (separate GitHub repo). |
| **Cross-instance boundary** | [cross-instance-boundary.md](cross-instance-boundary.md) | Two-repo contract; optional `check_forbidden_path_strings.py` for **peer** repos only. |
| **Feedback loops** | [feedback-loops](feedback-loops.md) | Proposal brief, calibrate-on-miss, low-friction approval, closed-loop verification, oversight cadence. |
| **Gate traffic (tiers)** | [RECURSION-GATE-THREE-TIER](recursion-gate-three-tier.md) | Tier 1–3 lanes, Bronze vs future Silver/Gold, `ready_for_quick_merge`, escalation CLI, metrics. |
| **OB1 / Open Brain bridge** | [START-HERE-OB1-USERS](start-here-ob1-users.md) | Translation table, Approval Inbox alias, imports — familiar entry without changing ontology. |
| **Workflow catalog** | [WORKFLOW-CATALOG](workflow-catalog.md) | Link index for daily brief, journal, bridge, Xavier, work-dev, gate, observability. |
| **Imports and capture** | [IMPORTS-AND-CAPTURE](imports-and-capture.md) | Safety boundary: evidence/prepared context vs gated Record. |
| **Skills (two layers)** | [SKILLS-EXPLAINED](skills-explained.md) | Portable skills vs SKILLS Record surface. |

**Hierarchy:** The protocol (IDENTITY-FORK-PROTOCOL) is the thing to implement. CORE is governance. CONCEPTUAL-FRAMEWORK and DESIGN-NOTES interpret and explain intent. WHITE-PAPER and prospectus are narrative and business.

**If validate-integrity reports stale derived exports:** run the refresh block in [DEVELOPMENT-HANDOFF § Quick Resume](development-handoff.md#quick-resume-commands).

**Objections answered:** See [DESIGN-NOTES §17](design-notes.md#17-objections-and-answers).
