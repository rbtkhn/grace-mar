# Prompt parity for IX-A / IX-B / IX-C (Voice and analyst)

**Purpose:** Operator-facing truth about how **Section IX** entries in [`users/grace-mar/self.md`](../users/grace-mar/self.md) relate to **[`bot/prompt.py`](../bot/prompt.py)** (`SYSTEM_PROMPT`, `ANALYST_PROMPT`), merge tooling, and harnesses—especially **drift** when `self.md` changes without matching prompt edits.

**Scope:** Documentation only. Does not change merge behavior or prompts.

**Related:** [instance doctrine — File Update Protocol and Prompt Architecture](../users/grace-mar/instance-doctrine.md) · [conceptual framework — companion self](conceptual-framework.md) · [governance unbundling](governance-unbundling.md)

---

## SSOT chain

| Layer | Role |
|-------|------|
| **`users/grace-mar/self.md`** | **Canonical Record** for merged IX-A (Knowledge), IX-B (Curiosity), IX-C (Personality) YAML lists. |
| **`scripts/process_approved_candidates.py`** | On approved merge, updates `self.md`, evidence, and optionally **`bot/prompt.py`** (see below). |
| **`bot/prompt.py`** | **`SYSTEM_PROMPT`** — Voice emulation inline text; **`ANALYST_PROMPT`** — signal detection and **deduplication** against embedded IX snapshots. |
| **`python scripts/export_prp.py -u grace-mar -o grace-mar-llm.txt`** | Compact PRP export; [instance doctrine](../users/grace-mar/instance-doctrine.md) expects refresh after SELF/prompt merges when output changes. |

Nothing in the Voice runtime reads `self.md` directly at inference time; the **prompt strings** are what the model sees unless RAG / lookup paths add context.

---

## Two prompt surfaces (both can drift)

1. **`SYSTEM_PROMPT`** — What the **Voice** uses in chat: narrative identity, **Curiosity** / **Personality** (and related) lines under **`## RECORD STATE`** in the current grace-mar layout.

2. **`ANALYST_PROMPT`** — Embeds **### IX-A / IX-B / IX-C** blocks so the analyst can **deduplicate** staging against “what’s already in the profile.”

These are **separate copies** of IX-shaped text. Updating **`self.md`** alone does **not** automatically refresh both unless the merge path or a manual edit brings them in sync.

**Honest default:** After IX merges that should affect dedup, verify **`ANALYST_PROMPT`**’s IX blocks match **`self.md`** (or accept stale dedup until updated).

---

## `rebuild_ix` and `rebuild_observation_sections_from_self`

Merge logic in [`scripts/process_approved_candidates.py`](../scripts/process_approved_candidates.py): if a candidate carries **`prompt_merge_mode: rebuild_ix`**, the script calls **`rebuild_observation_sections_from_self`** from [`src/grace_mar/merge/prompt_sync.py`](../src/grace_mar/merge/prompt_sync.py).

That function **only replaces** spans bounded by these **exact** headers in **`SYSTEM_PROMPT`**:

- `## YOUR KNOWLEDGE (from observations)` → next `## YOUR CURIOSITY (what catches your attention)`
- `## YOUR CURIOSITY (what catches your attention)` → next `## YOUR PERSONALITY (observed)`
- `## YOUR PERSONALITY (observed)` → next `## IMPORTANT CONSTRAINTS`

It rebuilds bullets from **`self.md`** YAML: IX-A **Facts** `topic:` lines, IX-B `topic:` lines, IX-C `observation:` lines. If a header is **missing**, that span is **skipped** (no error).

**grace-mar today:** [`bot/prompt.py`](../bot/prompt.py) uses **`## RECORD STATE`** with narrative **Curiosity** / **Personality** lists, **not** the `YOUR KNOWLEDGE` / `YOUR CURIOSITY` / `YOUR PERSONALITY` header triple above. So **`rebuild_ix` does not rewrite the current default `SYSTEM_PROMPT` layout** unless the prompt file is refactored to include those headers.

