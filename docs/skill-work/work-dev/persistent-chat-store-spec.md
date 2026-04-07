# Persistent Chat Store — Design Spec

**Status:** Implementing  
**Inspired by:** [openbrain-telegram-capture](https://github.com/rafaelmocelin/openbrain-telegram-capture) two-table pattern (Supabase), adapted to SQLite for grace-mar's file-based architecture.

---

## Problem

`conversations` in `bot/core.py` is an in-memory `defaultdict(list)`. Every restart wipes conversation history. The bot returns with no context beyond `self-memory.md` (manually curated) and the inlined Record in the system prompt. Older conversation turns (beyond the 20-turn window) are permanently lost to the LLM — they exist only in the append-only `session-transcript.md` which is never read back for context.

## Solution

SQLite-backed persistence with two tables and lazy auto-compaction.

### Two-table schema

| Table | Purpose |
|-------|---------|
| `chat_messages` | Raw conversation turns: channel_key, role, content, created_at |
| `chat_summaries` | Rolling compressed summary per channel: channel_key, summary, covers_through, updated_at |

**Rationale:** Separating raw turns from summaries keeps queries simple. Recent turns are loaded raw (high fidelity). Older turns are compressed into a rolling summary (bounded token cost). This is the same split OpenBrain uses with Supabase tables, but implemented in local SQLite (stdlib, no dependency, no network).

**DB location:** `data/chat_store.db` (repo root, gitignored). No secrets, no Record content — only ephemeral conversation turns.

### Compaction trigger

**Message-count with minimum age**, not time-only.

- **Threshold:** 80 messages older than 48 hours for a given channel_key
- **Trigger point:** Lazy check at the top of `get_response()` — runs as a no-op 99% of the time
- **Model:** GPT-4o-mini (same as analyst — cheap)
- **Observability:** Token usage logged to `compute-ledger.jsonl` as `task_type: "compaction"`

OpenBrain uses a 20-day timer. That is too passive for grace-mar's intensive sessions where 50+ exchanges can happen in a single work block.

### Prompt structure

```
SYSTEM_PROMPT (character, knowledge, Lexile, Record inline)
  + MEMORY APPENDIX (from self-memory.md — operator-curated horizons)
  + CONVERSATION SUMMARY (from chat_summaries — auto-generated)
  + RECENT MESSAGES (last 20 raw turns from chat_messages)
```

**Memory appendix** is what the operator thinks matters. **Chat summary** is what actually happened. They serve different purposes and both belong in the prompt. Combined new token cost per call: ~300 tokens for the summary section.

### What the summary preserves vs excludes

**Preserves:**
- Topics discussed (in order)
- Questions the companion asked
- Lookups performed and whether they were saved to the Record
- Emotional tone and energy level
- Unresolved threads or open questions
- Activities mentioned

**Excludes (knowledge boundary compliance):**
- Identity claims or self-descriptions (those go through the gate pipeline)
- Specific world facts (those are in the Record or looked up fresh)
- Verbatim quotes (the raw transcript has those in session-transcript.md)

### Relationship to existing layers

| Layer | Purpose | Changed? |
|-------|---------|----------|
| **In-memory dict** | Fast cache for current session | Stays — DB is source of truth on restart |
| **session-transcript.md** | Operator continuity log, append-only | No change |
| **self-memory.md** | Manually curated short/medium/long context | No change |
| **Chat summary (new)** | Auto-compressed conversation history | New layer |
| **Record (self.md)** | Governed identity state | No change |

### Deterministic commands

Three commands that bypass the Voice LLM entirely (zero token cost, no hallucination risk):

| Command | Data source | Purpose |
|---------|-------------|---------|
| `/recent [N]` | chat_messages | Show last N conversation turns |
| `/search <query>` | chat_messages + chat_summaries | Full-text search of conversation history |
| `/recall <query>` | self.md (IX-A/B/C) + self-archive.md | Direct read access to governed Record state |

### Files touched

| File | Change |
|------|--------|
| `bot/chat_store.py` | New — SQLite module |
| `bot/core.py` | Wire store/load/compact/summary into get_response and reset |
| `bot/bot.py` | Add /recent, /search, /recall handlers |
| `.gitignore` | Add data/chat_store.db |
| This file | Design spec |

### Files NOT touched

`prompt.py`, `self.md`, `self-memory.md`, `recursion-gate.md`, `session-transcript.md`, analyst pipeline, gated merge pipeline, dream/bridge scripts.
