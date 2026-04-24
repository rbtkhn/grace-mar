# Cici Telegram bot — Tier C and injected memory (advisor note, WORK)

**Captured:** 2026-04-08  
**Territory:** work-cici **evidence** — operator coaching; not Xavier’s Record; not a gate merge.  
**Git context (external):** Branch [`claude/telegram-bot-integration-Dvbdw`](https://github.com/Xavier-x01/Cici/tree/claude/telegram-bot-integration-Dvbdw) (not on `main` as of this note); auto-search commit [`ba709f3`](https://github.com/Xavier-x01/Cici/commit/ba709f37897b32168fb72ea628bed69a1163c114).

---

## Advisor note (one paragraph)

The Telegram Edge Function’s **pre-response MCP `search`** (query = user message, small result cap, snippets concatenated into the **system** prompt next to `CICI_SYSTEM`) is the right *shape* for continuity, but it inherits the same epistemic class as every other **vector / MCP recall** path already called out in Cici’s companion layer: **Tier C** — useful **context**, not **verified** business or partner truth. Treat injected lines as **“might help, might be wrong, might be stale”** in coaching: encourage Xavier to add **one machine-obvious sentence** inside `CICI_SYSTEM` (or the injected block header) that tells the model to **quote or summarize memories as uncertain recall**, to **prefer abstention** on BrewMind facts unless Tier A/B, and never to **elevate** a retrieved line into a **public promise** without governed promotion — otherwise the bot will feel *smarter* while quietly **confident-wrong** on the channel where shame and screenshot risk are highest.

**Refs:** [Compare branch to `main`](https://github.com/Xavier-x01/Cici/compare/main...claude/telegram-bot-integration-Dvbdw) · Cici `CLAUDE.md` **Common Errors** / BrewMind companion **no retrieval-as-truth** (on `main`).
