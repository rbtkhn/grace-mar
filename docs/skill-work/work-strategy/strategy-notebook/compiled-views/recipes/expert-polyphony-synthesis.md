# Compilation Recipe: Expert Polyphony Synthesis

**Recipe ID:** RECIPE-STRATEGY-POLYPHONY-2026-04-22-001  
**Version:** 0.1 (Starter)  
**Last Generated:** *(set when you run the bundler or finish a narrative pass)*  
**Purpose:** Generate a browsable, derived **Symphony Snapshot** that weaves multiple expert voices from the strategy-notebook into coherent convergences, preserved tensions, and operator-guided judgment — without ever replacing the source thread files or strategy-page blocks.

**Source of Truth:**

- `experts/<expert_id>/thread.md` (or `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`), and lane-specific `voices/<voice_id>/thread.md` where used — **Journal** layer above the machine fence + **Machine** layer inside the fence  
- `chapters/YYYY-MM/days.md` and `meta.md`  
- `daily-strategy-inbox.md` (recent entries)  
- `strategy-page` blocks inside Journal layers  

**Output Location:** `compiled-views/expert-polyphony-synthesis-YYYY-MM-DD.md` (dated)  
**Regeneration Rule:** This is a **derived artifact only**. Never edit it directly. If the synthesis appears incorrect or outdated, correct the underlying thread files or strategy-page blocks and regenerate.

---

## Recipe Instructions for the Compilation Agent

You are a neutral, precise, polyphonic synthesizer operating strictly within Grace-Mar’s **WORK** layer. Your job is to read the current state of the strategy-notebook and produce a clean, Obsidian-friendly markdown snapshot that highlights the **Symphony of Civilization** without collapsing distinct expert voices.

**Operator calibration (governance):** You are **not** the conductor. The **operator** sets emphasis, promotion, and legitimacy. Your job is to **collate and attribute** per this recipe — especially **Emerging Operator Judgment**, which must come **only** from existing `strategy-page` / Journal prose. Optional self-check: *precision* (unambiguous convergences) vs *expression* (Judgment voice) vs *economy* (minimal overlay on the bundle) — see [SYNTHESIS-OPERATING-MODEL.md § Techniques inspired by the masters](../../SYNTHESIS-OPERATING-MODEL.md#techniques-inspired-by-the-masters).

### Step 1: Input Selection

- Identify the set of active experts to include (default: all experts with recent activity in the last 30 days; allow recipe parameter to specify a subset, e.g. `mercouris, marandi, ritter`).
- Pull:
  - Most recent **Machine Layer** extractions (structured content between `<!-- strategy-expert-thread:start -->` and `<!-- strategy-expert-thread:end -->`).
  - Most recent **Journal Layer** entries, especially `strategy-page` blocks (Signal / Judgment / Open format).
  - Relevant context from monthly `meta.md`, `days.md`, and any active `[watch]` or `[decision]` markers.

### Step 2: Synthesis Rules (Strict)

- **Preserve Polyphony**: Keep each expert’s voice distinct. Do not merge or average them. Use clear attribution (e.g. “Mercouris on…”, “Marandi counters with…”).
- **Surface Convergences**: Identify genuine alignments across experts (shared signals, overlapping predictions, reinforcing historical analogies).
- **Surface Tensions & Contradictions**: Explicitly flag meaningful dissonances, misalignments, or unresolved questions. Treat contradictions as strategic signals, not noise to be smoothed away.
- **Operator Voice Priority**: Ground final judgment sections in the operator’s existing `strategy-page` blocks and Journal Layer prose. **Do not invent** new operator judgment.
- **Historical Resonance**: Lightly reference relevant analogies from the History Notebook or CIV-MEM **only when they appear in the source material**.
- **No Contamination**: Do not propose changes to SELF, EVIDENCE, SKILLS, or any Record surface. Stay entirely inside the WORK layer.

### Step 3: Required Output Structure

## Symphony Snapshot — [YYYY-MM-DD]

**Active Experts:** [comma-separated list]  
**Time Window:** [e.g. past 30 days]  
**Generation Note:** Derived from thread files. Regenerate after major EOD updates.

### 1. Executive Summary

One-paragraph neutral overview of the current polyphonic state (tone, momentum, dominant themes).

### 2. Key Convergences

- Bullet list or short paragraphs with clear expert attribution.
- Focus on high-signal alignments (e.g. shared view on energy chokepoints, escalation risks, etc.).

### 3. Preserved Tensions & Contradictions

- Explicitly list meaningful dissonances.
- Format:  
  **Issue:** [brief description]  
  **Mercouris:** [quote or paraphrase]  
  **Marandi:** [counter]  
  **Implication:** [neutral strategic signal]

### 4. Emerging Operator Judgment

- Synthesize from existing `strategy-page` blocks only.
- Highlight any evolving arcs or open questions flagged in Journal layers.
- Include any active `[watch]` or `[decision]` items.

### 5. Recommended Next Actions

- Suggested EOD focus areas.
- Specific experts or threads to deepen in the next session.
- Potential promotion candidates (if any strategy-page blocks have stabilized).

### 6. Cross-References

- Links or citations back to specific `thread.md` files, strategy-page blocks, or raw-input dates.
- Optional graph-friendly section for Obsidian (e.g. `[[../experts/mercouris/thread]]` style links).

### Change Log

- Generated on [date] from recipe RECIPE-STRATEGY-POLYPHONY-2026-04-22-001
- Next recommended regeneration: after next EOD session or when new high-signal material arrives.

---

## Regeneration Prompt (Copy-Paste for Future Runs)

Re-run **Step 1–3** above using the current notebook tree; prefer the deterministic bundle from `python3 scripts/compile_strategy_view.py` as the paste-in **Source bundle** body, then fill **Symphony Snapshot** sections per the strict rules.

---

**Governance & Safety Note (enforced by compilation agent):**

This compiled view is **refreshable only**. It is not authoritative. The canonical record remains in the expert `thread.md` files and `strategy-page` blocks. Any corrections must be made at the source level, followed by regeneration.

**Do not edit** generated snapshot markdown by hand.

---

## See also

- [SYNTHESIS-OPERATING-MODEL.md § Polyphony synthesis rules](../../SYNTHESIS-OPERATING-MODEL.md#7-polyphony-synthesis-rules)
- [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor)
- [compiled-views/README.md](../README.md)
