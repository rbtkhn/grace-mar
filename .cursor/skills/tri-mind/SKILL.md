---
name: tri-mind
preferred_activation: tri-mind
description: >-
  Tri-lens pass with a fixed A/B/C menu (Mercouris, Mearsheimer, Barnes): one letter = solo; two letters = 1-on-1 duet; abc = roundtable with topic-led or operator-chosen opening order (varied permutations, not always A→B→C); ab+c = litigator-close (Mercouris–Mearsheimer duet then Barnes closing only — not symmetric abc).
  Triggers: tri-mind, tri-frame, tutti. WORK only; not the default on every strategy pass — see strategy-minds-granular.
---

# Tri-mind pass (`tri-mind`)

**Preferred activation (operator):** **`tri-mind`**. **Aliases:** **`tri-frame`**, **`tutti`**, **`three minds`**, **`full tri-frame`**.

**Purpose:** Run **in-voice** analysis using the **Tri-Frame** minds with a **fixed letter menu** — not every pass needs all three. This is **analysis in chat** (or inbox paste) first; it is **not** a substitute for **`strategy`** unless the operator also wants notebook capture.

**Design principle:** Tri-mind is the strategy **differentiator**, not the strategy **engine**. Use it when one lens is not enough, not as the default wrapper around every strategy pass.

**Relation to `skill-strategy`:** [`skill-strategy`](../skill-strategy/SKILL.md) is the **lane pass** (notebook, briefs, promotion). **`tri-mind`** is **lens choreography** when the operator wants **structured** Mercouris / Mearsheimer / Barnes output. Do **not** invoke **`tri-mind`** on every `strategy` turn — [strategy-minds-granular.mdc](../../rules/strategy-minds-granular.mdc).

**Relation to LEARN MODE:** If the operator is in **LEARN MODE** (full extraction, SCHOLAR hooks, strict ordering), follow [LEARN_MODE_RULES.md](../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md) — it may **override** section ordering and depth; say so when both apply.

**Relation to skill-write doctrine:** **`tri-mind`** produces **analysis**, not finished **operator publishing voice**. After the pass, calibrate public copy per [write-operator-preferences.md](../../../docs/skill-write/write-operator-preferences.md) and the **[`skill-write`](../skill-write/SKILL.md)** Cursor skill (same SSOT). **Locals:** before paste, satisfy **[write-shipping-checklist.md](../../../docs/skill-write/write-shipping-checklist.md) step 4** (*Closer*) — see **Procedure §5 — Write surface** (*Public copy*) below; run the **full** checklist when practical.

---

## Operator choice menu (always use these letters)

When **`tri-mind`** applies and the operator has **not** yet given a letter code in the **same** message, present **exactly** this block (no extra minds, no reorder):

```
Tri-mind — pick lens depth:
- A — Mercouris
- B — Mearsheimer
- C — Barnes
```

**Extended code (after the menu or in the same message — optional):**

| Code | Meaning |
|------|---------|
| **`ab+c`** | **Litigator-close** — Mercouris + Mearsheimer **duet** (`ab`), then **Barnes closing only** (see **Procedure §3**). **Not** the same as **`abc`**. |
| **`litigator-close`**, **`abc litigator-close`**, **“Barnes closes”** | Same as **`ab+c`**. |

**How to read the reply** (case-insensitive; ignore spaces):

| Input | Mode |
|-------|------|
| **One** of `a` `b` `c` | **Solo** — that mind only: one substantive in-voice block on the thesis. |
| **Two** distinct letters (e.g. `ab`, `ba`, `ac`, `bc`) | **Duet (1-on-1)** — only those two minds: each opens **in menu order** (sort the chosen letters as **A → B → C**), then **one cross-reply round** between **just those two** (pushback / agreement / missing dimension). No third voice. |
| **`ab+c`** or **`litigator-close`** (see table above) | **Litigator-close** — **`ab`** openings + **`ab`** cross-reply, then **one** Barnes block (no Barnes opening, no three-way cross-reply). See **Procedure §3**. |
| **`abc`** (all three letters, any order such as `acb`, `bca` — normalize to all three present) **and not** `ab+c` | **Roundtable** — full three-way pass (see **Procedure §4**). Optional same-line hint: **`abc order BCA`** / **`abc cab`** to fix **opening** order; if omitted, agent picks a **topic-led** permutation (not the same every time). |

If the operator **already** included the code with the thesis (e.g. “tri-mind `ab` … paste”), **skip** the menu and run the matching mode.

**Letter → mind map (SSOT for this skill):** **A = Mercouris**, **B = Mearsheimer**, **C = Barnes**.

**Ordering rules (quick reference):**
- Letters are always **A/B/C** = Mercouris / Mearsheimer / Barnes.
- Duets always open in **sorted letter order** (e.g. `ba` → A then B).
- Roundtables **vary** opening order by topic or operator override — not the same every time.
- Do **not** import other menu orderings (e.g. B → M → M program order) into tri-mind headings.

---

## When to use

- Operator says **`tri-mind`**, **`tri-frame`**, **`tutti`**, or **`three minds`** on a **specific** question.
- Optional: **civ-mem** grounding per [CIV-MEM-TRI-FRAME-ROUTING.md](../../../docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md) (Barnes → CONNECTIONS / liability; Mearsheimer → STATE / incentives; Mercouris → SCHOLAR / legitimacy) — usually on **roundtable** or when asked.

**Do not use** as the default wrapper around every work-strategy task.

---

## Grounding (read before writing)

