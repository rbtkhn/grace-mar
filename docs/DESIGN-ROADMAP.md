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

## 5. Dependencies

| Feature | Depends on |
|---------|------------|
| Grace-Mar email | Parent decision; no technical blocker |
| Outbound newsletter | Record query APIs; email send; playlist/recommendation logic (see YOUTUBE-PLAYLIST-DESIGN) |
| Inbound processing | Grace-Mar email; IMAP or Gmail API; matching logic; PENDING-REVIEW staging |
| X account (follow-only) | X API; matching logic; PENDING-REVIEW staging; parent manages account |

---

## 6. Related Docs

| Document | Relevance |
|----------|-----------|
| [BUSINESS-ROADMAP](BUSINESS-ROADMAP.md) | Strategy, monetization, go-to-market |
| [YOUTUBE-PLAYLIST-DESIGN](YOUTUBE-PLAYLIST-DESIGN.md) | Playlist building; watched-video detection; feeds into newsletter content |
| [ARCHITECTURE](ARCHITECTURE.md) | Pipeline, Record structure, gating |
| [INTEGRATION-APIS](INTEGRATION-APIS.md) | Multi-API context for email + YouTube + others |

---

*Document version: 1.0*
*Last updated: February 2026*
