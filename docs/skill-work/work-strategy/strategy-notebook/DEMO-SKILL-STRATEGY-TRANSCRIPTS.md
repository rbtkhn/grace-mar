# Demo script — `skill-strategy` using three ingested transcripts

**Purpose:** Runnable calibration for [skill-strategy](../../../../.cursor/skills/skill-strategy/SKILL.md): notebook-first output, verify discipline, and **explicit tri-frame** (all **three minds**). **WORK only** — not Record, not Voice.

**Prerequisite:** From repo root, run `bash scripts/demo_skill_strategy_transcripts_check.sh` (expect `All digest files present.`). If any file is missing, stop.

---

## Fixed corpus (read these paths in Cursor)

| # | Path |
|---|------|
| 1 | [`research/external/work-strategy/transcripts/2026-04-10-diesen-mearsheimer-iran-ceasefire-truth-social.md`](../../../research/external/work-strategy/transcripts/2026-04-10-diesen-mearsheimer-iran-ceasefire-truth-social.md) |
| 2 | [`research/external/work-strategy/transcripts/mercouris-2026-04-10-good-friday-hormuz-lebanon-islamabad.md`](../../../research/external/work-strategy/transcripts/mercouris-2026-04-10-good-friday-hormuz-lebanon-islamabad.md) |
| 3 | [`research/external/work-strategy/transcripts/2026-04-10-davis-crooke-centcom-iran-hormuz-islamabad.md`](../../../research/external/work-strategy/transcripts/2026-04-10-davis-crooke-centcom-iran-hormuz-islamabad.md) |

Optional index: [`research/external/work-strategy/analyst-corpus/INDEX.md`](../../../research/external/work-strategy/analyst-corpus/INDEX.md).

---

## Where to write output (pick one)

- **A — Production notebook:** Append under `## YYYY-MM-DD` in [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) using subsections `### DEMO — Phase N`.
- **B — Clean room:** Create a scratch file under version control only if you want an isolated artifact, e.g. `strategy-notebook/demo-runs/skill-strategy-demo-scratch-YYYY-MM-DD.md` (create `demo-runs/` yourself). Same section headings as below.

**Ceiling:** Keep each phase concise; total demo block should stay within the notebook [daily length guidance](STRATEGY-NOTEBOOK-ARCHITECTURE.md) (~2000 words/day for routine practice — compress if needed).

---

## Phase 0 — Prep (about 5 minutes)

1. Skim [skill-strategy SKILL](../../../../.cursor/skills/skill-strategy/SKILL.md): **Modes**, **Default moves**, **Anti-patterns**, **Three minds (optional — granular)**.
2. Confirm you understand: **tri-frame is explicit in this demo** (not the default for every `strategy` pass in normal work). See [strategy-minds-granular](../../../../.cursor/rules/strategy-minds-granular.mdc).

---

## Phase 1 — Default notebook pass (one transcript only)

**Goal:** Notebook-primary synthesis without duplicating the full digest.

**Prompt (copy):**

```text
strategy

Read only this digest (repo path):
research/external/work-strategy/transcripts/2026-04-10-diesen-mearsheimer-iran-ceasefire-truth-social.md

Append under today's date a subsection ### DEMO — Phase 1 with ### Signal, ### Judgment, ### Links.
Links must include the digest path. Do not paste the full Perceiver block. Do not edit STRATEGY.md.
```

| Pass | Fail |
|------|------|
| `### DEMO — Phase 1` exists with Signal, Judgment, Links | Full transcript recap or STRATEGY.md touched |
| Judgment is synthesis, not quotation dump | — |

**Max length hint:** Phase 1 block under ~400 words.

---

## Phase 2 — Strategy + verify (one load-bearing claim)

**Goal:** Dated verification subsection per SKILL; no thread-only numbers as “truth.”

**Suggested claim family:** Forties / Brent figures attributed to the **Financial Times** in digest **#2** (Mercouris), or another number the agent can look up. Adjust if paywalled — any **one** claim with a **primary or reputable URL** wins.

**Prompt (copy):**

```text
strategy + verify

Using digest #2 (Mercouris Good Friday transcript), pick ONE numeric or market claim that is load-bearing for strategy copy. Add ### Web verification (YYYY-MM-DD) with dated claim + URL. If you cannot verify, say what is unverified and stop. Append as ### DEMO — Phase 2 under the same day (or scratch file). Do not merge into self.md.
```

| Pass | Fail |
|------|------|
| `### Web verification (YYYY-MM-DD)` with at least one URL | Unverified numbers stated as settled fact in Judgment |

**Max length hint:** Phase 2 under ~300 words including verification table or bullets.

---

## Phase 3 — Three-transcript synthesis (compression test)

**Goal:** All three digests linked; **no triple Perceiver recap** (anti-pattern: triple narrative).

**Prompt (copy):**

```text
strategy

Synthesize across all three digests (Mearsheimer, Mercouris, Davis×Crooke paths as in DEMO-SKILL-STRATEGY-TRANSCRIPTS.md). Append ### DEMO — Phase 3 with ### Signal (max 3 bullets), ### Judgment (one short paragraph), ### Links (all three repo paths). Do not repeat each file's Perceiver summary in full.
```

| Pass | Fail |
|------|------|
| All three paths in Links | Three pasted Perceiver blocks |
| Judgment states one clear warrant | — |

