# EOD strategy session — MCQ protocol (v1)

**Status:** ACTIVE  
**SSOT for:** Structured, decision-first **end-of-day strategy sessions** when the operator wants multiple-choice routing before prose.  
**Governed by:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — capture → judgment → chronology; word bands; same-day merge; multi-pick duplication rules. This protocol **does not** replace architecture; it **sequences** decisions before drafting.

**Coexistence:** The architecture’s **minimal** EOD path is still valid: present **4–6** thesis-first **page-shape** stubs only (§ *EOD compose — page-shape menu*) when the operator wants speed, says **`no menu`**, or **`EXECUTE`** with an explicit thesis. Use **this MCQ stack** when they invoke **`EOD strategy session` + MCQ**, paste this doc, or ask for **decision-first** menus before any **`strategy-page`** / `days.md` prose.

**Invocation:** Operator says e.g. **EOD strategy session — MCQ**, **`strategy page compose` + MCQ**, or pastes the **recommended default prompt** (below). Canonical compose phrases remain **`strategy page`** / **`strategy page compose`** ([architecture § *End-of-day strategy session*](STRATEGY-NOTEBOOK-ARCHITECTURE.md#end-of-day-strategy-session-terminology)).

---

## Purpose

Use **MCQs** to drive the EOD session so the operator mostly makes **structured decisions first**, and prose is written only after **routing**, **promotion**, and **page-shape** choices are explicit.

## Core rule

| Surface | Role |
|--------|------|
| **Inbox** + **`raw-input/`** | **Capture** |
| Expert **`thread.md`** **`strategy-page`** blocks | **Judgment** |
| **`chapters/YYYY-MM/days.md`** | **Chronology / continuity** |

The EOD session is where **capture is promoted into judgment**. It should **synthesize**, not mirror raw input.

---

**Optional pre-Stage 0 orientation:** run `python3 scripts/strategy_console.py --mode eod` to refresh [`strategy-console/console-view.md`](strategy-console/console-view.md). This is a derived orientation surface only. It may suggest a conservative EOD route, but it does **not** replace the evidence pile, MCQ choices, or authorized drafting process.

---

## Stage 0 — Build the evidence pile

The assistant gathers:

- Today’s **`raw-input/YYYY-MM-DD/`** files (if any)
- Today’s lines in [daily-strategy-inbox.md](daily-strategy-inbox.md)
- Relevant **`batch-analysis`** rows
- Relevant **`experts/<expert_id>/transcript.md`** (when **`thread:`** ingests apply)
- Current **`experts/<expert_id>/thread.md`** (journal + existing **`strategy-page`** markers)
- Current **`chapters/YYYY-MM/days.md`** context (tail + target **`## YYYY-MM-DD`** if composing)

The assistant then says:

> EOD evidence pile prepared. I will drive this session by MCQ.  
> We will decide: (1) session type, (2) active lanes, (3) promotion threshold, (4) page shape, (5) page action (full protocol), (6) days.md continuity mode.  
> **Fast path:** skip (5) unless you need explicit append/revise/split control.  
> Then I will draft only what your choices authorize.

---

## Menu 1 — Session type

**Question:** What kind of EOD session is this tonight?

| Letter | Type | Summary |
|--------|------|---------|
| **A** | **Single-lane synthesis** | One expert owns the main analytical movement tonight. |
| **B** | **Dual-lane contrast** | Two experts need parallel treatment or contrast. |
| **C** | **Tri-mind pass** | Barnes / Mearsheimer / Mercouris get a coordinated pass — see [Optional tri-mind variant](#optional-tri-mind-variant) and [.cursor/skills/tri-mind/SKILL.md](../../../../.cursor/skills/tri-mind/SKILL.md). |
| **D** | **Continuity-only close** | Update `days.md` and preserve transcript context; **no** new **`strategy-page`** unless forced (breaking glass). |
| **E** | **Triage-and-defer** | Preserve material, route it, **defer** page composition. |
| **F** | **Bridge session** | One expert lane plus one **bridge** lane (often **Jiang** / history / civilizational framing). |

**Assistant output after selection:** Names the session type, proposes default **lane count**, moves to Menu 2.

---

## Menu 2 — Active lane selection

**Question:** Which expert lanes are active for tonight’s synthesis?

Present **4–8** options **tailored to today’s evidence pile** — example letters:

| Letter | Lane |
|--------|------|
| **A–G** | Named experts (e.g. Mercouris, Barnes, Mearsheimer, Ritter, Jiang, Pape) — **canonical `expert_id` slugs** only ([strategy-commentator-threads.md](strategy-commentator-threads.md)). |
| **H** | **Keep material cold / unresolved** — do not force promotion. |
| **(other)** | **Other named lane:** operator fills blank. |

**Rules:**

- Use **canonical expert slugs** only.
- Do **not** mix commentators into the wrong lane.
- If ownership is unclear, choose **cold / unresolved** rather than forcing promotion.

**Operator response format:**

- **Single letter** — single-lane session  
- **Two letters** — dual-lane  
- **Three letters** — tri-mind (or use fixed tri-mind Menu 2 below)  
- **One lane + bridge** — bridge session (e.g. `R` + `Jiang`)

**Assistant output after selection:** Confirms active lanes, groups evidence **by lane**, moves to Menu 3 **for each lane** (or once if session type is continuity-only / triage).

---

## Menu 3 — Promotion threshold (per lane)

**Question:** For **this lane**, what should happen to today’s material?

| Letter | Option | Notebook meaning |
|--------|--------|------------------|
| **A** | **Transcript only** | Preserve in transcript / machine context; **do not** promote into **`strategy-page`** judgment. |
| **B** | **Revise existing strategy-page** | Today **changes or sharpens** an existing page (`id=`). |
| **C** | **Start new strategy-page** | Today deserves a **fresh** fenced page in this thread. |
| **D** | **days.md continuity only** | Record notebook continuity; **do not** change expert-thread **substance** (no new/revised **`strategy-page`** body for this lane). |
| **E** | **Hold unresolved** | Keep in inbox / **`raw-input/`** / transcript orbit for tomorrow. |

**Decision rule:** Choose **B** or **C** only if today’s material **changes the lane’s interpretation**, **extends a recurring frame**, or **deserves durable analytical prose**. The EOD session is for **synthesis**, not copying.

**Assistant output after selection:** States promotion result **per lane**. If **B** or **C**, moves to Menu 4 for that lane. If **A**, **D**, or **E**, skips to continuity handling / next lane / Menu 6 as appropriate.

**Mapping (Menu 3 ↔ write surfaces):**

| Menu 3 | `strategy-page` | `days.md` |
|--------|-----------------|-----------|
| A, E | No new/revised judgment page | Optional continuity note only if operator wants |
| D | No thread substance change | Yes — thin continuity |
| B, C | Yes — per Menu 4–5 | Yes — per Menu 6 |

---

## Menu 4 — Page shape / thesis type

**Question:** What kind of **`strategy-page`** should **this lane** produce tonight?

Present **4–6** options max, **tailored to the day’s evidence** (architecture still expects thesis-first stubs — align with § *Page design and notebook-use jobs* in [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)).

| Letter | Shape | Typical notebook-use jobs ([strategy-commentator-threads.md](strategy-commentator-threads.md) § *Notebook-use tags*) |
|--------|--------|----------------------------------------------------------------------------------------------------------------------|
| **A** | **Main signal page** | **`orient`**, **`narrate`** — best single judgment from today’s evidence. |
| **B** | **Revision / correction page** | **`validate`** — updates or reverses earlier thread judgment. |
| **C** | **Stress-test page** | **`stress-test`** — countercase, failure mode, challenge to dominant thesis. |
| **D** | **Process page** | **`negotiate`** — sequencing, mediation, institutional mechanics. |
| **E** | **Legitimacy / domestic page** | **`authorize`** + C-plane hooks — law, coalition, domestic sustainability. |
| **F** | **Structural page** | Power, incentives, deterrence — aligns with [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) § *Weave skeletons (S1–S5)* spines. |
| **G** | **Historical / civilizational page** | **`historicize`** — analogy, PH bridge when engaged. |
| **H** | **Continuity stub only** | Too weak for full page; short marker / pointer only. |

**Assistant output after selection:** States chosen page shape, proposes **page title** / **`id=`** candidates, then asks Menu 5 (full protocol) or Menu 6 (fast path).

---

## Menu 5 — Page action (mechanical)

**Question:** How should the **thread** change mechanically?

| Letter | Action |
|--------|--------|
| **A** | Append a **new** page under current month (`## YYYY-MM`). |
| **B** | **Revise** the latest page only (same **`id=`** or explicit target). |
| **C** | **Split** one drifting page into two cleaner pages (new **`id=`**s; respect [architecture § *Same-day iteration*](STRATEGY-NOTEBOOK-ARCHITECTURE.md)). |
| **D** | Add a short **bridge note**, not a full page. |
| **E** | **No thread write**; carry forward only. |

This menu reduces accidental page sprawl. **Alignment with architecture:** **Multi-pick** sessions may still produce **one logical page per non-mergeable shape**, duplicated across experts with the same **`id=`** — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Multi-pick EOD options*. **Same-day** default: **one** consolidated **`## YYYY-MM-DD`** block in `days.md` unless episodic heading is justified.

---

## Menu 6 — days.md continuity mode

**Question:** How should tonight appear in **`chapters/YYYY-MM/days.md`**?

| Letter | Mode |
|--------|------|
| **A** | **Minimal continuity stub** — active lane(s) and page movement only. |
| **B** | **Standard day entry** — brief note on what changed and where it lives. |
| **C** | **Judgment-change emphasis** — what belief changed today. |
| **D** | **Open-questions emphasis** — what remains unresolved tomorrow. |
| **E** | **Cross-lane continuity** — how multiple lanes interacted. |

**Rule:** `days.md` preserves **chronology and continuity**, not a duplicate of full expert prose ([NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) — inbox vs notebook).

**Assistant output after selection:** Confirms day-entry mode, **then** drafts authorized artifacts.

---

## Drafting rules (after MCQs)

Only after Menus **1–6** are complete (or the **fast path** below) should the assistant draft:

1. **`strategy-page`** block(s) inside **`experts/<expert_id>/thread.md`** (when B/C + authorized by Menu 5)
2. Matching **`days.md`** continuity update
3. Optional short **tomorrow start point** (in chat or under **`### Foresight`**)

**Constraints:**

- Thread prose reflects **lane ownership** clearly.
- Do **not** mirror **`raw-input/`**; use transcript context as **evidence**, not as finished judgment.
- If the operator chose **transcript-only** or **defer**, do **not** smuggle in a full page.

**Word count:** **No** target band per **`strategy-page`** body—see [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) (**Page length**).

---

## Default short EOD flow

Fastest path — use when the operator wants fewer forks:

1. Menu 1 — Session type  
2. Menu 2 — Active lane(s)  
3. Menu 3 — Promote / revise / new / defer (per lane)  
4. Menu 4 — Page shape  
5. Menu 6 — `days.md` mode  

**Skip Menu 5** unless the operator needs explicit mechanical control (append vs revise vs split). Then draft.

---

## Assistant behavior rules

1. **Decision-first, prose-second.**  
2. **Never** write the page before **lane ownership** and **promotion threshold** are chosen (for MCQ sessions).  
3. If evidence is weak, recommend **transcript-only** or **defer**.  
4. If routing is ambiguous, keep it **cold** rather than forcing the wrong expert lane.  
5. Keep menus **short and tailored**; do not show giant universal menus every time.  
6. Favor **one strong page** over many shallow ones.  
7. End with a clean **recovery point** for tomorrow (`### Foresight` or one-line chat stub).

---

## Recommended default prompt (operator paste)

> EOD strategy session. Build today’s evidence pile, then drive me by MCQ.  
> First ask session type.  
> Then active lanes.  
> Then for each lane ask transcript / revise / new page / defer.  
> Then ask page shape.  
> Then ask days.md continuity mode.  
> Do not draft prose until I answer the menus.

---

## Optional tri-mind variant

If **Menu 1 = C (Tri-mind pass)**, use this **fixed** Menu 2:

| Letter | Lane |
|--------|------|
| **A** | Mercouris |
| **B** | Barnes |
| **C** | Mearsheimer |

Ask **Menu 3 separately** for each of the three lanes (transcript only / revise / new / continuity only / defer).

Then ask **one synthesis question:**

**Which of the three lanes should anchor tonight’s day entry?**

| Letter | Anchor |
|--------|--------|
| **A** | Mercouris |
| **B** | Barnes |
| **C** | Mearsheimer |
| **D** | Equal-weight continuity |

Tri-mind chat mechanics remain per [.cursor/skills/tri-mind/SKILL.md](../../../../.cursor/skills/tri-mind/SKILL.md); notebook gets **compressed judgment + Links**, not the raw three-lens wall unless the operator asks — [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Expert choreography*.

---

## One-sentence doctrine

The EOD strategy session should decide **what the notebook now believes**, which **expert lane** owns that belief, and whether it deserves a **new page**, a **revision**, or **only continuity**.

---

## See also

| Doc | Role |
|-----|------|
| [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *EOD compose — page-shape menu* | Minimal **thesis-first** fork; multi-pick; notebook-use jobs |
| [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) | EOD page-shape preference row; S1–S5 skeletons |
| [.cursor/skills/skill-strategy/SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md) | Skill entry; EOD obligations |
| [DEFAULT-PATH.md](../DEFAULT-PATH.md) | Three-move default; menu **A** → compose |
