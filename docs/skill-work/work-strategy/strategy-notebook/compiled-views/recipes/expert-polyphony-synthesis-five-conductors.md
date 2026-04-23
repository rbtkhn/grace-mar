# Compilation Recipe: Expert Polyphony Synthesis (Five Conductor Movements)

**Recipe ID:** RECIPE-STRATEGY-POLYPHONY-FIVE-CONDUCTORS-2026-04-23-003  
**Version:** 1.2  
**Last Generated:** *(set when you run the bundler or finish a narrative pass)*  
**Purpose:** Generate a browsable, derived **Symphony Snapshot** that weaves multiple expert voices into coherent **polyphony** using the same **five movement** map as the [Coffee Cadence (Conductor protocol)](../../COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) — precision through selectivity — without replacing source threads or `strategy-page` blocks, and optionally a compact **Unhobbling (frontier / tools)** pass backed by a dedicated queue.

**Source of truth (SSOT list):**

- `experts/<expert_id>/thread.md` (or `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`), and lane-specific `voices/<voice_id>/thread.md` where used — **Journal** layer above the machine fence + **Machine** layer inside the fence  
- `chapters/YYYY-MM/days.md` and `meta.md`  
- `daily-strategy-inbox.md` (recent entries)  
- `unhobbling-queue.md` (at strategy-notebook root) — **only** for the **Unhobbling** block; **not** a second SSOT for expert movements 1–5  
- `strategy-page` blocks inside Journal layers  

**Output location:** `compiled-views/expert-polyphony-synthesis-YYYY-MM-DD.md` (dated)  
**Regeneration rule:** This is a **derived artifact only**. Never edit it directly. If the synthesis appears incorrect or outdated, correct the underlying thread files or `strategy-page` blocks and regenerate.

**Relationship to 001 (starter):** The [expert-polyphony-synthesis.md](expert-polyphony-synthesis.md) (RECIPE-STRATEGY-POLYPHONY-2026-04-22-001) is the **executive-summary / six-section** shape. This recipe (003) is the **default narrative pass** for multi-lens work when you want **conductor-style prioritization** and alignment with the five-movement morning cadence, with optional **Unhobbling** for tool/frontier triage. Pick one recipe’s Step 3 output shape per run; do not double-fill both.

