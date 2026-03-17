# Positioning: Personality with Provenance (Coaches & Creators)

**Purpose:** Define the segment, value proposition, and go-to-market slice for **coaches, creator-educators, and small teams** who want a portable, evidence-backed profile of a person's interests, style, and growth. Same Grace-Mar stack; different ICP and messaging.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md). Source: [Market Research — Idea #3](market-research-commercial-ideas.md).

---

## 1. Segment (ICP)

| Who | Pain | Why us |
|-----|------|--------|
| **Coaches** (executive, life, career) | Client context scattered across notes, tools, sessions; handoffs and continuity break; no single "this is what we've documented about this person" that travels. | One Record per client (or per coachee): interests, style, growth signals — all **approved by the person**. Export for handoffs, supervision, or downstream tools. |
| **Creator-educators** (course creators, cohort leads, community builders) | Audience or participant "profile" is inferred from behavior or one-off forms; no durable, updatable identity that the *person* controls and can share. | Record = participant-owned profile; creator gets export (with consent) for personalization, or person brings their Record to the next cohort. |
| **Small teams** (pods, studios, advisory) | Shared context about a person (client, partner, member) lives in Slack/Notion/heads; no canonical "who they are" with provenance. | Single evidence-grounded profile; team reads (or person shares) Record; nothing enters without the person's approval. |

**Not:** A replacement for coaching software, LMS, or CRM. We are the **profile substrate** — the identity layer that other tools can consume.

---

## 2. Value proposition (one line)

**"Your documented interests, style, and growth — owned by you, approved by you, portable to any tool or handoff."**

Or:

**"Personality with provenance: every claim in the profile traces to something you approved. No inference; no platform override."**

---

## 3. Differentiation (vs. inferred personality)

| Inferred (typical) | Personality with provenance (us) |
|--------------------|----------------------------------|
| Platform derives interests/style from behavior, clicks, or AI | Person (or operator) approves every addition to the Record |
| Locked inside one product | Portable: export, API, PRP — take it to the next coach, tool, or cohort |
| No audit trail for "why we think this" | Full trail: evidence_id, recursion-gate, pipeline-events |
| Often child/minor or B2C only | Age-neutral; works for adults, coachees, creators, teams |

---

## 4. Use cases (concrete)

- **Coach → coach handoff:** Outgoing coach exports a summary (or PRP) of the coachee's documented interests and growth areas; incoming coach gets a trusted starting point; coachee stays in control.
- **Cohort / community:** Participants build a Record over the program; at the end they keep it and can share (e.g. with next program or employer); facilitator gets aggregate insights from consented exports.
- **Creator personalization:** Course or community member links their Record (read-only or scoped export); content or recommendations can use "documented interests" instead of inferred ones.
- **Team context:** One shared "client Record" or "member Record" that only updates when the person (or delegated operator) approves; no more conflicting notes.

---

## 5. Product fit (no pipeline change)

- **Same pipeline:** Signal detection → stage in recursion-gate → human approval → merge. No new merge path.
- **Same schema:** SELF (IX-A knowledge, IX-B curiosity, IX-C personality), EVIDENCE, skills. Optional: lighter onboarding (e.g. emphasize IX-B/IX-C for "style and interests").
- **Export:** PRP, JSON, Obsidian, or API — already in place or on roadmap. Add **segment-specific export** (e.g. "coach handoff pack": one-pager + structured JSON of interests and style).
- **Hosted / white-label:** Same hosted family product pattern; positioning and onboarding tailored to coaches/creators. Optional: "Record for teams" (multiple Records under one org).

---

## 6. Messaging (landing / one-pager)

**Headline:** Personality with provenance.

**Subhead:** A portable, evidence-backed profile of interests, style, and growth. You approve everything that goes in. You own the Record. Export it to any handoff or tool.

**Bullets:**
- **You gate, we store.** Nothing enters your profile without your explicit approval. No inferred personality; no platform override.
- **One Record, many uses.** Hand off to the next coach. Share with a cohort. Feed your favorite tools. Export as PRP, JSON, or API.
- **Audit trail built in.** Every claim links to evidence. Full history. Sovereign merge rule: only you (or your delegated operator) can merge.

**CTA:** Get early access · See the schema · Use open-source

**Audience line:** For coaches, creator-educators, and teams who need a single source of truth about a person — owned by that person.

---

## 7. Next steps (minimal)

| Step | Owner | Outcome |
|------|--------|---------|
| Add "Coach / creator" row to [Business Roadmap](business-roadmap.md) monetization table | Doc | Segment visible in strategy |
| Create landing page (or /coaches page on grace-mar.com / companion-self.com) using §6 copy | Marketing / dev | Lead capture or waitlist |
| **Done:** Coach handoff pack | Eng | `python scripts/export_fork.py --format coach-handoff -o coach-handoff-{user}` produces JSON + one-pager (.md) |
| Optional: One segment-specific onboarding flow (e.g. "Record for professional growth" vs "Record for my child") | Product | Clearer first-run for coaches |

No change to pipeline semantics or GRACE-MAR-CORE.
