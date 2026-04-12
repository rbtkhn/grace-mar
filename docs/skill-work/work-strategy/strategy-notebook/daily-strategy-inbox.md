# Daily strategy inbox (accumulator)

**Purpose:** **Append-only** scratch surface for the **current local calendar day** while you run **`strategy`**, read briefs, or capture links. Polished prose is **not** required — bullets, paste, URLs, half-sentences.

**X post ingest cadence:** Aim for **at least five** strategy ingests from X per local day (claim → why it matters → URL, plus verify tags as needed). **Five is a floor, not a cap** — capturing **more than five** on busy days is **normal**, not exceptional. Same one-line shape scales to 6+ rows without a separate workflow.

### Paste-ready one-liner (canonical unit)

**Purpose:** One **grep-friendly** line per ingest (clipboard-safe, easy to append in bulk).

**Suggested shape** (example, not a strict schema): optional source token (`X`, `YT`, etc.) **|** short **gist** (claim + why it matters) **|** URL, with an optional `verify:` tail for epistemic flags (e.g. `verify:OSINT-unverified`).

**Default assistant behavior:** When the operator asks for **strategy ingest** in Cursor, the assistant’s **default on-disk target** for those lines is **below the append line in this file** — not `session-transcript.md` unless the operator asks for a **session audit trail** (see [work-menu-conventions — Auditing picks](../work-menu-conventions.md#6-auditing-picks-choice-journal)).

**Fold at `dream`:** Synthesize into one **`## YYYY-MM-DD`** block in `chapters/YYYY-MM/days.md` (Signal / Judgment / Links / Open). Full rules (prune, stale-day handling, rolling file not auto-cleared): [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox*; agent steps: [.cursor/skills/dream/SKILL.md](../../../../.cursor/skills/dream/SKILL.md).

**Length (scratch section only — below the append line):** When the scratch body exceeds **~8000 characters**, **prune from the top** (oldest lines first) until roughly **≤ ~5000 characters** remain. Re-count after large pastes. Optional: full clear to the template below anytime.

**Git:** Prior versions remain in history when you commit.

---

**Accumulator for (local date):** _YYYY-MM-DD_

_(Append below this line during the day.)_
