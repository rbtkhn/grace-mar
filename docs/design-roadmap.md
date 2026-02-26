# Design Roadmap — Product & Feature Design

**Purpose:** Capture design concepts and planned features beyond current implementation. Use for prioritization, scoping, and integration planning. For business strategy and monetization, see [Business Roadmap](business-roadmap.md).

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

**Flow:** Build digest from Record → render as email → send to Grace-Mar address → operator triages; items can be approved for playlists or LIBRARY.

**Gating:** Everything proposed; operator (or user) decides what to surface or add.

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

**Reasonable scope:** Private or low-visibility account used *only for following* — consume feed, match to Record, stage candidates, Mind approves. Same pattern as inbound newsletters. *Posting* in fork's voice is out of scope.

**See:** [x-integration.md](x-integration.md) for X API v2 mapping, integration patterns (feed consumer vs DM vs posting), tricameral alignment, and technical placement.

---

## 5. OpenClaw Integration

**Rationale:** OpenClaw (personal AI assistant, runs on your machine, WhatsApp/Telegram/Discord/Signal/iMessage, persistent memory, skills/plugins, open source) can use the Grace-Mar Record as its identity layer. Session continuity spans both systems; OpenClaw artifacts can feed the grace-mar pipeline via "we did X."

**Scope:**
- **Record as identity** — Export SELF → user.md / SOUL.md via `scripts/export_user_identity.py`. OpenClaw knows who it serves.
- **Session continuity** — Before starting, read SESSION-LOG, PENDING-REVIEW, last EVIDENCE entries. Close the cybernetic loop.
- **Artifacts as evidence** — OpenClaw outputs (writing, drawings, summaries) → user invokes "we did X" → pipeline stages → user approves.
- **Staging automation** — OpenClaw skill/cron may stage candidates to PENDING-REVIEW; **never** merge. User remains the gate.

**Workspace patterns:** grace-mar as subdir of OpenClaw, or sibling repos in shared workspace.

**Chinese app integrations (future):** WeChat Official Account, WeCom (openclaw-plugin-wecom), personal WeChat (openclaw-wechat), DingTalk (dingtalk-openclaw-connector). Record as identity could serve these channels; same gating rules apply.

**See:** [OPENCLAW-INTEGRATION](openclaw-integration.md) for full guide.

---

## 6. Intersignal / The Braid Integration

**Rationale:** Intersignal (The Braid, Mesh Cache, Familiar nodes) builds local/offline multi-AI protocol with traceable identity. Grace-Mar provides the **identity substrate** Familiar nodes need: consent-bound, evidence-grounded, user-approved.

**Scope:**
- **Record as identity source** — Export SELF → `symbolic_identity.json` via `scripts/export_symbolic.py` (cache-oriented, Familiar-ready).
- **Session continuity** — Intersignal reads SESSION-LOG, PENDING-REVIEW, EVIDENCE before startup.
- **Staging contract** — Braid agents may stage to PENDING-REVIEW; **never** merge. User remains the gate.
- **Cache-level symbolic sharing** — Structured primitives (interests, IX-A/B/C summaries, evidence anchors, checksum) for Mesh Cache.

**Workspace patterns:** grace-mar as sibling to Intersignal mesh; export to `../intersignal-mesh/identity/`.

**Export:**
```bash
python integrations/export_hook.py --target intersignal -u grace-mar -o ../intersignal-mesh/
```

**See:** [INTERSIGNAL-INTEGRATION](intersignal-integration.md) for full guide.

---

## 7. Canva Integration

**Rationale:** Canva's APIs (Connect API, App SDK) enable design integration — templates, asset sync, automated creation. Grace-Mar could use Canva for WORK creation evidence (designs as creation log), newsletter layout (outbound digest → Canva template), or shareable content (JOURNAL, admissions portfolio).

**Scope:**
- **Designs as evidence** — User creates in Canva → export → "we designed X" → pipeline stages → EVIDENCE
- **Template population** — IX-B, LIBRARY, or JOURNAL highlights → insert into Canva template → operator-approved output
- **Newsletter layout** — Outbound digest rendered via Canva for visual polish

**APIs:** Connect API (workflow integration, asset sync), App SDK (content import, design automation). Admin/SCIM for org management if needed.

**See:** [CANVA-INTEGRATION](canva-integration.md) for API overview and use cases.

---

## 8. Journal ML — Attestation and Coherence

**Rationale:** A year (or more) of first-person journal entries forms a longitudinal corpus of the fork's linguistic fingerprint. ML over that corpus supports **attestation and coherence** — demonstrating that the fork's voice remained consistent over time, with no drift or contamination.

**Scope:**
- **Voice model / fine-tuning** — Fine-tune a small model on journal prose to capture vocabulary, syntax, and tone. That model could draft candidate journal entries, suggest completions for partial sentences, or extend her voice to new topics while staying in-character.
- **Linguistic fingerprint audit** — Quantify the fork's stylometric profile; detect drift from her documented voice, consistency of tone and style over time, misalignment with the Lexile ceiling or documented linguistic style.
- **Coherence analysis** — Stylometric profiling across entries; flag entries that diverge from the fork's typical voice.
- **Attestation** — Report or artifact: "Voice remained coherent over [period]." Useful for governance, admissions, or transfer.
- **Drift detection** — Alert when new entries deviate from the established fingerprint; supports curation quality.
- **Portable voice profile** — Produce a compact, ML-based representation of her linguistic fingerprint for Intersignal Familiar nodes, tutoring apps, or other platforms that need "her voice" without full Record access.

**Data:** JOURNAL entries (first-person prose, human-approved). Requires sufficient volume (e.g. 6–12 months) for statistical validity.

