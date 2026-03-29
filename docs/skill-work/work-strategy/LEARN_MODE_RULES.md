# LEARN_MODE_RULES

**Civilizational Strategy Learn Mode Adapter**  
**Version:** 2026-03-29 | **Last gated update:** _TBD_

## Purpose

This file defines how LEARN MODE operates inside the **work-strategy** surface, bridging the canonical CMC minds from **civ-mem** with the specialized geopolitics and history focus of [`STRATEGY.md`](STRATEGY.md) (operator shorthand: **STRATEGY**).

## Canonical mind references

All LEARN MODE sessions **must** reference the three primary CMC analytical lenses (canonical templates live in **civilization_memory**). In this repo, **entry-point stubs** live under [`minds/`](minds/); each stub links to the matching `CIV–MIND–*.md` template.

- **mind-mercouris.md** — Legitimacy, narrative grammar, recursive civilizational self-conception, doctrine evolution, and symbolic continuity.
- **mind-mearsheimer.md** — Power distribution, security dilemmas, offensive/defensive realism, alliance dynamics, and great-power competition geometry.
- **mind-barnes.md** — Material foundations, liability chains, extraction/defection logic, fiscal and resource constraints, and structural economic realities.

These three minds form the **Tri-Frame Synthesis** and must be applied unless a single-frame analysis is explicitly justified.

## LEARN MODE protocol (strict order)

1. **Mode declaration**  
   Every session must begin with:  
   `[LEARN MODE — [SINGLE-FRAME or TRI-FRAME] — [TOPIC]]`

2. **Context loading**  
   - Load current **STRATEGY** ledger: [`STRATEGY.md`](STRATEGY.md) (§I CORE + relevant lane-specific core + recent §III SCHOLAR).  
   - Load relevant **`WS–MEM–`** entries (§IV — work-strategy execution log **in this repo only**; not CMC `MEM–*` shards under `research/repos/civilization_memory/`).  
   - Load the three canonical minds via [`minds/`](minds/) (follow links to `CIV–MIND–*.md` as needed).

3. **Analysis sequence** (mandatory)  
   a. Failure-first scan (identify collapse points, legitimacy breakdowns, or structural overloads).  
   b. Apply the three minds in order:  
      - Mercouris frame (narrative / legitimacy lens)  
      - Mearsheimer frame (power / security lens)  
      - Barnes frame (material / liability lens)  
   c. Perform Tri-Frame Synthesis where tensions or synergies appear.  
   d. Explicitly flag contradictions between frames.

4. **Extraction rules**  
   - Convert insights into **heuristics / mental models** using this exact format:  
     `Model → Last applied (date + context) → Effectiveness note + explicit limitations + contradiction flags`  
   - Create or update **Extracted Lessons** and **Cross-Domain Patterns** under §III SCHOLAR.  
   - When a **binding procedural constraint** emerges, add or extend a **`WS–MEM–…`** entry (§IV). (No separate RLL file in this repo unless the operator adds one.)

5. **Governance constraints**  
   - All outputs are **additive-only**.  
   - Contradictions between minds or with documented evidence **must be preserved and flagged** (preserve CMC provenance when citing external MEM shards).  
   - No epistemic authority: record the derivation, never declare final truth.  
   - **RECURSION-GATE:** Stage **`CANDIDATE-XXXX`** when promoting content into **Record / Voice** or when the operator treats a change as an **explicit strategy milestone** (see [`STRATEGY.md`](STRATEGY.md) §VI). **Routine** SCHOLAR / WS–MEM updates follow normal **git / PR** workflow under **lane/work-strategy** without a gate row.

6. **Output requirements**  
   - Clearly label which mind/frame dominates each insight.  
   - Note explicit limitations and cross-frame contradictions.  
   - End with a short **Assimilation Summary** showing how the new learning integrates with existing SCHOLAR content.

## Usage

- The agent should load this file and the three **minds/** stubs at the start of any LEARN MODE session in work-strategy.  
- The human operator retains final approval via RECURSION-GATE when §VI requires it.

This adapter keeps **work-strategy** compatible with the broader Civilization Memory Codex while preserving its specialized focus on history and geopolitics.
