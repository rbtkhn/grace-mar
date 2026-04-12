---
name: tri-mind
preferred_activation: tri-mind
description: >-
  Tri-lens pass with a fixed A/B/C menu (Mercouris, Mearsheimer, Barnes): one letter = solo; two letters = 1-on-1 duet; abc = roundtable with topic-led or operator-chosen opening order (varied permutations, not always A→B→C).
  Triggers: tri-mind, tri-frame, tutti. WORK only; not the default on every strategy pass — see strategy-minds-granular.
---

# Tri-mind pass (`tri-mind`)

**Preferred activation (operator):** **`tri-mind`**. **Aliases:** **`tri-frame`**, **`tutti`**, **`three minds`**, **`full tri-frame`**.

**Purpose:** Run **in-voice** analysis using the **Tri-Frame** minds with a **fixed letter menu** — not every pass needs all three. This is **analysis in chat** (or inbox paste) first; it is **not** a substitute for **`strategy`** unless the operator also wants notebook capture.

**Relation to `skill-strategy`:** [`skill-strategy`](../skill-strategy/SKILL.md) is the **lane pass** (notebook, briefs, promotion). **`tri-mind`** is **lens choreography** when the operator wants **structured** Mercouris / Mearsheimer / Barnes output. Do **not** invoke **`tri-mind`** on every `strategy` turn — [strategy-minds-granular.mdc](../../rules/strategy-minds-granular.mdc).

**Relation to LEARN MODE:** If the operator is in **LEARN MODE** (full extraction, SCHOLAR hooks, strict ordering), follow [LEARN_MODE_RULES.md](../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md) — it may **override** section ordering and depth; say so when both apply.

**Relation to skill-write doctrine:** **`tri-mind`** produces **analysis**, not finished **operator publishing voice**. After the pass, calibrate public copy per [write-operator-preferences.md](../../../docs/skill-write/write-operator-preferences.md). **Locals:** before paste, satisfy **[write-shipping-checklist.md](../../../docs/skill-write/write-shipping-checklist.md) step 4** (*Closer*) — see **Procedure §4 — Public copy** below; run the **full** checklist when practical.

---

## Operator choice menu (always use these letters)

When **`tri-mind`** applies and the operator has **not** yet given a letter code in the **same** message, present **exactly** this block (no extra minds, no reorder):

```
Tri-mind — pick lens depth:
- A — Mercouris
- B — Mearsheimer
- C — Barnes
```

**How to read the reply** (case-insensitive; ignore spaces):

| Input | Mode |
|-------|------|
| **One** of `a` `b` `c` | **Solo** — that mind only: one substantive in-voice block on the thesis. |
| **Two** distinct letters (e.g. `ab`, `ba`, `ac`, `bc`) | **Duet (1-on-1)** — only those two minds: each opens **in menu order** (sort the chosen letters as **A → B → C**), then **one cross-reply round** between **just those two** (pushback / agreement / missing dimension). No third voice. |
| **`abc`** (all three letters, any order such as `acb`, `bca` — normalize to all three present) | **Roundtable** — full three-way pass (see below). Optional same-line hint: **`abc order BCA`** / **`abc cab`** to fix **opening** order; if omitted, agent picks a **topic-led** permutation (not the same every time). |

If the operator **already** included the code with the thesis (e.g. “tri-mind `ab` … paste”), **skip** the menu and run the matching mode.

**Letter → mind map (SSOT for this skill):** **A = Mercouris**, **B = Mearsheimer**, **C = Barnes**.

---

## When to use

- Operator says **`tri-mind`**, **`tri-frame`**, **`tutti`**, or **`three minds`** on a **specific** question.
- Optional: **civ-mem** grounding per [CIV-MEM-TRI-FRAME-ROUTING.md](../../../docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md) (Barnes → CONNECTIONS / liability; Mearsheimer → STATE / incentives; Mercouris → SCHOLAR / legitimacy) — usually on **roundtable** or when asked.

**Do not use** as the default wrapper around every work-strategy task.

---

## Grounding (read before writing)

| Letter | Mind | Canonical stub | Fingerprint (short) |
|--------|------|----------------|---------------------|
| **A** | Mercouris | [CIV-MIND-MERCOURIS.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-MERCOURIS.md) | Legitimacy, continuity, diplomatic narrative, staging |
| **B** | Mearsheimer | [CIV-MIND-MEARSHEIMER.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md) | Power, incentives, structure, security competition |
| **C** | Barnes | [CIV-MIND-BARNES.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-BARNES.md) | Liability, jurisdiction, enforceability, who pays |

Patterns and recipes: [MINDS-SKILL-STRATEGY-PATTERNS.md](../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md).

**Note:** [`skill-strategy`](../skill-strategy/SKILL.md) § Post-entry lens offer uses **B → M → M** program order for **one-liner** options (Barnes, Mearsheimer, Mercouris). **`tri-mind`** uses the **A/B/C** letter map above — do not conflate the two orderings when labeling output; use **A/B/C** headings here.

---

## Procedure (agent)

### 0. Thesis

**Restate** the operator’s thesis or paste in one short block so every mind addresses the **same** object.

### 1. Solo (**one** letter)

One subsection for that mind only — **one** substantive paragraph (or tight bullets), **in-voice** per **LINGUISTIC FINGERPRINT** — no generic placeholders. Optional **2–3 bullets** “what stays open.”

