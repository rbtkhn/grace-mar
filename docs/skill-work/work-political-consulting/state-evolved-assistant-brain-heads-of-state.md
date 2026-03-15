# STATE Evolved: Assistant Brain Product for Heads of State

**Purpose:** Product vision for evolving the **STATE** operating mode (from civ-mem) into an **assistant brain** for the federal executive branch (heads of state / principal + staff). **Goal: federal government contract.** STATE = present moment, structured options, multiple perspectives, tensions preserved, no write to long-term record except by explicit relay. The product is a persistent assistant that embodies that design; the **sale** is deployment under a federal contract (pilot, then sustain). **Human approval required** for any product commitment or outreach. Compliance: US federal only; no lobbying of appropriations unless separately cleared.

**Source:** [civ-mem-state-vs-scholar.md](../../civilization-memory/notes/civ-mem-state-vs-scholar.md), [notes-cmc-substance.md](../../notes-cmc-substance.md). **Related:** [sell-civ-mem-federal-executive.md](sell-civ-mem-federal-executive.md).

---

## 1. What STATE is (foundation)

In civ-mem, **STATE**:

- **Learns from the present** — Live context: the decision at hand, the options in front of the actor.
- **Provides structured decision-relevant options** — Not one recommendation; a set of options (e.g. through perspectives: legitimacy, power, liability).
- **Preserves tensions** — Multiple perspectives; tensions between them are **preserved, not resolved**. Duty of competence: surface **all material options**, including reversal/accommodation.
- **Does not write the long-term record** — Information from the present flows to the canonical layer only via **explicit relay** (the human accepts and merges). STATE does not update "doctrine" or "the record" on its own.

So STATE is an **orientation layer** for the present moment: options, perspectives, tensions visible, sovereign decides. No backdoor into the head of state's permanent record.

---

## 2. Product: Assistant brain for heads of state

**Evolve STATE into:** A persistent **assistant brain** that heads of state (or their immediate staff) can use in the flow of work. Not one-off briefs; a **always-available layer** that:

- **Ingests the present** — Current briefs, calendar, meeting context, the decision in front of them (to the extent the principal or staff feeds it in; no autonomous surveillance).
- **Surfaces structured options** — For any query or decision frame the user gives, the assistant returns **options** through **multiple perspectives** (e.g. legitimacy, power, liability; or security, prosperity, legitimacy; or custom perspectives per institution). Not "you should do X" — "here are the options through these lenses; tensions preserved."
- **Duty of competence** — The option set **must** include the full range of material options, including at least one at the accommodation/reversal end (e.g. "don't escalate," "delay," "reframe"). So the head of state always sees the full field, not a filtered "best" recommendation.
- **Tensions preserved** — When perspectives conflict (e.g. legitimacy says one thing, power says another), the assistant presents both and **does not resolve**. The head of state holds the tension and decides.
- **Explicit relay only** — The assistant **never** writes to the head of state's long-term record, doctrine, or institutional memory unless the user **explicitly** says "save this," "record this decision," or equivalent. So the "brain" is STATE-shaped: present-focused, options and perspectives, no silent write to canonical.
- **Optional: civ-mem / SCHOLAR as context** — If the head of state's institution has ingested a corpus (e.g. civ-mem essays, purpose of history, condition, seam, one subject many tongues), the assistant can **draw on that** when surfacing options — e.g. "through the civ-mem lens: one subject many tongues; see the face; is the seam visible?" — as one perspective among others. SCHOLAR (the ingested corpus) feeds STATE (the present-moment options); the head of state still decides and still controls what, if anything, is relayed to any permanent record.

---

## 3. What the product is not

- **Not a recommender** — It does not say "do this." It says "here are the options through these perspectives; here are the tensions; you choose."
- **Not a writer to the record by default** — It does not log decisions or update institutional memory unless the user explicitly requests a relay (e.g. "add this to the decision log," "record that we considered X").
- **Not a replacement for NSC, cabinet, or staff** — It is an **additional layer**: options and perspectives in the present, with duty of competence and tensions preserved. Policy and politics still flow through the normal chain.
- **Not autonomous** — It only sees what it is given (briefs, calendar, query). No unbidden access to classified or personal systems unless explicitly integrated and approved.

---

## 4. Core behaviors (product spec)