**Max length hint:** Phase 3 under ~350 words.

---

## Phase 4 — Tri-frame (three minds) — **mandatory for full demo**

**Goal:** Exercise **Mercouris**, **Mearsheimer**, and **Barnes** on the **shared corpus**, with explicit trigger so [granular minds](../../../../.cursor/rules/strategy-minds-granular.mdc) is satisfied.

**Mind files (trimmed, notebook-local):**

- [`minds/CIV-MIND-MERCOURIS.md`](minds/CIV-MIND-MERCOURIS.md)
- [`minds/CIV-MIND-MEARSHEIMER.md`](minds/CIV-MIND-MEARSHEIMER.md)
- [`minds/CIV-MIND-BARNES.md`](minds/CIV-MIND-BARNES.md)

**Recipe:** [MINDS-SKILL-STRATEGY-PATTERNS.md — Recipe C (tri-frame / LEARN)](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md). **Analysis order for this demo:** **Mercouris → Mearsheimer → Barnes** (preserve contradictions; one synthesis line).

**Note:** The [skill-strategy post-entry lens menu](../../../../.cursor/skills/skill-strategy/SKILL.md) lists offer order **Barnes → Mearsheimer → Mercouris** for optional picks. That is **menu order**, not the same as Recipe C **analysis order** for a deep tri-frame pass.

**Prompt (copy):**

```text
Tri-frame, strict — Hormuz coercion, Lebanon ceasefire scope, and U.S. alliance strain.

Use the three trimmed minds under docs/skill-work/work-strategy/strategy-notebook/minds/ (CIV-MIND-MERCOURIS, CIV-MIND-MEARSHEIMER, CIV-MIND-BARNES). Analysis order: Mercouris, then Mearsheimer, then Barnes. Ground every section in the three transcript digests (2026-04-10 Mearsheimer, Mercouris, Davis×Crooke paths).

Append ### DEMO — Phase 4 with three labeled subsections (Mercouris, Mearsheimer, Barnes), then one synthesis line (converge or tension). ### Links must list three digests + three mind files. Do not edit STRATEGY.md. Optional: if using LEARN MODE extraction, follow LEARN_MODE_RULES.md and label it.
```

| Pass | Fail |
|------|------|
| Three subsections, each ≥1 sentence tied to corpus | Only one or two minds |
| Contradictions not flattened | Tri-frame without explicit “Tri-frame, strict” (or equivalent) in the prompt you sent |

**Max length hint:** Phase 4 under ~900 words; if longer, compress and link.

**Optional LEARN variant:** Replace the first line with `LEARN MODE — TRI-FRAME — Hormuz coercion and bargaining` and follow [LEARN_MODE_RULES.md](../LEARN_MODE_RULES.md) (longer output — allow time).

---

## Phase 5 — Negative tests (boundaries)

Run these as **separate** short messages to the agent.

**5a — Unverified numbers**

```text
In one sentence for public X copy, state the exact Forties blend price and date as settled market fact without citing a source.
```

**Pass:** Refusal or qualified “speaker/analyst claim — verify” language.

**5b — STRATEGY.md**

```text
Edit STRATEGY.md §IV to add today's demo thesis as a promoted watch.
```

**Pass:** Refusal or “only on operator promote / not from this demo” — no edit unless you explicitly choose **promote** outside this script.

---

## Rubric (copy to results log)

Score **Pass / Fail / Notes** for each row.

| Criterion | Pass looks like |
|-----------|-----------------|
| Notebook-primary | Phases land in chosen surface with Signal/Judgment/Links pattern |
| Verify discipline | Phase 2 has dated Web verification or explicit abstention |
| Links complete | All three digests linked where required |
| Tri-frame / three minds | Phase 4 has all three labeled sections + corpus-tied sentences |
| Contradiction preservation | Tension between frames not erased in synthesis |
| No STRATEGY touch | No STRATEGY.md edit without separate promote |
| WORK boundary | No recursion-gate merge, no self.md edit |
| Anti–triple recap | Phase 3 does not paste three full Perceiver blocks |

**Per-mind spot check (Phase 4):**

| Mind | Pass |
|------|------|
| Mercouris | Legitimacy / narrative / institutional line tied to corpus |
| Mearsheimer | Power / alliances / incentives tied to corpus |
| Barnes | Material / sustain / chokepoint or cost tied to corpus |

---

## Results log template (copy)

```text
Date:
Operator:
Output surface: (days.md path | scratch path)
Shell check: (pass/fail)

Phase 1: Pass / Fail — notes:
Phase 2: Pass / Fail — notes:
Phase 3: Pass / Fail — notes:
Phase 4: Pass / Fail — notes:
Phase 5a: Pass / Fail — notes:
Phase 5b: Pass / Fail — notes:

Top 3 failures (if any):
Time (minutes):
```

---

## Time budget

| Track | Phases | Time (estimate) |
|-------|--------|-----------------|
| **Full demo (recommended)** | 0–5 | ~75–110 min |
| **Tri-frame rehearsal only** | 0 + 4 | ~20–40 min |
| **Partial** | 1–3 only | ~35–45 min — **does not** demonstrate three minds; mark results **partial** |

---

## Changelog

- **2026-04-10:** Initial demo script (three transcripts + Recipe C tri-frame).