**See:** [JOURNAL-SCHEMA](journal-schema.md) for entry format and linguistic fingerprint role.

---

## 9. Homeschool / Adaptive Curriculum Integration

**Rationale:** Grace-Mar's Voice teaches and tutors. External curriculum systems (homeschool bots, adaptive platforms like Khan, IXL, custom Glide/Zapier stacks) can use the Record as the **identity layer** to personalize lessons and activities. The Record tells the curriculum engine: what the student knows (IX-A), what they're curious about (IX-B), their skills edge (SKILLS), and their Lexile level.

**Scope:**
- **Record as identity source** — Export a curriculum-oriented view: IX-B (curiosity), SKILLS edge, Lexile, knowledge gaps. Use `scripts/export_engagement_profile.py -u [id]` for a motivation/engagement slice (interests, curiosity_topics, personality_snippets, talent_stack) in JSON or `--md` for markdown. Curriculum engines read this to tailor content.
- **Activity/lesson personalization** — "She's curious about reptiles and gemstones" → suggest crystal formation lab. "She just learned Jupiter's Red Spot" → extend with storm systems.
- **Grace-Mar Voice does tutoring** — Core tutoring happens in Grace-Mar. Curriculum systems can *supplement* (deliver structured lessons, labs, activities) while Grace-Mar answers questions and explains in-character.
- **Evidence loop** — Curriculum outputs (writing, photos, completion) flow back via "we did X" → pipeline stages → user approves → EVIDENCE, SELF.
- **Access needs** — Curriculum export includes `access_needs` (explanation level, dyslexia-friendly font, read speed) for assistive tools (e.g. World Pen Scan).
- **Assistive tools as signal source** — Reading pens, speech-to-text: vocabulary lookups and "tell me more" curiosity can flow into pipeline as IX-A/IX-B candidates.

**Workspace patterns:** Grace-Mar as sibling to curriculum stack; export `symbolic_identity.json` or a curriculum-specific schema; curriculum engine queries on schedule or at lesson generation.

**See:** [ADAPTIVE-CURRICULUM-INTEGRATION](adaptive-curriculum-integration.md) for full guide.

---

## 10. Learning Path from Record

**Rationale:** Curriculum platforms (SparkPath, Khan, homeschool stacks) use "learning paths" — sequences of lessons. Grace-Mar's Record can *drive* those paths: IX-B (curiosity) + SKILLS edge suggest what to assign next.

**Scope:**
- **Path generation** — Given `curriculum_profile.json`, generate a suggested sequence: "Curious about reptiles, WRITE edge for narrative → reptile fact sheet (read) → short story prompt (write)." Curriculum engine maps suggestions to its lesson library.
- **Skills-aware sequencing** — READ edge + curiosity topic → suggest text. WRITE edge + topic → suggest writing prompt. WORK (creation) edge → suggest creative task.
- **Knowledge-avoidance** — IX-A (knowledge) filters out already-learned content; path builds on gaps and stretches at the edge.

**Output:** Suggested path (lesson IDs or descriptors) that a curriculum platform consumes. Grace-Mar does not hold lessons; it holds the identity that *selects* them.

**See:** [ADAPTIVE-CURRICULUM-INTEGRATION](adaptive-curriculum-integration.md) for Record-as-identity pattern.

---

## 11. Dependencies

| Feature | Depends on |
|---------|------------|
| Grace-Mar email | Parent decision; no technical blocker |
| Outbound newsletter | Record query APIs; email send; playlist/recommendation logic (see YOUTUBE-PLAYLIST-DESIGN) |
| Inbound processing | Grace-Mar email; IMAP or Gmail API; matching logic; PENDING-REVIEW staging |
| X account (follow-only) | X API; matching logic; PENDING-REVIEW staging; operator manages account |
| OpenClaw integration | OpenClaw workspace; export script; OPENCLAW-INTEGRATION workflow |
| Intersignal / Braid integration | export_hook --target intersignal; INTERSIGNAL-INTEGRATION guide |
| Canva integration | Canva developer account; Connect API or App SDK; template design |
| Journal ML (attestation) | 6–12+ months of journal entries; stylometric/ML tooling |
| Adaptive curriculum integration | export_curriculum; curriculum engine (SparkPath, Glide, Zapier, custom) |
| Learning path from Record | curriculum_profile.json; path-generation logic (could be script or external) |

---

## 12. Related Docs

| Document | Relevance |
|----------|-----------|
| [BUSINESS-ROADMAP](business-roadmap.md) | Strategy, monetization, go-to-market |
| [YOUTUBE-PLAYLIST-DESIGN](youtube-playlist-design.md) | Playlist building; watched-video detection; feeds into newsletter content |
| [OPENCLAW-INTEGRATION](openclaw-integration.md) | Record as identity; session continuity; staging automation; Chinese apps |
| [INTERSIGNAL-INTEGRATION](intersignal-integration.md) | Symbolic export; Familiar nodes; Mesh Cache; The Braid |
| [CANVA-INTEGRATION](canva-integration.md) | Design APIs; WORK creation evidence; newsletter layout; template population |
| [JOURNAL-SCHEMA](journal-schema.md) | Entry format; linguistic fingerprint; attestation data source |
| [ADAPTIVE-CURRICULUM-INTEGRATION](adaptive-curriculum-integration.md) | Record as identity for curriculum engines; homeschool bots |
| [ARCHITECTURE](architecture.md) | Pipeline, Record structure, gating |
| [integration-apis](integration-apis.md) | Multi-API context for email + YouTube + others |

---

*Document version: 1.0*
*Last updated: February 2026*
