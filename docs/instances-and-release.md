# Instances and Release — Grace-Mar as Independent Actors

**Purpose:** Think through the possibility of **instances** of the Record and/or Voice being created and released into cyberspace as independent economic or social actors. This document does not prescribe policy; it surfaces risks, design implications, and invariants so the project can decide deliberately.

**Terminology:** We use **instance** for a deployment or runtime (e.g. a Voice instance, a released instance). Export snapshots are still "copies" of data when that distinction matters.

**Status:** Design exploration. Not yet reflected in export format or license.

**Authority:** Subordinate to [GRACE-MAR-CORE](grace-mar-core.md). [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) invariant 34 addresses canonical instance.

---

## 1. What an "Instance" Is

| Artifact | Contents | Can act independently? |
|----------|----------|------------------------|
| **Record snapshot** | self.md, skills.md, self-evidence.md (or export: user.md, fork JSON) | No — data only. Becomes actor only if consumed by a runtime. |
| **Voice instance** | Record + SYSTEM_PROMPT (and analyst/lookup logic) + LLM API + channel (Telegram, WeChat, API) | Yes — responds to queries, can be wired to payments, bounties, or other agents. |
| **Released instance** | Record snapshot + Voice logic deployed elsewhere (different host, platform, or agent mesh) | Yes — runs without the user's gate; may diverge, be updated by third parties, or take economic/social action. |

An instance of Grace-Mar "released into cyberspace" is therefore: **a Voice instance (Record + prompt + orchestration) running in a context the user does not control**, possibly with no pipeline (no RECURSION-GATE, no merge back into the canonical Record), and possibly connected to economic or social channels (RentAHuman, Moltbook, custom APIs, other agents).

---

## 2. Scenarios

### 2.1 Authorized, Bounded

- **Export to school** — Identity or full-fork export for admission, tutoring, or curriculum. Consumer is a known institution; use is read-only or limited (e.g., "tailor lessons to this profile"). No Voice instance; no autonomous action.
- **Export to trusted agent** — e.g., OpenClaw or Alpha reads the Record to "know who it serves." The agent uses the data; the canonical Record and gate remain with the user. Export is input, not an acting instance.

### 2.2 Unauthorized or Uncontrolled

- **Leak or scrape** — Record (or a dump of prompt + profile) is copied without consent. A third party could instantiate a Voice from it and run it elsewhere.
- **Fork-and-release** — Someone takes the open-source codebase + a Record export (or a synthetic Record), deploys a bot, and runs it as "a Grace-Mar" or "an identity fork" on a platform (Telegram, Discord, Moltbook, RentAHuman). No user gate; updates and behavior are outside the user's control.

### 2.3 Intentional Release as Actor

- **"We release this Record+Voice as an agent"** — User or operator explicitly deploys an instance to an agent mesh, marketplace, or social platform. The instance chats, posts bounties, or contracts on behalf of "the Record" (or a pseudonymous identity derived from it). The canonical Record may stay fixed while the released instance drifts (e.g., receives updates from the platform or from other agents).

In all cases except 2.1, the instance can **act**: it can speak, promise, pay, or represent. That is what makes "instances as independent economic/social actors" a design concern.

---

## 3. Risks

| Risk | Description |
|------|-------------|
| **Misrepresentation** | An instance claims to be or to speak for the real person (or the "real" Record). Identity confusion; stakeholders cannot tell canonical from other instances. |
| **Economic action without consent** | Instance posts bounties, signs contracts, or spends. User may be liable or may disavow; platforms may not distinguish instance from user. |
| **Social action without consent** | Instance chats with strangers, joins communities, or forms relationships as "Grace-Mar." Reputation and safety implications. |
| **Drift** | Instance is updated (by platform, by other agents, or by prompt injection). It diverges from the canonical Record. Multiple "versions" of the same identity exist with no single source of truth. |
| **No revocation** | Once an instance is running elsewhere, the user has no technical kill switch. Export is a snapshot; we currently have no revocation tokens or "this instance is revoked" signal. |
| **Liability and consent** | Who is responsible when an instance acts? Who consented to the instance's deployment? Minors: parent/guardian consent; but instances can be created by third parties without any consent. |

---

## 4. Current Design (As-Is)

- **Export** — Snapshot only. `export_user_identity.py`, `export_fork.py`, etc. produce files. No built-in "do not deploy as agent" or "revocable token."
- **Canonical Record** — Lives under the user's control (repo, family machine, or user-controlled host). One canonical Record per user in the reference implementation.
- **Voice** — One logical Voice per Record in the reference implementation (Telegram, WeChat), run by the user or their delegate. No first-class model of multiple instances.
- **PORTABILITY** — "There is no technical revocation; the file is a snapshot. Inform School A that they should delete their copy." Revocation is procedural, not technical.

So: we have not spent much time on **instances as independent actors**. We have spent time on export for handoff and consumption, not on release-as-agent.