### 2. Duet (**two** letters)

Take the **two** letters and sort them as **A < B < C** (e.g. `ba` and `ab` both → A then B; `cb` → B then C).

**Opening:** Two subsections in that **sorted** order — e.g. `ac` → Mercouris (A) then Barnes (C); `bc` → Mearsheimer (B) then Barnes (C).

**Cross-reply:** **One** round — each mind **one** paragraph responding to the **other** only. Preserve tension.

**Close:** **1–3 bullets** unresolved between these two lenses.

### 3. Roundtable (**abc**)

**Do not** default every roundtable to the same opening order (**A → B → C**). **Vary** how the three voices enter — the shape of the disagreement should feel **earned**, not templated.

#### Opening order (Round 1)

1. **Operator override** — If the operator names a permutation (e.g. **`abc order BCA`**, **`abc cab`**, or “**roundtable, Mercouris last**”), use that **letter order** for **subsection titles** in that sequence.

2. **Topic-led (default)** — Choose **one** of the six permutations of **A, B, C** using a **one-line warrant** (show it **once** before the openings, e.g. *Opening order this pass: B → C → A — structural incentives and material constraints before diplomatic framing.*). Rough **lead** heuristics (not exclusive):
   - **B** opens when the thesis turns first on **power, incentives, alliance pressure, security structure**.
   - **A** opens when **legitimacy, narrative, staging, institutional/diplomatic meaning** is the natural door.
   - **C** opens when **who pays, law/jurisdiction, enforcement, balance-sheet or liability** anchors the fight.

3. **Variety** — Across repeated **`tri-mind`** roundtables in a thread, **avoid** picking the **same** opening permutation **twice in a row** unless the operator asks for a repeat or LEARN MODE fixes order.

**Round 1 — Opening:** Three subsections in the **chosen** order. Each: **one** substantive paragraph (or tight bullets), **in-voice** per fingerprint. Headings use **letter + name** (e.g. `### B — Mearsheimer (opens)` when B leads).

#### Cross-reply (Round 2)

Each mind **one** paragraph (or labeled bullets) that **responds** to the **other two**. Preserve **disagreement**.

**Optional variation (use sometimes, not every pass):** Run cross-replies in **reverse** of the opening order (last opener **speaks first** in the reply round) so the thread **closes** on a different voice than it **opened** — or keep **same** order as Round 1 when a **linear pile-on** reads clearer. **One** sentence at the start of Round 2 is enough: *Cross-reply order: reverse of openings* or *same order as openings.*

#### Civ-mem (Round 3, optional)

If the operator asked to **integrate civ-mem** or **CIV-MEM**, add **one** paragraph **per mind** mapping to routing surfaces. If upstream `research/repos/civilization_memory` is **absent**, use [concept polyphony](../../../docs/civilization-memory/notes/concept-cognitive-polyphony.md) **lightly** — do not invent MEM ids. Order paragraphs **A, B, C** by letter here (stable index) **or** follow Round 1 order — pick one and be **consistent** in that pass.

**Close:** **Unresolved tension** — **2–4 bullets** (no fake consensus).

### 4. Write surface

Default **chat only**. To append to [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) use **paste-ready** lines or a bounded `batch-analysis` block per inbox rules. **`chapters/YYYY-MM/days.md`** only when the operator **directs** or at **`dream`** fold — same boundary as [NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md).

**Public copy:** When the operator publishes **`tri-mind` output** (or prose derived from it) to **Locals / X / YouTube**, follow **[write-operator-preferences.md](../../../docs/skill-write/write-operator-preferences.md)** — topic-first ledes, closers, surface calibration. **Step 4 (*Closer*)** in **[write-shipping-checklist.md](../../../docs/skill-write/write-shipping-checklist.md)** must pass before **Locals** paste: **memorable** final sentence encapsulating the core argument; **no** abstract stacked closer; **no** rhetorical question as the last line (see [write-memorable-closer.md](../../../docs/skill-write/write-memorable-closer.md), [write-no-abstract-stacked-closers.md](../../../docs/skill-write/write-no-abstract-stacked-closers.md), [write-no-rhetorical-question-closer.md](../../../docs/skill-write/write-no-rhetorical-question-closer.md)). **X / PH:** same **step 4** on the shipped trim unless the operator opts out.

---

## Variants (operator may request)

| Variant | Behavior |
|---------|----------|
| **Strict + web** | Add [fact-check](../fact-check/SKILL.md) or explicit **verify** on load-bearing claims; cite **URLs** in a final **Links** block if writing to disk. |
| **Roundtable depth** | Extra cross-reply rounds — keep bounded; offer **condense** if output exceeds ~2k words. |

---

## Boundaries

- **WORK only** — not Record, not `self.md` / EVIDENCE / gate merge.
- **No default tri-frame** on generic **`strategy`** — [strategy-minds-granular.mdc](../../rules/strategy-minds-granular.mdc).
- **Do not** parody the three voices; stay within **fingerprint** guidance in the CIV-MIND files.

---

## See also

- [minds/README.md](../../../docs/skill-work/work-strategy/minds/README.md)
- [CIV-MEM-TRI-FRAME-ROUTING.md](../../../docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md)
- [skill-strategy/SKILL.md](../skill-strategy/SKILL.md) § Three minds (optional — granular)