**Optional input:** Recent notes from the [Coffee Cadence](../../COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (verification flags, `[[watch]]` seeds, balance notes) may inform **Movement 1** and **Movement 5** but must not introduce facts absent from the SSOT list above. **Unhobbling** does not use Coffee outputs as a substitute for `unhobbling-queue.md` rows.

---

## Recipe instructions for the compilation agent

You are a neutral, precise, polyphonic synthesizer operating strictly within Grace-Mar’s **WORK** layer. Your job is to read the current state of the strategy-notebook (or the deterministic bundle from `compile_strategy_view.py`) and produce a clean, Obsidian-friendly markdown snapshot that stages the **Symphony of Civilization** in **five movements** (Toscanini → Kleiber), then **optionally** a compact **Unhobbling** block when the queue has actionable rows, then seals with a **Conductor’s Summary** and **strategic next actions** — without collapsing distinct expert voices.

**Operator calibration (governance):** You are **not** the conductor. The **operator** sets emphasis, promotion, and legitimacy. Your job is to **collate and attribute** per this recipe. **Emerging operator judgment** on **experts** must come **only** from existing `strategy-page` / Journal prose. **Unhobbling** judgment must trace to **`unhobbling-queue.md`**: your job is *structuring* and a five-lens *stress-test* on **queued** items, *not* discovering what shipped from model weights. **No new facts** in the Symphony movements *or* in Unhobbling. Optional self-check: *precision* vs *expression* vs *economy* — see [SYNTHESIS-OPERATING-MODEL.md § Techniques inspired by the masters](../../SYNTHESIS-OPERATING-MODEL.md#techniques-inspired-by-the-masters).

### Step 1: Input selection

- Identify the set of active experts to include (default: all experts with recent activity in the last 30 days; allow a subset parameter, e.g. `mercouris, marandi, ritter`).  
- Pull:  
  - Most recent **Machine** extractions (between `<!-- strategy-expert-thread:start -->` and `<!-- strategy-expert-thread:end -->`).  
  - Most recent **Journal** entries, especially `strategy-page` blocks (Chronicle / Reflection / Foresight).  
  - Relevant context from monthly `meta.md`, `days.md`, and any active `[watch]`, `[decision]`, or `[promote]` markers.  
- **Unhobbling:** Read [`unhobbling-queue.md`](../../unhobbling-queue.md). Treat the queue as **empty** for a narrative Unhobbling pass if there is **no** row with **`id`**, **`item`**, and **`evidence`** all non-empty (ignore a lone `_example-row_` or template placeholder as non-actionable).  
- If the operator used **Coffee Cadence** recently, you may use those outputs as *hints* for which **expert** movement to weight — not as a second SSOT for Unhobbling.

### Step 2: Synthesis rules (strict)

- **Preserve polyphony (movements 1–5):** Keep each expert’s voice distinct. Do not merge or average. Attribute clearly.  
- **Surface convergences and tensions** as in 001, but **assign** them to the movement where they best fit.  
- **Operator voice (experts):** Ground judgment in existing `strategy-page` blocks. **Do not invent** operator judgment.  
- **Unhobbling (queue):** **Do not** add new queue rows in the snapshot. **Do not** fill `what_changed` from undiscovered web search. You may rephrase or table rows already in the queue + bundle.  
- **Historical resonance:** Only when it appears in the source material.  
- **No contamination:** No proposals that change SELF, EVIDENCE, SKILLS, or any Record surface.

### Step 3: Required output structure (Symphony + optional Unhobbling)

## Symphony Snapshot — [YYYY-MM-DD]

**Active Experts:** [comma-separated list]  
**Time Window:** [e.g. past 30 days]  
**Generation Note:** Derived from thread files and/or source bundle. Regenerate after major EOD updates.

Fill the body using the **five movements** below. Each section should contain attributed expert material; empty sections are allowed if the day’s material does not use that movement.

### Movement 1 — Precision (Toscanini)

**Role:** Clean score, seams, and verifiability.  
- What is unambiguous in the Machine/Journal material? (claims, names, time windows, explicit convergences.)  
- What needs verification or is explicitly flagged as uncertain?  
- Short bullets; **no** smoothing of contradictions here — name them for Movement 2.

### Movement 2 — Flow (Furtwängler)

**Role:** Let tensions and resonances show without forced resolution.  
- Where do experts **disagree**, **hedge**, or **talk past** each other?  
- What historical or thematic resonances appear in the threads (from source only)?

### Movement 3 — Vitality (Bernstein)

**Role:** Heat, stakes, and narrative energy — without inventing facts.  
- What is the **pulse of the day or week** across voices? (Urgency, risk framing, “what would change the story.”)  
- One short paragraph is enough if bullets would flatten the drama.

### Movement 4 — Elegance & Polish (Karajan)

**Role:** Long arc, balance, and monthly shape.  
- How does this week sit in **`meta.md` / `days.md`** themes?  
- **Balance across experts:** who is driving the main melodic line for this window vs supporting lines?

### Movement 5 — Selectivity & Depth (Kleiber)

**Role:** Ruthless focus — what deserves deep follow-up or promotion *as a decision*, not a wish.  
- One or two threads/arcs that merit disproportionate next-session attention.  
- Explicit **watch / decision / promote** style signals **only** if already present in source markers or strategy-page text.

### Unhobbling (frontier and tools) — v1.2

**Role:** Second substrate, **same five movement names**, **different evidence** — stress-test **at most N = 3** queue **ids** (default: most recent by `date_noted`, or an explicit operator pick in the session) against Toscanini → Kleiber, then one **Kleiber-style** tag per id: `invest` \| `watch` \| `reject` (only in this block).

- If the queue is **empty** (per Step 1), output a **single** line: **Unhobbling** — N/A (queue empty). **Do not** use expert thread material in this block.  
- If the queue is **non-empty:** Prefer a **compact** shape: a small table (e.g. movement × one line for each of up to 3 `id`s) and/or one short sub-block per id. **No** vendor noise in Movements 1–5; keep tool/frontier content **here** only.

### Conductor’s Summary

- **2–4 sentences** unifying Movements 1–5, overall tone, dominant tension, and one clear strategic line the operator can re-enter on.  
- If Unhobbling is **not** N/A, add **at most one** additional sentence (still **no new facts**) on how frontier triage and expert symphony fit together.  
- Still **no new facts** — only what the movements and the queue rows already support.

### Strategic utility & next actions

- **EOD / next session:** suggested focus, which threads to open first. If Unhobbling is non-N/A, you may add one line on whether to return to a queued `id` in work-dev or steward, without inventing scope.  
- **Compiled-view hygiene:** if this snapshot is handoff, name the **bundle date** or expert subset used.  
- **Optional:** pointer to [compiled-views/README.md](../README.md) for regeneration commands.

### Cross-references

- Links or citations to specific `thread.md` paths, `strategy-page` ids, or inbox dates; and `unhobbling-queue.md` `id` values when Unhobbling is non-N/A.

### Change Log

- Generated on [date] from recipe `RECIPE-STRATEGY-POLYPHONY-FIVE-CONDUCTORS-2026-04-23-003`  
- Next recommended regeneration: after next EOD session or when new high-signal material arrives.

---

## Regeneration prompt (copy-paste for future runs)

Re-run **Step 1–3** using the current notebook tree; prefer the deterministic bundle from `python3 scripts/compile_strategy_view.py` as the paste-in **Source bundle** body, then fill the **Symphony Snapshot** and **Unhobbling** per the five movements and queue rules above.

---

**Governance & safety (enforced by compilation agent):**

This compiled view is **refreshable only**. It is not authoritative. The canonical record remains in the expert `thread.md` files and `strategy-page` blocks. **Do not edit** generated snapshot markdown by hand.

---

## See also

- [expert-polyphony-synthesis.md](expert-polyphony-synthesis.md) (001 — executive summary / six-section starter)  
- [SYNTHESIS-OPERATING-MODEL.md § Polyphony synthesis rules](../../SYNTHESIS-OPERATING-MODEL.md#7-polyphony-synthesis-rules)  
- [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor)  
- [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (five movements SSOT)  
- [`unhobbling-queue.md`](../../unhobbling-queue.md) (Unhobbling row SSOT)  
- [compiled-views/README.md](../README.md)

## Key refinements (v1.2)

- **Unhobbling block:** Optional **seventh** output section with **queue-first, strict** evidence: only [`unhobbling-queue.md`](../../unhobbling-queue.md) rows; default **N = 3** ids per run; same five movement **labels** as the Coffee map with **separate** evidence from expert threads.  
- **Conductor’s Summary** may add **one** bridging sentence for Symphony + Unhobbling when the latter is non-N/A; no duplicate “operator lens” node — the summary stays the single seal.  
- **Default narrative recipe id** and bundler: **003**; bundles include a **tail** of `unhobbling-queue.md` for deterministic context.

## Key refinements (v1.1) — prior

- **Default narrative for Symphony Snapshot:** five-conductors is the **preferred** shape for multi-lens + prioritization; 001 remains the **starter** with **Executive Summary** and six numbered blocks.  
- **Movements** aligned with **Toscanini → Furtwängler → Bernstein → Karajan → Kleiber** as in the Coffee Cadence protocol.  
- **Kleiber movement (experts):** **selective depth** and **marker-grounded** watch/decision/promote signals.  
- **Conductor’s Summary** as **short seal**; **optional Coffee** inputs are **hints only** for **expert** weighting.

---

**Disclaimer:** *No new facts* — all substantive claims in the expert movements and in Unhobbling must trace to the listed sources (threads + `strategy-page` for experts; `unhobbling-queue.md` for the Unhobbling block). LLM or bundler may not add knowledge from training data to the “Symphony” or Unhobbling text.
