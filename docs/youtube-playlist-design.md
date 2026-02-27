# YouTube Playlist Design — Grace-Mar × YouTube API

**Purpose:** Design methods for building YouTube playlists from the Grace-Mar Record, aligning media consumption with learner goals and curiosity. Appeals to educators and parents who want recommendations that follow the child's interests and learning targets, not just generic "for kids" content.

**Status:** Design spec. Not yet implemented.

**See also:** [ARCHITECTURE](architecture.md), [LIBRARY](architecture.md#library), [integration-apis](integration-apis.md) (if created).

---

## Value Proposition

**For parents:** "Recommendations that follow your child's curiosity and goals — not just their last click."

**For educators:** "Feed the Record; get playlists you can drop into lessons or send home. Media that supports learning targets."

The Record (SELF, SKILLS, IX-A/B) already captures goals and curiosity. This design turns that into actionable video suggestions — pre-filtered, staged for approval, aligned with what the fork knows.

---

## 1. Input Sources (What Grace-Mar Provides)

| Source | Section | Use in playlist building |
|--------|---------|--------------------------|
| **IX-B. Curiosity** | Topics, interests (CUR-*) | Primary driver — search for videos on these topics |
| **IX-A. Knowledge** | Already-learned facts (LEARN-*) | Avoid pure repetition; allow "next level" depth |
| **II. Preferences** | Favorites (movies, books) | Related content — e.g. Madeline → read-alouds |
| **LIBRARY** | Book titles, topics | Videos that extend reading (read-alouds, summaries) |
| **SKILLS THINK edge** | "Longer text, inference, retelling" | Suggest content at the edge of capability |
| **lexile_output** | 600L | Age-appropriateness heuristic |
| **EVIDENCE** | Recent WRITE/CREATE topics | Follow-up content on same themes |

---

## 2. Core Methods

### 2.1 `build_curiosity_playlist(topics: list[str], max_videos: int = 10) -> list[VideoCandidate]`

Builds a playlist from IX-B curiosity topics.

**Logic:**
1. Extract topics from IX-B (and optionally IX-A for "next level").
2. For each topic, generate search phrases via `topics_to_search_queries()`.
3. Call YouTube Data API `search.list` with `type=video`, `safeSearch=strict`, `videoDuration=short|medium`.
4. Filter by channel reputation, view count, recency.
5. Deduplicate; return top `max_videos` with provenance.

---

### 2.2 `build_library_extension_playlist() -> list[VideoCandidate]`

Videos that extend the LIBRARY (books already known).

**Logic:**
1. Read LIBRARY entries (titles, topics).
2. Query: `"{title} read aloud"`, `"{title} for kids"`, `"{topic} educational"`.
3. Search with `videoCategoryId=27` (Education) when relevant.
4. Score by relevance; return ordered by LIBRARY entry.

---

### 2.3 `build_edge_playlist(skill_module: str) -> list[VideoCandidate]`

Content at the SKILLS edge — stretches capability.

**Logic:**
1. Read `edge` for module (e.g. THINK: "Longer text, inference, retelling").
2. Map edge phrases → search terms: "read aloud chapter book", "reading comprehension for kids".
3. Optionally intersect with IX-B topics.
4. Search; filter; return.

---

### 2.4 `build_project_playlist(evidence_ids: list[str]) -> list[VideoCandidate]`

Videos supporting a specific project from EVIDENCE.

**Logic:**
1. Resolve EVIDENCE entries (CREATE-*, WRITE-*); extract topics.
2. Search per topic; prefer "how to", "tutorial", "explainer".
3. Return ordered by project → topic → relevance.

---

### 2.5 `build_mixed_playlist(strategy: str, max_videos: int = 15) -> list[VideoCandidate]`

Combines strategies into one playlist.

**Strategies:**
- `curiosity_heavy` — 70% curiosity, 30% library
- `balance` — 1/3 curiosity, 1/3 library, 1/3 edge
- `project` — project-only
- `discovery` — more "next level", less repetition

**Logic:**
1. Call base methods; merge results.
2. Apply diversity (cap per channel, topic).
3. Rank by weighted score; return top `max_videos`.

---

## 3. Query Generation

### 3.1 `topics_to_search_queries(topics: list[str], context: str) -> list[str]`

Maps Record topics to YouTube search queries.

**Examples:**
- `"Ancient Egypt"` → `["Ancient Egypt for kids", "Egypt pharaohs educational"]`
- `"Reptiles"` → `["Reptiles for kids", "Snakes lizards educational"]`
- `"The Nutcracker"` → `["Nutcracker ballet for kids", "Nutcracker story"]`

**Context:** `learning` (append " for kids", " educational"); `books` (append " read aloud", " story").

---

### 3.2 `apply_lexile_filter(candidates: list[VideoCandidate], lexile: str) -> list[VideoCandidate]`

Heuristic age-appropriateness. Options:
- Filter by `videoCategoryId=27`, `contentRating`, channel type
- Exclude advanced keywords in title/description
- Prefer `videoDuration=short|medium` for younger learners

---

## 4. YouTube API Usage

| Endpoint | Use |
|----------|-----|
| `search.list` | Query → video IDs, titles, channels |
| `videos.list` | Enrich: duration, category, contentRating |
| `playlists.insert` | Create playlist (if user has OAuth) |
| `playlistItems.insert` | Add videos to playlist |

**Flow:**
1. `search.list` with `q`, `type=video`, `safeSearch=strict`, `videoDuration`, `relevanceLanguage`
2. `videos.list` for duration, category, rating
3. Filter; rank; build `VideoCandidate` list
4. Store as "virtual" playlist (list of IDs) or create via API if OAuth available

---

## 5. Data Structures

```python
@dataclass
class VideoCandidate:
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    duration_seconds: int
    topic: str
    reason: str  # "curiosity", "library", "edge", "project"
    search_query: str
    relevance_score: float

@dataclass
class PlaylistSpec:
    name: str
    strategy: str
    source_topics: list[str]
    videos: list[VideoCandidate]
    created_at: str
    status: str  # "proposed", "approved", "rejected"
```

---

## 6. Pipeline Integration (Gated)

Playlists are **suggestions** until approved. No auto-merge.

1. Build playlist → `PlaylistSpec` with `status="proposed"`
2. Stage to `PENDING-PLAYLISTS.md` (or equivalent)
3. User reviews; approves or rejects
4. On approve: create playlist (if OAuth), add to LIBRARY or video-playlist index, log in EVIDENCE

Optional: "We watched this playlist" → stage THINK evidence from playlist topics.

---

## 7. Watched Video Detection (History Polling)

**Scope:** Record only videos that Grace-Mar recommended and that appear in the user's watch history. No full history sync; no videos we didn't suggest.

**Flow:**
1. **OAuth** — Parent connects YouTube account (one-time; `youtube.readonly` scope).
2. **Poll** — Cron (e.g. daily) fetches watch history via `playlists.list` for playlist ID `HL` (History) or equivalent endpoint.
3. **Filter** — Keep only video IDs that match Grace-Mar's recommended playlists (compare against `PlaylistSpec.videos` for approved playlists).
4. **Diff** — Compare polled history to `RECOMMENDED-WATCHED.jsonl` (or similar) to find *new* watches.
5. **Stage** — For each new watched recommended video, create candidate → append to RECURSION-GATE or PENDING-VIDEOS.
6. **Approve** — User reviews; approved → add to LIBRARY videos section, log in EVIDENCE.

**Store recommended IDs:** When a playlist is approved, persist `video_id` list to `RECOMMENDED-VIDEO-IDS.json` (or in PlaylistSpec). Poll uses this as the allowlist.

**Store last-seen:** After each poll, persist last-seen history snapshot or "highest timestamp" so next poll only processes new entries.

**Manual fallback:** User can still report "we watched it" (chat, button) for any recommended video; same staging flow.

---

## 8. Constraints

- **SafeSearch:** Always `strict`
- **Kids content:** Prefer Education category, kid-friendly channels
- **COPPA:** Parent OAuth; only recommended videos recorded; no full history sync
- **Knowledge boundary:** Only topics from Record; no LLM inference of interests
- **Rate limits:** Cache searches; batch API calls; poll history at most daily

---

## 9. Implementation Order

1. `topics_to_search_queries` + `build_curiosity_playlist`
2. `build_library_extension_playlist`
3. Filtering (`apply_lexile_filter`, duration, category)
4. `build_mixed_playlist`
5. `build_edge_playlist`, `build_project_playlist`
6. PENDING-PLAYLISTS staging + approval flow
7. OAuth + history poll + watched-video staging (optional)

---

*Document version: 1.0*
*Last updated: February 2026*