| Behavior | Specification |
|----------|----------------|
| **Input** | User (or staff on behalf of principal) provides: current decision or question; optional context (meeting, briefing excerpt, calendar). **Optional: instinct first** — user may state their leaning ("Where are you leaning?" / "What's your read?") before receiving the field; the system then shows A/B/C and where that instinct sits relative to the perspectives (testing judgment literally). **Optional integrations:** calendar connector, briefing/doc source; authenticate once; no autonomous scraping unless explicitly designed in and approved. |
| **Output** | Structured **options** (not one answer) through **fixed perspectives** — see [Polyphonic cognition implementation](#polyphonic-cognition-implementation) below. Each option labeled (e.g. A/B/C). When two perspectives conflict, **label explicitly** ("Tension: A and C conflict here") and do not resolve. Include a **Reversibility** line or tag: what becomes irreversible (if we do X, delay, or escalate). At least one option at the accommodation/reversal end. **Optional:** plain-language / 600L tier for principals who prefer simple language. **Optional:** export run as one-pager PDF or simple A/B/C diagram (three boxes + tension arrows). |
| **Relay** | Nothing is written to any long-term or institutional record unless the user **explicitly** invokes relay ("save," "record," "add to log"). Relay is a separate action, not automatic. **Optional: post-decision capture** — after the principal decides, prompt "What did you do? What happened?"; store only if user says "record." Supports learning loop and "we did X" habit. |
| **Civ-mem lens (optional)** | If the institution has ingested the civ-mem corpus (condition, seam, one subject many tongues, purpose of history), the assistant can include a **perspective** or **lens** that applies that frame to the current decision (e.g. "Through the coordination lens: one subject, many tongues; see the face; is the seam visible?"). Offered as one of the perspectives, not as the only one. |
| **Sovereign** | The head of state (or their delegated user) is the **sovereign**. The assistant serves: it surfaces, it does not decide. It preserves tensions; it does not collapse them. It writes to the record only when explicitly told to. |
| **No model branding** | In any UI or exported output, show only "A / B / C" and content — no model names or "X said." Focus on structure; reduce vendor lock-in. |

**Polyphonic cognition implementation:** Adapt the upstream civ-mem pattern (three named minds: Mercouris, Mearsheimer, Barnes). Use **fixed slots** so the user always gets the same perspectives: **A = Legitimacy/orientation** (narrative, legitimacy, civilizational continuity; Mercouris-like). **B = Structure/constraints** (power distribution, institutional constraints; Mearsheimer-like). **C = Liability/mechanism** (who bears risk, defection incentive, who defects first; Barnes-like). **D (optional) = Civ-mem lens** when the institution has ingested the corpus: condition, seam, one subject many tongues, see the face — as one perspective among others. Optional: when C is invoked, next response can offer "A reframed in light of C" and "B reframed in light of C" (catalyst reframe). See [concept-cognitive-polyphony.md](../../civilization-memory/notes/concept-cognitive-polyphony.md) § Implementation and § For Grace-Mar.

**Implementation note (parallel perspective agents):** If building a multi-agent implementation, use one orchestrator; A, B, C (and optional D) as parallel sub-agents; each produces its slot; aggregate **without synthesis**; add tension and reversibility labels. Combine, do not resolve.

---

## 5. How it differs from current "sell civ-mem" offers

| Current offer (sell-civ-mem) | STATE-evolved assistant brain |
|------------------------------|---------------------------------|
| One-off or periodic **briefs** (scenario prep, purpose-of-history report) | **Persistent** assistant available in the flow of work |
| Human-delivered or human-generated briefs | **Product**: software/service the head of state or staff queries; returns STATE-shaped output (options, perspectives, tensions) |
| Civ-mem as **content** (essays, frame) | Civ-mem as **one perspective** inside the assistant (optional); STATE as the **operating mode** of the assistant |
| Sale = delivery of briefs, access to corpus | Sale = **deployment** of the assistant brain (on-prem, secure cloud, or hybrid); subscription or license; optional integration with existing briefings/calendar |

So the evolution is: from **delivering STATE-like content** (briefs) to **delivering a STATE-shaped product** (an assistant that behaves like STATE: present, options, perspectives, tensions, relay-only).

---

## 6. Target buyer and deployment (federal)

- **Primary buyer (goal: federal contract):** Federal executive branch — White House, NSC, DPC, chief of staff, or equivalent (see [sell-civ-mem-federal-executive](sell-civ-mem-federal-executive.md) §3). The **user** may be the principal or a small circle of senior staff who run queries on behalf of the principal. Entry point: staff director, deputy, or senior advisor with budget for external advisory or tools.
- **Deployment:** Secure; on-prem or fed-approved cloud (e.g. FedRAMP, or agency-specific). Inputs (briefs, calendar, query) stay inside the government boundary. Optional integrations: calendar connector, briefing/doc source; authenticate once; no autonomous scraping. No training on government data without explicit contract and consent. Relay (if used) writes only to the agency’s own decision log or record system.
- **Other geographies:** The product design generalizes to other heads of state; the **contract goal** for this doc is US federal. Other countries are a later path if approved.

---

## 7. Federal contract path

**Goal:** Land a federal government contract to deploy the STATE-evolved assistant brain (pilot, then sustain).

| Element | Approach |
|--------|----------|
| **Vehicle** | (a) **GSA Schedule** if you or a partner are on schedule; (b) **BPA** under schedule or existing contract; (c) **Sole-source** if the capability is unique (STATE-shaped assistant: options not recommendation, tensions preserved, explicit relay only, duty of competence — distinct from typical decision-support tools); (d) **Subcontract** through a prime that holds a White House or agency contract (advisory, professional services, decision support). |
| **Capability statement** | Use [capability-statement-assistant-brain.md](capability-statement-assistant-brain.md). One page: STATE-evolved assistant brain, polyphonic cognition, fixed perspectives, relay-only, duty of competence; why unique; who for; past performance (fill as applicable). |
| **One-pager for the principal** | Use [one-pager-assistant-brain-cognitive-polyphony.md](one-pager-assistant-brain-cognitive-polyphony.md). "The executive branch has policy briefs and recommendations. It rarely has a **tool** that only surfaces options and perspectives and leaves the decision to you — no silent logging, no single 'answer.' We deploy an assistant brain that does exactly that: options, tensions preserved, you decide. Pilot: 90 days in one office." |
| **Pilot as contract** | Propose a **pilot contract**: deploy the assistant (or a minimal viable version) for 90 days in one office (e.g. NSC or DPC). Fixed fee. Deliverables: deployment, training on the **Polyphonic cognition protocol** (when to query, read A/B/C, relay only if "record"), and the one-page [cheat-sheet-polyphonic-cognition-protocol.md](cheat-sheet-polyphonic-cognition-protocol.md). Success = renewal or expansion. Reduces buyer risk and fits federal procurement (defined scope, fixed period). |
| **Compliance** | Advisory and decision-support only. No policy authority; no lobbying of appropriations or legislation unless separately cleared. The product does not recommend; it surfaces. Human approval for all outreach, pricing, and commitments. |

---

## 8. Roadmap (high level)

| Stage | Focus |
|-------|--------|
| **Concept and spec** | Lock the product spec (STATE-shaped behavior, relay-only, duty of competence, tensions preserved). Document; get principal/operator approval. |
| **Prototype** | Build a minimal version: user supplies a decision frame + optional context; system returns options through 2–3 perspectives, tensions preserved; no relay unless user says "save." Optional: one perspective is "civ-mem lens" (condition, seam, one subject many tongues). |
| **Pilot (federal contract)** | Land a **pilot contract** with one federal executive office (e.g. NSC, DPC, transition team). 90 days; fixed fee; deploy assistant, train users, measure usage and feedback ("options not recommendation," relay use, perspectives). Goal: prove value and convert to sustain/expansion. |
| **Productize** | Security (fed-approved or on-prem), deployment options, configurability (perspectives, corpus). Position as "assistant brain for the principal — STATE-shaped: options, perspectives, tensions preserved, you decide." |
| **Sustain** | Renew or expand after pilot; add offices or use cases under the same or new contract vehicle. |

---

## 9. Summary

**STATE** (civ-mem) = present moment, structured options, multiple perspectives, tensions preserved, no write to long-term record except by explicit relay. **Evolve it** into an **assistant brain** for the federal executive branch; **goal: federal government contract.** The product is a persistent assistant that ingests the present (what the user gives it), surfaces options through multiple perspectives, preserves tensions, never writes to the record unless the user explicitly relays, and optionally applies the civ-mem lens as one perspective. The principal remains sovereign; the assistant serves. Distinct from one-off briefs — it’s the STATE **operating mode** as a deployable product. **Target:** federal executive (NSC, DPC, chief of staff). **Contract path:** GSA/BPA/sole-source/subcontract; capability statement and one-pager; pilot (90 days, one office) as first contract; then sustain. Compliance: advisory only; no lobbying; human approval for all commitments.
