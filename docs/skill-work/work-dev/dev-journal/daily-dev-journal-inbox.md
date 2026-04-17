# Daily dev journal inbox (accumulator)

**Purpose:** **Append-only** scratch surface for the **current local calendar day** while you work the **work-dev** lane — harness notes, integration friction, links, half-formed reflections — **before** they become the finished journal page.

**Fold at `dream`:** Synthesize into the canonical day file for this calendar window: **`YYYY-MM-DD-day-NN.md`** in this folder (**NN** = journal day number from your chosen anchor — match your latest entry or next ordinal). If that file does not exist yet, **create** it from the fold (short sections: focus, actions, wins, blockers, tomorrow — see [README](README.md)). The rolling file is **not** automatically cleared each dream; clear or trim manually when you want a fresh buffer.

**Length (scratch section only — below the append line):** When the scratch body exceeds **~20000 characters**, **prune from the top** (oldest lines first) in **~5000-character blocks** until **≤ ~20000 characters** remain (repeat if a single paste still leaves you above the limit). Re-count after large pastes.

**Missed `dream`:** Before appending on a new day, fold or merge stale content into the correct dated `*-day-NN.md` page.

**Contrast:** [work-dev-history.md](../work-dev-history.md) stays the **milestone** log; this inbox is a **volatile buffer** — same pattern as [strategy-notebook daily-strategy-inbox](../../work-strategy/strategy-notebook/daily-strategy-inbox.md).

**Git:** Commits preserve history.

---

**Accumulator for (local date):** 2026-04-17

_(Append below this line during the day.)_

- **SemaClaw bridge proposal evaluated and rejected.** LLM-generated GitHub issue/PR templates for a "SemaClaw bridging plan" — proposed Docker profiles, React web UI, 4-layer plugin architecture, multi-channel adapters (Feishu/QQ/Discord), plugin loader, schema-registry, marketplace. Evaluated against actual repo: ~60% premature infrastructure, ~20% already exists (Docker Compose, gate-review app, MCP adapter Wave 4B, PR template, `src/grace_mar/`), ~20% architecturally wrong (treats Grace-Mar as multi-tenant SaaS, not sovereign single-companion system). Rejected wholesale. The proposal was generated without reading the repo.