**Implication:** Do **not** assume a merge with `rebuild_ix` updated the visible Voice narrative unless you’ve confirmed the header layout matches [`prompt_sync.py`](../src/grace_mar/merge/prompt_sync.py).

**Legacy append path:** Candidates may use **`prompt_addition`** + **`prompt_section`** (`YOUR KNOWLEDGE` / `YOUR CURIOSITY` / `YOUR PERSONALITY`). [`insert_prompt_addition`](../src/grace_mar/merge/prompt_sync.py) maps those to specific headers **or** falls back to older placeholder anchors (`## WHAT YOU LOVE`, `## HOW YOU HANDLE THINGS`). If neither matches, the addition may not apply—another reason to **verify `prompt.py` by hand** after merges.

---

## Drift checklist (after IX-B / IX-C–affecting merges)

Use this when you need **prompt parity** with the Record:

1. **`self.md`** — IX-B / IX-C entries merged as intended (YAML ids, `topic:` / `observation:`, provenance).
2. **`bot/prompt.py` — `SYSTEM_PROMPT`** — Narrative under **`## RECORD STATE`** (or your future section layout) reflects new curiosity/personality lines **if** the Voice should speak them.
3. **`bot/prompt.py` — `ANALYST_PROMPT`** — **### IX-B** / **### IX-C** (and IX-A if present) blocks match **`self.md`** enough that staging dedup is not wrong.
4. **PRP** — Run `python scripts/export_prp.py -u grace-mar -o grace-mar-llm.txt` (or repo default); commit if diff (per [instance doctrine](../users/grace-mar/instance-doctrine.md)).
5. **Harnesses (optional but relevant)** — Counterfactual / voice / **judgment probes** import prompt text from **`prompt.py`**; rerun when you care about regression signal after prompt edits.

---

## IX-B vs IX-C scope (identity vs WORK)

- **IX-B (Curiosity)** — Durable **topics and engagement signals** that belong in the companion’s **documented** interests after gate approval—not every transient link or inbox item.
- **IX-C (Personality)** — **Observed patterns**, speech habits, **tensions** suitable for Voice texture and [judgment probes](../scripts/run_judgment_probes.py)—not a substitute for **operator cadence**, **skill-work** rituals, or **work-cadence** logs unless the companion explicitly treats those as **identity**.

**Work is adjacent:** [`conceptual-framework.md`](conceptual-framework.md) — WORK crosses into the Record **through the gate**. Pending governance discussions (e.g. moving **work rhythm** lines out of IX-C) live in **`recursion-gate.md`**; this doc does not resolve them.

---

## Probes and harnesses

[`scripts/run_judgment_probes.py`](../scripts/run_judgment_probes.py) imports **`SYSTEM_PROMPT`** from [`bot/prompt.py`](../bot/prompt.py). Scores reflect **embedded prompt text**, not a live read of **`self.md`**. If **`SYSTEM_PROMPT`** lags **`self.md`**, probes measure **prompt**, not the Record alone—fix parity before inferring “Record regression.”

---

## Summarization tiers (token pressure)

When IX lists grow, [instance doctrine](../users/grace-mar/instance-doctrine.md) calls for **summarization tiers** on **`SYSTEM_PROMPT`**. Practically:

- **Compress** grouped facts into category lines without dropping **warrants** or **named tensions** where IX-C depends on them.
- **Avoid** duplicating the same bullet in **`SYSTEM_PROMPT`** and **`ANALYST_PROMPT`** if one side can stay shorter (analyst needs dedup fidelity; Voice needs readable voice).

---

## See also

- [instance-doctrine.md — Prompt Architecture](../users/grace-mar/instance-doctrine.md#prompt-architecture-botpromptpy)
- [AGENTS.md — Three-Dimension Mind Model](../AGENTS.md) (repository structure section)
- [src/grace_mar/merge/prompt_sync.py](../src/grace_mar/merge/prompt_sync.py) — rebuild and append helpers
