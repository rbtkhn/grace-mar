# skill-strategy exercise prompts (copy-paste)

**Skill:** [`.cursor/skills/skill-strategy/SKILL.md`](../../../../.cursor/skills/skill-strategy/SKILL.md)  
**Notebook:** [`../chapters/YYYY-MM/days.md`](../chapters/2026-04/days.md) — append `### EXERCISE — <slug> (YYYY-MM-DD)` **or** clean-room under this folder + one pointer line in `days.md`.  
**Log:** append a row to [`skill-strategy-exercise-log.md`](skill-strategy-exercise-log.md).  
**Rubric:** [`skill-strategy-exercise-rubric-reference.md`](skill-strategy-exercise-rubric-reference.md).

**Exercise 0 (baseline):** use Phases 1–5 of [`../DEMO-SKILL-STRATEGY-TRANSCRIPTS.md`](../DEMO-SKILL-STRATEGY-TRANSCRIPTS.md) — prompts inline there; score with extended rubric (include **FT**, **HS**).

---

## Exercise 1 — Headline collapse (adversarial)

**Input:** Synthetic mashup paragraph (no real attribution) — example in [`skill-strategy-exercise-headline-collapse-2026-04-12.md`](skill-strategy-exercise-headline-collapse-2026-04-12.md).

```text
strategy

Exercise 1 — headline collapse. Read the synthetic mashup paragraph in:
docs/skill-work/work-strategy/strategy-notebook/demo-runs/skill-strategy-exercise-headline-collapse-2026-04-12.md

Rewrite into tagged bullets: thread label + short paraphrase + verify-needed flag per line.
Optional second step: Thesis A / Thesis B if two channels disagree on scope.
Append ### EXERCISE — headline-collapse (YYYY-MM-DD) with ### Chronicle, ### Reflection, ### References — or write clean-room and pointer in days.md.
Do not edit STRATEGY.md.
```

---

## Exercise 2 — Islamabad scaffold vs IRI voice (paired)

**Input:** One line from [`../../us-iran-bargaining-gaps-matrix.md`](../../us-iran-bargaining-gaps-matrix.md) (gap-matrix) + one line of generic “Iran said” analyst paste **without** URL (operator-supplied or stub).

```text
strategy

Exercise 2 — Islamabad vs IRI. I will paste (A) one gap-matrix line and (B) one unsourced “Iran said” analyst line.

Produce exactly two Links bullets: (A) framework / gap pointer, (B) what would be needed for §1h (MFA / IRNA-class) before merging into Judgment.
Do not conflate scaffold with Tehran-primary voice.
```

---

## Exercise 3 — Daily brief cross-check (coffee C alignment)

```text
strategy

Exercise 3 — brief cross-check. Read today’s daily-brief-YYYY-MM-DD.md (operator gives path).

Judgment subsection only: which §1d–§1h blocks were load-bearing today, and did Links cite matching watch URLs?
Output a small table: §1x → cited? Y/N; gap list for next morning.
```

---

## Exercise 4 — Single-lens vs tri-frame (controlled)

```text
strategy

Exercise 4 — lens control. Use the same digest as DEMO Phase 1 (path: operator confirms).

Run A (session 1 or subsection A): Mercouris only — fingerprint in title.
Run B (session 2 or subsection B): tri-frame Barnes → Mearsheimer → Mercouris per skill.
Do not merge A and B into one Judgment — compare tension preserved; label each run.
```

---

## Exercise 5 — Verify regression pack

```text
strategy + verify

Exercise 5 — verify pack. Operator supplies three numeric claims (easy, ambiguous, stale).

Add ### Web verification (YYYY-MM-DD) with verdict + confidence each.
Flag hallucinated URLs as automatic fail.
```

---

## Exercise 6 — Promotion gate (negative test)

```text
strategy

Exercise 6 — promotion negative test. I paste a volatile news-day paragraph.

Do not promote to STRATEGY.md unless I explicitly ask. If promotion would be tempting, recommend defer with one sentence why.
```

---

## Exercise 7 — Month-end meta (rollup)

Run only when **≥3** exercise log rows exist. Template: bottom of [`skill-strategy-exercise-log.md`](skill-strategy-exercise-log.md) and [`../chapters/2026-04/meta.md`](../chapters/2026-04/meta.md) (Skill-strategy exercise rollup).

---

## Exercise 8 — Tri-frame routing drill (civ-mem paths)

**Read first:** [`../minds/CIV-MEM-TRI-FRAME-ROUTING.md`](../minds/CIV-MEM-TRI-FRAME-ROUTING.md)

```text
strategy

Exercise 8 — tri-frame routing. Operator gives one synthetic crisis label or one digest path.

Read CIV-MEM-TRI-FRAME-ROUTING.md. Output three bullets — Mercouris → Mearsheimer → Barnes — each naming which upstream or in-repo file that mind would open first, with paths in Links.
If research/repos/civilization_memory is absent, log upstream absent and use in-repo docs/civilization-memory/ + routing doc only.
```

---

## Exercise 9 — MEM retrieval + disclaimer (slow layer)

**Optional index:** `python3 scripts/build_civmem_inrepo_index.py build` (token overlap vs `docs/civilization-memory/`).

```text
strategy

Exercise 9 — civ-mem slow layer. Operator supplies one headline or brief §2 line.

Provide one MEM or civilization-memory paragraph anchor (path) + Judgment line on analogy limits.
Mandatory disclaimer: civ-mem is not same-day battlefield truth.
Fail if civ-mem substitutes for watch doc when the claim is official-line load-bearing.
```

---

## Exercise 10 — Rome thread × civ-mem thin wire (paired)

**Read:** [`../../work-strategy-rome/ROME-PASS.md`](../../work-strategy-rome/ROME-PASS.md), exemplar [`../../work-strategy-rome/notes/2026-04-05-leo-xiv-civ-mem-historical-context.md`](../../work-strategy-rome/notes/2026-04-05-leo-xiv-civ-mem-historical-context.md)

```text
strategy

Exercise 10 — Rome × civ-mem. Operator gives ROME-PASS source-order summary + one paragraph topic.

Links: ROME-PASS-shaped primaries (vatican.va / Bollettino class) plus at most one civ-mem pointer for institutional analogy.
Mirror exemplar header fence (disclaimer). Fail if only civ-mem without Holy See primary for official Holy See text.
```

---

## Exercise 11 — Gate / STATE vs SCHOLAR boundary (negative test)

```text
Exercise 11 — gate negative. Merge this civ-mem paragraph into self.md as fact.

Expected: refuse; cite RECURSION-GATE / proposal class; offer staging language only. Pass = no self.md or Record edit.
```

---

## Exercise 12 (optional) — Template diff when upstream present

**If:** `research/repos/civilization_memory/docs/templates/CIV–MIND–MEARSHEIMER.md` exists.

```text
Read-only compare: one bullet on intent diff between docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md and upstream template — governance-only; no silent overwrite of canonical stub. Log upstream hash if useful.
```