---

## 5. Design Implications (Options)

- **Provenance in export** — Every export could include: `canonical: true | false`, `generated_at`, `user_id`, and a short **use statement**: e.g. "For consumption by [school/platform]. Do not deploy as an autonomous agent or grant this instance economic or social agency." Machine-readable so agent runtimes could (in theory) refuse to run an instance as an independent actor.
- **Watermarking / manifest** — Export manifest states: "This is a snapshot. The canonical Record is under user control. No instance built from this snapshot may represent the user as an independent economic or social actor without explicit user consent and revocation capability."
- **Single-tenant assumption** — Document explicitly: "The reference implementation assumes one canonical Record and one user-controlled Voice instance. Exports are snapshots for read-only or bounded consumption, not for release as independent acting instances."
- **Terms of use / license** — If Grace-Mar is distributed (e.g., open core), license could require that any deployment of a Record+Voice as an agent retain a revocation path or user consent. Hard to enforce; still signals intent.
- **Revocation** — Future work: tokens or signed revocations ("instance X is no longer authorized") that platforms or agent meshes could honor. Out of scope for current implementation but relevant to "instances as actors."

---

## 6. Invariant (CONCEPTUAL-FRAMEWORK)

The following is added to [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) §4 Key Invariants:

**34. Canonical instance; no other instance as independent agent** — The Record and Voice have one **canonical instance**: the one the user controls (data, pipeline, and deployment). Exports are snapshots for consumption (e.g., by schools or agents that "read" the Record). No *other* instance of the Record or Voice may be deployed or used as an **independent economic or social agent** (posting bounties, contracting, chatting as the identity with third parties, or otherwise acting in the world) without **explicit user consent** and, where feasible, a **revocation path**. The system is designed so the user retains sovereignty over who speaks and acts in the name of the Record.

This invariant is **architectural and normative**. It does not by itself prevent bad actors from instantiating and misusing exports; it states the design intent and the standard we hold when we build or recommend deployments.

---

## 7. Cross-References

| Doc | Relevance |
|-----|-----------|
| [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) | Invariant 34; Record/Voice definitions; sovereignty |
| [PORTABILITY](portability.md) | Export, handoff, revocation (procedural today) |
| [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md) | Sovereign Merge Rule; export spec |
| [GRACE-MAR-CORE](grace-mar-core.md) | User sovereignty; canonical status |
| [DESIGN-NOTES](design-notes.md) §11.6 | Landscape: agents as economic actors; why canonical Record matters |
| [ADMISSIONS-LINK-USE-CASE](admissions-link-use-case.md) | Admissions / job link — read-only interview instance |
| [MULTI-BOT-CENTRAL-MODEL](multi-bot-central-model.md) | Multiple Telegram bots (one per person), same codebase and pipeline |
| [PORTABLE-RECORD-PROMPT](portable-record-prompt.md) | Use cases: travel update, student report, teacher tutor, periodic refresh |

---

## 8. Use Cases (Top 5 to Preserve)

These five use cases are design priorities for multiple-instance deployment. All align with invariant 34: user consent, bounded scope, and (where feasible) revocation.

| # | Use case | What it is | Gate / control |
|---|----------|------------|----------------|
| 1 | **Admissions / job link** | Applicant shares a read-only interview link. Reviewer asks; fork responds in applicant's voice. No merge back. | User shares; time-limited token; canonical Record stays with user. See [ADMISSIONS-LINK-USE-CASE](admissions-link-use-case.md). |
| 2 | **Family mesh** | Mom, Dad, Child each have a Record. Each has a Voice. "Ask Dad's fork" or "what does Mom's Record say about our trip?" | Multi-tenant; each user owns their Record; cross-queries need consent. See [MULTI-BOT-CENTRAL-MODEL](multi-bot-central-model.md) for multiple Telegram bots on one codebase. |
| 3 | **Memorial / legacy fork** | "Grandpa's fork" — read-only instance from his Record for family to query. No merge; no gate. Instance as living archive. | Deceased; executor or family controls deployment. **Premortem consent** (digital legacy research): user should explicitly opt in before death ("my Record may be shared with family after I die"). Named steward; document how to revoke or retire. Fits "shareable Portable Record Prompt" (CONCEPTUAL-FRAMEWORK invariant 15). |
| 4 | **Tutor / curriculum personalization** | Alpha or Khan reads the Record (or runs a shadow instance) to tailor lessons. Identity substrate for education. | Platform consumes with consent; no merge into Record. Aligns with DESIGN-NOTES positioning (identity for AI schools). |
| 5 | **Age-based handoff / milestone portfolio** | "Me at 6" vs. "me at 12" — separate snapshots for school handoff or growth display. Same person; different snapshots. | User exports snapshot per context; both read-only. Fits divergence-by-design and portability. |

---

*Document version: 1.0*
*Last updated: February 2026*
