# Default path — strategy pass

**Purpose:** The minimum viable strategy pass. Three moves, then stop. Everything else in the lane (minds, civ-mem, promotion, verify, history notebook, commentator threads) is **optional** and triggered only when the operator asks or the day demands it.

**When:** Normal day. Operator says **`strategy`** or **`strategy pass`**. **`strategy page read`** — **read-only** notebook frontier (no `days.md` / **`strategy-page`** writes); see [architecture § *End-of-day strategy session* — *Read-only variant*](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#end-of-day-strategy-session-terminology). No special modifiers otherwise.

**Full sequence (SSOT):** When you need the **numbered** inbox-first path (accumulate → **EOD strategy session** → optional markers → escalation → STRATEGY → no Record), use [STRATEGY-NOTEBOOK-ARCHITECTURE.md — Default operating path](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#default-operating-path-ssot). The three moves below are the **minimum**; that section is the **long-form** contract.

---

## The three moves

### 1. Read the frontier

If the operator said **`strategy page read`**, stay in **read-only** mode for this pass: complete this step (and optional daily-brief skim), summarize **where the notebook stands** in chat, then stop or offer a **short** pivot menu — **do not** compose into `days.md` or **`strategy-page`**, and **do not** append inbox **unless** they also ask to capture. Otherwise proceed with the full three moves below.

Open **two files**, scan **one**:

- [`strategy-notebook/STATUS.md`](strategy-notebook/STATUS.md) — where are we?
- [`daily-strategy-inbox.md`](strategy-notebook/daily-strategy-inbox.md) — what accumulated?
- Tail of active `chapters/YYYY-MM/days.md` — what did the last entry leave in **Open**?

If a daily brief exists for today (`daily-brief-YYYY-MM-DD.md`), skim its lead.

**Time:** <1 minute.

### 2. Write the inbox (Capture)

Append paste-ready lines to [`daily-strategy-inbox.md`](strategy-notebook/daily-strategy-inbox.md). Shape: one-liner or two-tier gist (`cold: … // hook: …`). Tag the plane when load-bearing (§1d–§1h watch tags).

Do **not** touch `days.md` unless the operator says **`strategy page`**, **`strategy page compose`**, or otherwise directs **EOD notebook compose** / **end-of-day strategy session** (or **breaking glass**). *Deprecated prompt:* **`weave`**.

**Time:** Variable (5–30 min depending on ingest volume).

### 3. Offer the menu

End the pass with **3–5 options** (standard WORK menu). Typical forks on a normal day:

| Letter | Option |
|--------|--------|
| **A** | **`strategy page`** / **`strategy page compose`** — inbox + **`raw-input/`** → **`strategy-page`** block(s) + `days.md` continuity; optional **MCQ-driven** sequencing per [EOD-MCQ-PROTOCOL.md](strategy-notebook/EOD-MCQ-PROTOCOL.md) |
| **B** | Verify — run `strategy + verify` on a claim |
| **C** | Lens — B/M/M one-liners (pick one, two, or skip) |
| **D** | Promote — stitch a stabilized arc to STRATEGY.md |
| **E** | Pivot to another lane or park |

If the operator picks **A**, follow the **EOD compose** contract ([architecture § End-of-day strategy session](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#end-of-day-strategy-session-terminology)): compose or extend **`strategy-page`** blocks in expert **`thread.md`** with Chronicle / Reflection / References minimum, update `days.md` continuity, then condense if over ~1200 words. If they skip, the inbox + **`raw-input/`** hold state for the next **EOD session**.

---

## What is NOT part of the default path

These are all valuable. None are required on every pass.

| Feature | When to add |
|---------|-------------|
| **Tri-frame / minds** | Operator says `tri-mind`, `tri-frame`, `tutti`, or picks a lens from the menu |
| **Civ-mem lookup** | Operator asks for upstream MEM depth or civilizational grounding |
| **History notebook wire** | Judgment leans on a mechanism pattern from LIB-0156 |
| **Commentator thread correlation** | Two+ ingests from indexed experts on the same crisis |
| **ROME-PASS source order** | Day touches Leo XIV / Holy See |
| **Watch doc passes (§1d–§1h)** | Day touches Putin / Vance / PRC / IRI — skim the relevant watch doc |
| **Promotion to STRATEGY.md** | Arc has stabilized (weekly or less) |
| **Current-events analysis pipeline** | Live event needs the full 11-section workflow |
| **Condense-to-target (Full path)** | Draft mixes notebook + DEMO + lens walls |
| **LLM / pasted strategic digest triage** | Dense §1f paste uses the **same** falsifiable-table + verify-before-**EOD compose** discipline as generator stubs ([NOTEBOOK-PREFERENCES — daily brief supplements](strategy-notebook/NOTEBOOK-PREFERENCES.md#daily-brief-supplements)) |

Each optional feature has its own section in [SKILL.md](../../.cursor/skills/skill-strategy/SKILL.md) and the architecture docs. Consult them when the operator triggers them — not before.

---

## Decision count

A normal pass requires **three decisions**: (1) read the frontier, (2) capture to inbox, (3) pick from the menu. The menu is the only branching point. Everything else is a response to an explicit operator choice or a signal from the day's material.

Compare: the full skill file describes ~15 optional features, 5 watch threads, 4 condense tiers, 3 session checklists, and 7 promotion stages. Those exist for completeness and governance. They are not the daily workflow.

---

## See also

| Doc | Role |
|-----|------|
| [SYNTHESIS-OPERATING-MODEL.md](strategy-notebook/SYNTHESIS-OPERATING-MODEL.md) | Session types A–D, section router, minds defaults |
| [NOTEBOOK-PREFERENCES.md](strategy-notebook/NOTEBOOK-PREFERENCES.md) | Operator narrowings (minimum sections, prose register, EOD compose rhythm) |
| [STRATEGY-NOTEBOOK-ARCHITECTURE.md](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) | Full architecture (condense, entry model, polyphony, templates) |
| [SKILL.md](../../.cursor/skills/skill-strategy/SKILL.md) | Complete skill contract (all features, all obligations) |