**Cursor rule (voice fidelity):** [`.cursor/rules/minds-authentic-voice.mdc`](../../rules/minds-authentic-voice.mdc) — tri-mind and any **`CIV-MIND-*`**-grounded output must use each mind’s **authentic register** (read fingerprints below), not neutral meta-summary.

| Letter | Mind | SSOT (read fingerprint here) | Fingerprint (short) |
|--------|------|-------------------------------|---------------------|
| **A** | Mercouris | [strategy-expert-mercouris-mind.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-expert-mercouris-mind.md) | Legitimacy, continuity, diplomatic narrative, staging |
| **B** | Mearsheimer | [strategy-expert-mearsheimer-mind.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-expert-mearsheimer-mind.md) | Power, incentives, structure, security competition |
| **C** | Barnes | [strategy-expert-barnes-mind.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-expert-barnes-mind.md) | Liability, jurisdiction, enforceability, who pays |

Patterns and recipes: [MINDS-SKILL-STRATEGY-PATTERNS.md](../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md).

**Note:** [`skill-strategy`](../skill-strategy/SKILL.md) § Post-entry lens offer uses **B → M → M** program order for **one-liner** options (Barnes, Mearsheimer, Mercouris). **`tri-mind`** uses the **A/B/C** letter map above — do not conflate the two orderings when labeling output; use **A/B/C** headings here.

---

## Mode shapes (quick reference)

| Mode | Shape |
|------|-------|
| **Solo** (one letter) | One substantive in-voice pass |
| **Duet** (two letters) | Two openings in sorted order + one cross-reply round |
| **Litigator-close** (`ab+c`) | Mercouris + Mearsheimer duet, then **one** Barnes closing block (latch to A and B) |
| **Roundtable** (`abc`) | Three openings (varied order) + one cross-reply round + unresolved tensions |

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

### 3. Litigator-close (`ab+c`)

**Aliases:** **`ab+c`**, **`litigator-close`**, **`abc litigator-close`**, operator phrases like **“Barnes closes”** / **“litigator last.”**

**Not** interchangeable with **`abc` roundtable:** Barnes is the **concluding voice only** — he does **not** open alongside A/B, and there is **no** three-way cross-reply round. Matches **CIV-MIND-BARNES** as **orthogonal catalyst** (counsel after two “expert” frames), not a third parallel geopolitics opener.

**Sequence**

1. **Round 1 — Openings:** **Mercouris (A)** then **Mearsheimer (B)** — one substantive paragraph each (or tight bullets), **in-voice**, same object as **Procedure §0** thesis.
2. **Round 2 — Cross-reply:** **A ↔ B only** — **one** round; each mind **one** paragraph responding to the **other** only. Preserve tension (same discipline as **§2 Duet**).
3. **Round 3 — Barnes closing:** **One** **C** subsection — the **litigator**: jurisdiction, enforceability, what counts as evidence, who pays, US civic machinery when load-bearing. **Latch rule:** the block must **explicitly engage** **both** prior minds — **at least one** hook to **Mercouris’s** frame (staging, legitimacy, channels) **and** **at least one** to **Mearsheimer’s** (incentives, structure, security); may reference **cross-reply** as well as openings. Barnes **does not** “pick a winner” between A and B; he **maps** what would need to be **proven**, **binding**, or **enforced** for either story to **bite**.

**Close:** **2–4 bullets** unresolved tension (optional); **no** fake consensus.

**When to prefer litigator-close:** Default **three-voice** pass when the operator wants **A/B dialectic first**, **Barnes** as **closer** (typical tri-mind = Mercouris, Mearsheimer, Mercouris–Mearsheimer cross, Barnes).

**When to use full `abc` roundtable instead:** Liability / jurisdiction / US institutional lever **anchors the fight from line one**; or Barnes must **interrupt** early (e.g. paymasters, sanctions, war powers before expert framing).

**Optional:** **Civ-mem** mapping — after Round 3, **one** short paragraph per letter **A, B, C** in order (stable index) if the operator asked **CIV-MEM**; otherwise skip.

### 4. Roundtable (**abc**)

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

### 5. Write surface

Default **chat only**. To append to [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) use **paste-ready** lines or a bounded `batch-analysis` block per inbox rules. **`chapters/YYYY-MM/days.md`** only when the operator **directs** or at **`dream`** fold — same boundary as [NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md).

**Public copy:** When the operator publishes **`tri-mind` output** (or prose derived from it) to **Locals / X / YouTube**, follow **[write-operator-preferences.md](../../../docs/skill-write/write-operator-preferences.md)** and **[`skill-write`](../skill-write/SKILL.md)** — topic-first ledes, closers, surface calibration. **Step 4 (*Closer*)** in **[write-shipping-checklist.md](../../../docs/skill-write/write-shipping-checklist.md)** must pass before **Locals** paste: **memorable** final sentence encapsulating the core argument; **no** abstract stacked closer; **no** rhetorical question as the last line (see [write-memorable-closer.md](../../../docs/skill-write/write-memorable-closer.md), [write-no-abstract-stacked-closers.md](../../../docs/skill-write/write-no-abstract-stacked-closers.md), [write-no-rhetorical-question-closer.md](../../../docs/skill-write/write-no-rhetorical-question-closer.md)). **X / PH:** same **step 4** on the shipped trim unless the operator opts out.

---

## Variants (operator may request)

| Variant | Behavior |
|---------|----------|
| **Litigator-close (`ab+c`)** | **Procedure §3** — duet **`ab`** then Barnes **closing** only; not symmetric **`abc`**. |
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
