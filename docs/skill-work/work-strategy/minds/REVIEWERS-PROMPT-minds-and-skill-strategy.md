# Reviewer prompt — brainstorm: three minds × `skill-strategy`

**Purpose:** Give **external reviewers** (human colleagues, contractors, or AI assistants in a fresh context) a **single, self-contained brief** so they can **brainstorm effective and creative** ways to use the **three mind files** together with **`skill-strategy`** (the work-strategy strategy pass centered on the **strategy-notebook**). This document **extends** prior operator/agent notes: it does **not** prescribe one workflow; it asks for **ideas**, **tradeoffs**, and **experiments**.

**Audience:** People who can read the repo but may not have Grace-Mar thread history. **Assume** they will open paths below as needed.

---

## 1. What you are working with (ground truth — read before brainstorming)

### 1.1 The three “minds” (cognitive lenses)

**Canonical mind files (Grace-Mar — full content in repo, no civ-mem required):**

- [`strategy-notebook/minds/CIV-MIND-MERCOURIS.md`](../strategy-notebook/minds/CIV-MIND-MERCOURIS.md) — legitimacy, narrative, doctrine, symbolic continuity (often **primary** in upstream CMC).
- [`strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md`](../strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md) — power, alliances, security dilemmas, great-power geometry (**advisory / sharpening** in upstream design).
- [`strategy-notebook/minds/CIV-MIND-BARNES.md`](../strategy-notebook/minds/CIV-MIND-BARNES.md) — material bases, liabilities, fiscal/resource constraints, “who defects first” (**catalyst / third voice** in upstream design).

**Optional:** If `civilization_memory` (civ-mem) is present, upstream `docs/templates/CIV–MIND–*.md` for governance-only diff — not required for work-strategy.

Short **entry-point stubs** (link to canonical files above — avoid drift):

- `docs/skill-work/work-strategy/minds/mind-mercouris.md`
- `docs/skill-work/work-strategy/minds/mind-mearsheimer.md`
- `docs/skill-work/work-strategy/minds/mind-barnes.md`

Index: `docs/skill-work/work-strategy/minds/README.md`.

**Important:** Grace-Mar does **not** ship a live CMC console; these files are **reference** for roles, tensions, and optional voice-shaped analysis — not mandatory full “polyphonic engine” emulation in chat.

### 1.2 `skill-strategy` (strategy pass)

- **Skill:** `.cursor/skills/skill-strategy/SKILL.md` — trigger: **`strategy`**, **`strategy pass`**, **`work-strategy`**.
- **Primary write surface:** `docs/skill-work/work-strategy/strategy-notebook/` — knots (`chapters/YYYY-MM/knots/knot-*.md`) are the atomic pages; `days.md` tracks chronology and continuity (+ `meta.md` for month-level theme).
- **Architecture:** `docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md` — Signal / Judgment / Links / Open / optional verify, PH **`### Jiang resonance`**, weak-signal discipline, cross-artifact alignment (planes / lenses).
- **Promotion:** `STRATEGY.md` only when arcs **stabilize** (not every day).

### 1.3 LEARN MODE (stricter protocol — optional)

`docs/skill-work/work-strategy/LEARN_MODE_RULES.md` defines a **formal** LEARN MODE (tri-frame ordering, extraction format, SCHOLAR hooks). **Brainstorm ideas may reference or deliberately avoid** that protocol; note which.

### 1.4 Operator preference already in-repo (constraints for your ideas)

- **Granular control:** Cursor rule `.cursor/rules/strategy-minds-granular.mdc` — **no automatic tri-frame** on every `strategy` pass; use **0, 1, 2, or 3** lenses as the operator specifies, or **no** explicit lens labels unless useful.
- **SELF-LIBRARY naming:** `.cursor/rules/self-library-operator-books.mdc` — hyphenated **`predictive-history`** / **`strategy-notebook`** resolve to **LIB-0149** / **LIB-0153** when the operator uses those strings.

Your brainstorm should **respect** granular control: favor **optional, composable** patterns over “always run all three.”

