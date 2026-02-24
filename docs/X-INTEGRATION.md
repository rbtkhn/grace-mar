# X.com (Twitter) API — Integration Options

**Purpose:** Outline how X.com API could integrate with Grace-Mar. Builds on [Design Roadmap §4 (Grace-Mar X Account)](DESIGN-ROADMAP.md#4-grace-mar-x-twitter-account).

**Status:** Design-stage. No implementation yet.

---

## 1. Existing design scope (Design Roadmap §4)

- **Identity separation** — Handle (e.g. `@grace_mar`) distinguishes fork persona from family accounts.
- **Inbound discovery** — Follow authors, museums, educators, book-related accounts; feed timeline (or lists/bookmarks) through matching logic; stage candidates; Mind approves. Same pattern as inbound newsletters.
- **Out of scope for current pilot** — Fork posting in its own voice (public, permanent). *Posting* in Voice is higher-risk and deferred.
- **Reasonable first step** — Private or low-visibility account used *only for following*: consume feed → match to Record → stage → approve. No Voice-on-X.

---

## 2. X API v2 fit

| API area | Relevance to Grace-Mar | Notes |
|----------|------------------------|--------|
| **Read: timeline, list timeline, bookmarks** | Feed consumption for match → stage | Free tier: 100 reads/month; Basic: 10k reads/month. Sufficient for "follow list + match to IX-B/LIBRARY" at low volume. |
| **Read: user lookup, follows** | Resolve followed accounts, filter by list | Needed to know *what* to pull into the feed. |
| **Read: search / filtered stream** | Optional: keyword or topic filters | Pro tier+. Not required for MVP. |
| **Read: DMs** | Optional: X as observation window (like Telegram) | Would require DM as input channel; same pipeline as Telegram/WeChat (get_response, archive, analyst). Higher complexity and ToS/age considerations. |
| **Write: post, reply, DM** | Voice posting, or Mind posting with Record context | **Deferred.** Public posts are permanent and platform-dependent; conflicts with "Voice speaks only when queried" if automated. |
| **Write: like, bookmark** | Save items for later matching | Could support "bookmark → stage" flow without posting. |

**Tricameral alignment:**

- **MIND** — Decides what to follow, what to approve from staged X-sourced candidates; can post *as themselves* from a linked account if desired (out of scope for automation).
- **RECORD** — Enriched by approved X-sourced candidates (e.g. new curiosity, links) via existing gated pipeline. No direct X write from Record.
- **VOICE** — Does not post on X in current design. Voice remains query-triggered (Telegram, WeChat, Mini App, etc.). X is an *input* to the pipeline, not an output channel for the Voice.

So: **X as read-only feed into the Record (gated), not as a Voice channel.**

---

## 3. Integration patterns

### A. Feed consumer (recommended first)

1. **Auth** — OAuth 2.0 user context (or app-only for a single "Grace-Mar" account). Store token per user or per pilot.
2. **Pull** — Periodically (cron) or on-demand: fetch home timeline, or list timeline, or bookmarks (depending on product choice). Stay within rate limits (Free: 100 reads/month; Basic: 10k).
3. **Match** — Score items against Record: IX-B (curiosity), LIBRARY, SKILLS edge. Same style as inbound newsletter matching (Design Roadmap §3).
4. **Stage** — Matches above threshold → PENDING-REVIEW with provenance (e.g. "X: @author, link, excerpt"). Use existing staging path (e.g. `/stage` or script analogous to `openclaw_stage.py`).
5. **Approve** — Mind approves in existing pipeline; merge into Record/LIBRARY/playlists as today.

**Channel key:** e.g. `x:feed` or `x:{user_id}` for archive and pipeline events. Exchanges are "system → stage," not conversational; no `get_response` in the loop.

**New pieces:** X API client (read-only), match logic (reuse or extend newsletter matcher), staging script or `/stage` payload with `source=x_feed`.

### B. X as observation window (conversation)

- **Concept** — User DMs with a Grace-Mar-linked account; bot responds in Voice (like Telegram). Same core: `get_response`, archive, analyst, pipeline.
- **Complexity** — DM API, webhook or polling, token lifecycle, and X's developer/ToS constraints. Age and compliance (e.g. 13+ for X) must be explicit.
- **Priority** — Lower than feed consumer. Only consider if Telegram/WeChat/Mini App are insufficient and X DM is a hard requirement.

### C. Voice posting on X (deferred)

- **Risks** — Public, permanent, platform-dependent; "Voice speaks only when queried" is violated if the system *posts* without explicit user request per post. Automation could blur Mind vs Voice.
- **If ever in scope** — Treat as "Mind approves each post" or "Mind drafts, system posts once approved." No autonomous Voice-on-X.

---

## 4. Technical placement

| Piece | Where it lives | Notes |
|-------|----------------|-------|
| X API client (read) | New: `integrations/x_feed.py` or `bot/x_client.py` | OAuth or app-only; read timeline/list/bookmarks only. |
| Match to Record | New script or extend newsletter matcher | Input: raw tweets/post objects; output: scored list → stage. |
| Staging | Existing `/stage` or new `integrations/x_stage.py` | Same contract as OpenClaw: stage-only, never merge. `channel_key` e.g. `x:feed`. |
| Pipeline events | Existing `emit_pipeline_event` | e.g. `x_feed:pull`, `staged` with `source=x_feed`. |
| Archive | SELF-ARCHIVE | Single sink for approved activity (voice and non-voice). Today: Telegram, WeChat, Mini App. When X DM or email (or other channels) are added, they append to the same SELF-ARCHIVE with channel label (e.g. X, Email). Feed-only pulls may be logged with `x:feed` for audit. |
| Config | `users/[id]/` or repo env | X credentials, follow list or list ID, poll interval. |

No change to `bot/core.py` for feed-only: no X channel in `get_response`. Only if we add X DM as a conversation channel would we add an X entry point that calls `get_response` and archive.

---

## 5. Risks and constraints

| Risk | Mitigation |
|------|-------------|
| **Age** | X ToS typically 13+. Pilot may be under 13; account would be operator/family, not child. No child PII in X; use only for feed consumption and staging. |
| **Platform dependency** | X policy and pricing can change. Prefer thin integration: read → stage; no lock-in of Record content into X-native formats. |
| **Public posting** | Do not implement Voice-on-X in pilot. If posting at all, explicit "Mind posts" flow only. |
| **Rate limits** | Free tier 100 reads/month is tight. Basic ($200/mo) for any real feed volume. Design for "batch pull → match → stage" once per day or per N hours. |
| **Data handling** | Tweets/post content in PENDING-REVIEW and pipeline events. Retain only what's needed for matching and provenance; document in privacy/DPA if needed. |

---

## 6. Recommendation

1. **Implement feed consumer only** — Follow/list or bookmarks → match to Record (IX-B, LIBRARY) → stage to PENDING-REVIEW → Mind approves. Aligns with Design Roadmap §4 and tricameral mind (X feeds RECORD, gated by MIND; VOICE not on X).
2. **Reuse patterns** — Staging like OpenClaw (stage-only script or `/stage`), existing pipeline and merge flow, `channel_key` for X.
3. **Defer** — X as conversational channel (DM), Voice posting, and any write path until there is a clear product need and compliance path.
4. **Document** — Add "X feed" to DESIGN-ROADMAP §4 and any integration table (e.g. OPENCLAW-INTEGRATION style) once we add an implementation ticket.

---

## 7. References

- [Design Roadmap §4 — Grace-Mar X (Twitter) Account](DESIGN-ROADMAP.md#4-grace-mar-x-twitter-account)
- [Design Roadmap §3 — Inbound Newsletter Processing](DESIGN-ROADMAP.md#3-inbound-newsletter-processing) (same match → stage pattern)
- [OpenClaw Integration](OPENCLAW-INTEGRATION.md) (staging contract, stage-only, channel_key)
- X API: [developer.x.com](https://developer.x.com/en/docs/x-api) (v2, tiers, read/write endpoints)
