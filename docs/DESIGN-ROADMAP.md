# Design Roadmap — Product & Feature Design

**Purpose:** Capture design concepts and planned features beyond current implementation. Use for prioritization, scoping, and integration planning. For business strategy and monetization, see [Business Roadmap](BUSINESS-ROADMAP.md).

**Status:** Living document. Items are design-stage unless noted otherwise.

---

## 1. Grace-Mar Email Address

**Rationale:** A dedicated email for the fork enables:
- Clear separation of fork-linked accounts (YouTube, Khan, etc.) from family accounts
- OAuth identity clarity — which Google/SSO is "the fork's learning stack"
- Inbound and outbound content delivery (see below)

**Scope:** Optional. Parent creates/manages the address.

---

## 2. Outbound Curated Newsletter

**Concept:** Grace-Mar generates a periodic digest (e.g. weekly) and sends it to the fork's email.

**Content sources:**
- **IX-B Curiosity** — Topics and interests → 2–3 recommended links (YouTube, read-alouds, Khan)
- **LIBRARY** — Extensions of books: read-alouds, related videos, "if you liked X…"
- **SKILLS edge** — One "stretch" item per issue (e.g. longer read-aloud, slightly harder activity)

**Flow:** Build digest from Record → render as email → send to Grace-Mar address → parent triages; items can be approved for playlists or LIBRARY.

**Gating:** Everything proposed; parent decides what to surface or add.

---

## 3. Inbound Newsletter Processing

**Concept:** Subscribe the Grace-Mar email to trusted external newsletters. System ingests, matches to Record, stages candidates.

**Flow:**
1. **Subscribe** — Grace-Mar email receives newsletters from allowlisted sources (e.g. Khan Kids, Common Sense Media, Smithsonian for Kids, book/series newsletters)
2. **Ingest** — Cron polls inbox; fetches new messages; extracts links, titles, topics
3. **Match** — Score each item against IX-B, LIBRARY, SKILLS edge
4. **Stage** — Matches above threshold → PENDING-REVIEW: "Newsletter X recommended this on [topic]; matches curiosity in Y"
5. **Approve** — Parent approves → add to playlists, LIBRARY, or feed back into curiosity

**Principle:** Record filters input, not just drives output. External curators suggest; Record selects relevance. Still fully gated.

**Requirements:** Allowlist of trusted newsletters; unsubscribe path for any source no longer wanted; email parsing (IMAP or provider API).

---

## 4. Grace-Mar X (Twitter) Account

**Potential rationale:**
- **Identity separation** — Handle like `@grace_mar` distinguishes fork persona from family accounts
- **Inbound discovery** — Follow authors, museums, educators, book-related accounts; feed timeline content through matching logic (similar to inbound newsletters)
- **Export/presence** — If fork is shared (e.g. admissions link), a stable public handle could reinforce identity

**Higher-risk use:** Fork posts in its own voice (e.g. "I learned X today") — public, permanent; out of scope for current pilot.

**Design concerns:**
- **Public and permanent** — Unlike inbox, posts are visible and hard to fully retract
- **Platform dependency** — X policies and direction add long-term uncertainty

**Reasonable scope:** Private or low-visibility account used *only for following* — consume feed, match to Record, stage candidates, parent approves. Same pattern as inbound newsletters. *Posting* in fork's voice is out of scope.

---

## 5. OpenClaw Integration

**Rationale:** OpenClaw (personal AI assistant, runs on your machine, WhatsApp/Telegram/Discord/Signal/iMessage, persistent memory, skills/plugins, open source) can use the Grace-Mar Record as its identity layer. Session continuity spans both systems; OpenClaw artifacts can feed the grace-mar pipeline via "we did X."

**Scope:**
- **Record as identity** — Export SELF → USER.md / SOUL.md via `scripts/export_user_identity.py`. OpenClaw knows who it serves.
- **Session continuity** — Before starting, read SESSION-LOG, PENDING-REVIEW, last EVIDENCE entries. Close the cybernetic loop.
- **Artifacts as evidence** — OpenClaw outputs (writing, drawings, summaries) → user invokes "we did X" → pipeline stages → user approves.
- **Staging automation** — OpenClaw skill/cron may stage candidates to PENDING-REVIEW; **never** merge. User remains the gate.

**Workspace patterns:** grace-mar as subdir of OpenClaw, or sibling repos in shared workspace.

**Chinese app integrations (future):** WeChat Official Account, WeCom (openclaw-plugin-wecom), personal WeChat (openclaw-wechat), DingTalk (dingtalk-openclaw-connector). Record as identity could serve these channels; same gating rules apply.

**See:** [OPENCLAW-INTEGRATION](OPENCLAW-INTEGRATION.md) for full guide.

---

## 6. Canva Integration

**Rationale:** Canva's APIs (Connect API, App SDK) enable design integration — templates, asset sync, automated creation. Grace-Mar could use Canva for IMAGINE evidence (designs as creation log), newsletter layout (outbound digest → Canva template), or shareable content (JOURNAL, admissions portfolio).

**Scope:**
- **Designs as evidence** — User creates in Canva → export → "we designed X" → pipeline stages → EVIDENCE
- **Template population** — IX-B, LIBRARY, or JOURNAL highlights → insert into Canva template → parent-approved output
- **Newsletter layout** — Outbound digest rendered via Canva for visual polish

**APIs:** Connect API (workflow integration, asset sync), App SDK (content import, design automation). Admin/SCIM for org management if needed.

**See:** [CANVA-INTEGRATION](CANVA-INTEGRATION.md) for API overview and use cases.

---

## 7. Dependencies

| Feature | Depends on |
|---------|------------|
| Grace-Mar email | Parent decision; no technical blocker |
| Outbound newsletter | Record query APIs; email send; playlist/recommendation logic (see YOUTUBE-PLAYLIST-DESIGN) |
| Inbound processing | Grace-Mar email; IMAP or Gmail API; matching logic; PENDING-REVIEW staging |
| X account (follow-only) | X API; matching logic; PENDING-REVIEW staging; parent manages account |
| OpenClaw integration | OpenClaw workspace; export script; OPENCLAW-INTEGRATION workflow |
| Canva integration | Canva developer account; Connect API or App SDK; template design |

---

## 8. Related Docs

| Document | Relevance |
|----------|-----------|
| [BUSINESS-ROADMAP](BUSINESS-ROADMAP.md) | Strategy, monetization, go-to-market |
| [YOUTUBE-PLAYLIST-DESIGN](YOUTUBE-PLAYLIST-DESIGN.md) | Playlist building; watched-video detection; feeds into newsletter content |
| [OPENCLAW-INTEGRATION](OPENCLAW-INTEGRATION.md) | Record as identity; session continuity; staging automation; Chinese apps |
| [CANVA-INTEGRATION](CANVA-INTEGRATION.md) | Design APIs; IMAGINE evidence; newsletter layout; template population |
| [ARCHITECTURE](ARCHITECTURE.md) | Pipeline, Record structure, gating |
| [INTEGRATION-APIS](INTEGRATION-APIS.md) | Multi-API context for email + YouTube + others |

---

*Document version: 1.0*
*Last updated: February 2026*