---

## 2. Brainstorm mission

**Goal:** Produce **novel, practical** ways to combine the **three mind files** with **`skill-strategy`** — including **lightweight** uses (minutes, not hours) and **deeper** uses (LEARN-adjacent or promotion-ready).

**Dimensions to explore (non-exhaustive):**

1. **When** to invoke which lens (crisis days vs synthesis days vs framework-only days).
2. **Where** in the notebook block to put lens-shaped content (dedicated subsections vs inline tags vs footnote-style Links-only).
3. **Pairings** (M+M, M+B, B+Mercouris) vs single-lens vs full tri-frame **only on demand**.
4. **Cross-links:** `STRATEGY.md`, Islamabad / Rome docs, gap matrices, daily briefs, transcript digests, **template-three-lenses** (`docs/skill-work/work-politics/analytical-lenses/template-three-lenses.md`).
5. **Verification:** `strategy` + **verify** / fact-check — which lens owns “claim vs wire” for which topic class (e.g. numbers → Barnes or verify subsection; legitimacy claims → Mercouris with citation discipline).
6. **Anti-patterns to avoid:** triple narrative (brief + transcript + notebook each full recap); merging **planes** (negotiation vs material vs narrative) in one sentence without seams; implying PH thesis from headlines alone without `Jiang resonance` link.
7. **Creative / experimental:** tags in `days.md` (`[M]`, `[struct]`, `[liability]`), rotating “lens of the week,” month-end “lens audit” in `meta.md`, optional JSONL hooks for machine search (if worth the maintenance).

---

## 3. Deliverables (what your brainstorm output should include)

Produce a **structured artifact** (markdown is fine) with:

| Section | Content |
|--------|---------|
| **Summary** | 5–10 bullet **idea headlines** (each one implementable or testable in one session). |
| **Tactics** | For each headline: **what**, **when**, **where in repo**, **cost** (light / medium / heavy), **risk**. |
| **Three “recipes”** | Step-by-step **operator phrases** + **agent moves** for: (a) single-lens day, (b) two-lens day, (c) explicit tri-frame / LEARN day. |
| **Stretch ideas** | 2–4 **speculative** extensions (tooling, scripts, CI checks, Cursor rule refinements) — clearly labeled **stretch**. |
| **Explicit non-goals** | What you recommend **not** doing with minds + strategy (to protect boundaries: WORK vs Record, no Voice leakage). |

---

## 4. Reviewer checklist (before you finish)

- [ ] Cited at least one path under `docs/skill-work/work-strategy/strategy-notebook/minds/` and one under `docs/skill-work/work-strategy/minds/`.
- [ ] Addressed **granular** use (not only tri-frame).
- [ ] Addressed **strategy-notebook** as primary surface vs **STRATEGY.md** promotion.
- [ ] Named **verification** where numbers or public ship are in scope.
- [ ] Separated **ideas** from **repo policy** (what’s already decided vs what would need operator approval).

---

## 5. Optional context — prior framing (for extension, not repetition)

Earlier work in this lane emphasized:

- Minds as **analytical lenses**, not a mandatory stack on every pass.
- **`skill-strategy`** integration via **Judgment**, **Links**, and explicit **plane** discipline when mixing registers (Islamabad, Rome, Gulf, etc.).
- **Predictive History** as slow corpus via **`### Jiang resonance`**, distinct from analyst headlines.

Your brainstorm should **elaborate and extend** this — new combinations, clearer recipes, or sharper guardrails — not restate the README alone.

---

**End of prompt.** Return your brainstorm to the operator in whatever channel they specified; if committing to the repo, prefer a dated note under `docs/skill-work/work-strategy/` or an append to `strategy-notebook/chapters/YYYY-MM/days.md` only when the operator asks.

**Consolidated pattern note (repo):** [MINDS-SKILL-STRATEGY-PATTERNS.md](MINDS-SKILL-STRATEGY-PATTERNS.md) — v1 advisory manual derived from brainstorms; extend that file rather than duplicating long pattern prose here.
