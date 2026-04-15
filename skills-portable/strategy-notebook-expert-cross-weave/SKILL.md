---
name: strategy-notebook-expert-cross-weave
preferred_activation: weave expert cross
description: "Fold two strategy-notebook expert-thread ingests into one days.md seam (Signal/Judgment/Links/Open), optional batch-analysis rows and chapter meta grep anchor; WORK lane only."
portable: true
version: 0.1.0
tags:
  - operator
  - work-strategy
  - strategy-notebook
---

# Strategy notebook — expert cross-weave

**Preferred activation (operator):** **`weave <expert-a> <expert-b>`**, **`expert cross-weave`**, **`crosses:expert-a+expert-b`**.

Use this skill when two indexed **`thread:<expert_id>`** lines in the daily strategy inbox should become **one explicit Judgment seam** on a calendar **`days.md`** page — without collapsing distinct evidence chains.

## Preconditions

1. Both experts appear in the **commentator roster** (`strategy-commentator-threads.md` pattern) with stable **`expert_id`** values.
2. Source lines exist (or are recoverable) in **`daily-strategy-inbox.md`** — including any **`crosses:`** / **`batch-analysis`** tails you intend to preserve.
3. You know the **calendar date** for the **`## YYYY-MM-DD`** section (session “today,” not an arbitrary forward stub unless the notebook already uses that convention).

## Procedure

### 0) Knot-shape fork (before any file write)

When the operator invokes **`weave`** without naming a single shape, present **4–6** labeled options (**A–F** or **1–6**) that describe **this** weave’s **thesis / knot shape** (e.g. **cross-expert seam** vs **continuity-only days.md** vs **new knot file + pointer** vs **Judgment-heavy / Links-light** vs **verify-first Open**). **Stub only**—no developed weave until the operator picks. If they already said **`weave <expert-a> <expert-b>`** or **`no menu`**, skip or shorten per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave command — knot-shape menu*.

### 1) Name the seam

- **`crosses:<expert-a>+<expert-b>`** — hyphenated ids, **alphabetical or roster order** if the repo already fixed a convention; stay consistent with inbox **`batch-analysis`** rows.
- One sentence each: **what A answers** vs **what B answers** (mechanism / bargaining / ORBAT / legitimacy — do not pretend they are the same question).

### 2) Write **`days.md`** (target month chapter)

Under **`chapters/YYYY-MM/days.md`**, in the correct **`## YYYY-MM-DD`** block:

1. **Signal** — One bullet: **sources** (inbox blocks, digest path, episode id), **before → after** (parallel ingests → single seam).
2. **Judgment** — One bullet: **`crosses:`** line, **convergence** (where both undercut the same fairy tale), **tension** (what must **not** be merged — e.g. transcript **quant** table vs **X** macro clause without pins), **pointers** to prior days / knots on the same topic.
3. **Links** — Inbox pointer, transcript or episode links, profile URLs; flag **pin exact status URL** where social ingests are still tier-C.
4. **Open** — Optional explicit **`batch-analysis | YYYY-MM-DD | A × B | crosses:…`** suggestion for grep membership; **tier** / verify reminders.

**Do not** add a second top-level **`##`** for the same calendar day if that heading already exists — **append** bullets to that day’s **Signal** / **Judgment** / **Links** / **Open**.

### 3) Optional — **`daily-strategy-inbox.md`**

- Add or extend a **`batch-analysis`** line: tension-first prose in the fourth column when the architecture expects it.
- Append a **minimal grep stub** on its own line when you want a **pure** `rg` hit:

  `batch-analysis | YYYY-MM-DD | Short label | crosses:expert-a+expert-b`

### 4) Optional — **`meta.md`** (month chapter)

- One **grep anchor** line under **April arc** (or the month’s one-screen summary): the exact **`batch-analysis`** stub ↔ **`days.md`** section anchor — helps humans and search.

### 5) **`STATUS.md`** (strategy-notebook)

- Bump **Last substantive entry** when this weave closes real notebook work (compound line is fine if a larger same-week entry already exists).

## Guardrails

- **WORK only** — not SELF, not EVIDENCE, not Voice; no RECURSION-GATE merges.
- **Do not** treat **digest** or **transcript** quantities as **wire-grade** without the notebook’s verify discipline.
- **Do not** fold **unrelated** third experts into the seam without an explicit **`batch-analysis`** or operator request.

## See also

- Strategy notebook architecture — daily inbox contract, entry model, output path.
- **Expert-thread continuity** section in **`daily-strategy-inbox.md`**.
- **`strategy-commentator-threads.md`** — stable **`expert_id`** and crossing rules.
